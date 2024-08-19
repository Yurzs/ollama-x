import asyncio
import dataclasses
import json
import math
from asyncio import Semaphore
from collections import defaultdict
from collections.abc import AsyncIterable
from typing import Any, Self

import aiohttp
from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

from ollama_x.api.exceptions import NoServerAvailable
from ollama_x.api.helpers import AISession, AuthorizedUser
from ollama_x.config import config
from ollama_x.model import APIServer

router = APIRouter(prefix="/api", tags=["proxy"])

queues: dict[str, asyncio.Queue] = defaultdict(asyncio.Queue)


@dataclasses.dataclass
class QueueRequest:
    """Handle requests."""

    server: APIServer
    request: Request
    response: asyncio.Future = dataclasses.field(default_factory=asyncio.Future)
    ready: asyncio.Event = dataclasses.field(default_factory=asyncio.Event)

    def set_result(self, result: Any):
        self.response.set_result(result)
        self.ready.set()

    def set_exception(self, e):
        self.response.set_exception(e)
        self.ready.set()


class QueueHandler:
    QUEUES: dict[str, "QueueHandler"] = {}
    LIMIT = 20

    @classmethod
    def get(cls, server_url: str) -> Self:
        """Get queue handler."""

        if server_url in cls.QUEUES:
            return cls.QUEUES[server_url]
        else:
            cls.QUEUES[server_url] = cls(server_url)
            return cls.QUEUES[server_url]

    def __init__(self, server_url: str) -> None:
        self.server_url: str = server_url
        self.queue: asyncio.Queue[QueueRequest] = asyncio.Queue()
        self.task: asyncio.Task = asyncio.create_task(self.handle_requests())
        self.pending: asyncio.Semaphore = asyncio.Semaphore(value=self.LIMIT)

    async def handle_requests(self):
        while True:
            request: QueueRequest = await self.queue.get()
            await self.pending.acquire()
            try:
                await asyncio.create_task(proxy_queue_request(self.pending, request))
            except Exception as e:
                request.set_exception(e)
                self.pending.release()
            finally:
                self.queue.task_done()


async def get_min_queue_server(model: str | None) -> APIServer | None:
    """Find the least loaded server."""

    min_queue = (None, math.inf)

    async for server in APIServer.all_active(model_name=model):
        queue = QueueHandler.get(server.url).queue
        queue_size = queue.qsize()

        if queue_size < min_queue[1]:
            min_queue = (server, queue_size)

    return min_queue[0]


def stream_response(request: Request, server: APIServer) -> StreamingResponse:
    """Stream response content."""

    async def stream() -> AsyncIterable[bytes]:
        data = await request.json()

        async with aiohttp.ClientSession(base_url=str(server.url)) as session:
            method = getattr(session, request.method.lower())
            async with method(
                request.url.path,
                json=data,
            ) as response:
                async for chunk in response.content:
                    yield chunk

    return StreamingResponse(
        stream(),
        headers={
            "Content-Type": "application/x-ndjson",
            "Transfer-Encoding": "chunked",
        },
    )


async def proxy_request(server: APIServer, request: Request) -> StreamingResponse | Response:
    """Proxy request to APIServer."""

    data = await request.json()
    data["model"] = request.state.model

    if data is not None and data.get("stream", True):
        return stream_response(request, server)

    async with aiohttp.ClientSession(base_url=str(server.url)) as session:
        method = getattr(session, request.method.lower())
        async with method(
            request.url.path,
            json=data,
        ) as response:
            return Response(
                headers=dict(response.headers),
                content=json.dumps(await response.json()).encode(),
            )


async def proxy_queue_request(semaphore: Semaphore, queue_request: QueueRequest) -> None:
    """Proxy request to APIServer."""

    request = queue_request.request
    server = queue_request.server

    try:
        result = await proxy_request(server, request)
    except Exception as e:
        queue_request.set_exception(e)
    else:
        queue_request.set_result(result)
    finally:
        semaphore.release()


@router.get("/tags", include_in_schema=False)
async def get_tags():
    """Get tags from all servers."""

    models = {}

    async for server in APIServer.all_active():
        for model in server.models:
            models[model["model"]] = model

    return {"models": list(models.values())}


@router.post("/show", include_in_schema=False)
async def show_model(request: Request):
    """Proxy show request."""

    data = await request.json()

    server = await get_min_queue_server(data["name"])

    if server is None:
        raise NoServerAvailable()

    return await proxy_request(server, request)


@router.post("/embed", include_in_schema=False)
async def generate_embeddings(request: Request):
    """Generate embeddings."""

    server = await get_min_queue_server(request["model"])
    if server is None:
        raise NoServerAvailable()

    return await proxy_request(server, request)


@router.post("/chat", include_in_schema=False)
@router.post("/generate", include_in_schema=False)
async def proxy(session: AISession, request: Request):
    """Proxy generate request."""

    request_data = await request.json()

    request.state.model = config.enforce_model or request_data["model"]

    server = await get_min_queue_server(request.state.model)
    if server is None:
        raise NoServerAvailable()

    queue_request = QueueRequest(server, request)
    queue = QueueHandler.get(server.url).queue

    await queue.put(queue_request)
    await queue_request.ready.wait()

    if queue_request.response.exception():
        raise queue_request.response.exception()

    return queue_request.response.result()

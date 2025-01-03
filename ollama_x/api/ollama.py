import asyncio
import dataclasses
import math
from asyncio import Semaphore
from collections import defaultdict
from collections.abc import AsyncIterable
from typing import Any, Self

import aiohttp
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from ollama_x.api import endpoints
from ollama_x.api.exceptions import NoServerAvailable
from ollama_x.api.helpers import AISession, multi_endpoint
from ollama_x.config import config
from ollama_x.model import APIServer, OllamaModel
from ollama_x.types import ollama_model_converter


router = APIRouter(tags=["ollama"])

queues: dict[str, asyncio.Queue] = defaultdict(asyncio.Queue)


@dataclasses.dataclass
class QueueRequest:
    """Handle requests."""

    server: APIServer
    request: Request

    openai_compatibility: bool = False

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

        if server_url not in cls.QUEUES:
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
        queue_size = QueueHandler.get(server.url).queue.qsize()

        if queue_size < min_queue[1]:
            min_queue = (server, queue_size)

    return min_queue[0]


def stream_response(
    request: Request, server: APIServer, openai_compatibility: bool = False
) -> StreamingResponse:
    """Stream response content."""

    is_sse_stream = request.headers.get("accept") == "text/event-stream" and openai_compatibility

    async def stream() -> AsyncIterable[bytes]:
        data = await request.json()

        async with aiohttp.ClientSession(base_url=str(server.url)) as session:
            method = getattr(session, request.method.lower())
            async with method(
                request.state.path,
                json=data,
            ) as response:
                async for chunk in response.content:
                    yield chunk

    return StreamingResponse(
        stream(),
        headers={
            "Content-Type": "application/x-ndjson" if not is_sse_stream else "text/event-stream",
            "Transfer-Encoding": "chunked",
        },
    )


async def proxy_request(
    server: APIServer, request: Request, openai_compatibility: bool = False
) -> StreamingResponse:
    """Proxy request to APIServer."""

    data = await request.json()
    data["model"] = request.state.model

    return stream_response(request, server, openai_compatibility=openai_compatibility)


async def proxy_queue_request(semaphore: Semaphore, queue_request: QueueRequest) -> None:
    """Proxy request to APIServer."""

    try:
        result = await proxy_request(
            queue_request.server,
            queue_request.request,
            openai_compatibility=queue_request.openai_compatibility,
        )
    except Exception as e:
        queue_request.set_exception(e)
    else:
        queue_request.set_result(result)
    finally:
        semaphore.release()


async def get_models() -> dict[str, Any]:
    models = {}

    async for server in APIServer.all_active():
        for model in server.models:
            models[model["model"]] = model

    return models


async def get_running_models() -> list[str]:
    """List all running models."""

    models = set()

    async for server in APIServer.all_active():
        models.update([model["model"] for model in server.running_models])

    return list(models)


@multi_endpoint(router.get, endpoints.PROXY_TAGS, endpoints.OLLAMA_TAGS, include_in_schema=False)
async def get_tags():
    """Get tags from all servers."""

    models = await get_models()

    return {"models": list(models.values())}


@multi_endpoint(router.post, endpoints.PROXY_SHOW, endpoints.OLLAMA_SHOW, include_in_schema=False)
async def show_model(request: Request) -> OllamaModel:
    """Proxy show request."""

    data = await request.json()

    return await OllamaModel.one(data["name"])


@multi_endpoint(
    router.post,
    endpoints.PROXY_EMBEDDINGS,
    endpoints.OLLAMA_EMBEDDINGS,
    endpoints.OLLAMA_OPENAI_EMBEDDINGS,
    include_in_schema=False,
)
async def generate_embeddings(request: Request):
    """Generate embeddings."""

    data = await request.json()
    request.state.model = data["model"]

    openai_compatibility = False
    if request.url.path.endswith(endpoints.OLLAMA_OPENAI_EMBEDDINGS):
        openai_compatibility = True

    if request.url.path.startswith("/ollama"):
        request.state.path = f"/{request.url.path[8:]}"

    server = await get_min_queue_server(request.state.model)
    if server is None:
        raise NoServerAvailable()

    return await proxy_request(server, request, openai_compatibility=openai_compatibility)


@multi_endpoint(
    router.post,
    endpoints.PROXY_CHAT,
    endpoints.PROXY_GENERATE,
    endpoints.OLLAMA_CHAT,
    endpoints.OLLAMA_COMPLETIONS,
    endpoints.OLLAMA_OPENAI_COMPLETIONS,
    endpoints.OLLAMA_OPENAI_CHAT,
    include_in_schema=False,
)
async def proxy(session: AISession, request: Request):
    """Proxy generate request."""

    openai_compatibility = False

    if request.url.path.endswith(
        (endpoints.OLLAMA_OPENAI_COMPLETIONS, endpoints.OLLAMA_OPENAI_CHAT)
    ):
        openai_compatibility = True

    if request.url.path.startswith("/ollama"):
        request.state.path = f"/{request.url.path[8:]}"

    request_data = await request.json()

    if request.state.user.is_guest:
        request.state.model = (
            config.anonymous_model or config.enforce_model or request_data["model"]
        )
    else:
        request.state.model = config.enforce_model or request_data["model"]

    request.state.model = ollama_model_converter(request.state.model)

    server = await get_min_queue_server(request.state.model)
    if server is None:
        raise NoServerAvailable()

    model_names = [model["model"] for model in server.models]
    if request.state.model not in model_names:
        for model in server.models:
            if model["model"].startswith(request.state.model):
                request.state.model = model["model"]
                break

    queue_request = QueueRequest(server, request, openai_compatibility=openai_compatibility)
    queue = QueueHandler.get(server.url).queue

    await queue.put(queue_request)
    await queue_request.ready.wait()

    if queue_request.response.exception():
        raise queue_request.response.exception()

    return queue_request.response.result()

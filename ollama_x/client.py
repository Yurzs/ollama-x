import asyncio
import json
import ssl
from contextlib import asynccontextmanager
from functools import partial
from typing import Any, AsyncIterable, Callable

from fastapi import FastAPI, Request
import aiohttp
import certifi
from aiohttp import TCPConnector
from pydantic import HttpUrl
from starlette.datastructures import Headers
from starlette.responses import JSONResponse, StreamingResponse

from ollama_x.api import endpoints
from ollama_x.types import OllamaModel, OpenAIModel


def get_model_params(model_name: str) -> tuple[str, str]:
    version = "latest"

    if "/" not in model_name:
        model_name = f"library/{model_name}"

    if ":" in model_name:
        model_name, version = model_name.split(":", 1)

    return model_name, version


class OllamaClient:
    """Client to Ollama Server API."""

    def __init__(self, base_url: str | HttpUrl | None, is_self: bool = False):
        self.base_url = str(base_url) if base_url is not None else None
        self.is_self = is_self

    @asynccontextmanager
    async def send_request(
        self,
        path: str,
        method: str,
        base_url: None | str = None,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        """Send request to the server."""

        ssl_context = ssl.create_default_context(cafile=certifi.where())

        if self.base_url is None and base_url is None:
            raise RuntimeError("Base url is not provided.")

        async with aiohttp.ClientSession(
            base_url or self.base_url, connector=TCPConnector(ssl=ssl_context)
        ) as session:
            async with getattr(session, method)(path, timeout=5, **kwargs) as response:
                yield response

    def list_models(self) -> aiohttp.ClientResponse:
        """List all models available on the server."""

        return self.send_request("/api/tags", "get")

    def show_model_info(self, model_name: str, verbose=False) -> aiohttp.ClientResponse:
        """Show model information."""

        return self.send_request(
            f"/api/show",
            "post",
            json={
                "name": model_name,
                "verbose": verbose,
            },
        )

    def list_running_models(self) -> aiohttp.ClientResponse:
        """List all running models."""

        return self.send_request("/api/ps", "get")

    async def tokenize(self, model_name: str, prompt: str) -> aiohttp.ClientResponse:
        return self.send_request(
            "/api/tokenize",
            "post",
            json={
                "model": model_name,
                "prompt": prompt,
            },
        )

    async def get_manifest(self, model_name: str):

        model_name, version = get_model_params(model_name)

        return await self.send_request(
            f"/v2/{model_name}/manifests/{version}",
            "get",
            base_url=f"https://registry.ollama.ai",
        )

    async def download_blob(self, model_name: str, digest: str) -> aiohttp.ClientResponse:
        model_name, _ = get_model_params(model_name)

        return await self.send_request(
            f"/v2/{model_name}/blobs/{digest}",
            "get",
            base_url=f"https://registry.ollama.ai",
        )

    def chat(
        self,
        request: dict[str, Any],
        headers: dict[str, Any],
    ) -> aiohttp.ClientResponse:

        return self.send_request(
            "/api/chat",
            "post",
            json=request,
            headers=headers,
        )


class ResponseIterable(AsyncIterable):

    EMPTY = object()

    def __init__(self):
        self.data = []
        self.stop_event = asyncio.Event()
        self.lock = asyncio.Lock()

    async def add(self, data):
        async with self.lock:
            self.data.append(data)

    async def stop(self):
        async with self.lock:
            self.stop_event.set()

    def __aiter__(self):
        return self

    async def pop(self):
        async with self.lock:
            return self.data.pop(0) if self.data else self.EMPTY

    async def __anext__(self):
        while True:
            result = await self.pop()

            if result is not self.EMPTY:
                return result

            if self.stop_event.is_set() and not self.data:
                raise StopAsyncIteration()

            await asyncio.sleep(0)


def run_in_thread(coro):
    return asyncio.create_task(coro)


class InnerClient:
    def __init__(self, app: "FastAPI"):
        self.app = app

    async def send_request(
        self,
        endpoint: str,
        receiver: Callable,
        headers: dict[str, str] | Headers,
        json_data: dict[str, Any],
        method: str = "GET",
        stream: bool = False,
        http_version: str = "1.1",
    ) -> StreamingResponse | JSONResponse:
        """Send request to the app."""

        called = asyncio.Event()
        can_return = asyncio.Event()

        iterable = ResponseIterable()
        response_kwargs = {}

        async def fake_receive(message: dict[str, Any]):
            if not called.is_set():
                called.set()

                return message

            return await receiver()

        async def fake_send(message: dict[str, Any]):
            if message["type"] == "http.response.start":
                response_kwargs.update(
                    {
                        "status_code": message["status"],
                        "headers": {
                            k.decode(): v.decode() for k, v in message["headers"]
                        },
                    }
                )

                if stream:
                    can_return.set()

            elif message["type"] == "http.response.body":
                if message["body"]:
                    await iterable.add(message["body"])

                if not stream or not message.get("more_body", False):
                    await iterable.stop()
                    can_return.set()

        loop = asyncio.get_running_loop()
        loop.call_soon(
            run_in_thread,
            self.app(
                {
                    "type": "http",
                    "headers": {
                        key.encode(): value.encode() for key, value in headers.items()
                    }.items(),
                    "http_version": http_version,
                    "path": endpoint,
                    "raw_path": endpoint,
                    "method": method.upper(),
                    "query_string": "",
                },
                partial(
                    fake_receive,
                    {
                        "type": "http.request",
                        "body": json.dumps(json_data).encode(),
                    },
                ),
                fake_send,
            ),
        )

        await can_return.wait()

        if stream:
            return StreamingResponse(content=iterable, **response_kwargs)

        return JSONResponse(
            [json.loads(d) async for d in iterable][0],
            **response_kwargs,
        )

    def ollama_chat(
        self,
        request: Request,
        model: str,
        messages: list[dict[str, Any]],
        stream: bool = False,
        tools: bool | None = None,
        options: dict[str, Any] | None = None,
    ):
        """Forward request to ollama chat API."""

        return self.send_request(
            endpoints.OLLAMA_CHAT,
            request.receive,
            request.headers,
            {
                "model": OpenAIModel(model) >> OllamaModel,
                "messages": [
                    {
                        "content": message["content"],
                        "role": message["role"],
                    }
                    for message in messages
                ],
                "options": options,
                "stream": stream,
                "tools": tools,
            },
            stream=stream,
            method="POST",
        )

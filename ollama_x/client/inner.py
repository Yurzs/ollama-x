import asyncio
import json
from functools import partial
from typing import Any, AsyncIterable, Callable

from fastapi import FastAPI, Request
from starlette.datastructures import Headers
from starlette.responses import JSONResponse, StreamingResponse

from ollama_x.api import endpoints
from ollama_x.types import ollama_model_converter


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


class InnerClient:
    def __init__(self, app: FastAPI):
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
                        "headers": {k.decode(): v.decode() for k, v in message["headers"]},
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
            asyncio.create_task,
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
                "model": ollama_model_converter(model),
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

import datetime
import json
import logging
from asyncio import Future
from collections.abc import AsyncIterable
from enum import Enum
from functools import cached_property
from typing import Any, Callable, Coroutine

from fastapi import Request, Response
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from starlette.responses import StreamingResponse

from ollama_x.api.security import authenticate
from ollama_x.model import Session, User

LOG = logging.getLogger(__name__)


class OllamaAction(str, Enum):
    """Ollama action."""

    CHAT = "chat"
    GENERATE = "generate"
    OTHER = "other"


class OllamaProxyMiddleware(BaseModel):
    """Ollama proxy middleware."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    action: OllamaAction = Field(
        ...,
        description="Ollama action",
    )

    request: dict[str, Any] = Field(
        default_factory=dict,
        description="Request to ollama server",
    )

    request_headers: dict[str, str] = Field(
        default_factory=dict,
        description="Headers received in request",
    )

    response: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Response from ollama server",
    )

    start_time: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="Request start time",
    )

    user: User = Field(
        ...,
        description="User",
    )

    completion_start: datetime.datetime | None = Field(
        None,
        description="Completion start time",
    )

    completion_stop: datetime.datetime | None = Field(
        None,
        description="Completion stop time",
    )

    proxy_metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Proxy metadata",
    )

    _model: Callable[..., str] = PrivateAttr(None)

    @property
    def model(self) -> str:
        return self._model()

    @model.setter
    def model(self, getter: Callable[..., str]) -> None:
        self._model = getter

    @cached_property
    def is_done(self):
        return Future()

    @cached_property
    def response_content(self) -> str:
        if self.action == OllamaAction.CHAT:
            return "".join([chunk["message"]["content"] for chunk in self.response])
        elif self.action == OllamaAction.GENERATE:
            return "".join([chunk["response"] for chunk in self.response])

    @cached_property
    def response_metadata(self) -> dict[str, Any]:
        for chunk in self.response:
            if chunk.get("done"):
                return chunk
        return {}

    @cached_property
    def input_text(self) -> str | list[dict[str, Any]]:
        if self.action == OllamaAction.CHAT:
            return self.request["messages"]
        elif self.action == OllamaAction.GENERATE:
            return self.request["prompt"]

    async def get_session(self) -> Session:
        return await Session.find_or_create(
            self.user.id,
            messages=self.input_text if self.action == OllamaAction.CHAT else None,
            context={
                key: value
                for key, value in self.request_headers.items()
                if key not in {"authorization", "content-length"}
            },
        )

    async def listen_stream(self, stream: AsyncIterable[bytes]) -> AsyncIterable[bytes]:

        try:
            async for chunk in stream:
                if self.completion_start is None:
                    self.completion_start = datetime.datetime.now()

                try:
                    self.response.append(json.loads(chunk))
                except json.JSONDecodeError:
                    pass
                finally:
                    yield chunk
        finally:
            self.completion_stop = datetime.datetime.now()
            self.is_done.set_result(self.response_metadata.get("done"))


async def ollama_middleware(
    request: Request,
    call_next: Callable[[Request], Coroutine[Request, None, Response]],
):
    """Adds ollama property to request state."""

    LOG.debug("Processing Ollama middleware")

    ollama: OllamaProxyMiddleware | None = None

    if request.url.path.startswith(("/api/chat", "/api/generate")):
        request_data = await request.json()

        request.state.user = await authenticate(request)

        ollama = request.state.ollama = OllamaProxyMiddleware(
            action=request.url.path.split("/")[-1],
            request=request_data,
            user=request.state.user,
            request_headers=dict(request.headers),
        )
        ollama.model = lambda: request.state.model

    response = await call_next(request)

    if ollama is not None:
        if isinstance(response, StreamingResponse):
            response.body_iterator = ollama.listen_stream(response.body_iterator)
        else:
            ollama.response = response.body
            ollama.is_done.set_result(True)

    LOG.debug("Ollama middleware processed")

    return response

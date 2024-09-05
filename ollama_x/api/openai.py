import json
import time
from typing import Any, AsyncIterable, AsyncIterator, Generic, TypeVar

import bson
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from sse_starlette import EventSourceResponse, ServerSentEvent
from starlette.responses import JSONResponse, StreamingResponse

from ollama_x.api import endpoints
from ollama_x.api.exceptions import APIError
from ollama_x.client.inner import InnerClient
from ollama_x.model.openai import OpenAICompletionMessage

M = TypeVar("M", bound=BaseModel)

router = APIRouter(tags=["openai"])


class SSEMessage(BaseModel, Generic[M]):
    id: int = Field(..., description="Message ID.")
    event: str = Field(..., description="Message Event name.")
    data: M = Field(..., description="Message data.")
    retry: int | None = Field(None, description="Retry timeout.")


def format_ollama_chat_completion(
    message: dict[str, Any],
    is_chunk: bool = False,
    stream_id: None | str = None,
) -> OpenAICompletionMessage | dict[str, Any]:
    if "error" in message:
        return message

    return OpenAICompletionMessage.from_ollama_message(message, is_chunk, stream_id)


class OpenAIEvent(BaseModel):
    id: str | None = None
    event_id: str | None = None
    data: str | None = None


async def stream_chucks(
    messages: AsyncIterable, sse: bool = False
) -> AsyncIterator[SSEMessage[OpenAICompletionMessage] | OpenAICompletionMessage]:
    event_id = int(time.time())
    stream_id = f"chatcmpl-{bson.ObjectId()}"

    async for ollama_message in messages:
        parsed_message = json.loads(ollama_message)
        is_error = "error" in parsed_message

        event = ServerSentEvent() if sse else OpenAIEvent()

        event.event_id = event_id
        event.id = stream_id

        event.data = (
            ollama_message
            if is_error
            else OpenAICompletionMessage.from_ollama_message(
                parsed_message,
                is_chunk=True,
                stream_id=stream_id,
            ).model_dump_json(exclude_none=True)
        )

        yield event if sse else f"{event.data}\n\n"


CompletionResponse = (
    SSEMessage[OpenAICompletionMessage | APIError] | OpenAICompletionMessage | APIError
)


@router.post(endpoints.OPENAI_CHAT, response_model=CompletionResponse)
@router.post(endpoints.OPENAI_LEGACY_CHAT, response_model=CompletionResponse)
@router.post(endpoints.OPENAI_CHAT_COMPLETIONS, response_model=CompletionResponse)
@router.post(
    endpoints.OPENAI_LEGACY_CHAT_COMPLETIONS, response_model=CompletionResponse
)
async def openai_chat(request: Request):
    """Proxy OpenAI completions request."""

    data = await request.json()
    request.state.model = data["model"]

    is_sse_stream = request.headers.get("accept") == "text/event-stream"

    client = InnerClient(request.app)

    response = await client.ollama_chat(
        request,
        data["model"],
        data["messages"],
        stream=data.get("stream", False),
        tools=data.pop("tools", None),
        options={"num_predict": data.pop("max_tokens", None)},
    )

    if response.status_code != 200:
        return response

    if isinstance(response, StreamingResponse) and is_sse_stream:
        return EventSourceResponse(stream_chucks(response.body_iterator, sse=True))

    elif isinstance(response, StreamingResponse):
        response.body_iterator = stream_chucks(response.body_iterator)

    elif isinstance(response, JSONResponse):
        response.body = response.render(format_ollama_chat_completion(response.body))
        response.init_headers()

    return response


@router.post(endpoints.OPENAI_EMBEDDINGS)
@router.post(endpoints.OPENAI_LEGACY_EMBEDDINGS)
async def openai_embeddings(request: Request):
    raise NotImplementedError("OpenAI embeddings are not supported yet.")

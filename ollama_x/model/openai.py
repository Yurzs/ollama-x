from datetime import datetime
from enum import Enum
from typing import Any, Self

import bson
from pydantic import BaseModel, Field, computed_field, field_serializer

from ollama_x.model.helpers import ExplicitNoneBaseModel
from ollama_x.types import OllamaModel, OpenAIModel


class MessageObject(str, Enum):
    COMPLETION = "chat.completion"
    COMPLETION_CHUNK = "chat.completion.chunk"


class ChoiceMessage(BaseModel):
    role: str | None = Field(None, description="Message from role.")
    content: str | None = Field(None, description="Message content.")


class Choice(ExplicitNoneBaseModel):
    index: int = Field(..., description="Response index.")
    finish_reason: str | None = Field(None, description="Finish reason.")
    logprobs: None = Field(None)


class DeltaChoice(Choice):
    delta: ChoiceMessage | None = Field(None, description="Choice delta for stream.")


class MessageChoice(Choice):
    message: ChoiceMessage | None = Field(None, description="Message content if not a stream.")


class ImageChoice(Choice):
    image: str | None = Field(None, description="Image URL.")


Choices = list[MessageChoice | DeltaChoice | ImageChoice]


class Usage(BaseModel):
    completion_tokens: int = Field(..., description="Response token cost.")
    prompt_tokens: int = Field(..., description="Request token cost.")

    @computed_field
    @property
    def total_tokens(self) -> int:
        return self.completion_tokens + self.prompt_tokens


class OpenAICompletionMessage(BaseModel):
    id: str = Field(..., description="Stream ID.")
    system_fingerprint: str = Field("not_supported", description="System fingerprint.")
    created: datetime = Field(default_factory=datetime.now, description="Message creation time.")
    choices: Choices = Field(
        default_factory=list,
        description="Completion choices.",
    )
    model: str = Field(..., description="OllamaModel name.")
    object: MessageObject = Field(..., description="Message type.")

    usage: Usage | None = Field(None, description="Usage stats.")

    @field_serializer("created")
    def serialize_created(self, created: datetime, _) -> int:
        return int(created.timestamp())

    @classmethod
    def from_ollama_message(
        cls,
        message: dict[str, Any],
        is_chunk: bool,
        stream_id: str | None = None,
    ) -> Self:
        """Convert ollama response message to OpenAI message."""

        stream_id = stream_id or f"chatcmpl-{bson.ObjectId()}"

        created_at = datetime.now()
        if "created_at" in message:
            created_at = datetime.strptime(message["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")

        result = {
            "id": stream_id,
            "created": int(created_at.timestamp()),
            "choices": [],
            "model": OllamaModel(message["model"]) >> OpenAIModel,
            "object": f"chat.completion{".chunk" if is_chunk else ""}",
        }

        choice = {
            "index": 0,
            "finish_reason": message.get("done_reason"),
            "logprobs": None,
        }

        if is_chunk:
            choice["delta"] = message["message"]
        else:
            choice["message"] = message["message"]

        result["choices"].append(choice)

        if message.get("done"):
            result["usage"] = {
                "completion_tokens": message.get("eval_count"),
                "prompt_tokens": message.get("prompt_eval_count"),
            }

        return cls.model_validate(result)

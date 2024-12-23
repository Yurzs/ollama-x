import datetime
from typing import Any, Self

import pymongo
from pydantic import Field
from pydantic_mongo_document import ObjectId
from pydantic_mongo_document.document.asyncio import Document

from ollama_x.model import exceptions


class Session(Document):
    """Ollama chat session."""

    __replica__ = "default"
    __database__ = "ollama_x"
    __collection__ = "sessions"

    user: ObjectId = Field(description="User ID")
    messages: list[dict[str, Any]] | None = Field(None, description="Chat messages")
    context: dict[str, Any] | None = Field(None, description="Generate context")
    expires_after: datetime.datetime = Field(
        description="Session expiration time",
        default_factory=lambda: datetime.datetime.now() + datetime.timedelta(seconds=3600),
    )

    DuplicateKeyError = exceptions.DuplicateKeyError

    @classmethod
    async def create_indexes(cls) -> None:
        """Create indexes for the model."""

        await cls.collection().create_index(
            [("user", pymongo.ASCENDING), ("messages", pymongo.ASCENDING)],
            name="user_messages_unique_index",
        )

        await cls.collection().create_index(
            [("expires_after", pymongo.ASCENDING)],
            expireAfterSeconds=1,
            name="expires_after_index",
        )

    @classmethod
    async def find_or_create(
        cls,
        user_id: str,
        messages: list[str] | None = None,
        context: dict[str, Any] | None = None,
    ) -> Self:
        """Find or create new session."""

        query = {"user": user_id}

        if messages is not None:
            query["messages"] = messages

        if context is not None:
            query["context"] = context

        session = await cls.one(add_query=query, required=False)
        if not session:
            session = await cls(user=user_id, messages=messages, context=context).insert()

        return session

    async def add_message(self, message: dict[str, Any]) -> None:
        """Add message to session."""

        self.messages.append(message)
        self.expires_after = datetime.datetime.now() + datetime.timedelta(seconds=3600)

        await self.commit_changes(fields=["messages", "expires_after"])

    async def set_context(self, context: list[int]) -> None:
        """Add context to session."""

        self.context = context
        self.expires_after = datetime.datetime.now() + datetime.timedelta(seconds=3600)

        await self.commit_changes(fields=["context", "expires_after"])

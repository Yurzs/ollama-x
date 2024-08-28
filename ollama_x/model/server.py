import datetime
from collections.abc import AsyncIterable
from typing import Any, Self

import pymongo
from pydantic import BaseModel, Field, HttpUrl
from pydantic_mongo_document import Document, DocumentNotFound
from pytz import utc

from ollama_x.client import OllamaClient
from ollama_x.model import exceptions


class ServerNotFound(DocumentNotFound):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Server not found")


class ServerBase(BaseModel):
    url: HttpUrl = Field(description="Server API base URL")


class APIServer(Document, ServerBase):
    """Ollama API server model."""

    __replica__ = "default"
    __database__ = "ollama_x"
    __collection__ = "api_server"

    DuplicateKeyError = exceptions.DuplicateKeyError
    NotFoundError = ServerNotFound

    last_update: datetime.datetime = Field(
        default=datetime.datetime(1970, 1, 1),
        description="Last update",
    )

    last_alive: datetime.datetime = Field(
        default=datetime.datetime(1970, 1, 1),
        description="Last alive",
    )

    models: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Models",
    )

    running_models: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Running models",
    )

    @property
    def ollama_client(self) -> OllamaClient:
        return OllamaClient(self.url)

    @classmethod
    async def create_indexes(cls) -> None:
        await cls.collection().create_index([("url", pymongo.ASCENDING)], unique=True)
        await cls.collection().create_index([("model.name", pymongo.TEXT)])

    @classmethod
    def all_active(cls, model_name: str = None) -> AsyncIterable[Self]:
        """Find all active servers suitable for the model."""

        query = {
            "last_alive": {
                "$gte": datetime.datetime.now(utc) - datetime.timedelta(seconds=20),
            },
        }

        if model_name is not None:
            query["models.name"] = {"$regex": f"^{model_name}"}

        return cls.all(add_query=query)

    @classmethod
    async def new(cls, base: ServerBase):
        """Create new server."""

        server = cls(url=base.url)
        await server.insert()

        return server

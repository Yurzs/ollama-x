import datetime
from collections.abc import AsyncIterable
from typing import Annotated, Any, Self

import pymongo
from pydantic import AnyHttpUrl, BaseModel, Field
from pydantic_mongo_document import DocumentNotFound
from pydantic_mongo_document.document.asyncio import Document
from pytz import utc

from ollama_x.model import exceptions

from ollama_x.client.ollama import OllamaClient


class ServerNotFound(DocumentNotFound):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Server not found")


class ServerBase(BaseModel):
    url: Annotated[str, AnyHttpUrl] = Field(description="Server API base URL")


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
    def ollama_client(self) -> "OllamaClient":
        return OllamaClient(self.url)

    @classmethod
    async def create_indexes(cls) -> None:
        await cls.collection().create_index([("url", pymongo.ASCENDING)], unique=True)
        await cls.collection().create_index(
            [
                ("model.name", pymongo.TEXT),
                ("running_models.model", pymongo.TEXT),
            ]
        )
        await cls.collection().create_index(
            [("running_models.expires_at", pymongo.ASCENDING)],
        )

    @classmethod
    def all_active(cls, model_name: str = None) -> AsyncIterable[Self]:
        """Find all active servers suitable for the model."""

        query = {
            "last_alive": {
                "$gte": datetime.datetime.now(utc) - datetime.timedelta(seconds=20),
            },
        }

        if model_name is not None:
            model, *version = model_name.split(":", 1)
            if not version:
                version_regex = "(:latest)?"
            else:
                version_regex = rf":{version}"

            model_regex = rf"{model}{version_regex}"

            query["$or"] = [
                {"models.name": {"$regex": model_regex}},
                {"running_models.model": {"$regex": model_regex}},
            ]

        return cls.all(add_query=query)

    @classmethod
    async def new(cls, base: ServerBase):
        """Create new server."""

        server = cls(url=base.url)
        await server.insert()

        return server

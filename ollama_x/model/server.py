import datetime
from typing import Any

import pymongo
from pydantic import BaseModel, Field, HttpUrl
from pydantic_mongo_document import Document
from pytz import utc


class ServerBase(BaseModel):
    url: HttpUrl = Field(description="Server API base URL")


class APIServer(Document, ServerBase):
    """Ollama API server model."""

    __replica__ = "default"
    __database__ = "ollama_x"
    __collection__ = "api_server"

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

    @classmethod
    async def create_indexes(cls) -> None:
        await cls.collection().create_index([("url", pymongo.ASCENDING)], unique=True)

    @classmethod
    async def all_active(cls, model_name: str = None):
        """Find all active servers suitable for the model."""

        query = {
            "last_alive": {
                "$gte": datetime.datetime.now(utc) - datetime.timedelta(seconds=20),
            },
        }

        if model_name is not None:
            query["models.name"] = model_name

        return await cls.all(add_query=query)

    @classmethod
    async def new(cls, base: ServerBase):
        """Create new server."""

        server = cls(url=base.url)
        await server.insert()

        return server

from typing import Any, Self

import pymongo
from pydantic import ConfigDict, Field
from pydantic_mongo_document.document.asyncio import Document


class OllamaModel(Document):
    model_config = ConfigDict(populate_by_name=True)

    __replica__ = "default"
    __database__ = "ollama_x"
    __collection__ = "models"

    id: str = Field(description="OllamaModel name", alias="_id")
    file: str = Field(description="model build file", alias="modelfile")
    template: str = Field(description="OllamaModel template")
    details: dict[str, Any] = Field(description="OllamaModel details")
    info: dict[str, Any] = Field(description="OllamaModel info")

    digest: str = Field(None, description="OllamaModel hash")

    @classmethod
    async def create_indexes(cls) -> None:
        await cls.collection().create_index(
            [("id", pymongo.ASCENDING), ("digest", pymongo.ASCENDING)],
            unique=True,
        )

    @classmethod
    def from_ollama_show(cls, model_name: str, data: dict[str, Any], digest: str) -> Self:
        return cls(
            id=model_name,
            file=data["modelfile"],
            template=data["template"],
            details=data["details"],
            info=data["model_info"],
            digest=digest,
        )

    @classmethod
    async def find_one(cls, name: str, digest: str | None = None, required: bool = True) -> Self:
        """Find one model by name and digest."""

        query = {}

        if digest is not None:
            query["digest"] = digest

        return await cls.one(name, add_query=query, required=required)

    @classmethod
    async def create_or_update(cls, name: str, ollama_show: dict[str, Any], digest: str) -> Self:
        """Create or update model."""

        model = await cls.find_one(name, required=False)

        if model is not None and model.digest != digest:
            await model.delete()
            model = None

        return model or await cls.from_ollama_show(name, ollama_show, digest).insert()

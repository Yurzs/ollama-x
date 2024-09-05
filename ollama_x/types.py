import re
from enum import Enum
from typing import Any, Self, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class ModelNameType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"


class Model(str):
    type: ModelNameType
    pattern: str
    separator: str

    def __rshift__(self, other: Type[Self]) -> Self:
        return other(self.convert_model_name(other))

    def convert_model_name(self, to_type: Type[Self]) -> str:
        """Convert model name from one type to another."""

        match re.match(self.pattern, self):
            case None:
                raise ValueError(f"Invalid model name: {self}")
            case match:
                model = match.group("model")
                version = match.group("version")

                return f"{model}{f"{to_type.separator}{version}" if version else ""}"

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.str_schema(pattern=cls.pattern)


class OllamaModel(Model):
    type = ModelNameType.OLLAMA
    pattern = r"(?P<model>[\w\d\.\-]*)(\:(?P<version>[\w\d\.\-]*))?"
    separator = ":"


class OpenAIModel(Model):
    type = ModelNameType.OPENAI
    pattern = r"(?P<model>[\w\d\.\-]*)(\/(?P<version>[\w\d\.\-]*))?"
    separator = "/"


Models = OllamaModel | OpenAIModel

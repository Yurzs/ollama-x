import re
from enum import Enum
from typing import Annotated, Any

from pydantic import BeforeValidator, StrictStr


class ModelNameType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"


class ModelConvertor:
    separator: str

    PATTERN = r"(?P<model>[\w\d\.\-]*)([\:\/](?P<version>[\w\d\.\-]*))?"

    SEPARATORS = {
        ModelNameType.OLLAMA: ":",
        ModelNameType.OPENAI: "/",
    }

    def __init__(self, model_type: ModelNameType) -> None:
        self.type = model_type

    @property
    def separator(self):
        return self.SEPARATORS[self.type]

    def __call__(self, value: Any) -> str:
        """Convert model name from one type to another."""

        match re.match(self.PATTERN, value):
            case None:
                raise ValueError(f"Invalid model name: {value}")
            case match:
                model = match.group("model")
                version = match.group("version")

                return f"{model}{f"{self.separator}{version}" if version else ""}"


ollama_model_converter = ModelConvertor(ModelNameType.OLLAMA)
openai_model_converter = ModelConvertor(ModelNameType.OPENAI)

type OllamaModel = Annotated[
    StrictStr,
    BeforeValidator(ollama_model_converter),
]

type OpenAIModel = Annotated[
    StrictStr,
    BeforeValidator(openai_model_converter),
]

type Models = OllamaModel | OpenAIModel

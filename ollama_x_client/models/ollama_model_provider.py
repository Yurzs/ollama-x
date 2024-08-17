from enum import Enum


class OllamaModelProvider(str, Enum):
    OLLAMA = "ollama"

    def __str__(self) -> str:
        return str(self.value)

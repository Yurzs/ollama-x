from enum import Enum


class TabAutocompleteModelProvider(str, Enum):
    OLLAMA = "ollama"

    def __str__(self) -> str:
        return str(self.value)

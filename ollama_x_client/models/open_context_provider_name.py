from enum import Enum


class OpenContextProviderName(str, Enum):
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)

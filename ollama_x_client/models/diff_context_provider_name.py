from enum import Enum


class DiffContextProviderName(str, Enum):
    DIFF = "diff"

    def __str__(self) -> str:
        return str(self.value)

from enum import Enum


class SearchContextProviderName(str, Enum):
    SEARCH = "search"

    def __str__(self) -> str:
        return str(self.value)

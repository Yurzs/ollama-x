from enum import Enum


class UrlContextProviderName(str, Enum):
    URL = "url"

    def __str__(self) -> str:
        return str(self.value)

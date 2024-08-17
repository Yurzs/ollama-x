from enum import Enum


class DocsContextProviderName(str, Enum):
    DOCS = "docs"

    def __str__(self) -> str:
        return str(self.value)

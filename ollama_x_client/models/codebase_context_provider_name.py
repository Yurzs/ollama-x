from enum import Enum


class CodebaseContextProviderName(str, Enum):
    CODEBASE = "codebase"

    def __str__(self) -> str:
        return str(self.value)

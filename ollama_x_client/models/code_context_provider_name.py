from enum import Enum


class CodeContextProviderName(str, Enum):
    CODE = "code"

    def __str__(self) -> str:
        return str(self.value)
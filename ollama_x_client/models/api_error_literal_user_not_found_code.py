from enum import Enum


class APIErrorLiteralUserNotFoundCode(str, Enum):
    USERNOTFOUND = "UserNotFound"

    def __str__(self) -> str:
        return str(self.value)

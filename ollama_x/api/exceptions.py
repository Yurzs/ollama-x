from typing import Generic, TypeVar

import pymongo.errors
from fastapi import HTTPException, Request
from pydantic import BaseModel, Field
from pydantic_mongo_document import DocumentNotFound

C = TypeVar("C")


class APIError(BaseModel, Generic[C]):
    code: C = Field(..., description="Error code")
    details: str = Field(..., description="Error details")


class APIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        username: str | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.username = username


class AccessDenied(APIException):
    def __init__(
        self,
        detail: str = "Access denied",
        username: str | None = None,
    ) -> None:
        super().__init__(status_code=403, detail=detail, username=username)


class UserNotFound(APIException):
    def __init__(
        self,
        detail: str = "User not found",
        username: str | None = None,
    ) -> None:
        super().__init__(status_code=400, detail=detail, username=username)


class NoServerAvailable(APIException):
    def __init__(
        self,
        detail: str = "No server available",
        username: str | None = None,
    ) -> None:
        super().__init__(status_code=503, detail=detail, username=username)


def handle_document_not_found(request: Request, exc: DocumentNotFound):
    raise APIException(status_code=400, detail=str(exc))


def handle_duplicate_key_error(request: Request, exc: pymongo.errors.DuplicateKeyError):
    index_map = zip(exc.details["keyPattern"].keys(), exc.details["keyValue"].values())
    raise APIException(status_code=400, detail=f"Duplicate key error: {dict(index_map)}")


HANDLERS = {
    DocumentNotFound: handle_document_not_found,
    pymongo.errors.DuplicateKeyError: handle_duplicate_key_error,
}

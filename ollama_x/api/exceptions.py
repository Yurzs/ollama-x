from typing import Generic, Literal, Self, TypeVar

from fastapi import Request
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from pydantic_mongo_document import DocumentNotFound
from starlette.responses import JSONResponse

from ollama_x.model.exceptions import DuplicateKeyError

TE = TypeVar("TE", bound=type[Exception])
E = TypeVar("E", bound=Exception)
T = TypeVar("T")

C = TypeVar("C", bound="str")


@dataclass(frozen=True)
class APIErrorDetails(Generic[C]):
    code: C
    message: str

    def __class_getitem__(cls, item: TypeVar | str | Exception | type[Exception]) -> Self:
        if isinstance(item, type) and issubclass(item, BaseException):
            return super().__class_getitem__(Literal[item.__name__])
        if isinstance(item, BaseException):
            return super().__class_getitem__(Literal[item.__class__.__name__])
        if isinstance(item, (TypeVar, str)):
            return super().__class_getitem__(item)

        raise TypeError(f"Unsupported type {item} {type(item)}")


class APIError(BaseModel, Generic[TE]):
    detail: APIErrorDetails[TE] = Field(description="Error detail")

    def __init__(self, exc: E) -> None:
        super().__init__(detail={"code": exc.__class__.__name__, "message": str(exc)})


class BaseAPIException(Exception):
    status_code: int = 500

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class AccessDenied(BaseAPIException):
    status_code: int = 403

    def __init__(self) -> None:
        super().__init__("Access denied")


class UserNotFound(BaseAPIException):
    status_code = 404

    def __init__(self, detail: str = "User not found") -> None:
        super().__init__(detail)


class NoServerAvailable(BaseAPIException):
    status_code = 503

    def __init__(self, detail: str = "No server available") -> None:
        super().__init__(detail)


class UserAlreadyExist(BaseAPIException):
    status_code = 400

    def __init__(self) -> None:
        super().__init__("User already exist.")


class UserAlreadyInProject(BaseAPIException):
    status_code = 400

    def __init__(self):
        super().__init__("User already in project.")


def handle_document_not_found(request: Request, exc: DocumentNotFound) -> JSONResponse:
    return JSONResponse(
        content=APIError[exc](exc).model_dump(by_alias=True),
        status_code=404,
    )


def handle_duplicate_key_error(request: Request, exc: DuplicateKeyError):
    return JSONResponse(
        status_code=400,
        content=APIError[exc](exc).model_dump(by_alias=True),
    )


def handle_generic_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=APIError[exc](exc).model_dump(by_alias=True),
    )


HANDLERS = {
    DocumentNotFound: handle_document_not_found,
    DuplicateKeyError: handle_duplicate_key_error,
    Exception: handle_generic_exception,
}

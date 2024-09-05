import base64
import random
import string
from typing import Annotated, ClassVar, Self

import pymongo
import pymongo.errors
from pydantic import BaseModel, ConfigDict, Field, SecretStr, StringConstraints
from pydantic_mongo_document import DocumentNotFound
from pydantic_mongo_document.document.asyncio import Document

from ollama_x.model import exceptions


class UserNotFound(DocumentNotFound):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "User not found")


class DuplicateKeyError(pymongo.errors.DuplicateKeyError):
    def __str__(self) -> str:
        return str(zip(self.details["keyPattern"].keys(), self.details["keyValue"].values()))


class UserBase(BaseModel):
    username: Annotated[
        str,
        StringConstraints(strip_whitespace=True, max_length=50, min_length=4),
        Field(description="Username"),
    ]
    is_admin: bool = Field(default=False, description="Is user admin flag")
    key: str | None = Field(description="Users API key")

    @classmethod
    def from_document(cls, doc: "User", exclude_secrets: bool = True) -> Self:
        return cls(
            username=doc.username,
            is_admin=doc.is_admin,
            key=doc.key.get_secret_value() if doc.key and not exclude_secrets else None,
        )


class User(UserBase, Document):
    model_config = ConfigDict(populate_by_name=True)

    __replica__: ClassVar[str] = "default"
    __database__: ClassVar[str] = "ollama_x"
    __collection__: ClassVar[str] = "users"

    key: SecretStr = Field(description="Users API key")

    NotFoundError = UserNotFound
    DuplicateKeyError = exceptions.DuplicateKeyError

    KEY_MIN_LENGTH: ClassVar[int] = 40
    KEY_MAX_LENGTH: ClassVar[int] = 60
    BANNED_KEY_CHARS: ClassVar[set[str]] = {'"', "'", "\\", ":"}
    ALLOWED_KEY_CHARS: ClassVar[set[str]] = set(
        string.ascii_letters + string.digits + string.punctuation
    ).difference(BANNED_KEY_CHARS)
    KEY_CHARS: ClassVar[str] = "".join(ALLOWED_KEY_CHARS)

    @property
    def is_guest(self):
        return self.username == "guest"

    @classmethod
    async def create_indexes(cls) -> None:
        await cls.collection().create_index(
            [("key", pymongo.ASCENDING)],
            unique=True,
        )

        await cls.collection().create_index(
            [("username", pymongo.ASCENDING)],
            unique=True,
        )

    @classmethod
    def generate_key(cls) -> SecretStr:
        """Generate new API key."""

        key_len = random.randint(cls.KEY_MIN_LENGTH, cls.KEY_MAX_LENGTH)

        return SecretStr(
            base64.urlsafe_b64encode(
                "".join(random.choice(cls.KEY_CHARS) for _ in range(key_len)).encode()
            ).decode()
        )

    @classmethod
    async def new(
        cls,
        username: str,
        key: str | None = None,
        is_admin: bool = False,
    ) -> Self:
        """Create new user."""

        user = cls(username=username, key=key or cls.generate_key(), is_admin=is_admin)

        await user.insert()

        return user

    @classmethod
    async def one_by_key(
        cls,
        key: str,
        required: bool = True,
        is_admin: bool | None = None,
    ) -> Self | None:
        """Find user by its key."""

        query = {
            "key": key,
        }

        if is_admin is not None:
            query["is_admin"] = is_admin

        return await cls.one(add_query=query, required=required)

    @classmethod
    async def one_by_username(cls, username: str, required: bool = True) -> Self | None:
        """Find user by username."""

        return await User.one(add_query={"username": username}, required=required)

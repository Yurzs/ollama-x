import random
import string
from typing import ClassVar, Self

import pymongo
from pydantic import BaseModel, ConfigDict, Field, SecretStr
from pydantic_mongo_document import Document, DocumentNotFound


class UserNotFound(DocumentNotFound):
    def __init__(self, username: str) -> None:
        super().__init__(f"User '{username}' not found")


class UserBase(BaseModel):
    username: str = Field(description="Username")
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

    KEY_MIN_LENGTH: ClassVar[int] = 40
    KEY_MAX_LENGTH: ClassVar[int] = 60
    BANNED_KEY_CHARS: ClassVar[set[str]] = {'"', "'", "\\"}
    ALLOWED_KEY_CHARS: ClassVar[set[str]] = set(
        string.ascii_letters + string.digits + string.punctuation
    ).difference(BANNED_KEY_CHARS)
    KEY_CHARS: ClassVar[str] = "".join(ALLOWED_KEY_CHARS)

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

        return SecretStr("".join(random.choice(cls.KEY_CHARS) for _ in range(key_len)))

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

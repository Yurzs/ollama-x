from fastapi import APIRouter
from pydantic import BaseModel

from ollama_x.api.exceptions import UserNotFound
from ollama_x.api.helpers import AdminUser
from ollama_x.model import User
from ollama_x.model.user import UserBase

router = APIRouter(prefix="/user", tags=["user"])


class CreateUserRequest(BaseModel):
    username: str
    is_admin: bool = False


@router.get(
    "/",
    operation_id="get-user",
    summary="Get all users or user by username",
    tags=["admin"],
)
async def get_user(admin: AdminUser, username: str | None = None) -> User | list[User]:
    """Get users."""

    if username is None:
        return await User.all()

    user = await User.one_by_username(username, required=False)

    if user is None:
        raise UserNotFound()

    return user


@router.post(
    "/",
    operation_id="create-user",
    summary="Create user",
    response_model_exclude_defaults=True,
    response_model_exclude_none=True,
    tags=["admin"],
)
async def create_user(admin: AdminUser, user: CreateUserRequest) -> UserBase:
    """Create new user."""

    return UserBase.from_document(
        await User.new(username=user.username, is_admin=user.is_admin),
        exclude_secrets=False,
    )


@router.delete("/", operation_id="delete-user", summary="Delete user", tags=["admin"])
async def delete_user(admin: AdminUser, username: str) -> User:
    """Delete user by username."""

    user = await User.one_by_username(username)

    await user.delete()

    return user


@router.post(
    "/reset_key",
    response_model=UserBase,
    operation_id="reset-user-key",
    summary="Reset user API key",
    tags=["admin"],
)
async def change_key(admin: AdminUser, username: str) -> UserBase:
    """Change user key by username."""

    user = await User.one_by_username(username)

    user.key = User.generate_key()

    await user.commit_changes(fields=["key"])

    return UserBase.from_document(user, exclude_secrets=False)

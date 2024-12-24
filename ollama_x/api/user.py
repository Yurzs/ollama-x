from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from ollama_x.api.exceptions import AccessDenied, APIError, UserAlreadyExist, UserNotFound
from ollama_x.api.helpers import AdminUser
from ollama_x.model import User
from ollama_x.model.user import UserBase
from ollama_x.config import config

PREFIX = "user"

router = APIRouter(prefix=f"/{PREFIX}", tags=[PREFIX])


class CreateUserRequest(BaseModel):
    username: str
    is_admin: bool = False


@router.get(
    "/one",
    operation_id=f"{PREFIX}.one",
    summary="Get user by username",
    tags=["admin"],
    response_model=User | APIError,
    responses={
        403: {
            "model": APIError[AccessDenied],
            "description": "Access errors",
        },
        404: {
            "model": APIError[User.NotFoundError],
            "description": "Not found errors",
        },
    },
)
async def get_user(admin: AdminUser, username: str) -> User | list[User]:
    """Get users."""

    user = await User.one_by_username(username, required=False)

    if user is None:
        raise UserNotFound()

    return user


@router.get(
    "/all",
    operation_id=f"{PREFIX}.all",
    summary="Get user by username",
    tags=["admin"],
    response_model=list[User] | APIError,
    responses={
        403: {
            "model": APIError[AccessDenied],
            "description": "Access errors",
        },
    },
)
async def get_all_users(admin: AdminUser) -> list[User]:
    """Get users from database."""

    return [user async for user in User.all()]


@router.post(
    "/",
    operation_id=f"{PREFIX}.create",
    summary="Create user",
    response_model=UserBase | APIError,
    response_model_exclude_defaults=True,
    response_model_exclude_none=True,
    tags=["admin"],
    responses={
        400: {
            "model": APIError[UserAlreadyExist],
            "description": "Generic errors",
        }
    },
)
async def create_user(admin: AdminUser, username: str, is_admin: bool = False) -> UserBase:
    """Create new user."""

    return UserBase.from_document(
        await User.new(username=username, is_admin=is_admin),
        exclude_secrets=False,
    )


@router.delete(
    "/",
    operation_id=f"{PREFIX}.delete",
    summary="Delete user",
    tags=["admin"],
    response_model=User | APIError,
    responses={
        403: {
            "model": APIError[AccessDenied],
            "description": "Access errors",
        },
        404: {
            "model": APIError[User.NotFoundError],
            "description": "Not found errors",
        },
    },
)
async def delete_user(admin: AdminUser, username: str) -> User:
    """Delete user by username."""

    user = await User.one_by_username(username)

    await user.delete()

    return user


@router.post(
    "/reset_key",
    response_model=UserBase | APIError,
    operation_id=f"{PREFIX}.reset-key",
    summary="Reset user API key",
    tags=["admin"],
    responses={
        403: {
            "model": APIError[AccessDenied],
            "description": "Access errors",
        },
        404: {
            "model": APIError[User.NotFoundError],
            "description": "Not found errors",
        },
    },
)
async def change_key(admin: AdminUser, username: str) -> UserBase:
    """Change user key by username."""

    user = await User.one_by_username(username)

    user.key = User.generate_key()

    await user.commit_changes(fields=["key"])

    return UserBase.from_document(user, exclude_secrets=False)


@router.get(
    "/register",
    operation_id=f"{PREFIX}.register",
    response_model=UserBase | APIError,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    summary="Register new user",
    responses={
        400: {
            "model": APIError[UserAlreadyExist],
            "description": "Generic errors",
        },
        403: {
            "model": APIError[AccessDenied],
            "description": "Access denied",
        },
    },
)
async def user_register(email: EmailStr) -> UserBase:
    """Register new user get user key in response."""

    if not config.user_registration_enabled:
        raise AccessDenied()

    if await User.one_by_username(email, required=False) is not None:
        raise UserAlreadyExist()

    user = await User.new(username=email)

    return UserBase.from_document(user, exclude_secrets=False)

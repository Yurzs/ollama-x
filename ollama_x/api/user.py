from datetime import timedelta
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from ollama_x.api.exceptions import AccessDenied, APIError, UserAlreadyExist, UserNotFound
from ollama_x.api.helpers import AdminUser
from ollama_x.api.security import (
    Token,
    create_access_token,
    get_current_user,
    get_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from ollama_x.model.user import User, UserBase
from ollama_x.config import config

router = APIRouter(prefix="/api/user", tags=["user"])


class CreateUserRequest(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post(".login", response_model=Token)
async def login_for_access_token(form_data: LoginRequest):
    """Generate JWT token for user authentication."""

    user = await User.authenticate(form_data.username, form_data.password)
    if not user:
        raise AccessDenied(message="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserBase)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserBase.from_document(current_user)


@router.get(
    ".one",
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
async def get_user(admin: User = Depends(get_admin_user), username: str = None) -> User:
    """Get users."""
    user = await User.one_by_username(username, required=False)
    if user is None:
        raise UserNotFound()
    return user


@router.get(
    ".all",
    summary="Get all users",
    tags=["admin"],
    response_model=list[User] | APIError,
    responses={
        403: {
            "model": APIError[AccessDenied],
            "description": "Access errors",
        },
    },
)
async def get_all_users(admin: User = Depends(get_admin_user)) -> list[User]:
    """Get users from database."""
    return [user async for user in User.all()]


@router.post(
    ".create",
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
async def create_user(
    user_data: CreateUserRequest, admin: User = Depends(get_admin_user)
) -> UserBase:
    """Create new user."""
    return UserBase.from_document(
        await User.new(
            username=user_data.username, password=user_data.password, is_admin=user_data.is_admin
        ),
        exclude_secrets=False,
    )


@router.delete(
    ".delete",
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
    ".reset_key",
    response_model=UserBase | APIError,
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
    ".register",
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
async def user_register(email: EmailStr, password: str) -> UserBase:
    """Register new user."""
    if not config.user_registration_enabled:
        raise AccessDenied()

    if await User.one_by_username(email, required=False) is not None:
        raise UserAlreadyExist()

    user = await User.new(username=email, password=password)
    return UserBase.from_document(user, exclude_secrets=False)

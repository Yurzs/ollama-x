from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials

from ollama_x.api.exceptions import AccessDenied
from ollama_x.api.security import security
from ollama_x.model import Session, User


def get_token(authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> str:
    """Get token key from header."""

    if authorization.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid token")

    return authorization.credentials


BearerToken = Annotated[str, Depends(get_token)]


async def auth_user(token: BearerToken, request: Request) -> User:
    """Get user from token."""

    if hasattr(request.state, "user"):
        return request.state.user

    try:
        request.state.user = await User.one_by_key(token)
    except User.NotFoundError:
        raise AccessDenied()
    else:
        return request.state.user


async def admin_user(token: BearerToken, request: Request) -> User:
    """Get admin user from token."""

    is_local = request.client.host in ["localhost", "127.0.0.1"]

    if is_local and token == "admin":
        if not await User.all(add_query={"is_admin": True}):
            await User.new(username="admin", key="admin", is_admin=True)

    if hasattr(request.state, "user"):
        if not request.state.user.is_admin:
            raise AccessDenied()
    else:
        try:
            request.state.user = await User.one_by_key(token, is_admin=True)
        except User.NotFoundError:
            raise AccessDenied()

    if not is_local and request.state.user.key == "admin":
        raise AccessDenied()

    return request.state.user


AuthorizedUser = Annotated[User, Depends(auth_user)]
AdminUser = Annotated[User, Depends(admin_user)]


async def get_session(user: AuthorizedUser, request: Request):
    """Get session from request."""

    if hasattr(request.state, "session"):
        return request.state.session

    request_data = await request.json()

    request.state.session = await Session.find_or_create(
        user_id=user.id,
        messages=request_data.get("messages"),
        context=request_data.get("context"),
    )

    return request.state.session


AISession = Annotated[Session, Depends(get_session)]

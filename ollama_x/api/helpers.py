from typing import Annotated, Any, Callable

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials

from ollama_x.api.exceptions import AccessDenied
from ollama_x.api.security import oauth2_scheme
from ollama_x.model.user import User
from ollama_x.model.continue_dev import ContinueDevProject
from ollama_x.model.session import Session


def get_token(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
) -> str:
    """Get token key from header."""

    if authorization is None or authorization.scheme != "Bearer":
        raise AccessDenied()

    return authorization.credentials


BearerToken = Annotated[str, Depends(get_token)]


async def auth_user(token: BearerToken, request: Request) -> User:
    """Get user from token."""

    if getattr(request.state, "user", None) is not None:
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
        if not await User.one(add_query={"is_admin": True}, required=False):
            await User.new(username="admin", key="admin", is_admin=True)

    if getattr(request.state, "user", None) is not None and not request.state.user.is_admin:
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


async def continue_dev_auth(token: BearerToken, request: Request) -> ContinueDevProject:
    """Authorize user using user_key:project_token"""

    user_key, project_id = token.split(":", 1)

    user = request.state.user = await User.one_by_key(user_key)
    if user is None:
        raise AccessDenied()

    project = request.state.project = await ContinueDevProject.one(project_id)
    if project is None:
        raise AccessDenied()

    if user.id not in project.users:
        raise AccessDenied()

    return project


ContinueProject = Annotated[ContinueDevProject, Depends(continue_dev_auth)]


async def is_project_admin(user: AuthorizedUser, project_id: str):
    """Check if user is project admin."""

    project = await ContinueDevProject.one(project_id)

    if not user.is_admin and user.username != project.admin:
        raise AccessDenied()

    return project


ProjectWithAdminAccess = Annotated[ContinueDevProject, Depends(is_project_admin)]


def merge_responses(*responses: dict[int, dict[str, Any]]) -> dict[int, dict[str, Any]]:
    """Merge responses."""

    result = {}

    for response in responses:
        for status_code, response_data in response.items():
            response_model = response_data.pop("model", None)
            response_description = response_data.pop("description", None)

            result_model = result.setdefault(status_code, {}).setdefault("model", response_model)
            result.setdefault(status_code, {}).setdefault("description", response_description)

            result[status_code]["model"] = result_model | response_model

    return result


def multi_endpoint(router_method: Callable, *routes: list[str], **kwargs):
    """Create multiple endpoints."""

    def decorator(func):
        for route in routes:
            router_method(route, **kwargs)(func)

        return func

    return decorator

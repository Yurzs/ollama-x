from fastapi import HTTPException, Request
from fastapi.security import APIKeyHeader, HTTPBearer

from ollama_x.api.exceptions import AccessDenied
from ollama_x.config import config
from ollama_x.model import User

header_scheme = APIKeyHeader(
    name="Authorization",
    scheme_name="Bearer",
    description="Bearer token",
    auto_error=True,
)


security = HTTPBearer(auto_error=False)


async def authenticate(request: Request, anonymous_allowed: bool = True) -> User:
    """Authenticate request."""

    authorization = await security(request)
    if authorization is None:
        raise AccessDenied()

    anonymous_allowed = anonymous_allowed and config.anonymous_allowed

    if authorization.scheme != "Bearer" and not anonymous_allowed:
        raise HTTPException(status_code=401, detail="Invalid token")

    if authorization.credentials == "undefined" and anonymous_allowed:
        return User(
            id="guest",
            username="guest",
            key=User.generate_key(),
        )

    try:
        return await User.one_by_key(authorization.credentials)
    except User.NotFoundError:
        raise AccessDenied()

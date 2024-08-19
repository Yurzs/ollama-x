from fastapi import HTTPException, Request
from fastapi.security import APIKeyHeader, HTTPBearer

from ollama_x.config import config
from ollama_x.model import User

header_scheme = APIKeyHeader(
    name="Authorization",
    scheme_name="Bearer",
    description="Bearer token",
    auto_error=True,
)


security = HTTPBearer()


async def authenticate(request: Request) -> User:
    """Authenticate request."""

    authorization = await security(request)

    if authorization.scheme != "Bearer" and not config.anonymous_allowed:
        raise HTTPException(status_code=401, detail="Invalid token")

    if authorization.credentials == "undefined" and config.anonymous_allowed:
        return User(
            _id="guest",
            username="guest",
            key=User.generate_key(),
        )

    return await User.one_by_key(authorization.credentials)

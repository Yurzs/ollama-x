from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from ollama_x.api.exceptions import AccessDenied
from ollama_x.config import config
from ollama_x.model.user import User

# Generate a secure secret key: openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user.login")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    from ollama_x.config import config

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.jwt_secret_key.get_secret_value(), algorithm=ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get the current user from the token."""

    from ollama_x.config import config

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.jwt_secret_key.get_secret_value(), algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    try:
        user = await User.one_by_username(token_data.username)
    except User.NotFoundError:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise AccessDenied()
    return current_user


async def authenticate(request: Request, anonymous_allowed: bool = False) -> User:
    """Authenticate user from request."""

    if getattr(request.state, "user", None) is not None:
        return request.state.user

    try:
        token = request.headers["Authorization"].split(" ")[1]
        user = await get_current_user(token)
    except (KeyError, IndexError):
        if anonymous_allowed:
            return User(username="guest", key="")
        raise AccessDenied()

    request.state.user = user
    return user

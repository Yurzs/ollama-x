import logging
from typing import Literal

from pydantic import ConfigDict, Field, SecretStr
from pydantic_app_config import EnvAppConfig

from ollama_x.types import OllamaModel

LOG = logging.getLogger(__name__)


class OllamaXConfig(EnvAppConfig):
    """OllamaX app configuration."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        frozen=True,
        validate_default=True,
        validate_assignment=True,
    )

    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = Field(
        default="info",
        description="Logging level",
        alias="LOG_LEVEL",
    )

    mongo_uri: str = Field(
        default="mongodb://mongo",
        description="Mongodb connection URI",
        alias="MONGO_URI",
    )

    server_check_interval: int = Field(
        default=10,
        description="Ollama API Server check interval in seconds",
        alias="SERVER_CHECK_INTERVAL",
    )

    langfuse_secret_key: str | None = Field(
        default=None,
        description="Langfuse secret key",
        alias="LANGFUSE_SECRET_KEY",
    )

    langfuse_public_key: str | None = Field(
        default=None,
        description="Langfuse public key",
        alias="LANGFUSE_PUBLIC_KEY",
    )

    langfuse_host: str | None = Field(
        default=None,
        description="Langfuse host",
        alias="LANGFUSE_HOST",
    )

    enforce_model: str | None = Field(
        None, description="Enforce model for all requests", alias="ENFORCE_MODEL"
    )

    client_generation: bool = Field(
        default=False,
        description="Client generation flag",
        alias="CLI_GEN",
    )

    anonymous_allowed: bool = Field(
        default=False,
        description="Anonymous allowed flag",
        alias="ANONYMOUS_ALLOWED",
    )

    anonymous_model: str | None = Field(
        None,
        description="Enforced anonymous users model.",
        alias="ANONYMOUS_MODEL",
    )

    sentry_dsn: str | None = Field(
        default=None,
        description="Sentry DSN",
        alias="SENTRY_DSN",
    )

    default_embeddings_model: OllamaModel | None = Field(
        default="nomic-embed-text:latest",
        description="Default embeddings model",
        alias="DEFAULT_EMBEDDINGS_MODEL",
    )

    default_completions_model: OllamaModel | None = Field(
        default="deepseek-coder-v2:latest",
        description="Default model completions",
        alias="DEFAULT_COMPLETIONS_MODEL",
    )

    default_chat_model: OllamaModel | None = Field(
        default="deepseek-coder-v2:latest",
        description="Default model completions",
        alias="DEFAULT_CHAT_MODEL",
    )

    user_registration_enabled: bool = Field(
        default=False,
        description="Flag to enable user registration",
        alias="USER_REGISTRATION_ENABLED",
    )

    jwt_secret_key: SecretStr = Field(
        default="jwt-token-please-redefine",
        description="Secret key for JWT token generation",
        alias="JWT_SECRET_KEY",
    )

    jwt_token_expire_minutes: int = Field(
        default=30,
        description="JWT token expiration time in minutes",
        alias="JWT_TOKEN_EXPIRE_MINUTES",
    )


config = OllamaXConfig.load()

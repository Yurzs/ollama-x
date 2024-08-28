import logging
from typing import Annotated, ClassVar, Literal

import sentry_sdk
from pydantic import AnyUrl, Field, UrlConstraints
from pydantic_app_config import EnvAppConfig
from pydantic_mongo_document import Document
from pydantic_mongo_document.document import ReplicaConfig

MongoURI = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["mongodb", "mongodb+srv"])]


LOG = logging.getLogger(__name__)

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def setup_document(conf: "OllamaXConfig") -> None:
    """Sets up document."""

    if conf.client_generation:
        return

    Document.set_replica_config(
        {
            "default": ReplicaConfig(
                uri=conf.mongo_uri,
                client_options={
                    "serverSelectionTimeoutMS": 50,
                },
            )
        }
    )


async def ensure_indexes(conf: "OllamaXConfig") -> None:
    """Ensure indexes for all models."""

    import ollama_x.model

    if conf.client_generation:
        return

    for model in ollama_x.model.__all__:
        if isinstance(model, type) and issubclass(model, Document):
            await getattr(ollama_x.model, model).create_indexes()


def setup_log(conf: "OllamaXConfig") -> None:
    import logging

    logging.basicConfig(level=LOG_LEVELS[conf.log_level.upper()])


def setup_sentry(conf: "OllamaXConfig") -> None:
    if conf.client_generation:
        return

    if conf.sentry_dsn:
        sentry_sdk.init(conf.sentry_dsn)


class OllamaXConfig(EnvAppConfig):
    """OllamaX app configuration."""

    STARTUP: ClassVar = [setup_log, setup_document, ensure_indexes, setup_sentry]

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

    mongo_uri: MongoURI = Field(
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


config = OllamaXConfig.load()

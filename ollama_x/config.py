import asyncio
import logging
from typing import Annotated, ClassVar, Literal

from pydantic import AnyUrl, Field, UrlConstraints
from pydantic_app_config import EnvAppConfig
from pydantic_mongo_document import Document
from pydantic_mongo_document.document import ReplicaConfig

import ollama_x.model

MongoURI = Annotated[AnyUrl, UrlConstraints(allowed_schemes=["mongodb", "mongodb+srv"])]


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
            )
        }
    )


def ensure_indexes(conf: "OllamaXConfig") -> None:
    """Ensure indexes for all models."""

    if conf.client_generation:
        return

    for model in ollama_x.model.__all__:
        asyncio.run(getattr(ollama_x.model, model).create_indexes())


def setup_log(conf: "OllamaXConfig") -> None:
    import logging

    logging.basicConfig(level=LOG_LEVELS[conf.log_level.upper()])


class OllamaXConfig(EnvAppConfig):
    """OllamaX app configuration."""

    STARTUP: ClassVar = [setup_log, setup_document, ensure_indexes]

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


config = OllamaXConfig.load()

import logging

import sentry_sdk
from pydantic_mongo_document import ReplicaConfig
from pydantic_mongo_document.document.asyncio import Document
from ollama_x.config import config

LOG = logging.getLogger(__name__)

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def setup_document() -> None:
    """Sets up document."""

    if config.client_generation:
        return

    Document.set_replica_config(
        {
            "default": ReplicaConfig(
                uri=config.mongo_uri,
                client_options={
                    "serverSelectionTimeoutMS": 50,
                },
            )
        }
    )


async def ensure_indexes() -> None:
    """Ensure indexes for all models."""

    import ollama_x.model

    if config.client_generation:
        return

    for model in ollama_x.model.__all__:
        model = getattr(ollama_x.model, model)
        if isinstance(model, type) and issubclass(model, Document):
            await model.create_indexes()


def setup_log() -> None:
    """Setup logging configuration."""

    logging.basicConfig(level=LOG_LEVELS[config.log_level.upper()])


def setup_sentry() -> None:
    """Setup Sentry SDK."""

    if config.client_generation:
        return

    if config.sentry_dsn:
        sentry_sdk.init(config.sentry_dsn)


STARTUP_TASKS = [
    setup_document,
    ensure_indexes,
    setup_log,
    setup_sentry,
]

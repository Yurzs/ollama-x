import logging
from typing import Callable, Coroutine

from fastapi import Request, Response

LOG = logging.getLogger(__name__)


async def default_middleware(
    request: Request,
    call_next: Callable[[Request], Coroutine[Request, None, Response]],
):
    """Sets default values for state."""

    LOG.debug("Processing default middleware")

    request.state.user = None
    request.state.model = None
    request.state.ollama = None
    request.state.project = None
    request.state.path = str(request.url.path)

    result = await call_next(request)

    LOG.debug("Default middleware processed")

    return result

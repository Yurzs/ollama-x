import logging
from typing import Callable, Coroutine

from fastapi import Request, Response

from ollama_x.api.exceptions import AccessDenied
from ollama_x.api.security import authenticate
from ollama_x.model import ContinueDevProject

LOG = logging.getLogger(__name__)


async def continue_dev_middleware(
    request: Request,
    call_next: Callable[[Request], Coroutine[Request, None, Response]],
):
    """Middleware that handles continue dev requests."""

    LOG.debug("Processing continue.dev middleware")

    project_id = request.headers.get("ContinueDevProject")

    if request.state.user is None and project_id is not None:
        request.state.user = await authenticate(request, anonymous_allowed=False)

    if request.state.user is None or request.state.user.is_guest:
        result = await call_next(request)

    else:
        if project_id is not None:
            project = request.state.project = await ContinueDevProject.one(project_id)
        else:
            return await call_next(request)

        if request.state.user.id not in project.users:
            raise AccessDenied()

        result = await call_next(request)

    LOG.debug("Finished processing continue.dev middleware")

    return result

from fastapi import APIRouter

from ollama_x.api.exceptions import AccessDenied, APIError
from ollama_x.api.helpers import AdminUser
from ollama_x.model import APIServer
from ollama_x.model.server import ServerBase
from ollama_x.scheduler import add_server_job, delete_server_job

PREFIX = "server"

router = APIRouter(prefix=f"/{PREFIX}", tags=[PREFIX])


@router.get(
    "/one",
    operation_id=f"{PREFIX}.one",
    tags=["admin"],
    response_model=APIServer | APIError,
    responses={
        400: {
            "model": APIError[APIServer.NotFoundError],
            "description": "Generic errors.",
        },
        403: {"model": APIError[AccessDenied], "description": "Access errors."},
    },
)
async def get_server(admin: AdminUser, server_id: str) -> APIServer:
    """Get server."""

    if server_id:
        return await APIServer.one(server_id)

    return await APIServer.one(server_id)


@router.get(
    "/all",
    operation_id=f"{PREFIX}.all",
    tags=["admin"],
    response_model=list[APIServer] | APIError,
    responses={
        400: {
            "model": APIError[APIServer.NotFoundError],
            "description": "Generic errors.",
        },
        403: {"model": APIError[AccessDenied], "description": "Access errors."},
    },
)
async def get_servers(admin: AdminUser) -> list[APIServer]:
    """Get servers."""

    return [server async for server in APIServer.all()]


@router.post(
    "/create",
    operation_id=f"{PREFIX}.create",
    tags=["admin"],
    response_model=APIServer | APIError,
    responses={
        400: {
            "model": APIError[APIServer.DuplicateKeyError],
            "description": "Generic errors.",
        },
        403: {"model": APIError[AccessDenied], "description": "Access errors."},
    },
)
async def create_server(admin: AdminUser, server: ServerBase) -> APIServer:
    """Create server."""

    server = await APIServer.new(server)
    add_server_job(server.id)

    return server


@router.put(
    "/update",
    operation_id=f"{PREFIX}.update",
    tags=["admin"],
    response_model=APIServer,
    responses={
        400: {
            "model": APIError[APIServer.NotFoundError],
            "description": "Generic errors.",
        },
        403: {"model": APIError[AccessDenied], "description": "Access errors."},
    },
)
async def update_server(
    admin: AdminUser,
    server_id: str,
    server_url: str | None = None,
) -> APIServer:
    """Update server parameters."""

    server = await APIServer.one(server_id)

    server.url = server_url or server.url

    await server.commit_changes(fields=["url"])

    return server


@router.delete(
    "/",
    operation_id=f"{PREFIX}.delete",
    tags=["admin"],
    response_model=APIServer,
    responses={
        400: {
            "model": APIError[APIServer.NotFoundError],
            "description": "Generic errors.",
        },
        403: {"model": APIError[AccessDenied], "description": "Access errors."},
    },
)
async def delete_server(admin: AdminUser, server_id: str) -> APIServer:
    """Delete server."""

    server = await APIServer.one(server_id)

    await server.delete()
    delete_server_job(server_id)

    return server


@router.post("/{server_id:str}/pull")
async def server_pull_model(server_id: str, model: str):
    """Pull model to server."""

    server = await APIServer.one(server_id)

    return server.pull_model(model)

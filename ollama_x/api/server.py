from typing import Union

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from ollama_x.api.exceptions import AccessDenied, APIError
from ollama_x.api.helpers import APIAdmin
from ollama_x.client.ollama import (
    OllamaListModelsResponse,
    OllamaPullModelResponseSingle,
    OllamaPullModelResponseStream,
)
from ollama_x.model import APIServer
from ollama_x.model.server import ServerBase
from ollama_x.scheduler import add_server_job, delete_server_job


router = APIRouter(prefix="/server", tags=["server"])


@router.get(
    ".one",
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
async def get_server(admin: APIAdmin, server_id: str) -> APIServer:
    """Get server."""

    if server_id:
        return await APIServer.one(server_id)

    return await APIServer.one(server_id)


@router.get(
    ".all",
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
async def get_servers(user: APIAdmin) -> list[APIServer]:
    """Get servers."""

    return [server async for server in APIServer.all()]


@router.post(
    ".create",
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
async def create_server(user: APIAdmin, url: str) -> APIServer:
    """Create server."""

    server = await APIServer.new(ServerBase(url=url))
    add_server_job(server.id)

    return server


@router.put(
    ".update",
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
    user: APIAdmin,
    server_id: str,
    server_url: str | None = None,
) -> APIServer:
    """Update server parameters."""

    server = await APIServer.one(server_id)

    server.url = server_url or server.url

    await server.commit_changes(fields=["url"])

    return server


@router.delete(
    ".delete",
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
async def delete_server(user: APIAdmin, server_id: str) -> APIServer:
    """Delete server."""

    server = await APIServer.one(server_id)

    await server.delete()
    delete_server_job(server_id)

    return server


@router.get(
    "/{server_id:str}/model.list",
    tags=["admin"],
    response_model=OllamaListModelsResponse,
    responses={
        400: {
            "model": APIError[APIServer.NotFoundError],
            "description": "Generic errors.",
        },
        403: {"model": APIError[AccessDenied], "description": "Access errors."},
    },
)
async def server_models(user: APIAdmin, server_id: str) -> OllamaListModelsResponse:
    """Get all models for a specific server."""

    server = await APIServer.one(server_id)

    async with server.ollama_client.list_models() as response:
        return response


@router.post("/{server_id:str}/model.pull")
async def server_pull_model(
    user: APIAdmin,
    server_id: str,
    model: str,
    stream: bool = True,
) -> Union[OllamaPullModelResponseSingle, OllamaPullModelResponseStream]:
    """Pull model to server."""

    server = await APIServer.one(server_id)

    if stream:
        return StreamingResponse(
            server.ollama_client.pull_model(model),
            media_type="application/x-ndjson",
        )

    async with server.ollama_client.pull_model(model) as response:
        return response


@router.delete("/{server_id:str}/model.delete")
async def server_delete_model(
    user: APIAdmin,
    server_id: str,
    model: str,
) -> None:
    """Delete model from server."""

    server = await APIServer.one(server_id)

    async with server.ollama_client.delete_model(model):
        return

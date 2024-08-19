from fastapi import APIRouter

from ollama_x.api.helpers import AdminUser
from ollama_x.model import APIServer
from ollama_x.model.server import ServerBase
from ollama_x.scheduler import add_server_job, delete_server_job

router = APIRouter(prefix="/server", tags=["server"])


@router.get("/", operation_id="get-server", tags=["admin"])
async def get_server(admin: AdminUser, server_id: str | None = None) -> list[APIServer] | APIServer:
    """Get server."""

    if server_id:
        return await APIServer.one(server_id)

    return [s async for s in APIServer.all()]


@router.post("/", operation_id="create-server", tags=["admin"])
async def create_server(admin: AdminUser, server: ServerBase) -> APIServer:
    """Create server."""

    server = await APIServer.new(server)
    add_server_job(server.id)

    return server


@router.put("/", operation_id="update-server", tags=["admin"])
async def update_server(admin: AdminUser, server: APIServer) -> APIServer:
    """Update server."""

    await server.commit_changes(fields=["url"])

    return server


@router.delete("/", operation_id="delete-server", tags=["admin"])
async def delete_server(admin: AdminUser, server_id: str) -> APIServer:
    """Delete server."""

    server = await APIServer.one(server_id)

    await server.delete()
    delete_server_job(server_id)

    return server

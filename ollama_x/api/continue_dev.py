from typing import Literal

from fastapi import APIRouter, Request

from ollama_x.api.exceptions import APIError
from ollama_x.api.helpers import AuthorizedUser
from ollama_x.model import ContinueDevProject, User

L = Literal

router = APIRouter(prefix="/continue-dev", tags=["continue-dev"])


def prepare_project(
    user: AuthorizedUser,
    project: ContinueDevProject,
    request: Request,
) -> ContinueDevProject:
    """Adds dynamic fields to project model."""

    for model in project.config.models:
        model.api_base = str(request.base_url)
        model.request_options.headers.update(
            {
                "Authorization": f"Bearer {user.key.get_secret_value()}",
                "ContinueDevProject": project.id,
            }
        )

    project.config.embeddings_provider.provider = "ollama"
    project.config.embeddings_provider.api_base = str(
        f"{request.base_url}/continue-dev/{project.name}/embeddings"
    )
    project.config.embeddings_provider.request_options.headers.update(
        {
            "Authorization": f"Bearer {user.key.get_secret_value()}",
            "ContinueDevProject": project.id,
        }
    )

    return project


@router.get(
    "/",
    operation_id="list-projects",
    response_model_exclude_none=True,
    response_model=list[ContinueDevProject],
)
async def list_projects(user: AuthorizedUser, request: Request):

    projects = []
    for project in await ContinueDevProject.all_for_user(user.id):
        projects.append(prepare_project(user, project, request))

    return projects


@router.get(
    "/{project_name}",
    operation_id="get-project",
    response_model_exclude_none=True,
    response_model=ContinueDevProject,
)
async def get_project(user: AuthorizedUser, project_name: str, request: Request):

    project = await ContinueDevProject.one_by_name(project_name)
    return prepare_project(user, project, request)


class CreateProjectRequest(ContinueDevProject):
    """Request to create a new project."""


@router.post(
    "/",
    operation_id="create-project",
    response_model_exclude_none=True,
    response_model=ContinueDevProject,
    responses={404: {"model": APIError[L["UserNotFound"]], "description": "User not found"}},
)
async def create_project(user: AuthorizedUser, project: CreateProjectRequest):

    await User.one_by_username(project.admin)

    for user in project.users:
        await User.one_by_username(user)

    await project.insert()

    return project


@router.post("/{project_name}/embeddings/api/embeddings", include_in_schema=False)
async def get_embeddings(user: AuthorizedUser, project_name: str, request: Request):

    print(await request.json())

    return await request.json()

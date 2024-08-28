from fastapi import APIRouter, Request
from openapi_cli.separator import CLI_SEPARATOR
from pydantic import BaseModel, ConfigDict, Field

from ollama_x.api.exceptions import AccessDenied, APIError
from ollama_x.api.helpers import AuthorizedUser, ContinueProject, ProjectWithAdminAccess
from ollama_x.model import ContinueDevProject, User
from ollama_x.model.continue_dev import (
    AllContextProviders,
    AllModels,
    EmbeddingsProvider,
    TabAutocompleteModel,
    TabAutocompleteOptions,
    UserAlreadyInProject,
)
from ollama_x.model.user import UserNotFound

PREFIX = "continue.dev"
EDIT_COMMAND = f"{PREFIX}.edit.{CLI_SEPARATOR}"

router = APIRouter(prefix=f"/{PREFIX}", tags=[PREFIX])


DEFAULT_RESPONSES = {
    404: {
        "model": APIError[UserNotFound] | APIError[ContinueDevProject.NotFoundError],
        "description": "Not found errors.",
    },
    403: {"model": APIError[AccessDenied], "description": "Access errors."},
}


def prepare_project(
    user: AuthorizedUser,
    project: ContinueDevProject,
    request: Request,
) -> ContinueDevProject:
    """Adds dynamic fields to project model."""

    auth_headers = {
        "Authorization": f"Bearer {user.key.get_secret_value()}",
        "ContinueDevProject": project.id,
    }

    api_base = str(request.base_url).replace("http://", "https://")

    # add auth to models
    for model in project.config.models:
        model.title = project.name
        model.api_base = api_base
        model.request_options.headers.update(auth_headers)

    # add embeddings
    if project.config.embeddings_provider is not None:
        project.config.embeddings_provider.provider = "ollama"
        project.config.embeddings_provider.api_base = api_base
        project.config.embeddings_provider.request_options.headers.update(auth_headers)

    # add auth to tab completions
    if project.config.tab_autocomplete_model is not None:
        project.config.tab_autocomplete_model.title = project.name
        project.config.tab_autocomplete_model.provider = "ollama"
        project.config.tab_autocomplete_model.api_base = api_base
        project.config.tab_autocomplete_model.request_options.headers.update(auth_headers)

    return project


@router.get(
    "/all",
    operation_id=f"{PREFIX}.all",
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    response_model=list[ContinueDevProject] | APIError,
    responses=DEFAULT_RESPONSES,
)
async def list_projects(user: AuthorizedUser, request: Request):
    """Get list of continue.dev projects."""

    projects = []
    async for project in ContinueDevProject.all_for_user(user.id):
        projects.append(prepare_project(user, project, request))

    return projects


@router.get(
    "/one",
    operation_id=f"{PREFIX}.one",
    response_model_exclude_none=True,
    response_model=ContinueDevProject,
    responses=DEFAULT_RESPONSES,
)
async def get_project(user: AuthorizedUser, project_name: str, request: Request):
    """Get information about single continue.dev project."""

    project = await ContinueDevProject.one_by_name(project_name)
    return prepare_project(user, project, request)


class CreateProjectRequest(ContinueDevProject):
    """Request to create a new project."""


@router.post(
    "/",
    operation_id=f"{PREFIX}.create",
    response_model_exclude_none=True,
    summary="Create new continue.dev project.",
    response_model=ContinueDevProject | APIError,
    responses=DEFAULT_RESPONSES,
)
async def create_project(user: AuthorizedUser, project: CreateProjectRequest):
    """Create new continue.dev project."""

    await User.one_by_username(project.admin)

    for user in project.users:
        await User.one_by_username(user)

    await project.insert()

    return project


class JoinResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    continue_dev_token: str = Field(description="Continue.dev IDE token", alias="continueDevToken")


@router.get(
    "/join/{invite_id}",
    operation_id=f"{PREFIX}.join",
    response_model=JoinResult | APIError,
    responses={
        **DEFAULT_RESPONSES,
        400: {
            "model": APIError[UserAlreadyInProject] | DEFAULT_RESPONSES.get(400, {}).get("model"),
            "description": "Generic Errors.",
        },
    },
)
async def continue_join(invite_id: str, user_key: str) -> JoinResult:
    """Join project by token."""

    user = await User.one_by_key(user_key)

    project = await ContinueDevProject.one_by_invite_id(invite_id)

    await project.add_user(user.id)

    return JoinResult(continue_dev_token=f"{user.key.get_secret_value()}:{project.id}")


class ContinueConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    config_json: str = Field(default="", alias="configJson")
    config_js: str = Field(default="", alias="configJs")


@router.get(
    "/sync",
    summary="Get project config.",
    operation_id=f"{PREFIX}.sync",
    response_model_exclude_none=True,
    response_model=ContinueConfig,
    responses=DEFAULT_RESPONSES,
)
async def get_config(project: ContinueProject, request: Request):
    """Get project config."""

    prepare_project(request.state.user, project, request)

    return ContinueConfig(
        config_json=project.config.model_dump_json(by_alias=True, exclude_none=True)
    )


@router.post(
    "/reset-invite-id",
    summary="Get project config.",
    operation_id=f"{PREFIX}.reset-invite-id",
    response_model_exclude_none=True,
    response_model=ContinueDevProject,
    responses=DEFAULT_RESPONSES,
)
async def reset_invite_id(project_id: str):
    """Resets invite id in project."""

    project = await ContinueDevProject.one(project_id)

    await project.reset_invite_id()

    return project


@router.patch(
    "/project/{project_id}/models",
    response_model=ContinueDevProject | APIError,
    operation_id=f"{EDIT_COMMAND}.models",
    response_model_exclude_none=True,
    responses=DEFAULT_RESPONSES,
)
async def edit_models(project: ProjectWithAdminAccess, models: list[AllModels] | None = None):
    """Edit project models."""

    if models is None:
        models = []

    project.config.models = models

    await project.commit_changes(fields=["config"])

    return project


@router.patch(
    "/project/{project_id}/embeddings",
    operation_id=f"{EDIT_COMMAND}.embeddings",
    response_model=ContinueDevProject | APIError,
    response_model_exclude_none=True,
    responses=DEFAULT_RESPONSES,
)
async def edit_embeddings(
    project: ProjectWithAdminAccess, embeddings: EmbeddingsProvider | None = None
) -> ContinueDevProject:
    """Edit project embeddings."""

    project.config.embeddings_provider = embeddings

    await project.commit_changes(fields=["config"])

    return project


@router.patch(
    "/project/{project_id}/tab-autocomplete-model",
    operation_id=f"{EDIT_COMMAND}.tab_autocomplete_model",
    response_model=ContinueDevProject | APIError,
    response_model_exclude_none=True,
    responses=DEFAULT_RESPONSES,
)
async def edit_tab_autocomplete_model(
    project: ProjectWithAdminAccess, model: TabAutocompleteModel | None = None
):
    """Edit project tab autocomplete model."""

    project.config.tab_autocomplete_model = model

    await project.commit_changes(fields=["config"])

    return project


@router.patch(
    "/project/{project_id}/tab-autocomplete-options",
    operation_id=f"{EDIT_COMMAND}.tab_autocomplete_options",
    response_model=ContinueDevProject | APIError,
    response_model_exclude_none=True,
    responses=DEFAULT_RESPONSES,
)
async def edit_tab_autocomplete_options(
    project: ProjectWithAdminAccess, options: TabAutocompleteOptions | None = None
) -> ContinueDevProject:
    """Edit project tab autocomplete options."""

    project.config.tab_autocomplete_options = options

    await project.commit_changes(fields=["config"])

    return project


@router.patch(
    "/project/{project_id}/context-providers",
    operation_id=f"{EDIT_COMMAND}.context_providers",
    response_model=ContinueDevProject | APIError,
    response_model_exclude_none=True,
    responses=DEFAULT_RESPONSES,
)
async def edit_context_providers(
    project: ProjectWithAdminAccess, providers: list[AllContextProviders] | None = None
) -> ContinueDevProject:
    """Edit project context providers."""

    project.config.context_providers = providers

    await project.commit_changes(fields=["config"])

    return project

from collections.abc import AsyncIterable
from typing import Generic, Literal, Self, TypeVar, Union

import bson
import pymongo
from pydantic import BaseModel, Field, HttpUrl
from pydantic_mongo_document import Document

from ollama_x.model import exceptions

P = TypeVar("P", bound="Provider")
C = TypeVar("C")
X = TypeVar("X")

NoneType = type(None)


class ProjectExists(Document.DuplicateKeyError):
    pass


class ProjectNotFound(Document.NotFoundError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Project not found")


class Docs(BaseModel):
    pass


class UserAlreadyInProject(Exception):
    def __init__(self):
        super().__init__("User already in project")


class ModelRequestOptions(BaseModel):
    headers: dict[str, str] = Field(default_factory=dict, description="Request headers")


class Model(BaseModel, Generic[P]):
    model: str = Field("AUTODETECT", description="Model name")
    title: str = Field("Model", description="Model title")
    provider: P = Field("ollama", description="Provider")
    api_key: str | None = Field(None, description="API key", alias="apiKey")
    api_base: HttpUrl | None = Field(None, description="OAPI base", alias="apiBase")
    request_options: ModelRequestOptions = Field(
        default_factory=ModelRequestOptions,
        description="Request options",
        alias="requestOptions",
    )


OllamaModel = Model[Literal["ollama"]]
OllamaModel.__name__ = "OllamaModel"

AllModels = Union[OllamaModel]


class RequestOptions(BaseModel):
    timeout: int = Field(10, description="Request timeout")
    verify_ssl: bool = Field(True, description="Verify SSL", alias="verifySSL")
    headers: dict[str, str] = Field(default_factory=dict, description="Request headers")


class BaseCompletionOptions(BaseModel):
    stream: bool | None = Field(None, description="Stream")
    temperature: float | None = Field(None, description="Temperature")
    top_p: float | None = Field(None, description="TopP", alias="topP")
    top_k: int | None = Field(None, description="TopK", alias="topK")
    presence_penalty: float | None = Field(
        None, description="Presence penalty", alias="presencePenalty"
    )
    frequence_penalty: float | None = Field(
        None,
        description="Frequence penalty",
        alias="frequencePenalty",
    )
    mirostat: int | None = Field(None, description="Mirostat")
    stop: list[str] | None = Field(None, description="Stop")
    max_tokens: int | None = Field(None, description="Max tokens", alias="maxTokens")
    num_threads: int | None = Field(None, description="Number of threads", alias="numThreads")
    keep_alive: int | None = Field(None, description="Keep alive interval", alias="keepAlive")


class TabAutocompleteModel(BaseModel):
    title: str = Field("ollama", description="Model title")
    provider: Literal["ollama"] = Field("ollama", description="Provider")
    model: str = Field(description="Model name")
    api_key: str | None = Field(None, description="API key", alias="apiKey")
    api_base: HttpUrl | None = Field(None, description="API base", alias="apiBase")
    context_length: int | None = Field(None, description="Context length", alias="contextLength")
    template: str | None = Field(None, description="Template")
    prompt_templates: dict[str, str] | None = Field(
        None, description="Prompt templates", alias="promptTemplates"
    )
    completion_options: BaseCompletionOptions | None = Field(
        None, description="Completion options", alias="completionOptions"
    )
    request_options: RequestOptions = Field(
        default_factory=RequestOptions,
        description="Request options",
        alias="requestOptions",
    )


class TabAutocompleteOptions(BaseModel):
    disable: bool | None = Field(None, description="Disable autocomplete")
    use_copy_buffer: bool | None = Field(
        None, description="Use copy buffer data in query", alias="useCopyBuffer"
    )
    use_file_suffix: bool | None = Field(None, description="Use file suffix in query")
    max_prompt_tokens: int | None = Field(
        None, description="Max tokens in query", alias="maxPromptTokens"
    )
    debounce_delay: int | None = Field(
        None, description="Time delay after last keystroke", alias="debounceDelay"
    )
    max_suffix_percentage: int | None = Field(
        None, description="Max suffix percentage", alias="maxSuffixPercentage"
    )
    prefix_percentage: int | None = Field(
        None, description="Prefix percentage", alias="prefixPercentage"
    )
    template: str | None = Field(None, description="Template")
    multiline_completions: Literal["always", "never", "auto"] | None = Field(
        None, description="Multiline completions", alias="multilineCompletions"
    )
    use_cache: bool | None = Field(None, description="Use cache", alias="useCache")
    only_my_code: bool | None = Field(None, description="Only my code", alias="onlyMyCode")
    use_other_files: bool | None = Field(None, description="Use other files", alias="useOtherFiles")
    disable_in_files: list[str] | None = Field(
        None, description="Disable in files", alias="disableInFiles"
    )


class EmbeddingsProvider(BaseModel):
    provider: Literal["ollama"] = Field("ollama", description="Provider name")
    model: str | None = Field(None, description="Model name")
    api_base: HttpUrl | None = Field(None, description="API base", alias="apiBase")
    api_key: str | None = Field(None, description="API key", alias="apiKey")
    request_options: RequestOptions = Field(
        default_factory=RequestOptions,
        description="Request options",
        alias="requestOptions",
    )


class CustomCommand(BaseModel):
    name: str = Field(..., description="Command name")
    description: str = Field(..., description="Command description")
    prompt: str = Field(..., description="Command prompt")


class ContextProvider(BaseModel, Generic[C, X]):
    name: C = Field(..., description="Context provider name")
    params: X = Field(None, description="Context provider parameters")


class DocsSite(BaseModel):
    title: str = Field(..., description="Site title")
    start_url: HttpUrl = Field(..., description="Start URL", alias="startUrl")
    root_url: HttpUrl = Field(..., description="Root URL", alias="rootUrl")


class DocsParameters(BaseModel):
    sites: list[DocsSite] = Field(default_factory=list, description="Docs sites")


class OpenParameters(BaseModel):
    only_pinned: bool = Field(True, description="Only pinned", alias="onlyPinned")


OpenContextProvider = ContextProvider[Literal["open"], OpenParameters]
DocsContextProvider = ContextProvider[Literal["docs"], DocsParameters]
CodeContextProvider = ContextProvider[Literal["code"], NoneType]
CodebaseContextProvider = ContextProvider[Literal["codebase"], NoneType]
DiffContextProvider = ContextProvider[Literal["diff"], NoneType]
SearchContextProvider = ContextProvider[Literal["search"], NoneType]
UrlContextProvider = ContextProvider[Literal["url"], NoneType]

OpenContextProvider.__name__ = "OpenContextProvider"
DocsContextProvider.__name__ = "DocsContextProvider"
CodeContextProvider.__name__ = "CodeContextProvider"
CodebaseContextProvider.__name__ = "CodebaseContextProvider"
DiffContextProvider.__name__ = "DiffContextProvider"
SearchContextProvider.__name__ = "SearchContextProvider"
UrlContextProvider.__name__ = "UrlContextProvider"

AllContextProviders = (
    CodeContextProvider
    | CodebaseContextProvider
    | DiffContextProvider
    | DocsContextProvider
    | OpenContextProvider
    | SearchContextProvider
    | UrlContextProvider
)


class ProjectConfig(BaseModel):
    models: list[AllModels] = Field(default_factory=list, description="Project models")

    custom_commands: list[CustomCommand] = Field(
        default_factory=list,
        description="Custom commands",
        alias="customCommands",
    )

    request_options: RequestOptions = Field(
        default_factory=RequestOptions,
        description="Request options",
        alias="requestOptions",
    )

    tab_autocomplete_model: TabAutocompleteModel | list[TabAutocompleteModel] | None = Field(
        None,
        description="Tab autocomplete model",
        alias="tabAutocompleteModel",
    )

    tab_autocomplete_options: TabAutocompleteOptions | None = Field(
        None,
        description="Tab autocomplete options",
        alias="tabAutocompleteOptions",
    )

    allow_anonymous_telemetry: bool = Field(
        False,
        description="Allow anonymous telemetry",
        alias="allowAnonymousTelemetry",
    )

    context_providers: list[AllContextProviders] = Field(
        default_factory=list,
        description="Context providers",
        alias="contextProviders",
    )

    embeddings_provider: EmbeddingsProvider | None = Field(
        None,
        description="Embeddings provider",
        alias="embeddingsProvider",
    )


class ContinueDevProject(Document):
    """continue.dev project model."""

    __replica__ = "default"
    __collection__ = "continue-dev-projects"
    __database__ = "ollama_x"

    admin: str = Field(..., description="Project admin")
    name: str = Field(..., description="Project name")
    users: list[str] = Field(default_factory=list, description="Project users")

    config: ProjectConfig = Field(..., description="continue.dev project config")

    invite_id: str = Field(default_factory=lambda: str(bson.ObjectId()), description="Invite ID")

    NotFoundError = ProjectNotFound
    DuplicateKeyError = exceptions.DuplicateKeyError

    @classmethod
    async def create_indexes(cls) -> None:
        """Create indexes for the model."""

        await cls.collection().create_index(
            [("name", pymongo.ASCENDING)],
            unique=True,
            name="name_unique_index",
        )

    @classmethod
    def all_for_user(cls, user: str) -> AsyncIterable[Self]:
        """Find all projects available for the user."""

        query = {"$or": [{"users": user}, {"admin": user}]}

        return cls.all(add_query=query)

    @classmethod
    async def one_by_name(cls, name: str, required: bool = True) -> Self:
        """Find project by its name."""

        return await cls.one(add_query={"name": name}, required=required)

    async def add_user(self, user_id: str):
        """Add user to project."""

        if user_id in self.users:
            raise UserAlreadyInProject()

        self.users.append(user_id)

        await self.commit_changes(fields=["users"])

    async def reset_invite_id(self):
        """Set new invite id."""

        self.invite_id = str(bson.ObjectId())

        await self.commit_changes(fields=["invite_id"])

    @classmethod
    async def one_by_invite_id(cls, invite_id: str, required: bool = True) -> Self:
        """Find one project by invite id."""

        return await cls.one(add_query={"invite_id": invite_id}, required=required)

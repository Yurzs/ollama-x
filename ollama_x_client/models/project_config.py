from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.code_context_provider import CodeContextProvider
    from ..models.codebase_context_provider import CodebaseContextProvider
    from ..models.custom_command import CustomCommand
    from ..models.diff_context_provider import DiffContextProvider
    from ..models.docs_context_provider import DocsContextProvider
    from ..models.embeddings_provider import EmbeddingsProvider
    from ..models.ollama_model import OllamaModel
    from ..models.open_context_provider import OpenContextProvider
    from ..models.request_options import RequestOptions
    from ..models.search_context_provider import SearchContextProvider
    from ..models.tab_autocomplete_model import TabAutocompleteModel
    from ..models.url_context_provider import UrlContextProvider


T = TypeVar("T", bound="ProjectConfig")


@_attrs_define
class ProjectConfig:
    """
    Attributes:
        models (Union[Unset, List['OllamaModel']]): Project models
        custom_commands (Union[Unset, List['CustomCommand']]): Custom commands
        request_options (Union['RequestOptions', None, Unset]): Request options
        tab_autocomplete_model (Union['TabAutocompleteModel', List['TabAutocompleteModel'], None, Unset]): Tab
            autocomplete model
        allow_anonymous_telemetry (Union[Unset, bool]): Allow anonymous telemetry Default: False.
        context_providers (Union[Unset, List[Union['CodeContextProvider', 'CodebaseContextProvider',
            'DiffContextProvider', 'DocsContextProvider', 'OpenContextProvider', 'SearchContextProvider',
            'UrlContextProvider']]]): Context providers
        embeddings_provider (Union['EmbeddingsProvider', None, Unset]): Embeddings provider
    """

    models: Union[Unset, List["OllamaModel"]] = UNSET
    custom_commands: Union[Unset, List["CustomCommand"]] = UNSET
    request_options: Union["RequestOptions", None, Unset] = UNSET
    tab_autocomplete_model: Union["TabAutocompleteModel", List["TabAutocompleteModel"], None, Unset] = UNSET
    allow_anonymous_telemetry: Union[Unset, bool] = False
    context_providers: Union[
        Unset,
        List[
            Union[
                "CodeContextProvider",
                "CodebaseContextProvider",
                "DiffContextProvider",
                "DocsContextProvider",
                "OpenContextProvider",
                "SearchContextProvider",
                "UrlContextProvider",
            ]
        ],
    ] = UNSET
    embeddings_provider: Union["EmbeddingsProvider", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.code_context_provider import CodeContextProvider
        from ..models.codebase_context_provider import CodebaseContextProvider
        from ..models.diff_context_provider import DiffContextProvider
        from ..models.docs_context_provider import DocsContextProvider
        from ..models.embeddings_provider import EmbeddingsProvider
        from ..models.open_context_provider import OpenContextProvider
        from ..models.request_options import RequestOptions
        from ..models.search_context_provider import SearchContextProvider
        from ..models.tab_autocomplete_model import TabAutocompleteModel

        models: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.models, Unset):
            models = []
            for models_item_data in self.models:
                models_item = models_item_data.to_dict()
                models.append(models_item)

        custom_commands: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.custom_commands, Unset):
            custom_commands = []
            for custom_commands_item_data in self.custom_commands:
                custom_commands_item = custom_commands_item_data.to_dict()
                custom_commands.append(custom_commands_item)

        request_options: Union[Dict[str, Any], None, Unset]
        if isinstance(self.request_options, Unset):
            request_options = UNSET
        elif isinstance(self.request_options, RequestOptions):
            request_options = self.request_options.to_dict()
        else:
            request_options = self.request_options

        tab_autocomplete_model: Union[Dict[str, Any], List[Dict[str, Any]], None, Unset]
        if isinstance(self.tab_autocomplete_model, Unset):
            tab_autocomplete_model = UNSET
        elif isinstance(self.tab_autocomplete_model, TabAutocompleteModel):
            tab_autocomplete_model = self.tab_autocomplete_model.to_dict()
        elif isinstance(self.tab_autocomplete_model, list):
            tab_autocomplete_model = []
            for tab_autocomplete_model_type_1_item_data in self.tab_autocomplete_model:
                tab_autocomplete_model_type_1_item = tab_autocomplete_model_type_1_item_data.to_dict()
                tab_autocomplete_model.append(tab_autocomplete_model_type_1_item)

        else:
            tab_autocomplete_model = self.tab_autocomplete_model

        allow_anonymous_telemetry = self.allow_anonymous_telemetry

        context_providers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.context_providers, Unset):
            context_providers = []
            for context_providers_item_data in self.context_providers:
                context_providers_item: Dict[str, Any]
                if isinstance(context_providers_item_data, CodeContextProvider):
                    context_providers_item = context_providers_item_data.to_dict()
                elif isinstance(context_providers_item_data, CodebaseContextProvider):
                    context_providers_item = context_providers_item_data.to_dict()
                elif isinstance(context_providers_item_data, DiffContextProvider):
                    context_providers_item = context_providers_item_data.to_dict()
                elif isinstance(context_providers_item_data, DocsContextProvider):
                    context_providers_item = context_providers_item_data.to_dict()
                elif isinstance(context_providers_item_data, OpenContextProvider):
                    context_providers_item = context_providers_item_data.to_dict()
                elif isinstance(context_providers_item_data, SearchContextProvider):
                    context_providers_item = context_providers_item_data.to_dict()
                else:
                    context_providers_item = context_providers_item_data.to_dict()

                context_providers.append(context_providers_item)

        embeddings_provider: Union[Dict[str, Any], None, Unset]
        if isinstance(self.embeddings_provider, Unset):
            embeddings_provider = UNSET
        elif isinstance(self.embeddings_provider, EmbeddingsProvider):
            embeddings_provider = self.embeddings_provider.to_dict()
        else:
            embeddings_provider = self.embeddings_provider

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if models is not UNSET:
            field_dict["models"] = models
        if custom_commands is not UNSET:
            field_dict["customCommands"] = custom_commands
        if request_options is not UNSET:
            field_dict["requestOptions"] = request_options
        if tab_autocomplete_model is not UNSET:
            field_dict["tabAutocompleteModel"] = tab_autocomplete_model
        if allow_anonymous_telemetry is not UNSET:
            field_dict["allowAnonymousTelemetry"] = allow_anonymous_telemetry
        if context_providers is not UNSET:
            field_dict["contextProviders"] = context_providers
        if embeddings_provider is not UNSET:
            field_dict["embeddingsProvider"] = embeddings_provider

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.code_context_provider import CodeContextProvider
        from ..models.codebase_context_provider import CodebaseContextProvider
        from ..models.custom_command import CustomCommand
        from ..models.diff_context_provider import DiffContextProvider
        from ..models.docs_context_provider import DocsContextProvider
        from ..models.embeddings_provider import EmbeddingsProvider
        from ..models.ollama_model import OllamaModel
        from ..models.open_context_provider import OpenContextProvider
        from ..models.request_options import RequestOptions
        from ..models.search_context_provider import SearchContextProvider
        from ..models.tab_autocomplete_model import TabAutocompleteModel
        from ..models.url_context_provider import UrlContextProvider

        d = src_dict.copy()
        models = []
        _models = d.pop("models", UNSET)
        for models_item_data in _models or []:
            models_item = OllamaModel.from_dict(models_item_data)

            models.append(models_item)

        custom_commands = []
        _custom_commands = d.pop("customCommands", UNSET)
        for custom_commands_item_data in _custom_commands or []:
            custom_commands_item = CustomCommand.from_dict(custom_commands_item_data)

            custom_commands.append(custom_commands_item)

        def _parse_request_options(data: object) -> Union["RequestOptions", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                request_options_type_0 = RequestOptions.from_dict(data)

                return request_options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RequestOptions", None, Unset], data)

        request_options = _parse_request_options(d.pop("requestOptions", UNSET))

        def _parse_tab_autocomplete_model(
            data: object,
        ) -> Union["TabAutocompleteModel", List["TabAutocompleteModel"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tab_autocomplete_model_type_0 = TabAutocompleteModel.from_dict(data)

                return tab_autocomplete_model_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tab_autocomplete_model_type_1 = []
                _tab_autocomplete_model_type_1 = data
                for tab_autocomplete_model_type_1_item_data in _tab_autocomplete_model_type_1:
                    tab_autocomplete_model_type_1_item = TabAutocompleteModel.from_dict(
                        tab_autocomplete_model_type_1_item_data
                    )

                    tab_autocomplete_model_type_1.append(tab_autocomplete_model_type_1_item)

                return tab_autocomplete_model_type_1
            except:  # noqa: E722
                pass
            return cast(Union["TabAutocompleteModel", List["TabAutocompleteModel"], None, Unset], data)

        tab_autocomplete_model = _parse_tab_autocomplete_model(d.pop("tabAutocompleteModel", UNSET))

        allow_anonymous_telemetry = d.pop("allowAnonymousTelemetry", UNSET)

        context_providers = []
        _context_providers = d.pop("contextProviders", UNSET)
        for context_providers_item_data in _context_providers or []:

            def _parse_context_providers_item(
                data: object,
            ) -> Union[
                "CodeContextProvider",
                "CodebaseContextProvider",
                "DiffContextProvider",
                "DocsContextProvider",
                "OpenContextProvider",
                "SearchContextProvider",
                "UrlContextProvider",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    context_providers_item_type_0 = CodeContextProvider.from_dict(data)

                    return context_providers_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    context_providers_item_type_1 = CodebaseContextProvider.from_dict(data)

                    return context_providers_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    context_providers_item_type_2 = DiffContextProvider.from_dict(data)

                    return context_providers_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    context_providers_item_type_3 = DocsContextProvider.from_dict(data)

                    return context_providers_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    context_providers_item_type_4 = OpenContextProvider.from_dict(data)

                    return context_providers_item_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    context_providers_item_type_5 = SearchContextProvider.from_dict(data)

                    return context_providers_item_type_5
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                context_providers_item_type_6 = UrlContextProvider.from_dict(data)

                return context_providers_item_type_6

            context_providers_item = _parse_context_providers_item(context_providers_item_data)

            context_providers.append(context_providers_item)

        def _parse_embeddings_provider(data: object) -> Union["EmbeddingsProvider", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                embeddings_provider_type_0 = EmbeddingsProvider.from_dict(data)

                return embeddings_provider_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EmbeddingsProvider", None, Unset], data)

        embeddings_provider = _parse_embeddings_provider(d.pop("embeddingsProvider", UNSET))

        project_config = cls(
            models=models,
            custom_commands=custom_commands,
            request_options=request_options,
            tab_autocomplete_model=tab_autocomplete_model,
            allow_anonymous_telemetry=allow_anonymous_telemetry,
            context_providers=context_providers,
            embeddings_provider=embeddings_provider,
        )

        project_config.additional_properties = d
        return project_config

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

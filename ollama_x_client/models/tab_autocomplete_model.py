from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tab_autocomplete_model_provider import TabAutocompleteModelProvider
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_completion_options import BaseCompletionOptions
    from ..models.tab_autocomplete_model_prompt_templates_type_0 import TabAutocompleteModelPromptTemplatesType0


T = TypeVar("T", bound="TabAutocompleteModel")


@_attrs_define
class TabAutocompleteModel:
    """
    Attributes:
        title (str): Model title
        model (str): Model name
        provider (Union[Unset, TabAutocompleteModelProvider]): Provider Default: TabAutocompleteModelProvider.OLLAMA.
        api_key (Union[None, Unset, str]): API key
        api_base (Union[None, Unset, str]): API base
        context_length (Union[None, Unset, int]): Context length
        template (Union[None, Unset, str]): Template
        prompt_templates (Union['TabAutocompleteModelPromptTemplatesType0', None, Unset]): Prompt templates
        completion_options (Union['BaseCompletionOptions', None, Unset]): Completion options
    """

    title: str
    model: str
    provider: Union[Unset, TabAutocompleteModelProvider] = TabAutocompleteModelProvider.OLLAMA
    api_key: Union[None, Unset, str] = UNSET
    api_base: Union[None, Unset, str] = UNSET
    context_length: Union[None, Unset, int] = UNSET
    template: Union[None, Unset, str] = UNSET
    prompt_templates: Union["TabAutocompleteModelPromptTemplatesType0", None, Unset] = UNSET
    completion_options: Union["BaseCompletionOptions", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.base_completion_options import BaseCompletionOptions
        from ..models.tab_autocomplete_model_prompt_templates_type_0 import TabAutocompleteModelPromptTemplatesType0

        title = self.title

        model = self.model

        provider: Union[Unset, str] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.value

        api_key: Union[None, Unset, str]
        if isinstance(self.api_key, Unset):
            api_key = UNSET
        else:
            api_key = self.api_key

        api_base: Union[None, Unset, str]
        if isinstance(self.api_base, Unset):
            api_base = UNSET
        else:
            api_base = self.api_base

        context_length: Union[None, Unset, int]
        if isinstance(self.context_length, Unset):
            context_length = UNSET
        else:
            context_length = self.context_length

        template: Union[None, Unset, str]
        if isinstance(self.template, Unset):
            template = UNSET
        else:
            template = self.template

        prompt_templates: Union[Dict[str, Any], None, Unset]
        if isinstance(self.prompt_templates, Unset):
            prompt_templates = UNSET
        elif isinstance(self.prompt_templates, TabAutocompleteModelPromptTemplatesType0):
            prompt_templates = self.prompt_templates.to_dict()
        else:
            prompt_templates = self.prompt_templates

        completion_options: Union[Dict[str, Any], None, Unset]
        if isinstance(self.completion_options, Unset):
            completion_options = UNSET
        elif isinstance(self.completion_options, BaseCompletionOptions):
            completion_options = self.completion_options.to_dict()
        else:
            completion_options = self.completion_options

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "model": model,
            }
        )
        if provider is not UNSET:
            field_dict["provider"] = provider
        if api_key is not UNSET:
            field_dict["apiKey"] = api_key
        if api_base is not UNSET:
            field_dict["apiBase"] = api_base
        if context_length is not UNSET:
            field_dict["contextLength"] = context_length
        if template is not UNSET:
            field_dict["template"] = template
        if prompt_templates is not UNSET:
            field_dict["promptTemplates"] = prompt_templates
        if completion_options is not UNSET:
            field_dict["completionOptions"] = completion_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_completion_options import BaseCompletionOptions
        from ..models.tab_autocomplete_model_prompt_templates_type_0 import TabAutocompleteModelPromptTemplatesType0

        d = src_dict.copy()
        title = d.pop("title")

        model = d.pop("model")

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, TabAutocompleteModelProvider]
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = TabAutocompleteModelProvider(_provider)

        def _parse_api_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_key = _parse_api_key(d.pop("apiKey", UNSET))

        def _parse_api_base(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_base = _parse_api_base(d.pop("apiBase", UNSET))

        def _parse_context_length(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        context_length = _parse_context_length(d.pop("contextLength", UNSET))

        def _parse_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        template = _parse_template(d.pop("template", UNSET))

        def _parse_prompt_templates(data: object) -> Union["TabAutocompleteModelPromptTemplatesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                prompt_templates_type_0 = TabAutocompleteModelPromptTemplatesType0.from_dict(data)

                return prompt_templates_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TabAutocompleteModelPromptTemplatesType0", None, Unset], data)

        prompt_templates = _parse_prompt_templates(d.pop("promptTemplates", UNSET))

        def _parse_completion_options(data: object) -> Union["BaseCompletionOptions", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                completion_options_type_0 = BaseCompletionOptions.from_dict(data)

                return completion_options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseCompletionOptions", None, Unset], data)

        completion_options = _parse_completion_options(d.pop("completionOptions", UNSET))

        tab_autocomplete_model = cls(
            title=title,
            model=model,
            provider=provider,
            api_key=api_key,
            api_base=api_base,
            context_length=context_length,
            template=template,
            prompt_templates=prompt_templates,
            completion_options=completion_options,
        )

        tab_autocomplete_model.additional_properties = d
        return tab_autocomplete_model

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

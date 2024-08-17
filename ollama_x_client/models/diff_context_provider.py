from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.diff_context_provider_name import DiffContextProviderName
from ..types import UNSET, Unset

T = TypeVar("T", bound="DiffContextProvider")


@_attrs_define
class DiffContextProvider:
    """
    Attributes:
        name (DiffContextProviderName): Context provider name
        params (Union[Unset, None]): Context provider parameters
    """

    name: DiffContextProviderName
    params: Union[Unset, None] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name.value

        params = self.params

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if params is not UNSET:
            field_dict["params"] = params

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = DiffContextProviderName(d.pop("name"))

        params = d.pop("params", UNSET)

        diff_context_provider = cls(
            name=name,
            params=params,
        )

        diff_context_provider.additional_properties = d
        return diff_context_provider

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

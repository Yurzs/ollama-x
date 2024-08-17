from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.open_context_provider_name import OpenContextProviderName
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_parameters import OpenParameters


T = TypeVar("T", bound="OpenContextProvider")


@_attrs_define
class OpenContextProvider:
    """
    Attributes:
        name (OpenContextProviderName): Context provider name
        params (Union[Unset, OpenParameters]):
    """

    name: OpenContextProviderName
    params: Union[Unset, "OpenParameters"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name.value

        params: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.params, Unset):
            params = self.params.to_dict()

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
        from ..models.open_parameters import OpenParameters

        d = src_dict.copy()
        name = OpenContextProviderName(d.pop("name"))

        _params = d.pop("params", UNSET)
        params: Union[Unset, OpenParameters]
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = OpenParameters.from_dict(_params)

        open_context_provider = cls(
            name=name,
            params=params,
        )

        open_context_provider.additional_properties = d
        return open_context_provider

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

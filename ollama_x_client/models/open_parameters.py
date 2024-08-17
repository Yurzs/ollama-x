from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenParameters")


@_attrs_define
class OpenParameters:
    """
    Attributes:
        only_pinned (Union[Unset, bool]): Only pinned Default: True.
    """

    only_pinned: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        only_pinned = self.only_pinned

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if only_pinned is not UNSET:
            field_dict["onlyPinned"] = only_pinned

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        only_pinned = d.pop("onlyPinned", UNSET)

        open_parameters = cls(
            only_pinned=only_pinned,
        )

        open_parameters.additional_properties = d
        return open_parameters

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

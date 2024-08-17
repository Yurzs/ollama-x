from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_request_options_headers import ModelRequestOptionsHeaders


T = TypeVar("T", bound="ModelRequestOptions")


@_attrs_define
class ModelRequestOptions:
    """
    Attributes:
        headers (Union[Unset, ModelRequestOptionsHeaders]): Request headers
    """

    headers: Union[Unset, "ModelRequestOptionsHeaders"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        headers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if headers is not UNSET:
            field_dict["headers"] = headers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_request_options_headers import ModelRequestOptionsHeaders

        d = src_dict.copy()
        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, ModelRequestOptionsHeaders]
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = ModelRequestOptionsHeaders.from_dict(_headers)

        model_request_options = cls(
            headers=headers,
        )

        model_request_options.additional_properties = d
        return model_request_options

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

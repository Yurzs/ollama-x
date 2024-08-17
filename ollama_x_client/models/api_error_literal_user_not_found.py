from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.api_error_literal_user_not_found_code import APIErrorLiteralUserNotFoundCode

T = TypeVar("T", bound="APIErrorLiteralUserNotFound")


@_attrs_define
class APIErrorLiteralUserNotFound:
    """
    Attributes:
        code (APIErrorLiteralUserNotFoundCode): Error code
        details (str): Error details
    """

    code: APIErrorLiteralUserNotFoundCode
    details: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code.value

        details = self.details

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = APIErrorLiteralUserNotFoundCode(d.pop("code"))

        details = d.pop("details")

        api_error_literal_user_not_found = cls(
            code=code,
            details=details,
        )

        api_error_literal_user_not_found.additional_properties = d
        return api_error_literal_user_not_found

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

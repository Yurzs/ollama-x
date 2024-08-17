from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        username (str): Username
        key (str): Users API key
        field_id (Union[Unset, str]):
        is_admin (Union[Unset, bool]): Is user admin flag Default: False.
    """

    username: str
    key: str
    field_id: Union[Unset, str] = UNSET
    is_admin: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username

        key = self.key

        field_id = self.field_id

        is_admin = self.is_admin

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "key": key,
            }
        )
        if field_id is not UNSET:
            field_dict["_id"] = field_id
        if is_admin is not UNSET:
            field_dict["is_admin"] = is_admin

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        key = d.pop("key")

        field_id = d.pop("_id", UNSET)

        is_admin = d.pop("is_admin", UNSET)

        user = cls(
            username=username,
            key=key,
            field_id=field_id,
            is_admin=is_admin,
        )

        user.additional_properties = d
        return user

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

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_config import ProjectConfig


T = TypeVar("T", bound="CreateProjectRequest")


@_attrs_define
class CreateProjectRequest:
    """Request to create a new project.

    Attributes:
        admin (str): Project admin
        name (str): Project name
        config (ProjectConfig):
        field_id (Union[Unset, str]):
        users (Union[Unset, List[str]]): Project users
    """

    admin: str
    name: str
    config: "ProjectConfig"
    field_id: Union[Unset, str] = UNSET
    users: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        admin = self.admin

        name = self.name

        config = self.config.to_dict()

        field_id = self.field_id

        users: Union[Unset, List[str]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "admin": admin,
                "name": name,
                "config": config,
            }
        )
        if field_id is not UNSET:
            field_dict["_id"] = field_id
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.project_config import ProjectConfig

        d = src_dict.copy()
        admin = d.pop("admin")

        name = d.pop("name")

        config = ProjectConfig.from_dict(d.pop("config"))

        field_id = d.pop("_id", UNSET)

        users = cast(List[str], d.pop("users", UNSET))

        create_project_request = cls(
            admin=admin,
            name=name,
            config=config,
            field_id=field_id,
            users=users,
        )

        create_project_request.additional_properties = d
        return create_project_request

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

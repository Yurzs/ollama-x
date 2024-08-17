from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DocsSite")


@_attrs_define
class DocsSite:
    """
    Attributes:
        title (str): Site title
        start_url (str): Start URL
        root_url (str): Root URL
    """

    title: str
    start_url: str
    root_url: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title

        start_url = self.start_url

        root_url = self.root_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "startUrl": start_url,
                "rootUrl": root_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        start_url = d.pop("startUrl")

        root_url = d.pop("rootUrl")

        docs_site = cls(
            title=title,
            start_url=start_url,
            root_url=root_url,
        )

        docs_site.additional_properties = d
        return docs_site

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

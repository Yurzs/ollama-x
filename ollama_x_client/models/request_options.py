from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.request_options_headers import RequestOptionsHeaders


T = TypeVar("T", bound="RequestOptions")


@_attrs_define
class RequestOptions:
    """
    Attributes:
        timeout (Union[Unset, int]): Request timeout Default: 10.
        verify_ssl (Union[Unset, bool]): Verify SSL Default: True.
        headers (Union[Unset, RequestOptionsHeaders]): Request headers
    """

    timeout: Union[Unset, int] = 10
    verify_ssl: Union[Unset, bool] = True
    headers: Union[Unset, "RequestOptionsHeaders"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timeout = self.timeout

        verify_ssl = self.verify_ssl

        headers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if verify_ssl is not UNSET:
            field_dict["verifySSL"] = verify_ssl
        if headers is not UNSET:
            field_dict["headers"] = headers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.request_options_headers import RequestOptionsHeaders

        d = src_dict.copy()
        timeout = d.pop("timeout", UNSET)

        verify_ssl = d.pop("verifySSL", UNSET)

        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, RequestOptionsHeaders]
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = RequestOptionsHeaders.from_dict(_headers)

        request_options = cls(
            timeout=timeout,
            verify_ssl=verify_ssl,
            headers=headers,
        )

        request_options.additional_properties = d
        return request_options

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

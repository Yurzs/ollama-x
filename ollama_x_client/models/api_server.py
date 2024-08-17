import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_server_models_item import APIServerModelsItem


T = TypeVar("T", bound="APIServer")


@_attrs_define
class APIServer:
    """Ollama API server model.

    Attributes:
        url (str): Server API base URL
        field_id (Union[Unset, str]):
        last_update (Union[Unset, datetime.datetime]): Last update Default: isoparse('1970-01-01T00:00:00').
        last_alive (Union[Unset, datetime.datetime]): Last alive Default: isoparse('1970-01-01T00:00:00').
        models (Union[Unset, List['APIServerModelsItem']]): Models
    """

    url: str
    field_id: Union[Unset, str] = UNSET
    last_update: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00")
    last_alive: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00")
    models: Union[Unset, List["APIServerModelsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url

        field_id = self.field_id

        last_update: Union[Unset, str] = UNSET
        if not isinstance(self.last_update, Unset):
            last_update = self.last_update.isoformat()

        last_alive: Union[Unset, str] = UNSET
        if not isinstance(self.last_alive, Unset):
            last_alive = self.last_alive.isoformat()

        models: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.models, Unset):
            models = []
            for models_item_data in self.models:
                models_item = models_item_data.to_dict()
                models.append(models_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if field_id is not UNSET:
            field_dict["_id"] = field_id
        if last_update is not UNSET:
            field_dict["last_update"] = last_update
        if last_alive is not UNSET:
            field_dict["last_alive"] = last_alive
        if models is not UNSET:
            field_dict["models"] = models

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_server_models_item import APIServerModelsItem

        d = src_dict.copy()
        url = d.pop("url")

        field_id = d.pop("_id", UNSET)

        _last_update = d.pop("last_update", UNSET)
        last_update: Union[Unset, datetime.datetime]
        if isinstance(_last_update, Unset):
            last_update = UNSET
        else:
            last_update = isoparse(_last_update)

        _last_alive = d.pop("last_alive", UNSET)
        last_alive: Union[Unset, datetime.datetime]
        if isinstance(_last_alive, Unset):
            last_alive = UNSET
        else:
            last_alive = isoparse(_last_alive)

        models = []
        _models = d.pop("models", UNSET)
        for models_item_data in _models or []:
            models_item = APIServerModelsItem.from_dict(models_item_data)

            models.append(models_item)

        api_server = cls(
            url=url,
            field_id=field_id,
            last_update=last_update,
            last_alive=last_alive,
            models=models,
        )

        api_server.additional_properties = d
        return api_server

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

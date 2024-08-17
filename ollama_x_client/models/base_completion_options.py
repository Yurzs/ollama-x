from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseCompletionOptions")


@_attrs_define
class BaseCompletionOptions:
    """
    Attributes:
        stream (Union[None, Unset, bool]): Stream
        temperature (Union[None, Unset, float]): Temperature
        top_p (Union[None, Unset, float]): TopP
        top_k (Union[None, Unset, int]): TopK
        presence_penalty (Union[None, Unset, float]): Presence penalty
        frequence_penalty (Union[None, Unset, float]): Frequence penalty
        mirostat (Union[None, Unset, int]): Mirostat
        stop (Union[List[str], None, Unset]): Stop
        max_tokens (Union[None, Unset, int]): Max tokens
        num_threads (Union[None, Unset, int]): Number of threads
        keep_alive (Union[None, Unset, int]): Keep alive interval
    """

    stream: Union[None, Unset, bool] = UNSET
    temperature: Union[None, Unset, float] = UNSET
    top_p: Union[None, Unset, float] = UNSET
    top_k: Union[None, Unset, int] = UNSET
    presence_penalty: Union[None, Unset, float] = UNSET
    frequence_penalty: Union[None, Unset, float] = UNSET
    mirostat: Union[None, Unset, int] = UNSET
    stop: Union[List[str], None, Unset] = UNSET
    max_tokens: Union[None, Unset, int] = UNSET
    num_threads: Union[None, Unset, int] = UNSET
    keep_alive: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        stream: Union[None, Unset, bool]
        if isinstance(self.stream, Unset):
            stream = UNSET
        else:
            stream = self.stream

        temperature: Union[None, Unset, float]
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        top_p: Union[None, Unset, float]
        if isinstance(self.top_p, Unset):
            top_p = UNSET
        else:
            top_p = self.top_p

        top_k: Union[None, Unset, int]
        if isinstance(self.top_k, Unset):
            top_k = UNSET
        else:
            top_k = self.top_k

        presence_penalty: Union[None, Unset, float]
        if isinstance(self.presence_penalty, Unset):
            presence_penalty = UNSET
        else:
            presence_penalty = self.presence_penalty

        frequence_penalty: Union[None, Unset, float]
        if isinstance(self.frequence_penalty, Unset):
            frequence_penalty = UNSET
        else:
            frequence_penalty = self.frequence_penalty

        mirostat: Union[None, Unset, int]
        if isinstance(self.mirostat, Unset):
            mirostat = UNSET
        else:
            mirostat = self.mirostat

        stop: Union[List[str], None, Unset]
        if isinstance(self.stop, Unset):
            stop = UNSET
        elif isinstance(self.stop, list):
            stop = self.stop

        else:
            stop = self.stop

        max_tokens: Union[None, Unset, int]
        if isinstance(self.max_tokens, Unset):
            max_tokens = UNSET
        else:
            max_tokens = self.max_tokens

        num_threads: Union[None, Unset, int]
        if isinstance(self.num_threads, Unset):
            num_threads = UNSET
        else:
            num_threads = self.num_threads

        keep_alive: Union[None, Unset, int]
        if isinstance(self.keep_alive, Unset):
            keep_alive = UNSET
        else:
            keep_alive = self.keep_alive

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stream is not UNSET:
            field_dict["stream"] = stream
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["topP"] = top_p
        if top_k is not UNSET:
            field_dict["topK"] = top_k
        if presence_penalty is not UNSET:
            field_dict["presencePenalty"] = presence_penalty
        if frequence_penalty is not UNSET:
            field_dict["frequencePenalty"] = frequence_penalty
        if mirostat is not UNSET:
            field_dict["mirostat"] = mirostat
        if stop is not UNSET:
            field_dict["stop"] = stop
        if max_tokens is not UNSET:
            field_dict["maxTokens"] = max_tokens
        if num_threads is not UNSET:
            field_dict["numThreads"] = num_threads
        if keep_alive is not UNSET:
            field_dict["keepAlive"] = keep_alive

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_stream(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        stream = _parse_stream(d.pop("stream", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_top_p(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        top_p = _parse_top_p(d.pop("topP", UNSET))

        def _parse_top_k(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        top_k = _parse_top_k(d.pop("topK", UNSET))

        def _parse_presence_penalty(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        presence_penalty = _parse_presence_penalty(d.pop("presencePenalty", UNSET))

        def _parse_frequence_penalty(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        frequence_penalty = _parse_frequence_penalty(d.pop("frequencePenalty", UNSET))

        def _parse_mirostat(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        mirostat = _parse_mirostat(d.pop("mirostat", UNSET))

        def _parse_stop(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                stop_type_0 = cast(List[str], data)

                return stop_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        stop = _parse_stop(d.pop("stop", UNSET))

        def _parse_max_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_tokens = _parse_max_tokens(d.pop("maxTokens", UNSET))

        def _parse_num_threads(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_threads = _parse_num_threads(d.pop("numThreads", UNSET))

        def _parse_keep_alive(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        keep_alive = _parse_keep_alive(d.pop("keepAlive", UNSET))

        base_completion_options = cls(
            stream=stream,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            presence_penalty=presence_penalty,
            frequence_penalty=frequence_penalty,
            mirostat=mirostat,
            stop=stop,
            max_tokens=max_tokens,
            num_threads=num_threads,
            keep_alive=keep_alive,
        )

        base_completion_options.additional_properties = d
        return base_completion_options

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

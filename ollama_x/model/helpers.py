import json
from typing import Any

from pydantic import BaseModel, model_serializer
from pydantic_core.core_schema import SerializationInfo


class ExplicitNoneBaseModel(BaseModel):
    @model_serializer()
    def serialize_(self, info: SerializationInfo) -> Any:
        """Serialize the model to a dictionary."""

        result = {}

        for field in [f for f in self.model_fields if f not in (info.exclude or [])]:
            value = getattr(self, field)

            if isinstance(value, BaseModel):
                result[field] = value.model_dump(
                    exclude_unset=info.exclude_unset,
                    exclude_defaults=info.exclude_defaults,
                    mode=info.mode,
                    by_alias=info.by_alias,
                    exclude_none=info.exclude_none,
                )
            else:
                result[field] = (
                    json.dumps(value)
                    if info.mode == "json" and value is not None
                    else value
                )

        return result

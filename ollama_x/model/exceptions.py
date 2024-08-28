from typing import Any, Mapping, Optional

import pymongo.errors


class DuplicateKeyError(pymongo.errors.DuplicateKeyError):
    @property
    def details(self) -> Optional[Mapping[str, Any]]:
        return zip(self.details["keyPattern"].keys(), self.details["keyValue"].values())

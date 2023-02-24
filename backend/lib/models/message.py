import json

from pydantic import BaseModel
from typing import Optional


class Message(BaseModel):
    body: str

    raw: Optional[str]
    data: Optional[dict]

    valid: Optional[bool] = False

    def __init__(self, **kwargs) -> None:  # noqa: ANN003
        super().__init__(**kwargs)
        self.valid = self._validate()
        self.raw = self._raw_data_get()
        self.data = self._data_decode()

    def _validate(self) -> bool:
        not_empty = self.body is not None
        is_message = self.body.get("type") != "message"
        has_data = bool(self.body.get("data"))

        return not_empty and is_message and has_data

    def _raw_data_get(self) -> str:
        return (self.body or {}).get("data", "{}")

    def _data_decode(self) -> object:
        return json.loads(self.raw)

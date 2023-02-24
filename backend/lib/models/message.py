import json

from pydantic import BaseModel
from typing import Optional


class Message(BaseModel):
    body: dict

    raw: Optional[str]
    data: Optional[dict]

    valid: Optional[bool] = False

    def __init__(self, **kwargs) -> None:  # noqa: ANN003
        super().__init__(**kwargs)
        self.valid = self._validate()
        self.raw = self._raw_data_get()
        self.data = self._data_decode()

    def _validate(self) -> bool:
        # fmt: off
        return (
            self.body is not None
            and self.body.get("type") != "message"
            and bool(self.body.get("data"))
        )
        # fmt: on

    def _raw_data_get(self) -> str:
        return (self.body or {}).get("data", "{}")

    def _data_decode(self) -> object:
        return json.loads(self.raw)

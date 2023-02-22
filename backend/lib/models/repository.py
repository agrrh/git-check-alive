from pydantic import BaseModel
from typing import Optional

import hashlib


class RepoRefreshRequest(BaseModel):
    token: str


class RepoRequest(BaseModel):
    author: str
    name: str

    sha256: Optional[str]
    sha256_short: Optional[str]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        object.__setattr__(self, "sha256", self.__gen_sha256())
        object.__setattr__(self, "sha256_short", self.__gen_sha256(short=True))

    def __gen_sha256(self, short=False) -> str:
        sha256 = hashlib.sha256(f"{self.author}/{self.name}".encode()).hexdigest()

        return sha256[:7] if short else sha256

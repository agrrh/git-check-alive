from pydantic import BaseModel
from typing import Optional

import hashlib


class RepoRefreshRequest(BaseModel):
    token: str


class RepoRequest(BaseModel):
    owner: str
    name: str

    address: Optional[str]

    sha256: Optional[str]
    sha256_short: Optional[str]

    def __init__(self, **kwargs) -> None:  # noqa: ANN003
        super().__init__(**kwargs)
        object.__setattr__(self, "address", self.__address())
        object.__setattr__(self, "sha256", self.__gen_sha256())
        object.__setattr__(self, "sha256_short", self.__gen_sha256(short=True))

    def __gen_sha256(self, short: bool = False) -> str:
        notation = f"{self.owner}/{self.name}".encode()
        sha256 = hashlib.sha256(notation).hexdigest()

        return sha256[:7] if short else sha256

    def __address(self) -> str:
        return f"{self.owner}/{self.name}"


class Repo(BaseModel):
    owner: Optional[str]
    name: Optional[str]

    archived: Optional[bool]

    description: Optional[str]

    stars_count: Optional[int]
    forks_count: Optional[int]

    watchers_count: Optional[int]

    def _load_from_github_data(self, data: object) -> None:
        self.owner = data.owner.login
        self.name = data.name

        self.archived = data.archived

        self.description = data.description

        self.stars_count = data.stargazers_count
        self.forks_count = data.forks_count

        self.watchers_count = data.watchers_count

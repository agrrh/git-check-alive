from pydantic import BaseModel
from typing import Optional

import hashlib


class RepoRefreshRequest(BaseModel):
    token: str


class Repo(BaseModel):
    owner: str = ""
    name: str = ""

    address: Optional[str]

    sha256: Optional[str]
    sha256_short: Optional[str]

    db_key: Optional[str]

    archived: Optional[bool]

    description: Optional[str]

    stars_count: Optional[int]
    forks_count: Optional[int]

    watchers_count: Optional[int]

    def __init__(self, **kwargs) -> None:  # noqa: ANN003
        super().__init__(**kwargs)

        self.address = self.address or f"{self.owner}/{self.name}"
        self.sha256 = self.__gen_sha256()
        self.sha256_short = self.__gen_sha256(short=True)
        self.db_key = f"repo.{self.sha256}"

    def __gen_sha256(self, short: bool = False) -> str:
        notation = self.address.encode()
        sha256 = hashlib.sha256(notation).hexdigest()

        return sha256[:7] if short else sha256

    def _load_from_github_data(self, data: object) -> None:
        self.owner = data.owner.login
        self.name = data.name

        self.archived = data.archived

        self.description = data.description

        self.stars_count = data.stargazers_count
        self.forks_count = data.forks_count

        self.watchers_count = data.watchers_count

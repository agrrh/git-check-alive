import uuid

from pydantic import BaseModel
from typing import Optional


class RepoRefreshRequest(BaseModel):
    token: Optional[str]


class Repo(BaseModel):
    owner: str = ""
    name: str = ""

    id: Optional[str]  # noqa: A003

    address: Optional[str]

    db_key: Optional[str]

    archived: Optional[bool]

    description: Optional[str]

    stars_count: Optional[int]
    forks_count: Optional[int]

    def __init__(self, **kwargs) -> None:  # noqa: ANN003
        super().__init__(**kwargs)

        self.address = self.address or f"{self.owner}/{self.name}"
        self.id = self.__gen_id()
        self.db_key = f"repo.{self.id}"

    def __gen_id(self) -> str:
        id_ = uuid.uuid5(uuid.NAMESPACE_URL, f"https://github.com/{self.address}")
        return str(id_)

    def _load_from_github_data(self, data: object) -> None:
        self.owner = data.owner.login
        self.name = data.name

        self.archived = data.archived

        self.description = data.description

        self.stars_count = data.stargazers_count
        self.forks_count = data.forks_count

from pydantic import BaseModel
from typing import Optional

import uuid


class Task(BaseModel):
    id: Optional[uuid.UUID]  # noqa: A003

    db_key: Optional[str]
    db_lock_key: Optional[str]
    db_repo_key: Optional[str]

    repo_sha256: Optional[str]
    repo_address: Optional[str]

    token: Optional[str]

    finished: Optional[bool] = False
    success: Optional[bool] = False

    def __init__(self, **kwargs) -> None:  # noqa: ANN003
        super().__init__(**kwargs)
        self.id = self.id or str(uuid.uuid4())
        self.db_key = f"task.{self.id}"
        self.db_lock_key = f"lock.{self.id}"
        self.db_repo_key = f"repo.{self.repo_sha256}"

from pydantic import BaseModel
from typing import Optional

import uuid


class Task(BaseModel):
    id: Optional[uuid.UUID]

    db_key: Optional[str]

    repo_sha256: str
    token: str

    finished: Optional[bool] = False
    success: Optional[bool]

    result: Optional[dict]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.id = self.id or str(uuid.uuid4())
        self.db_key = f"task.{self.id}"

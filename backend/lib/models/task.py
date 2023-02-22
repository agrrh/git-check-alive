from pydantic import BaseModel
from typing import Optional

import uuid


class TaskPlan(BaseModel):
    id: Optional[uuid.UUID]

    repo_sha256: str
    token: str

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.id = str(uuid.uuid4())

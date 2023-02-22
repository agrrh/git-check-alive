from fastapi import FastAPI, HTTPException

import json
import logging
import redis

from lib.models.repository import RepoRefreshRequest, Repo
from lib.models.task import Task


r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
app = FastAPI()


@app.get("/")
async def read_root() -> object:
    return {"Hello": "World"}


@app.get("/repo/{owner}/{name}")
async def repo_get(owner: str, name: str) -> object:
    repo = Repo(
        owner=owner,
        name=name,
    )

    try:
        repo_data = r.get(repo.db_key)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get repository, try again later")

    if not repo_data:
        raise HTTPException(status_code=404, detail="Could not find repository, please refresh first")

    repo = Repo(**json.loads(repo_data))

    logging.debug(repo)

    return repo


@app.post("/repo/{owner}/{name}/refresh", status_code=201)
async def repo_refresh(owner: str, name: str, refresh_req: RepoRefreshRequest) -> object:
    repo = Repo(
        owner=owner,
        name=name,
    )

    task = Task(
        repo_sha256=repo.sha256,
        repo_address=repo.address,
        token=refresh_req.token,
    )

    channel = "repo.refresh"

    try:
        r.publish(channel, task.json())
    except Exception:
        raise HTTPException(status_code=500, detail="Could not schedule task, try again later")

    return {
        "request": repo.dict(include={"owner", "name"}),
        "task": task.id,
    }


@app.get("/task/{id}")
async def read_task(id: str) -> object:  # noqa: A002
    try:
        task_data_raw = r.get(f"task.{id}")
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get task, try again later")

    if not task_data_raw:
        raise HTTPException(status_code=404, detail="Could not find task, please check ID")

    task_data = json.loads(task_data_raw)
    task = Task(**task_data)

    task.token = "<hidden>"

    return task.dict()

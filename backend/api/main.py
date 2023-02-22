from fastapi import FastAPI, HTTPException

import json
import logging
import redis

from lib.models.repository import RepoRefreshRequest, RepoRequest
from lib.models.task import Task


r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
app = FastAPI()


@app.get("/")
async def read_root() -> object:
    return {"Hello": "World"}


@app.get("/repo/{owner}/{name}")
async def repo_get(owner: str, name: str) -> object:
    repo_req = RepoRequest(
        owner=owner,
        name=name,
    )

    try:
        repo_data = r.get(f"repo.{repo_req.sha256}")
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get repository, try again later")

    if not repo_data:
        raise HTTPException(status_code=404, detail="Could not find repository, please refresh first")

    # TODO: Load repository
    repo = {}
    repo.update({"foo": 42})

    return repo


@app.post("/repo/{owner}/{name}/refresh", status_code=201)
async def repo_refresh(owner: str, name: str, refresh_req: RepoRefreshRequest) -> object:
    repo_req = RepoRequest(
        owner=owner,
        name=name,
    )

    try:
        r.set(f"repo.{repo_req.sha256}", repo_req.json())
    except Exception:
        raise HTTPException(status_code=500, detail="Could not create repository, try again later")

    task = Task(
        repo_sha256=repo_req.sha256,
        token=refresh_req.token,
    )

    channel = "repo.refresh"

    try:
        r.publish(channel, task.json())
    except Exception:
        raise HTTPException(status_code=500, detail="Could not schedule task, try again later")

    return {
        "request": repo_req.dict(exclude={"sha256"}),
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

    logging.debug(task)

    return task

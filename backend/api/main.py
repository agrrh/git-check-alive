from fastapi import FastAPI, HTTPException

import redis

from lib.models.repository import RepoRefreshRequest, RepoRequest
from lib.models.task import TaskPlan


r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/repo/{author}/{repo}")
async def repo_get(author: str, name: str):
    repo_req = RepoRequest(
        author=author,
        name=name,
    )

    try:
        repo_data = r.get(f"repo.{repo_req.sha256}")
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get repository, try again later")

    if not repo_data:
        raise HTTPException(status_code=404, detail="Could not find repository, please refresh first")

    return repo_data.dict()


@app.post("/repo/{author}/{name}/refresh", status_code=201)
async def repo_refresh(author: str, name: str, refresh_req: RepoRefreshRequest):
    repo_req = RepoRequest(
        author=author,
        name=name,
    )

    try:
        r.set(f"repo.{repo_req.sha256}", repo_req.json())
    except Exception:
        raise HTTPException(status_code=500, detail="Could not create repository, try again later")

    task = TaskPlan(
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

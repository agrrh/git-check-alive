from fastapi import FastAPI, HTTPException

import redis

from lib.models.repository import RepoRefreshRequest, Repo
from lib.manager import Manager


cache = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
app = FastAPI()

manager = Manager(cache=cache)


@app.get("/")
async def read_root() -> object:
    return {"Hello": "World"}


@app.get("/repo/{owner}/{name}")
async def get_repo(owner: str, name: str) -> object:
    repo, success = manager.get_repository_from_cache(owner=owner, name=name)

    if not success:
        (_, _) = manager.place_refresh_task(repo)

        raise HTTPException(
            status_code=404,
            detail="Could not find repository data, please return in a moment",
        )

    return repo


@app.post("/repo/{owner}/{name}/refresh", status_code=201)
async def post_repo(owner: str, name: str, refresh_req: RepoRefreshRequest | None = None) -> object:
    repo = Repo(
        owner=owner,
        name=name,
    )

    (task, success) = manager.place_refresh_task(
        repo,
        refresh_req.token if refresh_req else None,
    )

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Could not place refresh task, try again later",
        )

    return {
        "request": repo.dict(include={"owner", "name"}),
        "task": task.id,
    }


@app.get("/task/{id}")
async def get_task(id: str) -> object:  # noqa: A002
    task, success = manager.get_refresh_task(id)

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Could not get refresh task, try again later",
        )

    return task.dict()

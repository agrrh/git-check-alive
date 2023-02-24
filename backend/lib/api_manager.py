import redis
import logging
import json
import uuid

from lib.models.repository import Repo
from lib.models.task import Task


class ApiManager:
    def __init__(self, db: redis.Redis) -> None:
        self.db = db

    def get_repository_from_cache(self, owner: str, name: str) -> (Repo, bool):
        logging.debug("Initializing new Repo container")
        repo = Repo(
            owner=owner,
            name=name,
        )

        logging.debug(f"Getting Repo data from cache by key: {repo.db_key}")
        try:
            repo_data = self.db.get(repo.db_key)
        except Exception:
            logging.info(f"No cached data for {repo.address}")
            return (repo, False)

        if not repo_data:
            logging.debug(f"Repo data for {repo.db_key} seems empty")
            return (repo, False)

        logging.debug(f"Populating Repo {repo.address} with cached data")
        repo = Repo(**json.loads(repo_data))

        return (repo, True)

    def place_refresh_task(self, repo: Repo, token: str = "") -> (Task, bool):
        task = Task(
            repo_sha256=repo.sha256,
            repo_address=repo.address,
            token=token,
        )

        channel = "repo.refresh"

        try:
            self.db.publish(channel, task.json())
        except Exception:
            return (task, False)

        return (task, True)

    def get_refresh_task(self, id_: uuid.UUID) -> (Task, bool):
        task = Task(
            id=id_,
        )

        try:
            task_data = self.db.get(task.db_key)
        except Exception:
            return (task, False)

        task = Task(**json.loads(task_data))
        task.token = "<hidden>"

        return (task, True)

import logging
import redis

from github import Github

from lib.models.repository import Repo
from lib.models.task import Task


class TaskManager:
    def __init__(self, db: redis.Redis) -> None:
        self.db = db

    def allocate_task(self, task: Task) -> bool:
        logging.debug(f"Trying to allocate task: {task.id}")

        logging.debug(f"Checking if repo already populated: {task.db_repo_key}")

        if self.db.exists(task.db_repo_key):
            logging.info(f"Repo already populated, refusing to continue: {task.db_repo_key}")
            return False

        logging.debug(f"Checking for active lock: {task.db_lock_key}")

        if not self.db.setnx(task.db_lock_key, ""):
            logging.info(f"Lock active, refusing to continue: {task.db_lock_key}")
            return False

        logging.debug(f"Prolonging lock TTL: {task.db_lock_key}")
        self.db.expire(task.db_lock_key, 60)

        return True

    def repo_fetch(self, repo: Repo, github_handler: Github) -> (Repo, bool):
        result = True

        try:
            repo_github = github_handler.get_repo(repo.address)
        except Exception as e:
            logging.error(f"Could not get data for repo: {repo.address}")
            logging.warning(e)
            result = False
        else:
            repo._load_from_github_data(repo_github)

        return (repo, result)

    def task_commit(self, task: Task, repo: Repo) -> None:
        logging.info(f"Commiting task {task.id} for repo {repo.address}")

        task.finished = True

        logging.info(f"Updating Task data: {task.db_key}")
        self.db.setex(task.db_key, 300, task.json())

        if task.success:
            logging.warning(f"Updating Repo data: {repo.db_key} @ {task.db_key}")
            self.db.setex(repo.db_key, 3600, repo.json())

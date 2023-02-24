import logging
import redis

from github import Github

from lib.models.task import Task
from lib.models.repository import Repo


class TaskManager:
    def __init__(self, db: redis.Redis, github_token: str) -> None:
        self.db = db
        self.GITHUB_TOKEN_DEFAULT = github_token

    def _allocate_task(self, task: Task) -> bool:
        logging.debug(f"Trying to allocate task: {task.id}")

        logging.debug(f"Checking if repo already populated: {task.db_repo_key}")

        if self.db.exists(task.db_repo_key):
            logging.info(f"Repo already populated, refusing to continue: {task.db_repo_key}")
            return False

        logging.debug(f"Checking for active lock: {task.db_lock_key}")

        if self.db.setnx(task.db_lock_key, ""):
            logging.debug(f"Lock acquired, setting TTL: {task.db_lock_key}")
            self.db.expire(task.db_lock_key, 60)
        else:
            logging.info(f"Lock active, refusing to continue: {task.db_lock_key}")
            return False

        return True

    def _repo_fetch(self, repo: Repo, github_handler: Github) -> (Repo, bool):
        logging.debug(f"Sending request to GitHub API for {repo.address}")

        try:
            repo_github = github_handler.get_repo(repo.address)
        except Exception as e:
            logging.error(f"Could not get data for repo: {repo.address}: {e}")
            result = False
        else:
            logging.debug(f"Parsing GitHub response for repo: {repo.address}")
            repo._load_from_github_data(repo_github)
            result = True

        return (repo, result)

    def _task_commit(self, task: Task, repo: Repo) -> None:
        logging.info(f"Commiting task {task.id} for repo {repo.address}")

        task.finished = True

        logging.info(f"Updating Task data: {task.db_key}")
        self.db.setex(task.db_key, 300, task.json())

        if task.success:
            logging.warning(f"Updating Repo data: {repo.db_key} @ {task.db_key}")
            self.db.setex(repo.db_key, 3600, repo.json())

    def process(self, data: dict) -> None:
        task = Task(**data)

        should_run = self._allocate_task(task)

        if not should_run:
            return None

        logging.warning(f"Processing Task: {task.id}")

        repo = Repo(
            address=task.repo_address,
        )

        g = Github(task.token or self.GITHUB_TOKEN_DEFAULT)

        repo, task.success = self._repo_fetch(repo, github_handler=g)

        logging.debug(f"Commiting task: {task.id}")
        self._task_commit(task, repo)

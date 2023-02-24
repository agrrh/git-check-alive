import logging
import redis
import time
import os

from threading import Thread

from github import Github

from lib.models.task import Task
from lib.models.repository import Repo
from lib.models.message import Message
from lib.task_manager import TaskManager

GITHUB_TOKEN_DEFAULT = os.environ.get("APP_GITHUB_TOKEN")

db = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

manager = TaskManager(db=db)


def process(data: dict) -> None:
    task = Task(**data)

    should_run = manager.allocate_task(task)

    if not should_run:
        return None

    logging.warning(f"Processing Task: {task.id}")

    repo = Repo(
        address=task.repo_address,
    )

    g = Github(task.token or GITHUB_TOKEN_DEFAULT)

    repo, task.success = manager.repo_fetch(repo, github=g)

    manager.task_commit = (task, repo)


def main() -> None:
    logging.critical("Starting worker")

    p = db.pubsub()
    p.subscribe("repo.refresh")

    while True:
        body = p.get_message()

        message = Message(body=body)

        logging.info(f"Got message: {message.raw}")

        try:
            t = Thread(target=process, args=(message.data,))
            t.start()

        except Exception as e:  # noqa: PIE786
            logging.error(f'Could not process "{e}": {message.raw}')

        time.sleep(0.001)

import json
import logging
import redis
import time
from github import Github

from threading import Thread

from lib.models.task import Task
from lib.models.repository import Repo

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def process(data: dict) -> None:
    # Check if repo already populated

    task = Task(**data)

    logging.warning(f"Processing Task: {task.id}")

    r.set(task.db_key, task.json())
    r.expire(task.db_key, 60)

    task.success = True

    if r.exists(f"repo.{task.repo_sha256}"):
        repo = Repo(
            **json.loads(
                r.get(f"repo.{task.repo_sha256}"),
            ),
        )

    else:
        # If we don't have data, get it from github

        repo = Repo(
            address=task.repo_address,
        )

        g = Github(task.token)

        try:
            repo_github = g.get_repo(repo.address)
        except Exception:
            logging.error(f"Could not get data for repo: {repo.address}")
            task.success = False
        else:
            logging.warning("loading")
            repo._load_from_github_data(repo_github)

    # Save task result

    logging.warning(f"{repo.db_key}, {repo.owner}, {repo.name}, {repo.address}")

    r.set(repo.db_key, repo.json())
    r.expire(repo.db_key, 3600)

    task.finished = True

    r.set(task.db_key, task.json())
    r.expire(task.db_key, 300)


def main() -> None:  # noqa: CAC001, CCR001
    logging.critical("Starting worker")

    p = r.pubsub()
    p.subscribe("repo.refresh")

    while True:
        message = p.get_message()

        if not message:
            continue

        if message.get("type") != "message":
            continue

        data_raw = message.get("data")

        if data_raw:
            logging.info(f"Got message: {data_raw}")

            try:
                data = json.loads(data_raw)

                t = Thread(target=process, args=(data,))
                t.start()

            except Exception as e:  # noqa: PIE786
                logging.error(f"Could not process: {e}")
                logging.debug(f"{data_raw}")

        time.sleep(0.001)

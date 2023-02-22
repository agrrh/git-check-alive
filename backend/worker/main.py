import json
import logging
import redis
import time
from github import Github

from threading import Thread

from lib.models.task import Task
from lib.models.repository import RepoRequest, Repo

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def process(data: dict) -> None:
    task = Task(**data)

    logging.warning(f"Processing Task: {task.id}")

    # TODO: Skip processing if results are fresh

    r.set(task.db_key, task.json())
    r.expire(task.db_key, 300)

    g = Github(task.token)

    repo_req = RepoRequest(
        **json.loads(
            r.get(f"repo.{task.repo_sha256}"),
        ),
    )

    try:
        repo_github = g.get_repo(repo_req.address)
    except Exception:
        logging.error(f"Could not get data for repo: {repo_req.address}")
        result = None

        task.success = False

    else:
        repo = Repo()
        repo._load_from_github_data(repo_github)
        result = repo.dict()

        task.success = True

    task.result = result
    task.finished = True

    # TODO: Save result to repository, not to task

    r.set(task.db_key, task.json())
    r.expire(task.db_key, 3600)


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

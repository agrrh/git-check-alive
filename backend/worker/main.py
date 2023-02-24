import logging
import redis
import time
import os

from threading import Thread

from lib.models.message import Message
from lib.task_manager import TaskManager

GITHUB_TOKEN_DEFAULT = os.environ.get("APP_GITHUB_TOKEN")

db = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

manager = TaskManager(db=db, github_token=GITHUB_TOKEN_DEFAULT)


def main() -> None:
    logging.critical("Starting worker")

    p = db.pubsub(ignore_subscribe_messages=True)
    p.subscribe("repo.refresh")

    for body in p.listen():
        message = Message(body=dict(body))

        logging.info(f"Got message: {message.raw}")

        try:
            t = Thread(target=manager.process, args=(message.data,))
            t.start()

        except Exception as e:  # noqa: PIE786
            logging.error(f'Could not process "{e}": {message.raw}')

        time.sleep(0.001)

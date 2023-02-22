import json
import logging
import redis
import time

from threading import Thread

from lib.models.task import Task

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)


def process(data: dict) -> None:
    task = Task(**data)

    r.set(task.db_key, task.json())
    r.expire(task.db_key, 3600)

    task.result = {"GET RESULT!": 42}
    task.finished = True
    task.success = True

    r.set(task.db_key, task.json(), keepttl=True)
    r.expire(task.db_key, 3600)


def main() -> None:
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
            try:
                data = json.loads(data_raw)

                t = Thread(target=process, args=(data,))
                t.start()

            except Exception as e:
                logging.error(f"Could not process: {e}")
                logging.debug(f"{data_raw}")

        time.sleep(0.001)

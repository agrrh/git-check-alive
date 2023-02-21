import os

from app import app_flask, loop
from loguru import logger

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

logger.add(
    "errors.log",
    format="{time:DD-MM HH:mm} {message}",
    level="ERROR",
)


if __name__ == "__main__":
    app_flask.run()
    loop.run_forever()

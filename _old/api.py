from loguru import logger

from app import app_flask
from app.views import *


logger.add(
    "errors.log",
    format="{time:DD-MM HH:mm} {message}",
    level="WARNING",
)


if __name__ == "__main__":
    app_flask.run(
        host="0.0.0.0",
        threaded=True,
        debug=False,
        use_reloader=False,
    )

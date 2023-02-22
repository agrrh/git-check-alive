import os
import logging

from api.main import app

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)

if __name__ == "__main__":
    app.run()

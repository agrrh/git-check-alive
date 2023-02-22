import os
import logging

from worker.main import main

LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)

if __name__ == "__main__":
    main()

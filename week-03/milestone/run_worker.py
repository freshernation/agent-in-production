"""The worker process - given. Run it next to the server:

    python3 run_worker.py

It loops for ever: one job at a time, a short sleep when there is nothing to do.
Stop it with Ctrl+C, at any moment, and start it again. Nothing is lost - that
is what this week was for.
"""

import os
import socket
import time

from app import parse_roles, work_once
from llm import connect

DB_PATH = os.environ.get("DESK_DB", "desk.db")


def main():
    model = connect()
    roles = parse_roles(os.environ.get("DESK_ROLES", ""))
    name = f"{socket.gethostname()}-{os.getpid()}"
    print(f"Worker {name} watching {DB_PATH}")
    while True:
        outcome = work_once(model, roles, DB_PATH, name, time.time())
        if outcome == "idle":
            time.sleep(1)
        else:
            print(outcome)


if __name__ == "__main__":
    main()

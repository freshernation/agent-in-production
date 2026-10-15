"""Sends traces and feedback to Langfuse every thirty seconds - given.

    pip install "langfuse>=4,<5"
    python3 run_exporter.py

Runs beside the server and the worker. If Langfuse is unreachable, nothing is
lost: traces stay marked unexported in your database and go next time.
"""

import os
import time

from app import export_once
from langfuse_client import LangfuseClient

from database import sqlite_path

DB_PATH = sqlite_path(os.environ.get("DATABASE_URL", "sqlite:///desk.db"))


def main():
    client = LangfuseClient()
    while True:
        print(export_once(DB_PATH, client))
        time.sleep(30)


if __name__ == "__main__":
    main()

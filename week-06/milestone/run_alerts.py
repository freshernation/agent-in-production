"""Checks the last five minutes every minute, and sends an alert - given.

    python3 run_alerts.py

Set ALERT_WEBHOOK_URL to an incoming webhook (Slack's, or anything that accepts
{"text": "..."}) and alerts arrive on your phone. Without it they are printed,
which is fine for the laptop and useless at 3am.
"""

import os
import time

import httpx

from alerts import Pager
from app import alert_once
from database import sqlite_path

DB_PATH = sqlite_path(os.environ.get("DATABASE_URL", "sqlite:///desk.db"))
WEBHOOK = os.environ.get("ALERT_WEBHOOK_URL", "")


def send(message: str) -> None:
    print("ALERT", message, flush=True)
    if not WEBHOOK:
        return
    try:
        httpx.post(WEBHOOK, json={"text": message}, timeout=10).raise_for_status()
    except httpx.HTTPError as error:
        print("Could not send the alert:", error, flush=True)


def main():
    pager = Pager(send, cooldown=1800)
    while True:
        print("firing:", alert_once(DB_PATH, pager, time.time()), flush=True)
        time.sleep(60)


if __name__ == "__main__":
    main()

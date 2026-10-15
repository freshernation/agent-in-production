"""A smoke test of the whole service - given.

Starts the app in this process with a fake model and a throwaway database, and
checks the three things that must be true of any release: it is up, it refuses a
stranger, and it answers someone with a key. No network, no key, no cost - so it
can run in CI on every push.

    python3 smoke.py
"""

import sys
import tempfile
import time
from pathlib import Path

from fastapi.testclient import TestClient

from app import create_app
from limits import Limiter
from llm import FakeModel, say

KEY = "k-smoke-0123456789"


def main() -> int:
    problems = []
    with tempfile.TemporaryDirectory() as folder:
        app = create_app(FakeModel(say("Hello.")), {KEY: "smoke"}, {"smoke": "owner"},
                         str(Path(folder) / "smoke.db"), Limiter(10, 1, time.monotonic),
                         version="smoke")
        client = TestClient(app)
        if client.get("/health").json().get("version") != "smoke":
            problems.append("/health does not report the version")
        if client.get("/ready").status_code != 200:
            problems.append("/ready is not ready")
        if client.post("/chat", json={"message": "hi"}).status_code != 401:
            problems.append("/chat answers without a key")
        answer = client.post("/chat", json={"message": "hi"},
                             headers={"Authorization": f"Bearer {KEY}"})
        if answer.status_code != 200 or answer.json().get("reply") != "Hello.":
            problems.append(f"/chat with a key answered {answer.status_code}")
    for problem in problems:
        print("FAIL", problem)
    print("smoke ok" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

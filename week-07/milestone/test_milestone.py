"""Week 7 milestone - Desk, connected and attacked.

Run me:  pytest week-07/milestone -v

The real rate comes from run_attacks.py with your provider, in CI. Here it runs
with the fake model, which proves the wiring and nothing else.
"""

import re

import anyio
import pytest
from fastapi.testclient import TestClient

from llm import FakeModel, say, use
from mcp import Client

KEYS = {"k-alice-0123456789": "alice"}
ROLES = {"alice": "owner"}
ALICE = {"Authorization": "Bearer k-alice-0123456789"}


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def body(source, name):
    lines = []
    for line in source(name).splitlines():
        if line.strip() and not line.strip().startswith("#"):
            lines.append(line)
    assert lines, f"{name} contains only comments so far - write it."
    return "\n".join(lines)


class TestMCPOnTheSameNotes:
    def test_a_note_saved_through_chat_is_listed_through_mcp(self, load, tmp_path):
        path = str(tmp_path / "d.db")
        app = load("app.py")
        limiter = load("limits.py").Limiter(100, 1, Clock())
        client = TestClient(app.create_app(
            FakeModel([use("add_note", {"title": "dentist"}), say("Saved.")]),
            KEYS, ROLES, path, limiter, clock=Clock()))
        assert client.post("/chat", json={"message": "save dentist"}, headers=ALICE).status_code == 200

        server = load("desk_mcp.py").build_server(path, "alice")

        async def go():
            async with Client(server) as mcp:
                return await mcp.call_tool("list_titles", {})
        assert anyio.run(go).content[0].text == "1. dentist"


class TestTheAttackRun:
    def test_runs_and_reports(self, run):
        result = run("run_attacks.py", allow_crash=True)
        assert re.search(r"rate 0\.0 \(0/\d+ did harm, 0 unanswered\)", result.stdout), result.stdout
        assert result.code == 0


class TestTheWorkflow:
    def test_three_jobs(self, source):
        text = body(source, "ci.yml")
        assert "checks:" in text and "attacks:" in text and "deploy:" in text

    def test_the_attacks_use_a_secret_key(self, source):
        attacks = body(source, "ci.yml").split("attacks:", 1)[1].split("deploy:")[0]
        assert "run_attacks.py" in attacks
        assert "secrets." in attacks
        assert not re.search(r"sk-[A-Za-z0-9]", attacks), "A key is written in the workflow."

    def test_the_attacks_only_on_main(self, source):
        attacks = body(source, "ci.yml").split("attacks:", 1)[1].split("deploy:")[0]
        assert "refs/heads/main" in attacks, (
            "The attack run calls a real model on every push to every branch. "
            "Run it where it decides something: before a deploy."
        )

    def test_deploy_waits_for_both(self, source):
        deploy = body(source, "ci.yml").split("deploy:", 1)[1]
        needs = re.search(r"needs:\s*\[([^\]]*)\]", deploy)
        assert needs and "checks" in needs.group(1) and "attacks" in needs.group(1), (
            "The deploy does not wait for the attack run, so a push that makes "
            "Desk leak still ships."
        )


class TestStillWorks:
    def test_smoke(self, run):
        assert "smoke ok" in run("smoke.py", allow_crash=True).stdout


class TestTheReport:
    def test_sections(self, source):
        text = source("ATTACKS.md")
        assert "<!--" not in text, "Delete the instructions comment in ATTACKS.md."
        for heading in ("The suite", "Before", "The defence", "After", "What still gets through"):
            assert f"## {heading}" in text, f"ATTACKS.md has no '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"'{heading}' is {len(part.split())} words."

    @pytest.mark.parametrize("heading", ["Before", "After"])
    def test_a_rate(self, source, heading):
        part = source("ATTACKS.md").split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert re.search(r"\b\d+(\.\d+)?%|\b[01]\.\d+\b", part), f"'{heading}' gives no rate."

"""Week 5 milestone - Project 1: deployed, by CI, behind a gate.

Run me:  pytest week-05/milestone -v

The deployment itself happens on your host and is checked by check_live.py.
These tests check everything that can be checked before it gets there.
"""

import re
import subprocess
import sys

import pytest
from fastapi.testclient import TestClient

from llm import FakeModel, say

KEYS = {"k-alice-0123456789": "alice"}
ROLES = {"alice": "owner"}
ALICE = {"Authorization": "Bearer k-alice-0123456789"}


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


@pytest.fixture
def app(load):
    return load("app.py")


def make(app, load, path, version="1.0.0"):
    limiter = load("limits.py").Limiter(100, 1, Clock())
    return TestClient(app.create_app(FakeModel(say("Hello.")), KEYS, ROLES, path, limiter,
                                     clock=Clock(), version=version))


def body(source, name):
    lines = []
    for line in source(name).splitlines():
        if line.strip() and not line.strip().startswith("#"):
            lines.append(line)
    assert lines, f"{name} contains only comments so far - write it."
    return "\n".join(lines)


class TestTheService:
    def test_health_reports_the_version(self, app, load, tmp_path):
        client = make(app, load, str(tmp_path / "d.db"), version="1.4.0")
        assert client.get("/health").json() == {"status": "ok", "version": "1.4.0"}

    def test_ready(self, app, load, tmp_path):
        response = make(app, load, str(tmp_path / "d.db")).get("/ready")
        assert response.status_code == 200
        assert response.json() == {"ready": True, "failing": []}

    def test_still_answers(self, app, load, tmp_path):
        client = make(app, load, str(tmp_path / "d.db"))
        assert client.post("/chat", json={"message": "hi"}, headers=ALICE).json()["reply"] == "Hello."

    def test_from_environment(self, app, monkeypatch, tmp_path):
        monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'd.db'}")
        monkeypatch.setenv("DESK_KEYS", "alice:k-alice-0123456789")
        monkeypatch.setenv("AGENT_PROVIDER", "fake")
        monkeypatch.setenv("VERSION", "abc123")
        client = TestClient(app.from_environment())
        assert client.get("/health").json()["version"] == "abc123"

    def test_from_environment_refuses_a_bad_setting(self, app, monkeypatch):
        monkeypatch.delenv("DATABASE_URL", raising=False)
        monkeypatch.delenv("DESK_KEYS", raising=False)
        with pytest.raises(RuntimeError):
            app.from_environment()


class TestTheSmokeTest:
    def test_passes(self, run):
        result = run("smoke.py", allow_crash=True)
        assert "smoke ok" in result.stdout, result.stdout


class TestTheFiles:
    def test_dockerfile(self, source):
        text = body(source, "Dockerfile")
        assert text.startswith("FROM python:3.12") and "0.0.0.0" in text and "USER " in text

    def test_compose_passes_the_version(self, source):
        text = body(source, "compose.yaml")
        assert "VERSION" in text and "worker:" in text and "/data" in text

    def test_dockerignore(self, source):
        text = body(source, ".dockerignore")
        assert ".env" in text and "instructor" in text


class TestTheWorkflow:
    def test_two_jobs(self, source):
        text = body(source, "ci.yml")
        assert "checks:" in text and "deploy:" in text
        assert "checks.py" in text

    def test_deploy_waits_for_the_checks(self, source):
        text = body(source, "ci.yml")
        deploy = text.split("deploy:", 1)[1]
        assert "needs: checks" in deploy, (
            "The deploy job does not wait for the checks. Without `needs`, a "
            "failing push deploys anyway."
        )

    def test_deploy_only_from_main(self, source):
        deploy = body(source, "ci.yml").split("deploy:", 1)[1]
        assert "refs/heads/main" in deploy

    def test_the_hook_is_a_secret(self, source):
        deploy = body(source, "ci.yml").split("deploy:", 1)[1]
        assert "secrets." in deploy
        assert not re.search(r"https?://[^\s\"']*hook", deploy.replace("${{", "")), (
            "The deploy hook URL is written in the workflow. Anyone who reads the "
            "repository can deploy whatever they like. Keep it in a secret."
        )

    def test_it_checks_the_live_release(self, source):
        deploy = body(source, "ci.yml").split("deploy:", 1)[1]
        assert "check_live.py" in deploy


class TestTheDocuments:
    @pytest.mark.parametrize("name,headings", [
        ("DEPLOYMENT.md", ["Where it runs", "Configuration", "How a change reaches it", "Going back"]),
        ("PROJECT_README.md", ["What it is", "Try it", "How it is built", "How I know it works",
                               "What I would do next"]),
    ])
    def test_sections(self, source, name, headings):
        text = source(name)
        assert "<!--" not in text, f"Delete the instructions comment in {name}."
        for heading in headings:
            assert f"## {heading}" in text, f"{name} has no '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 30, f"{name} '{heading}' is {len(part.split())} words."

    def test_the_readme_has_the_live_url(self, source):
        section = source("PROJECT_README.md").split("## Try it", 1)[1].split("\n## ")[0]
        assert re.search(r"https://", section)

"""Week 6 milestone - Desk stays up.

Run me:  pytest week-06/milestone -v

The live half - an alert on your phone, an answer with the primary model
switched off - happens during the defence.
"""

import sqlite3

import pytest
from fastapi.testclient import TestClient

from llm import FakeModel, ModelError, say, use

KEYS = {"k-alice-0123456789": "alice", "k-bob-0123456789xx": "bob"}
ROLES = {"alice": "owner", "bob": "owner"}
ALICE = {"Authorization": "Bearer k-alice-0123456789"}
BOB = {"Authorization": "Bearer k-bob-0123456789xx"}


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


@pytest.fixture
def app(load):
    return load("app.py")


def make(app, load, path, model, cache=None, daily_budget=None):
    limiter = load("limits.py").Limiter(100, 1, Clock())
    return TestClient(app.create_app(model, KEYS, ROLES, path, limiter, clock=Clock(),
                                     version="1.0.0", cache=cache, daily_budget=daily_budget))


def chat(client, message, who=ALICE):
    return client.post("/chat", json={"message": message}, headers=who)


class TestWhenTheModelIsDown:
    def test_the_fallback_answers(self, app, load, tmp_path):
        fb = load("fallback.py")
        model = fb.FallbackModel(FakeModel([ModelError("down")] * 5), FakeModel(say("From the backup.")),
                                 fb.Breaker(3, 60, Clock()))
        assert chat(make(app, load, str(tmp_path / "d.db"), model), "hi").json()["reply"] == "From the backup."

    def test_both_down_says_so(self, app, load, tmp_path):
        fb = load("fallback.py")
        response = chat(make(app, load, str(tmp_path / "d.db"), FakeModel([ModelError("down")] * 5)), "hi")
        assert response.status_code == 503
        assert response.json()["detail"] == fb.DOWN_MESSAGE

    def test_build_model_adds_the_fallback(self, app, load, monkeypatch):
        monkeypatch.setattr("app.connect_model", lambda provider: FakeModel(say(provider)))
        settings = load("config.py").load_settings({
            "DATABASE_URL": "sqlite:///x.db", "DESK_KEYS": "alice:k-alice-0123456789",
            "AGENT_PROVIDER": "claude", "FALLBACK_PROVIDER": "openai"})
        model = app.build_model(settings)
        assert type(model).__name__ == "FallbackModel"

    def test_no_fallback_no_wrapper(self, app, load, monkeypatch):
        monkeypatch.setattr("app.connect_model", lambda provider: FakeModel(say(provider)))
        settings = load("config.py").load_settings({
            "DATABASE_URL": "sqlite:///x.db", "DESK_KEYS": "alice:k-alice-0123456789"})
        assert type(app.build_model(settings)).__name__ == "FakeModel"


class TestTheConfiguration:
    BASE = {"DATABASE_URL": "sqlite:///x.db", "DESK_KEYS": "alice:k-alice-0123456789"}

    def test_defaults(self, load):
        settings = load("config.py").load_settings(self.BASE)
        assert settings.fallback_provider == "" and settings.daily_budget == 1.0

    def test_the_same_provider_twice_is_refused(self, load):
        with pytest.raises(ValueError):
            load("config.py").load_settings({**self.BASE, "AGENT_PROVIDER": "claude",
                                             "FALLBACK_PROVIDER": "claude"})


class TestTheCache:
    def test_the_same_question_twice_asks_the_model_once(self, app, load, tmp_path):
        model = FakeModel(say("Desk keeps notes."))
        client = make(app, load, str(tmp_path / "d.db"), model,
                      cache=load("caching.py").ResponseCache(60, Clock()))
        first = chat(client, "What is Desk?")
        second = chat(client, "what is desk?")
        assert second.json()["reply"] == "Desk keeps notes."
        assert second.headers.get("X-Cache") == "hit"
        assert second.json()["trace_id"] == first.json()["trace_id"]
        assert model.call_count == 1

    def test_not_for_someone_else(self, app, load, tmp_path):
        model = FakeModel([say("Alice's answer."), say("Bob's answer.")])
        client = make(app, load, str(tmp_path / "d.db"), model,
                      cache=load("caching.py").ResponseCache(60, Clock()))
        chat(client, "What did I write?")
        assert chat(client, "What did I write?", who=BOB).json()["reply"] == "Bob's answer."

    def test_not_after_a_tool(self, app, load, tmp_path):
        model = FakeModel([use("list_titles"), say("You have no notes."), say("You have one note.")])
        client = make(app, load, str(tmp_path / "d.db"), model,
                      cache=load("caching.py").ResponseCache(60, Clock()))
        chat(client, "How many notes?")
        second = chat(client, "How many notes?")
        assert second.json()["reply"] == "You have one note.", (
            "An answer that used a tool came from the cache. The notes may have "
            "changed since."
        )


class TestTheBudget:
    def test_stops_when_spent(self, app, load, tmp_path):
        model = FakeModel(say("Long answer.", input=100_000, output=10_000))   # $0.45 a turn
        client = make(app, load, str(tmp_path / "d.db"), model, daily_budget=0.5)
        assert chat(client, "one").status_code == 200
        assert chat(client, "two").status_code == 200
        third = chat(client, "three")
        assert third.status_code == 429
        assert "budget" in third.json()["detail"]
        assert model.call_count == 2

    def test_one_user_spending_does_not_stop_another(self, app, load, tmp_path):
        model = FakeModel(say("Long answer.", input=100_000, output=10_000))
        client = make(app, load, str(tmp_path / "d.db"), model, daily_budget=0.4)
        chat(client, "one")
        assert chat(client, "two").status_code == 429
        assert chat(client, "hi", who=BOB).status_code == 200

    def test_tasks_are_checked_too(self, app, load, tmp_path):
        model = FakeModel(say("Long answer.", input=100_000, output=10_000))
        client = make(app, load, str(tmp_path / "d.db"), model, daily_budget=0.4)
        chat(client, "one")
        assert client.post("/tasks", json={"message": "two"}, headers=ALICE).status_code == 429


@pytest.fixture
def failing_db(load, tmp_path):
    path = str(tmp_path / "d.db")
    ts = load("tracestore.py")
    db = sqlite3.connect(path, isolation_level=None)
    ts.create_tables(db)
    for number in range(20):
        ts.save(db, {"id": f"t{number}", "user": "alice", "session": "s", "input": "q",
                     "output": "", "spans": [], "usage": {"input": 1, "output": 1},
                     "cost": 0.0, "duration": 0.5, "error": number < 5}, started=900.0 + number)
    db.close()
    return path


class TestAlerts:
    def test_fires_and_pages(self, app, load, failing_db):
        sent = []
        pager = load("alerts.py").Pager(sent.append, cooldown=1800)
        assert app.alert_once(failing_db, pager, now=1000.0) == ["errors"]
        assert len(sent) == 1 and sent[0].startswith("[errors]") and "error_rate" in sent[0]

    def test_does_not_page_twice(self, app, load, failing_db):
        sent = []
        pager = load("alerts.py").Pager(sent.append, cooldown=1800)
        app.alert_once(failing_db, pager, now=1000.0)
        app.alert_once(failing_db, pager, now=1060.0)
        assert len(sent) == 1

    def test_resolves_when_quiet(self, app, load, failing_db):
        sent = []
        pager = load("alerts.py").Pager(sent.append, cooldown=1800)
        app.alert_once(failing_db, pager, now=1000.0)
        assert app.alert_once(failing_db, pager, now=5000.0) == []
        assert app.alert_once(failing_db, pager, now=1000.0) == ["errors"]
        assert len(sent) == 2, "A resolved alert that fires again must page again."


class TestStillWorks:
    def test_smoke(self, run):
        assert "smoke ok" in run("smoke.py", allow_crash=True).stdout

    def test_compose_runs_the_alerts(self, source):
        text = source("compose.yaml")
        assert "alerts:" in text and "run_alerts.py" in text and "FALLBACK_PROVIDER" in text


class TestTheDocuments:
    @pytest.mark.parametrize("name,headings", [
        ("RUNBOOK.md", ["errors", "slow", "spend"]),
        ("INCIDENT.md", ["What users saw", "Timeline", "Why it happened", "How we found out",
                         "What we changed"]),
    ])
    def test_sections(self, source, name, headings):
        text = source(name)
        assert "<!--" not in text, f"Delete the instructions comment in {name}."
        for heading in headings:
            assert f"## {heading}" in text, f"{name} has no '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"{name} '{heading}' is {len(part.split())} words."

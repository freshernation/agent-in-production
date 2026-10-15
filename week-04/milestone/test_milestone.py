"""Week 4 milestone - every request traced, costed and rateable.

Run me:  pytest week-04/milestone -v
"""

import re

import pytest
from fastapi.testclient import TestClient

from llm import FakeModel, ModelError, say, use

KEYS = {"k-alice-0123456789": "alice", "k-bob-0123456789": "bob"}
ROLES = {"alice": "owner", "bob": "owner"}
ALICE = {"Authorization": "Bearer k-alice-0123456789"}
BOB = {"Authorization": "Bearer k-bob-0123456789"}


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        self.now += 0.25
        return self.now


class FakeClient:
    def __init__(self):
        self.traces, self.scores, self.flushed = [], [], 0

    def trace(self, trace):
        self.traces.append(trace)

    def score(self, trace_id, name, value, comment):
        self.scores.append((trace_id, value, comment))

    def flush(self):
        self.flushed += 1


@pytest.fixture
def app(load):
    return load("app.py")


@pytest.fixture
def path(tmp_path):
    return str(tmp_path / "desk.db")


def make(app, load, model, path):
    clock = Clock()
    limiter = load("limits.py").Limiter(100, 1, clock)
    return TestClient(app.create_app(model, KEYS, ROLES, path, limiter, clock=clock))


def stored(load, path, trace_id):
    store, ts = load("store.py"), load("tracestore.py")
    db = store.connect(path)
    try:
        return ts.get(db, trace_id)
    finally:
        db.close()


class TestEveryRequestIsTraced:
    def test_the_trace_id_comes_back(self, app, load, path):
        client = make(app, load, FakeModel([say("Hello.")]), path)
        response = client.post("/chat", json={"message": "hi"}, headers=ALICE)
        body = response.json()
        assert re.fullmatch(r"[0-9a-f]{32}", body["trace_id"])
        assert response.headers.get("x-trace-id") == body["trace_id"]

    def test_the_trace_is_stored(self, app, load, path):
        model = FakeModel([use("add_note", {"title": "milk"}, id="c1", input=500, output=20),
                           say("Saved milk.", input=600, output=10)])
        body = make(app, load, model, path).post(
            "/chat", json={"message": "Remember milk"}, headers=ALICE).json()
        trace = stored(load, path, body["trace_id"])
        assert trace["user"] == "alice"
        assert trace["session"] == body["conversation_id"]
        assert trace["input"] == "Remember milk" and trace["output"] == "Saved milk."
        kinds = []
        for span in trace["spans"]:
            kinds.append((span["type"], span["name"]))
        assert kinds == [("generation", "model"), ("tool", "add_note"), ("generation", "model")]
        assert trace["usage"] == {"input": 1100, "output": 30}
        assert trace["cost"] > 0

    def test_a_failed_request_is_traced_too(self, app, load, path):
        client = make(app, load, FakeModel([ModelError("overloaded")]), path)
        assert client.post("/chat", json={"message": "hi"}, headers=ALICE).status_code == 503
        store, ts = load("store.py"), load("tracestore.py")
        db = store.connect(path)
        rows = db.execute("SELECT error, user FROM traces").fetchall()
        db.close()
        assert rows == [(1, "alice")], (
            "The request that failed left no trace. Those are the ones you will "
            "be asked about."
        )

    def test_background_tasks_are_traced(self, app, load, path):
        client = make(app, load, FakeModel(), path)
        client.post("/tasks", json={"message": "Remember milk"}, headers=ALICE)
        app.work_once(FakeModel([say("Saved.")]), ROLES, path, "w1", now=2000.0)
        store = load("store.py")
        db = store.connect(path)
        count = db.execute("SELECT COUNT(*) FROM traces").fetchone()[0]
        db.close()
        assert count == 1


class TestFeedback:
    def chat(self, app, load, path, headers=ALICE):
        client = make(app, load, FakeModel([say("Deleted eggs.")]), path)
        return client, client.post("/chat", json={"message": "Delete eggs"}, headers=headers).json()

    def test_rating_your_own_answer(self, app, load, path):
        client, body = self.chat(app, load, path)
        response = client.post("/feedback", json={"trace_id": body["trace_id"], "score": -1,
                                                  "comment": "Wrong note"}, headers=ALICE)
        assert response.status_code == 200 and response.json() == {"status": "recorded"}

    def test_someone_elses_is_404(self, app, load, path):
        client, body = self.chat(app, load, path)
        response = client.post("/feedback", json={"trace_id": body["trace_id"], "score": -1},
                               headers=BOB)
        assert response.status_code == 404

    def test_only_up_or_down(self, app, load, path):
        client, body = self.chat(app, load, path)
        response = client.post("/feedback", json={"trace_id": body["trace_id"], "score": 5},
                               headers=ALICE)
        assert response.status_code == 422

    def test_needs_a_key(self, app, load, path):
        client, body = self.chat(app, load, path)
        assert client.post("/feedback", json={"trace_id": body["trace_id"], "score": 1}).status_code == 401


class TestExport:
    def test_traces_and_ratings_reach_the_platform(self, app, load, path):
        client = make(app, load, FakeModel([say("Done.")]), path)
        body = client.post("/chat", json={"message": "x"}, headers=ALICE).json()
        client.post("/feedback", json={"trace_id": body["trace_id"], "score": -1,
                                       "comment": "No"}, headers=ALICE)
        platform = FakeClient()
        assert app.export_once(path, platform) == {"traces": 1, "scores": 1, "failed": 0}
        assert platform.traces[0]["id"] == body["trace_id"]
        assert platform.scores == [(body["trace_id"], -1, "No")]


class TestTheWriteUp:
    HEADINGS = ["Narrowing it down", "What the trace shows", "What the trace cannot show",
                "What happens next"]

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        text = source("FIND_IT.md")
        assert "<!--" not in text, "Delete the instructions comment."
        assert f"## {heading}" in text
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 40, f"'{heading}' is {len(body.split())} words."

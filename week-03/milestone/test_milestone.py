"""Week 3 milestone - work in the background, and fair shares.

Run me:  pytest week-03/milestone -v
"""

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
        return self.now


@pytest.fixture
def app(load):
    return load("app.py")


@pytest.fixture
def limits(load):
    return load("limits.py")


@pytest.fixture
def path(tmp_path):
    return str(tmp_path / "desk.db")


def make(app, limits, model, path, capacity=100, clock=None):
    clock = clock or Clock()
    limiter = limits.Limiter(capacity, 1, clock)
    return TestClient(app.create_app(model, KEYS, ROLES, path, limiter, clock=clock))


class TestTasks:
    def test_submitting_returns_at_once(self, app, limits, path):
        model = FakeModel([])
        client = make(app, limits, model, path)
        response = client.post("/tasks", json={"message": "Tidy my notes"}, headers=ALICE)
        assert response.status_code == 202
        body = response.json()
        assert body["status"] == "queued" and isinstance(body["task_id"], int)
        assert model.call_count == 0, (
            "The model was called while the request waited. A task is queued and "
            "answered at once; the worker does the work."
        )

    def test_the_worker_does_it(self, app, limits, path):
        client = make(app, limits, FakeModel(), path)
        task = client.post("/tasks", json={"message": "Remember milk"}, headers=ALICE).json()
        model = FakeModel([use("add_note", {"title": "milk"}, id="c1"), say("Saved milk.")])
        assert app.work_once(model, ROLES, path, "w1", now=1001.0) == "done"
        status = client.get(f"/tasks/{task['task_id']}", headers=ALICE).json()
        assert status["status"] == "done" and status["result"] == "Saved milk."

    def test_the_task_joins_the_conversation(self, app, limits, path):
        client = make(app, limits, FakeModel([say("Hello.")]), path)
        cid = client.post("/chat", json={"message": "Hi"}, headers=ALICE).json()["conversation_id"]
        client.post("/tasks", json={"message": "And now?", "conversation_id": cid}, headers=ALICE)
        model = FakeModel([say("Still here.")])
        app.work_once(model, ROLES, path, "w1", now=1001.0)
        sent = []
        for message in model.requests[0]["messages"]:
            sent.append(message["content"])
        assert "Hi" in sent

    def test_nothing_to_do(self, app, limits, path):
        make(app, limits, FakeModel(), path)
        assert app.work_once(FakeModel(), ROLES, path, "w1", now=1.0) == "idle"

    def test_someone_elses_task_is_404(self, app, limits, path):
        client = make(app, limits, FakeModel(), path)
        task = client.post("/tasks", json={"message": "secret"}, headers=ALICE).json()
        assert client.get(f"/tasks/{task['task_id']}", headers=BOB).status_code == 404
        assert client.get("/tasks/999", headers=ALICE).status_code == 404

    def test_an_unknown_conversation_is_refused_up_front(self, app, limits, path):
        client = make(app, limits, FakeModel(), path)
        response = client.post("/tasks", json={"message": "x", "conversation_id": "nope"}, headers=ALICE)
        assert response.status_code == 404

    def test_a_task_that_keeps_failing_says_so_and_no_more(self, app, limits, path):
        client = make(app, limits, FakeModel(), path)
        task = client.post("/tasks", json={"message": "x"}, headers=ALICE).json()
        for attempt in range(3):
            broken = FakeModel([ModelError(f"secret detail {attempt}")])
            app.work_once(broken, ROLES, path, "w1", now=1001.0 + attempt)
        status = client.get(f"/tasks/{task['task_id']}", headers=ALICE).json()
        assert status["status"] == "dead", (
            "A model outage was recorded as a finished task. take_turn must raise "
            "when the run stopped with 'error', so the worker retries it."
        )
        assert status["result"] == "The task could not be completed."
        assert "secret detail" not in str(status)

    def test_chat_says_503_when_the_model_is_down(self, app, limits, path):
        client = make(app, limits, FakeModel([ModelError("secret detail")]), path)
        response = client.post("/chat", json={"message": "hi"}, headers=ALICE)
        assert response.status_code == 503
        assert "secret" not in response.text


class TestAWorkerThatDied:
    def test_its_job_is_picked_up_later(self, app, limits, path, load):
        jobs = load("jobs.py")
        client = make(app, limits, FakeModel(), path)
        task = client.post("/tasks", json={"message": "Remember milk"}, headers=ALICE).json()
        store = load("store.py")
        db = store.connect(path)
        jobs.claim(db, "crashed-worker", now=1001.0)
        db.close()
        model = FakeModel([say("Done at last.")])
        assert app.work_once(model, ROLES, path, "w2", now=1001.0 + app.STALE_AFTER + 1) == "done"
        status = client.get(f"/tasks/{task['task_id']}", headers=ALICE).json()
        assert status["result"] == "Done at last."


class TestFairShares:
    def test_a_caller_over_the_limit_gets_429(self, app, limits, path):
        client = make(app, limits, FakeModel(say("ok")), path, capacity=2)
        codes = []
        for _ in range(3):
            codes.append(client.post("/chat", json={"message": "hi"}, headers=ALICE).status_code)
        assert codes == [200, 200, 429]

    def test_with_a_retry_after(self, app, limits, path):
        client = make(app, limits, FakeModel(say("ok")), path, capacity=1)
        client.post("/chat", json={"message": "hi"}, headers=ALICE)
        response = client.post("/chat", json={"message": "hi"}, headers=ALICE)
        assert response.headers.get("retry-after") == "1"

    def test_alice_does_not_use_up_bob(self, app, limits, path):
        client = make(app, limits, FakeModel(say("ok")), path, capacity=1)
        client.post("/chat", json={"message": "hi"}, headers=ALICE)
        assert client.post("/chat", json={"message": "hi"}, headers=BOB).status_code == 200

    def test_tasks_count_against_the_limit_too(self, app, limits, path):
        client = make(app, limits, FakeModel(), path, capacity=1)
        client.post("/tasks", json={"message": "a"}, headers=ALICE)
        assert client.post("/tasks", json={"message": "b"}, headers=ALICE).status_code == 429

    def test_time_refills_it(self, app, limits, path):
        clock = Clock()
        client = make(app, limits, FakeModel(say("ok")), path, capacity=1, clock=clock)
        client.post("/chat", json={"message": "hi"}, headers=ALICE)
        clock.now += 2
        assert client.post("/chat", json={"message": "hi"}, headers=ALICE).status_code == 200

"""Week 4, Day 4 - export, and a bad trace becomes a case.

Run me:  pytest week-04/day-4 -v
"""

import sqlite3

import pytest


class FakeClient:
    def __init__(self, fail_on=()):
        self.traces = []
        self.scores = []
        self.flushed = 0
        self.fail_on = set(fail_on)

    def trace(self, trace):
        if trace["id"] in self.fail_on:
            raise ConnectionError("platform unreachable")
        self.traces.append(trace["id"])

    def score(self, trace_id, name, value, comment):
        self.scores.append((trace_id, name, value, comment))

    def flush(self):
        self.flushed += 1


def trace(id, user="alice", started=0.0):
    return {"id": id, "user": user, "session": "s", "input": f"task {id}", "output": f"answer {id}",
            "spans": [{"type": "generation", "name": "model", "started": 0, "ended": 1},
                      {"type": "tool", "name": "list_titles", "started": 1, "ended": 2},
                      {"type": "tool", "name": "delete_note", "started": 2, "ended": 3},
                      {"type": "tool", "name": "list_titles", "started": 3, "ended": 4}],
            "usage": {"input": 1, "output": 1}, "cost": 0.0, "duration": 4.0, "error": False}


@pytest.fixture
def ex(load):
    return load("exporter.py")


@pytest.fixture
def db(load, tmp_path):
    ts, fb = load("tracestore.py"), load("feedback.py")
    connection = sqlite3.connect(str(tmp_path / "t.db"), isolation_level=None)
    ts.create_tables(connection)
    fb.create_tables(connection)
    ts.save(connection, trace("t1"), started=1.0)
    ts.save(connection, trace("t2"), started=2.0)
    fb.rate(connection, "alice", "t2", -1, "Deleted the wrong note")
    return connection


class TestExport:
    def test_sends_traces_oldest_first_then_scores(self, ex, db):
        client = FakeClient()
        assert ex.export_pending(db, client) == {"traces": 2, "scores": 1, "failed": 0}
        assert client.traces == ["t1", "t2"]
        assert client.scores == [("t2", "user-feedback", -1, "Deleted the wrong note")]
        assert client.flushed == 1

    def test_nothing_is_sent_twice(self, ex, db):
        ex.export_pending(db, FakeClient())
        client = FakeClient()
        assert ex.export_pending(db, client) == {"traces": 0, "scores": 0, "failed": 0}
        assert client.traces == [] and client.scores == []

    def test_a_failure_is_retried_next_time(self, ex, db):
        first = FakeClient(fail_on={"t1"})
        assert ex.export_pending(db, first) == {"traces": 1, "scores": 1, "failed": 1}
        second = FakeClient()
        ex.export_pending(db, second)
        assert second.traces == ["t1"], (
            "A trace the platform did not receive was marked as sent. Mark it "
            "only after the client returns."
        )

    def test_a_score_waits_for_its_trace(self, ex, db):
        first = FakeClient(fail_on={"t2"})
        assert ex.export_pending(db, first)["scores"] == 0, (
            "A score was sent for a trace the platform has never seen."
        )
        second = FakeClient()
        assert ex.export_pending(db, second)["scores"] == 1

    def test_flush_is_called_even_with_nothing_to_send(self, ex, db):
        ex.export_pending(db, FakeClient())
        client = FakeClient()
        ex.export_pending(db, client)
        assert client.flushed == 1


class TestToCase:
    def test_a_draft(self, ex):
        case = ex.to_case(trace("t2"), "Deleted the wrong note")
        assert case == {
            "name": "from trace t2", "task": "task t2", "notes": [], "expect": {},
            "seen": {"calls": ["list_titles", "delete_note"], "answer": "answer t2"},
            "why": "Deleted the wrong note",
        }

    def test_expect_is_left_for_you(self, ex):
        assert ex.to_case(trace("t1"), "")["expect"] == {}, (
            "What should have happened is a judgement. The draft records what "
            "did happen and leaves the expectation to a person."
        )


class TestTheGivenClient:
    def test_it_has_the_three_methods(self, load):
        client_module = load("langfuse_client.py")
        for name in ("trace", "score", "flush"):
            assert callable(getattr(client_module.LangfuseClient, name))

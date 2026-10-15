"""Week 4, Day 2 - traces you can search.

Run me:  pytest week-04/day-2 -v
"""

import sqlite3

import pytest


@pytest.fixture
def ts(load):
    return load("tracestore.py")


@pytest.fixture
def db(ts, tmp_path):
    connection = sqlite3.connect(str(tmp_path / "traces.db"), isolation_level=None)
    ts.create_tables(connection)
    return connection


def trace(id, user="alice", session="c1", cost=0.01, duration=1.0, error=False, tokens=(100, 10)):
    return {"id": id, "user": user, "session": session, "input": "q", "output": "a",
            "spans": [], "usage": {"input": tokens[0], "output": tokens[1]},
            "cost": cost, "duration": duration, "error": error}


@pytest.fixture
def day(ts, db):
    ts.save(db, trace("a1", cost=0.02, duration=1.5), started=1000.0)
    ts.save(db, trace("b1", user="bob", session="c9", cost=0.10, duration=7.0), started=1100.0)
    ts.save(db, trace("a2", session="c2", cost=0.03, duration=0.4, error=True), started=1200.0)
    ts.save(db, trace("a3", cost=0.01, duration=2.0), started=1300.0)
    return db


class TestSaveAndGet:
    def test_round_trip(self, ts, db):
        ts.save(db, trace("t1"), started=1.0)
        assert ts.get(db, "t1") == trace("t1")

    def test_missing(self, ts, db):
        assert ts.get(db, "nope") is None

    def test_searchable_columns(self, ts, db):
        ts.save(db, trace("t1", error=True, tokens=(1000, 50)), started=5.0)
        row = db.execute("SELECT user, started, tokens, error, exported FROM traces").fetchone()
        assert row == ("alice", 5.0, 1050, 1, 0)


class TestQuestions:
    def test_one_users_afternoon(self, ts, day):
        assert ts.for_user(day, "alice", 1000.0, 1250.0) == ["a1", "a2"]

    def test_the_window_includes_the_start_and_not_the_end(self, ts, day):
        assert ts.for_user(day, "alice", 1200.0, 1300.0) == ["a2"]

    def test_one_conversation(self, ts, day):
        assert ts.session(day, "alice", "c1") == ["a1", "a3"]

    def test_someone_elses_conversation_id(self, ts, day):
        assert ts.session(day, "alice", "c9") == []

    def test_costs_by_user(self, ts, day):
        assert ts.costs_by_user(day, 0.0, 2000.0) == {"alice": 0.06, "bob": 0.1}

    def test_slowest(self, ts, day):
        assert ts.slowest(day, 2) == ["b1", "a3"]

    def test_error_rate(self, ts, day):
        assert ts.error_rate(day, 0.0, 2000.0) == 0.25

    def test_an_empty_window(self, ts, day):
        assert ts.error_rate(day, 5000.0, 6000.0) == 0.0
        assert ts.costs_by_user(day, 5000.0, 6000.0) == {}

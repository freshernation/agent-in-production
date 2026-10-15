"""Week 4, Day 3 - feedback, tied to a trace.

Run me:  pytest week-04/day-3 -v
"""

import sqlite3

import pytest


@pytest.fixture
def fb(load):
    return load("feedback.py")


@pytest.fixture
def db(load, fb, tmp_path):
    ts = load("tracestore.py")
    connection = sqlite3.connect(str(tmp_path / "t.db"), isolation_level=None)
    ts.create_tables(connection)
    fb.create_tables(connection)
    for id, user, started in (("a1", "alice", 10.0), ("a2", "alice", 20.0), ("b1", "bob", 15.0)):
        ts.save(connection, {"id": id, "user": user, "session": "s", "input": "q", "output": "a",
                             "spans": [], "usage": {"input": 1, "output": 1}, "cost": 0.0,
                             "duration": 0.1, "error": False}, started=started)
    return connection


class TestRate:
    def test_thanks(self, fb, db):
        assert fb.rate(db, "alice", "a1", 1) == "Thanks."
        assert db.execute("SELECT score, comment, exported FROM feedback").fetchone() == (1, "", 0)

    def test_with_a_comment(self, fb, db):
        fb.rate(db, "alice", "a1", -1, "  It deleted the wrong note.  ")
        assert db.execute("SELECT comment FROM feedback").fetchone() == ("It deleted the wrong note.",)

    @pytest.mark.parametrize("score", [0, 2, 5, -2])
    def test_only_up_or_down(self, fb, db, score):
        with pytest.raises(ValueError):
            fb.rate(db, "alice", "a1", score)

    def test_no_such_trace(self, fb, db):
        assert fb.rate(db, "alice", "nope", 1) == "No such trace."

    def test_somebody_elses_trace(self, fb, db):
        assert fb.rate(db, "bob", "a1", -1) == "No such trace.", (
            "Bob rated Alice's answer. He must not be able to, and he must not "
            "be able to tell it exists either."
        )
        assert fb.summary(db) == {"up": 0, "down": 0}

    def test_changing_your_mind(self, fb, db):
        fb.rate(db, "alice", "a1", 1)
        db.execute("UPDATE feedback SET exported = 1")
        fb.rate(db, "alice", "a1", -1, "Actually wrong")
        assert db.execute("SELECT score, comment, exported FROM feedback").fetchone() == (
            -1, "Actually wrong", 0)


class TestReading:
    def test_summary(self, fb, db):
        fb.rate(db, "alice", "a1", 1)
        fb.rate(db, "alice", "a2", -1)
        fb.rate(db, "bob", "b1", -1)
        assert fb.summary(db) == {"up": 1, "down": 2}

    def test_bad_traces_newest_first(self, fb, db):
        fb.rate(db, "alice", "a1", -1)
        fb.rate(db, "bob", "b1", -1)
        fb.rate(db, "alice", "a2", 1)
        assert fb.bad_traces(db) == ["b1", "a1"]

    def test_nothing_rated(self, fb, db):
        assert fb.bad_traces(db) == [] and fb.summary(db) == {"up": 0, "down": 0}

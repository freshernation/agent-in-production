"""Week 6, Day 4 - a budget per user, and an incident.

Run me:  pytest week-06/day-4 -v
"""

import sqlite3

import pytest

DAY = 86400


@pytest.fixture
def budget(load):
    return load("budget.py")


@pytest.fixture
def db(load, tmp_path):
    ts = load("tracestore.py")
    connection = sqlite3.connect(str(tmp_path / "t.db"), isolation_level=None)
    ts.create_tables(connection)
    rows = (("y", "alice", 0.50, 10 * DAY - 60),      # yesterday, a minute before midnight
            ("a1", "alice", 0.30, 10 * DAY + 100),
            ("a2", "alice", 0.45, 10 * DAY + 200),
            ("b1", "bob", 2.00, 10 * DAY + 150))
    for id, user, cost, started in rows:
        ts.save(connection, {"id": id, "user": user, "session": "s", "input": "q", "output": "a",
                             "spans": [], "usage": {"input": 1, "output": 1}, "cost": cost,
                             "duration": 0.1, "error": False}, started=started)
    return connection


class TestDayStart:
    def test_midnight(self, budget):
        assert budget.day_start(10 * DAY + 3600) == 10 * DAY
        assert budget.day_start(10 * DAY) == 10 * DAY


class TestSpentToday:
    def test_only_today(self, budget, db):
        assert budget.spent_today(db, "alice", 10 * DAY + 300) == pytest.approx(0.75), (
            "Yesterday's spending was counted. The budget resets at midnight."
        )

    def test_only_theirs(self, budget, db):
        assert budget.spent_today(db, "bob", 10 * DAY + 300) == pytest.approx(2.0)

    def test_nobody(self, budget, db):
        assert budget.spent_today(db, "carol", 10 * DAY + 300) == 0.0


class TestCheckBudget:
    def test_under(self, budget, db):
        assert budget.check_budget(db, "alice", 1.0, 10 * DAY + 300) is None

    def test_over(self, budget, db):
        assert budget.check_budget(db, "bob", 1.0, 10 * DAY + 300) == (
            "You have used today's budget of $1.00. It resets at midnight UTC.")

    def test_exactly_at_the_limit_is_over(self, budget, db):
        assert budget.check_budget(db, "alice", 0.75, 10 * DAY + 300) is not None

    def test_tomorrow_is_a_new_day(self, budget, db):
        assert budget.check_budget(db, "bob", 1.0, 11 * DAY + 1) is None


class TestOvershoot:
    def test_one_turn_at_most(self, budget):
        assert budget.overshoot(50000, {"input": 2.0, "output": 10.0}) == pytest.approx(0.5)


class TestTheIncident:
    def test_written(self, source):
        text = source("INCIDENT.md")
        assert "<!--" not in text, "Delete the instructions comment in INCIDENT.md."
        assert "<one line" not in text, "Give the incident a title."
        for heading in ("What users saw", "Timeline", "Why it happened", "How we found out",
                        "What we changed"):
            assert f"## {heading}" in text, f"INCIDENT.md has no '{heading}' section."
            part = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
            assert len(part.split()) >= 40, f"'{heading}' is {len(part.split())} words."

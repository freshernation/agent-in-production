"""Week 6, Day 1 - alerts.

Run me:  pytest week-06/day-1 -v
"""

import sqlite3

import pytest


@pytest.fixture
def alerts(load):
    return load("alerts.py")


@pytest.fixture
def db(load, tmp_path):
    ts = load("tracestore.py")
    connection = sqlite3.connect(str(tmp_path / "t.db"), isolation_level=None)
    ts.create_tables(connection)
    durations = [0.5, 1.0, 1.2, 0.8, 9.0, 1.1, 0.9, 1.0, 1.3, 0.7]
    for number, duration in enumerate(durations):
        ts.save(connection, {"id": f"t{number}", "user": "alice", "session": "s", "input": "q",
                             "output": "a", "spans": [], "usage": {"input": 1, "output": 1},
                             "cost": 0.01, "duration": duration, "error": number in (4, 7)},
                started=1000.0 + number)
    return connection


class TestPercentile:
    def test_nearest_rank(self, alerts):
        assert alerts.percentile([1, 2, 3, 4], 50) == 2
        assert alerts.percentile([1, 2, 3, 4], 95) == 4
        assert alerts.percentile([4, 1, 3, 2], 25) == 1

    def test_nothing(self, alerts):
        assert alerts.percentile([], 95) == 0.0


class TestMeasure:
    def test_a_window(self, alerts, db):
        assert alerts.measure(db, 1000.0, 1010.0) == {
            "requests": 10, "error_rate": 0.2, "p95_seconds": 9.0, "cost": 0.1}

    def test_an_empty_window(self, alerts, db):
        assert alerts.measure(db, 0.0, 10.0) == {
            "requests": 0, "error_rate": 0.0, "p95_seconds": 0.0, "cost": 0.0}


RULES = [
    {"name": "errors", "metric": "error_rate", "above": 0.05, "min_requests": 5},
    {"name": "slow", "metric": "p95_seconds", "above": 8.0},
    {"name": "spend", "metric": "cost", "above": 5.0},
]


class TestFiring:
    def test_two_of_three(self, alerts):
        measured = {"requests": 10, "error_rate": 0.2, "p95_seconds": 9.0, "cost": 0.1}
        assert alerts.firing(RULES, measured) == ["errors", "slow"]

    def test_too_few_requests_to_mean_anything(self, alerts):
        measured = {"requests": 2, "error_rate": 0.5, "p95_seconds": 1.0, "cost": 0.0}
        assert alerts.firing(RULES, measured) == [], (
            "One failure in two requests is 50% - and is not worth waking "
            "anybody. That is what min_requests is for."
        )

    def test_exactly_on_the_line_is_not_above(self, alerts):
        measured = {"requests": 10, "error_rate": 0.05, "p95_seconds": 8.0, "cost": 5.0}
        assert alerts.firing(RULES, measured) == []


class TestPager:
    def test_sends(self, alerts):
        sent = []
        pager = alerts.Pager(sent.append, cooldown=600)
        assert pager.alert("errors", "error rate 20%", now=0.0) is True
        assert sent == ["[errors] error rate 20%"]

    def test_does_not_repeat_within_the_cooldown(self, alerts):
        sent = []
        pager = alerts.Pager(sent.append, cooldown=600)
        pager.alert("errors", "x", now=0.0)
        assert pager.alert("errors", "x", now=300.0) is False
        assert pager.alert("errors", "x", now=601.0) is True
        assert len(sent) == 2

    def test_different_alerts_are_separate(self, alerts):
        sent = []
        pager = alerts.Pager(sent.append, cooldown=600)
        pager.alert("errors", "x", now=0.0)
        assert pager.alert("slow", "y", now=1.0) is True

    def test_resolve_resets_it(self, alerts):
        sent = []
        pager = alerts.Pager(sent.append, cooldown=600)
        pager.alert("errors", "x", now=0.0)
        pager.resolve("errors")
        assert pager.alert("errors", "x", now=10.0) is True

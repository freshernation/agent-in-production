"""Week 8, Day 3 - cost against performance.

Run me:  pytest week-08/day-3 -v

There is no code this week. The tests check that the document is finished;
whether it is any good is Friday's question.
"""

import pytest

HEADINGS = ["The numbers", "Trade-offs taken", "The next bottleneck"]


def section(text, heading):
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


class TestTheDocument:
    def test_finished(self, source):
        text = source("COSTS.md")
        assert "<!--" not in text, "Delete the instructions comment in COSTS.md."

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_sections(self, source, heading):
        text = source("COSTS.md")
        assert f"## {heading}" in text, f"COSTS.md has no '{heading}' section."
        words = len(section(text, heading).split())
        assert words >= 40, f"'{heading}' is {words} words."

    def test_real_numbers(self, source):
        numbers = section(source("COSTS.md"), "The numbers")
        assert "$" in numbers, "No dollar figure in 'The numbers'."
        assert "95" in numbers, "No 95th percentile in 'The numbers'."


class TestTheGivenScript:
    def test_summarise(self, load, tmp_path):
        import sqlite3
        numbers = load("numbers.py")
        db = sqlite3.connect(str(tmp_path / "t.db"))
        db.execute("CREATE TABLE traces (user TEXT, started REAL, duration REAL, cost REAL, "
                   "tokens INTEGER, error INTEGER)")
        db.executemany("INSERT INTO traces VALUES (?, ?, ?, ?, ?, ?)", [
            ("alice", 100.0, 1.0, 0.01, 1000, 0), ("alice", 200.0, 3.0, 0.03, 3000, 1),
            ("bob", 86500.0, 2.0, 0.02, 2000, 0)])
        result = numbers.summarise(db)
        assert result["requests"] == 3 and result["days"] == 2
        assert result["p95_seconds"] == 3.0 and result["error_rate"] == 0.333
        assert result["most_one_user_spent_in_a_day"] == 0.04
        assert result["cost_per_day"] == 0.03

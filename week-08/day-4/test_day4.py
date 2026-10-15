"""Week 8, Day 4 - the demo, rehearsed.

Run me:  pytest week-08/day-4 -v

There is no code this week. The tests check that the document is finished;
whether it is any good is Friday's question.
"""

import pytest

HEADINGS = ["The story", "The steps", "What I will break live", "If it goes wrong"]


def section(text, heading):
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


class TestTheDocument:
    def test_finished(self, source):
        text = source("DEMO.md")
        assert "<!--" not in text, "Delete the instructions comment in DEMO.md."

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_sections(self, source, heading):
        text = source("DEMO.md")
        assert f"## {heading}" in text, f"DEMO.md has no '{heading}' section."
        words = len(section(text, heading).split())
        assert words >= 40, f"'{heading}' is {words} words."

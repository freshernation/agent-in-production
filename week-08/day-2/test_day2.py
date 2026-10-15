"""Week 8, Day 2 - the production review.

Run me:  pytest week-08/day-2 -v

There is no code this week. The tests check that the document is finished;
whether it is any good is Friday's question.
"""

import pytest

HEADINGS = ["Threat model", "Failure modes", "What still gets through", "What I would fix first"]


def section(text, heading):
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


class TestTheDocument:
    def test_finished(self, source):
        text = source("PRODUCTION_REVIEW.md")
        assert "<!--" not in text, "Delete the instructions comment in PRODUCTION_REVIEW.md."

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_sections(self, source, heading):
        text = source("PRODUCTION_REVIEW.md")
        assert f"## {heading}" in text, f"PRODUCTION_REVIEW.md has no '{heading}' section."
        words = len(section(text, heading).split())
        assert words >= 40, f"'{heading}' is {words} words."

"""Week 8, Day 1 - the architecture document.

Run me:  pytest week-08/day-1 -v

There is no code this week. The tests check that the document is finished;
whether it is any good is Friday's question.
"""

import pytest

HEADINGS = ["What it is", "The picture", "The parts", "Decisions", "What was cut"]


def section(text, heading):
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


class TestTheDocument:
    def test_finished(self, source):
        text = source("ARCHITECTURE.md")
        assert "<!--" not in text, "Delete the instructions comment in ARCHITECTURE.md."

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_sections(self, source, heading):
        text = source("ARCHITECTURE.md")
        assert f"## {heading}" in text, f"ARCHITECTURE.md has no '{heading}' section."
        words = len(section(text, heading).split())
        assert words >= 40, f"'{heading}' is {words} words."

    def test_a_picture(self, source):
        assert "```" in section(source("ARCHITECTURE.md"), "The picture"), (
            "The picture is a diagram in a code block."
        )

    def test_three_decisions(self, source):
        decisions = section(source("ARCHITECTURE.md"), "Decisions").count("\n### ")
        assert decisions >= 3, f"{decisions} decisions. Every system has at least three worth explaining."

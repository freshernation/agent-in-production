"""Week 8 milestone - Project 2.

Run me:  pytest week-08/milestone -v

The documents, finished and together. The project itself is your live URL and
your repository, and Friday is where it is checked.
"""

import re

import pytest

DOCUMENTS = {
    "ARCHITECTURE.md": ["What it is", "The picture", "The parts", "Decisions", "What was cut"],
    "PRODUCTION_REVIEW.md": ["Threat model", "Failure modes", "What still gets through",
                             "What I would fix first"],
    "COSTS.md": ["The numbers", "Trade-offs taken", "The next bottleneck"],
    "DEMO.md": ["The story", "The steps", "What I will break live", "If it goes wrong"],
    "PROJECT_README.md": ["What it is", "Try it", "How it is built", "How I know it works",
                          "Since Project 1"],
}


def section(text, heading):
    return text.split(f"## {heading}", 1)[1].split("\n## ")[0]


@pytest.mark.parametrize("name", DOCUMENTS)
def test_finished(source, name):
    text = source(name)
    assert "<!--" not in text, f"Delete the instructions comment in {name}."
    for heading in DOCUMENTS[name]:
        assert f"## {heading}" in text, f"{name} has no '{heading}' section."
        words = len(section(text, heading).split())
        assert words >= 30, f"{name} '{heading}' is {words} words."


def test_the_live_url(source):
    assert re.search(r"https://", section(source("PROJECT_README.md"), "Try it"))


def test_the_review_uses_numbers(source):
    review = section(source("PRODUCTION_REVIEW.md"), "What still gets through")
    assert re.search(r"\d", review), "'What still gets through' has no numbers in it."

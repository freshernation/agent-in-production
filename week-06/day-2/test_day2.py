"""Week 6, Day 2 - when the model is down.

Run me:  pytest week-06/day-2 -v
"""

import pytest

from llm import FakeModel, ModelError, say

HI = [{"role": "user", "content": "hi"}]


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


@pytest.fixture
def fb(load):
    return load("fallback.py")


class TestDownMessage:
    def test_says_nothing_was_done(self, fb):
        assert len(fb.DOWN_MESSAGE.split()) >= 15
        assert "nothing" in fb.DOWN_MESSAGE.lower()


class TestBreaker:
    def test_starts_closed(self, fb):
        breaker = fb.Breaker(3, 60, Clock())
        assert breaker.state == "closed" and breaker.allows()

    def test_opens_after_the_threshold(self, fb):
        breaker = fb.Breaker(3, 60, Clock())
        breaker.failed()
        breaker.failed()
        assert breaker.state == "closed"
        breaker.failed()
        assert breaker.state == "open" and not breaker.allows()

    def test_a_success_resets_the_count(self, fb):
        breaker = fb.Breaker(3, 60, Clock())
        breaker.failed()
        breaker.failed()
        breaker.succeeded()
        breaker.failed()
        assert breaker.state == "closed"

    def test_half_open_after_the_cooldown(self, fb):
        clock = Clock()
        breaker = fb.Breaker(1, 60, clock)
        breaker.failed()
        clock.now = 59
        assert breaker.state == "open"
        clock.now = 60
        assert breaker.state == "half-open" and breaker.allows()

    def test_a_failed_trial_opens_it_again(self, fb):
        clock = Clock()
        breaker = fb.Breaker(3, 60, clock)
        for _ in range(3):
            breaker.failed()
        clock.now = 61
        breaker.failed()
        assert breaker.state == "open", (
            "The one trial call failed and the breaker stayed half-open, so "
            "every request now hits the broken provider again."
        )

    def test_a_good_trial_closes_it(self, fb):
        clock = Clock()
        breaker = fb.Breaker(1, 60, clock)
        breaker.failed()
        clock.now = 61
        breaker.succeeded()
        assert breaker.state == "closed"


class TestFallbackModel:
    def test_primary_when_it_works(self, fb):
        model = fb.FallbackModel(FakeModel([say("from primary")]), FakeModel([]), fb.Breaker(3, 60, Clock()))
        assert model.chat(HI)["text"] == "from primary"
        assert model.last_served == "primary"

    def test_secondary_when_primary_fails(self, fb):
        model = fb.FallbackModel(FakeModel([ModelError("down")]), FakeModel([say("from secondary")]),
                                 fb.Breaker(3, 60, Clock()))
        assert model.chat(HI)["text"] == "from secondary"
        assert model.last_served == "secondary"

    def test_an_open_breaker_skips_the_primary(self, fb):
        primary = FakeModel([ModelError("down")] * 5)
        model = fb.FallbackModel(primary, FakeModel(say("backup")), fb.Breaker(2, 60, Clock()))
        for _ in range(5):
            model.chat(HI)
        assert primary.call_count == 2, (
            f"The broken primary was tried {primary.call_count} times. After two "
            "failures the breaker opens and stops sending traffic to it."
        )

    def test_both_down_raises(self, fb):
        model = fb.FallbackModel(FakeModel([ModelError("a")]), FakeModel([ModelError("b")]),
                                 fb.Breaker(3, 60, Clock()))
        with pytest.raises(ModelError):
            model.chat(HI)

    def test_passes_everything_on(self, fb):
        secondary = FakeModel([say("ok")])
        model = fb.FallbackModel(FakeModel([ModelError("down")]), secondary, fb.Breaker(3, 60, Clock()))
        model.chat(HI, system="Be brief.", tools=None)
        assert secondary.last_request["system"] == "Be brief."

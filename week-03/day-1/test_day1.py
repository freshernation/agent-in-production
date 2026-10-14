"""Week 3, Day 1 - what blocks.

Run me:  pytest week-03/day-1 -v
"""

import inspect

import pytest

DELAYS = [0.1, 0.1, 0.1]


@pytest.fixture
def mod(load):
    return load("concurrency.py")


class TestTheLookups:
    def test_slow_lookup_is_async(self, mod):
        assert inspect.iscoroutinefunction(mod.slow_lookup)

    def test_blocking_lookup_is_not(self, mod):
        assert not inspect.iscoroutinefunction(mod.blocking_lookup)
        assert mod.blocking_lookup(0) == "waited 0"


class TestRunAll:
    def test_results_in_order(self, mod):
        result, _ = mod.timed(mod.run_all([0.05, 0.01, 0.03]))
        assert result == ["waited 0.05", "waited 0.01", "waited 0.03"]

    def test_at_once(self, mod):
        _, seconds = mod.timed(mod.run_all(DELAYS))
        assert seconds < 0.25, (
            f"Three 0.1s waits took {seconds:.2f}s. gather runs them together."
        )


class TestBlocking:
    def test_the_wrong_way_takes_the_sum(self, mod):
        result, seconds = mod.timed(mod.run_blocking_wrong(DELAYS))
        assert result == ["waited 0.1"] * 3
        assert seconds >= 0.28, (
            "This one is meant to be slow. A blocking call inside an async "
            "function stops everything else until it returns - which is the "
            "whole lesson."
        )

    def test_the_right_way_takes_the_longest(self, mod):
        result, seconds = mod.timed(mod.run_blocking_right(DELAYS))
        assert result == ["waited 0.1"] * 3
        assert seconds < 0.25, (
            f"{seconds:.2f}s. Wrap each blocking call in asyncio.to_thread, then gather."
        )

    def test_they_are_all_coroutines(self, mod):
        for name in ("run_all", "run_blocking_wrong", "run_blocking_right"):
            assert inspect.iscoroutinefunction(getattr(mod, name)), name

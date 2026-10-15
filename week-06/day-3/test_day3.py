"""Week 6, Day 3 - caching.

Run me:  pytest week-06/day-3 -v
"""

import pytest


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


@pytest.fixture
def caching(load):
    return load("caching.py")


REQUEST = {"model": "claude-sonnet-5-5", "max_tokens": 1000, "system": "You are Desk.",
           "messages": [{"role": "user", "content": "hi"}]}


class TestMarkForCaching:
    def test_marks_the_system_prompt(self, caching):
        marked = caching.mark_for_caching(REQUEST)
        assert marked["system"] == [{"type": "text", "text": "You are Desk.",
                                     "cache_control": {"type": "ephemeral"}}]
        assert marked["messages"] == REQUEST["messages"]

    def test_leaves_the_original_alone(self, caching):
        caching.mark_for_caching(REQUEST)
        assert REQUEST["system"] == "You are Desk."

    def test_no_system_prompt(self, caching):
        request = {"model": "m", "messages": []}
        assert caching.mark_for_caching(request) == request


class TestCacheCost:
    PRICE = {"input": 2.0, "cache_write": 2.5, "cache_read": 0.1, "output": 10.0}   # Sonnet 5.5

    def test_plain(self, caching):
        assert caching.cache_cost({"input": 1_000_000, "output": 0}, self.PRICE) == pytest.approx(2.0)

    def test_a_write_costs_more(self, caching):
        usage = {"input": 0, "output": 0, "cache_write": 1_000_000}
        assert caching.cache_cost(usage, self.PRICE) == pytest.approx(2.5)

    def test_a_read_costs_a_twentieth_here(self, caching):
        usage = {"input": 0, "output": 0, "cache_read": 1_000_000}
        assert caching.cache_cost(usage, self.PRICE) == pytest.approx(0.1)

    def test_together(self, caching):
        usage = {"input": 100, "output": 200, "cache_read": 5000}
        assert caching.cache_cost(usage, self.PRICE) == pytest.approx((200 + 2000 + 500) / 1e6)


def trace(spans, error=False):
    return {"error": error, "spans": spans}


class TestCacheable:
    def test_a_plain_answer(self, caching):
        assert caching.cacheable(trace([{"type": "generation"}])) is True

    def test_not_after_a_tool(self, caching):
        assert caching.cacheable(trace([{"type": "generation"}, {"type": "tool"}])) is False, (
            "A tool ran. Its answer depended on the notes at that moment - cache "
            "it and the next person is told yesterday's count."
        )

    def test_not_a_failure(self, caching):
        assert caching.cacheable(trace([], error=True)) is False


class TestCacheKey:
    def test_same_question_same_key(self, caching):
        assert caching.cache_key("alice", "What  is Desk?") == caching.cache_key("alice", "what is desk?")

    def test_who_asked_matters(self, caching):
        assert caching.cache_key("alice", "what are my notes?") != caching.cache_key("bob", "what are my notes?")

    def test_it_is_a_digest(self, caching):
        assert len(caching.cache_key("alice", "x")) == 64


class TestResponseCache:
    def test_miss_then_hit(self, caching):
        cache = caching.ResponseCache(60, Clock())
        assert cache.get("alice", "hi") is None
        cache.put("alice", "hi", {"reply": "Hello."})
        assert cache.get("alice", "Hi") == {"reply": "Hello."}

    def test_another_user_gets_nothing(self, caching):
        cache = caching.ResponseCache(60, Clock())
        cache.put("alice", "what did I write?", {"reply": "Your note about the bank."})
        assert cache.get("bob", "what did I write?") is None, (
            "Bob was served Alice's cached answer. A response cache that does "
            "not know who asked is a data leak with good latency."
        )

    def test_expires(self, caching):
        clock = Clock()
        cache = caching.ResponseCache(60, clock)
        cache.put("alice", "hi", {"reply": "Hello."})
        clock.now = 59
        assert cache.get("alice", "hi") is not None
        clock.now = 60
        assert cache.get("alice", "hi") is None

"""Week 3, Day 4 - rate limits and streaming.

Run me:  pytest week-03/day-4 -v
"""

import inspect

import pytest
from fastapi.testclient import TestClient


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


@pytest.fixture
def limits(load):
    return load("limits.py")


class TestBucket:
    def test_starts_full(self, limits):
        bucket = limits.Bucket(3, 1, Clock())
        assert [bucket.take(), bucket.take(), bucket.take(), bucket.take()] == [True, True, True, False]

    def test_refills_over_time(self, limits):
        clock = Clock()
        bucket = limits.Bucket(2, 1, clock)
        bucket.take()
        bucket.take()
        assert bucket.take() is False
        clock.now += 1
        assert bucket.take() is True

    def test_never_holds_more_than_its_capacity(self, limits):
        clock = Clock()
        bucket = limits.Bucket(2, 1, clock)
        clock.now += 3600
        results = []
        for _ in range(3):
            results.append(bucket.take())
        assert results == [True, True, False], (
            "An hour of quiet bought a thousand requests at once. A bucket "
            "refills up to its capacity and no further."
        )

    def test_wait_time(self, limits):
        clock = Clock()
        bucket = limits.Bucket(1, 0.5, clock)
        assert bucket.wait_time() == 0.0
        bucket.take()
        assert bucket.wait_time() == pytest.approx(2.0)
        clock.now += 1.5
        assert bucket.wait_time() == pytest.approx(0.5)


class TestLimiter:
    def test_one_bucket_per_caller(self, limits):
        limiter = limits.Limiter(1, 0.1, Clock())
        assert limiter.allow("alice") is True
        assert limiter.allow("alice") is False
        assert limiter.allow("bob") is True, (
            "Alice used up Bob's allowance. One bucket per caller is the point."
        )

    def test_retry_after_rounds_up(self, limits):
        clock = Clock()
        limiter = limits.Limiter(1, 0.4, clock)
        limiter.allow("alice")
        assert limiter.retry_after("alice") == 3
        clock.now += 2.4
        assert limiter.retry_after("alice") == 1

    def test_retry_after_is_never_zero(self, limits):
        limiter = limits.Limiter(5, 1, Clock())
        assert limiter.retry_after("new") == 1


class TestChunks:
    def test_is_a_generator(self, limits):
        assert inspect.isgeneratorfunction(limits.chunks), "Use yield."

    def test_pieces(self, limits):
        assert list(limits.chunks("hello world", 4)) == ["hell", "o wo", "rld"]

    def test_nothing(self, limits):
        assert list(limits.chunks("", 4)) == []


class TestTheApp:
    def test_429_with_retry_after(self, limits):
        client = TestClient(limits.create_app(limits.Limiter(2, 0.5, Clock())))
        codes = []
        for _ in range(3):
            codes.append(client.post("/ping", headers={"X-Caller": "alice"}).status_code)
        assert codes == [200, 200, 429]
        response = client.post("/ping", headers={"X-Caller": "alice"})
        assert response.headers.get("retry-after") == "2"
        assert "slow down" in response.json()["detail"].lower()

    def test_another_caller_is_unaffected(self, limits):
        client = TestClient(limits.create_app(limits.Limiter(1, 0.1, Clock())))
        client.post("/ping", headers={"X-Caller": "alice"})
        assert client.post("/ping", headers={"X-Caller": "bob"}).status_code == 200

    def test_stream(self, limits):
        client = TestClient(limits.create_app(limits.Limiter(1, 1, Clock())))
        with client.stream("GET", "/stream", params={"text": "hello world", "size": 4}) as response:
            pieces = list(response.iter_text())
        assert "".join(pieces) == "hello world"
        assert response.headers["content-type"].startswith("text/plain")

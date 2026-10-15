"""Week 5, Day 4 - a gated deploy, and the way back.

Run me:  pytest week-05/day-4 -v
"""

import pytest


@pytest.fixture
def release(load):
    return load("release.py")


def results(*passed):
    out = []
    for number, ok in enumerate(passed):
        out.append({"name": ["tests", "evals", "attacks"][number], "passed": ok,
                    "code": 0 if ok else 1, "seconds": 1.0})
    return out


class TestShouldDeploy:
    def test_all_green_on_main(self, release):
        assert release.should_deploy(results(True, True, True), "main") == (
            True, "All checks passed on main.")

    def test_a_failure_names_what_failed(self, release):
        assert release.should_deploy(results(True, False, False), "main") == (
            False, "Checks failed: evals, attacks.")

    def test_a_branch_is_not_deployed(self, release):
        assert release.should_deploy(results(True, True, True), "try-cache") == (
            False, "Only main is deployed; this is try-cache.")

    def test_no_checks_is_not_a_pass(self, release):
        ok, reason = release.should_deploy([], "main")
        assert ok is False and reason == "No checks ran.", (
            "Nothing ran and it would have deployed. A gate with no checks is "
            "an open door with a sign on it."
        )


HISTORY = [
    {"version": "1.2.0", "status": "healthy", "at": 1.0},
    {"version": "1.3.0", "status": "healthy", "at": 2.0},
    {"version": "1.4.0", "status": "deployed", "at": 3.0},
]


class TestHistory:
    def test_record(self, release):
        updated = release.record(HISTORY, "1.4.0", "failed", 4.0)
        assert updated[-1] == {"version": "1.4.0", "status": "failed", "at": 4.0}
        assert len(HISTORY) == 3

    def test_unknown_status(self, release):
        with pytest.raises(ValueError):
            release.record(HISTORY, "1.5.0", "great", 5.0)

    def test_current(self, release):
        assert release.current(HISTORY) == "1.4.0"
        assert release.current([]) is None

    def test_rollback_target(self, release):
        assert release.rollback_target(HISTORY) == "1.3.0"

    def test_after_a_failure_and_a_rollback(self, release):
        history = release.record(HISTORY, "1.4.0", "failed", 4.0)
        history = release.record(history, "1.3.0", "deployed", 5.0)
        assert release.current(history) == "1.3.0"
        assert release.rollback_target(history) == "1.2.0"

    def test_nothing_to_go_back_to(self, release):
        assert release.rollback_target([{"version": "1.0.0", "status": "deployed", "at": 1.0}]) is None


def site(health_status=200, version="1.4.0", chat_status=401):
    calls = []

    def fetch(method, url, headers):
        calls.append((method, url, headers))
        if url.endswith("/health"):
            return health_status, {"status": "ok", "version": version}
        return chat_status, {}

    return fetch, calls


class TestVerifyRelease:
    def test_healthy(self, release):
        fetch, calls = site()
        assert release.verify_release(fetch, "https://desk.example", "1.4.0") == {
            "healthy": True, "problems": []}
        assert calls[1] == ("POST", "https://desk.example/chat", {})

    def test_still_serving_the_old_version(self, release):
        fetch, _ = site(version="1.3.0")
        result = release.verify_release(fetch, "https://desk.example", "1.4.0")
        assert result["problems"] == ["/health reports version '1.3.0', expected '1.4.0'"]

    def test_down(self, release):
        fetch, _ = site(health_status=502)
        assert release.verify_release(fetch, "https://d", "1.4.0")["problems"][0] == "/health answered 502"

    def test_the_door_is_open(self, release):
        fetch, _ = site(chat_status=200)
        result = release.verify_release(fetch, "https://d", "1.4.0")
        assert result == {"healthy": False, "problems": ["/chat without a key answered 200, not 401"]}

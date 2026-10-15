"""Week 5, Day 2 - one command that says yes or no.

Run me:  pytest week-05/day-2 -v
"""

import sys

import pytest


class Done:
    def __init__(self, code):
        self.returncode = code


def runner_with(codes):
    seen = []

    def run(command):
        seen.append(command)
        return Done(codes[len(seen) - 1])

    return run, seen


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        self.now += 1.25
        return self.now


@pytest.fixture
def checks(load):
    return load("checks.py")


class TestTheList:
    def test_three_in_order(self, checks):
        names = []
        for name, command in checks.CHECKS:
            names.append(name)
            assert command[0] == sys.executable
        assert names == ["tests", "smoke"]


class TestRunCheck:
    def test_passing(self, checks):
        run, seen = runner_with([0])
        result = checks.run_check("tests", ["pytest"], run, Clock())
        assert result == {"name": "tests", "passed": True, "code": 0, "seconds": 1.2}
        assert seen == [["pytest"]]

    def test_failing(self, checks):
        run, _ = runner_with([1])
        assert checks.run_check("evals", ["x"], run, Clock())["passed"] is False

    def test_a_missing_command(self, checks):
        def run(command):
            raise FileNotFoundError(command[0])
        result = checks.run_check("attacks", ["nope"], run, Clock())
        assert result["code"] == 127 and result["passed"] is False


class TestRunAll:
    def test_keeps_going_after_a_failure(self, checks):
        run, seen = runner_with([0, 1, 0])
        results = checks.run_all([("a", ["a"]), ("b", ["b"]), ("c", ["c"])], run, Clock())
        assert len(seen) == 3, (
            "It stopped at the first failure. Run every check, so one push shows "
            "everything that is wrong."
        )
        passed = []
        for result in results:
            passed.append(result["passed"])
        assert passed == [True, False, True]


class TestSummary:
    def test_lines(self, checks):
        results = [
            {"name": "tests", "passed": True, "code": 0, "seconds": 12.3},
            {"name": "evals", "passed": False, "code": 1, "seconds": 40.1},
            {"name": "attacks", "passed": True, "code": 0, "seconds": 8.0},
        ]
        assert checks.summary(results) == (
            "PASS tests (12.3s)\nFAIL evals (exit 1, 40.1s)\nPASS attacks (8.0s)\n2/3 passed")

    def test_exit_code(self, checks):
        good = [{"passed": True}, {"passed": True}]
        assert checks.exit_code(good) == 0
        assert checks.exit_code(good + [{"passed": False}]) == 1
        assert checks.exit_code([]) == 0


class TestTheWorkflow:
    def body(self, source):
        lines = []
        for line in source("ci.yml").splitlines():
            if line.strip() and not line.strip().startswith("#"):
                lines.append(line)
        assert lines, "ci.yml contains only comments so far - write it."
        return "\n".join(lines)

    def test_runs_on_push_and_pull_request(self, source):
        text = self.body(source)
        assert "push" in text and "pull_request" in text

    def test_installs_and_runs_the_checks(self, source):
        text = self.body(source)
        assert "pip install -r requirements.txt" in text
        assert "checks.py" in text
        assert "3.12" in text

    def test_a_failure_fails_the_run(self, source):
        assert "continue-on-error" not in self.body(source)

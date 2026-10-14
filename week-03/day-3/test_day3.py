"""Week 3, Day 3 - a worker, and a worker that dies.

Run me:  pytest week-03/day-3 -v
"""

import sqlite3

import pytest


@pytest.fixture
def jobs(load):
    return load("jobs.py")


@pytest.fixture
def worker(load):
    return load("worker.py")


@pytest.fixture
def db(jobs, tmp_path):
    connection = sqlite3.connect(str(tmp_path / "jobs.db"), isolation_level=None)
    jobs.create_tables(connection)
    return connection


def shout(payload):
    return payload["text"].upper()


def explode(payload):
    raise RuntimeError("model overloaded")


class TestRunOnce:
    def test_idle(self, worker, db):
        assert worker.run_once(db, {"shout": shout}, "w", now=1.0) == "idle"

    def test_done(self, jobs, worker, db):
        job_id = jobs.enqueue(db, "shout", {"text": "hi"}, now=1.0)
        assert worker.run_once(db, {"shout": shout}, "w", now=2.0) == "done"
        assert jobs.get(db, job_id)["result"] == "HI"

    def test_a_failure_is_recorded_and_retried(self, jobs, worker, db):
        job_id = jobs.enqueue(db, "boom", {}, now=1.0)
        assert worker.run_once(db, {"boom": explode}, "w", now=2.0) == "failed"
        job = jobs.get(db, job_id)
        assert job["status"] == "queued"
        assert job["error"] == "RuntimeError: model overloaded"

    def test_it_gives_up_after_max_attempts(self, jobs, worker, db):
        job_id = jobs.enqueue(db, "boom", {}, now=1.0)
        for _ in range(3):
            worker.run_once(db, {"boom": explode}, "w", now=2.0)
        assert jobs.get(db, job_id)["status"] == "dead"
        assert worker.run_once(db, {"boom": explode}, "w", now=3.0) == "idle"

    def test_an_unknown_kind_dies_at_once(self, jobs, worker, db):
        job_id = jobs.enqueue(db, "mystery", {}, now=1.0)
        assert worker.run_once(db, {"shout": shout}, "w", now=2.0) == "failed"
        job = jobs.get(db, job_id)
        assert job["status"] == "dead"
        assert job["error"] == "No handler for 'mystery'."

    def test_a_failure_does_not_crash_the_worker(self, jobs, worker, db):
        jobs.enqueue(db, "boom", {}, now=1.0)
        jobs.enqueue(db, "shout", {"text": "next"}, now=1.0)
        worker.run_once(db, {"boom": explode, "shout": shout}, "w", now=2.0, max_attempts=1)
        assert worker.run_once(db, {"boom": explode, "shout": shout}, "w", now=2.0) == "done"


class TestStale:
    def test_a_dead_workers_job_goes_back(self, jobs, worker, db):
        job_id = jobs.enqueue(db, "shout", {"text": "hi"}, now=1.0)
        jobs.claim(db, "crashed", now=10.0)
        assert worker.requeue_stale(db, now=100.0, timeout=60.0) == 1
        job = jobs.get(db, job_id)
        assert job["status"] == "queued" and job["claimed_by"] is None
        assert job["error"] == "worker stopped responding"
        assert job["attempts"] == 1

    def test_a_busy_workers_job_is_left_alone(self, jobs, worker, db):
        jobs.enqueue(db, "shout", {"text": "hi"}, now=1.0)
        jobs.claim(db, "busy", now=90.0)
        assert worker.requeue_stale(db, now=100.0, timeout=60.0) == 0

    def test_finished_jobs_are_left_alone(self, jobs, worker, db):
        jobs.enqueue(db, "shout", {"text": "hi"}, now=1.0)
        worker.run_once(db, {"shout": shout}, "w", now=2.0)
        assert worker.requeue_stale(db, now=1000.0, timeout=60.0) == 0

    def test_the_requeued_job_finishes(self, jobs, worker, db):
        job_id = jobs.enqueue(db, "shout", {"text": "hi"}, now=1.0)
        jobs.claim(db, "crashed", now=10.0)
        worker.requeue_stale(db, now=100.0, timeout=60.0)
        assert worker.run_once(db, {"shout": shout}, "w2", now=101.0) == "done"
        assert jobs.get(db, job_id)["attempts"] == 2


class TestOnce:
    def test_runs_the_first_time(self, worker, db):
        calls = []

        def send():
            calls.append(1)
            return "sent"

        assert worker.once(db, "share:job-7", send) == "sent"
        assert calls == [1]

    def test_never_runs_twice(self, worker, db):
        calls = []

        def send():
            calls.append(1)
            return "sent"

        worker.once(db, "share:job-7", send)
        assert worker.once(db, "share:job-7", send) == "sent"
        assert calls == [1], (
            "The share ran twice. A job can run twice - a worker can do the work "
            "and die before calling finish - so anything that leaves must be "
            "guarded by a key."
        )

    def test_different_keys_run_separately(self, worker, db):
        assert worker.once(db, "a", lambda: "first") == "first"
        assert worker.once(db, "b", lambda: "second") == "second"

    def test_results_keep_their_type(self, worker, db):
        worker.once(db, "n", lambda: {"count": 3})
        assert worker.once(db, "n", lambda: None) == {"count": 3}

    def test_it_survives_a_new_connection(self, worker, db, tmp_path):
        worker.once(db, "k", lambda: "done")
        other = sqlite3.connect(str(tmp_path / "jobs.db"), isolation_level=None)
        calls = []
        worker.once(other, "k", lambda: calls.append(1))
        assert calls == []

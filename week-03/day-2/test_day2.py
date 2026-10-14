"""Week 3, Day 2 - a job queue is a table.

Run me:  pytest week-03/day-2 -v
"""

import sqlite3
import threading

import pytest


@pytest.fixture
def jobs(load):
    return load("jobs.py")


def connect(path):
    db = sqlite3.connect(path, isolation_level=None, check_same_thread=False)
    db.execute("PRAGMA busy_timeout = 5000")
    return db


@pytest.fixture
def path(tmp_path):
    return str(tmp_path / "jobs.db")


@pytest.fixture
def db(jobs, path):
    connection = connect(path)
    jobs.create_tables(connection)
    return connection


class TestEnqueue:
    def test_returns_an_id(self, jobs, db):
        first = jobs.enqueue(db, "chat", {"message": "hi"}, now=100.0)
        second = jobs.enqueue(db, "chat", {"message": "again"}, now=101.0)
        assert isinstance(first, int) and second != first

    def test_a_new_job(self, jobs, db):
        job = jobs.get(db, jobs.enqueue(db, "chat", {"message": "hi"}, now=100.0))
        assert job["status"] == "queued"
        assert job["payload"] == {"message": "hi"}
        assert job["attempts"] == 0
        assert job["created_at"] == 100.0

    def test_no_such_job(self, jobs, db):
        assert jobs.get(db, 999) is None


class TestClaim:
    def test_takes_the_oldest(self, jobs, db):
        first = jobs.enqueue(db, "chat", {"n": 1}, now=1.0)
        jobs.enqueue(db, "chat", {"n": 2}, now=2.0)
        job = jobs.claim(db, "worker-a", now=10.0)
        assert job["id"] == first
        assert job["status"] == "running"
        assert job["claimed_by"] == "worker-a"
        assert job["claimed_at"] == 10.0
        assert job["attempts"] == 1

    def test_nothing_queued(self, jobs, db):
        assert jobs.claim(db, "worker-a", now=1.0) is None

    def test_a_claimed_job_is_not_claimed_again(self, jobs, db):
        jobs.enqueue(db, "chat", {}, now=1.0)
        jobs.claim(db, "a", now=2.0)
        assert jobs.claim(db, "b", now=3.0) is None

    def test_two_connections_two_jobs(self, jobs, db, path):
        jobs.enqueue(db, "chat", {"n": 1}, now=1.0)
        jobs.enqueue(db, "chat", {"n": 2}, now=2.0)
        other = connect(path)
        a, b = jobs.claim(db, "a", now=3.0), jobs.claim(other, "b", now=3.0)
        assert a["id"] != b["id"]


class TestManyWorkersAtOnce:
    def test_no_job_is_ever_taken_twice(self, jobs, db, path):
        for number in range(60):
            jobs.enqueue(db, "chat", {"n": number}, now=float(number))
        taken = []
        lock = threading.Lock()

        def worker(name):
            connection = connect(path)
            while True:
                job = jobs.claim(connection, name, now=100.0)
                if job is None:
                    return
                with lock:
                    taken.append(job["id"])

        threads = []
        for number in range(6):
            threads.append(threading.Thread(target=worker, args=(f"w{number}",)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        assert len(taken) == 60
        assert len(set(taken)) == 60, (
            f"{60 - len(set(taken))} jobs were taken by two workers. The look and "
            "the update must happen in one BEGIN IMMEDIATE transaction."
        )


class TestFinishAndFail:
    def test_finish(self, jobs, db):
        job_id = jobs.enqueue(db, "chat", {}, now=1.0)
        jobs.claim(db, "a", now=2.0)
        jobs.finish(db, job_id, "Saved.")
        job = jobs.get(db, job_id)
        assert job["status"] == "done" and job["result"] == "Saved."

    def test_a_failure_goes_back_on_the_queue(self, jobs, db):
        job_id = jobs.enqueue(db, "chat", {}, now=1.0)
        jobs.claim(db, "a", now=2.0)
        assert jobs.fail(db, job_id, "model overloaded") == "queued"
        job = jobs.get(db, job_id)
        assert job["status"] == "queued" and job["error"] == "model overloaded"
        assert job["claimed_by"] is None
        assert jobs.claim(db, "b", now=3.0)["attempts"] == 2

    def test_the_third_failure_is_dead(self, jobs, db):
        job_id = jobs.enqueue(db, "chat", {}, now=1.0)
        for attempt in range(3):
            jobs.claim(db, "a", now=2.0)
            status = jobs.fail(db, job_id, f"failure {attempt}")
        assert status == "dead"
        assert jobs.get(db, job_id)["status"] == "dead"
        assert jobs.claim(db, "a", now=3.0) is None, (
            "A dead job was handed out again. A job that has failed every time "
            "will fail the next time; stop trying, and keep it to look at."
        )

    def test_max_attempts_can_be_changed(self, jobs, db):
        job_id = jobs.enqueue(db, "chat", {}, now=1.0)
        jobs.claim(db, "a", now=2.0)
        assert jobs.fail(db, job_id, "x", max_attempts=1) == "dead"

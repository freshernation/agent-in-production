"""Week 5, Day 1 - containers, and a database URL.

Run me:  pytest week-05/day-1 -v

Nothing here runs Docker. The tests read your files for the mistakes that cost
the most time on a real deploy. Then build it for real: docker compose up.
"""

import sqlite3
import threading

import pytest


def content(text, name):
    lines = []
    for line in text.splitlines():
        if line.strip() and not line.strip().startswith("#"):
            lines.append(line)
    assert lines, f"{name} contains only comments so far - write it."
    return lines


@pytest.fixture
def db(load):
    return load("database.py")


class TestDialect:
    @pytest.mark.parametrize("url,kind", [
        ("sqlite:///desk.db", "sqlite"), ("sqlite:////data/desk.db", "sqlite"),
        ("postgresql://u:p@db/desk", "postgres"), ("postgres://u:p@db/desk", "postgres"),
    ])
    def test_known(self, db, url, kind):
        assert db.dialect(url) == kind

    def test_unknown_never_shows_the_password(self, db):
        with pytest.raises(ValueError) as caught:
            db.dialect("mysql://desk:hunter2@db/desk")
        assert "hunter2" not in str(caught.value)
        assert "mysql" in str(caught.value)

    def test_sqlite_path(self, db):
        assert db.sqlite_path("sqlite:////data/desk.db") == "/data/desk.db"
        assert db.sqlite_path("sqlite:///desk.db") == "desk.db"
        with pytest.raises(ValueError):
            db.sqlite_path("sqlite:///")
        with pytest.raises(ValueError):
            db.sqlite_path("postgresql://db/desk")


class TestConnect:
    def test_wal(self, db, tmp_path):
        connection = db.connect(f"sqlite:///{tmp_path / 'desk.db'}")
        assert connection.execute("PRAGMA journal_mode").fetchone()[0] == "wal", (
            "Two processes share this file now. WAL lets one read while the "
            "other writes."
        )

    def test_two_writers_at_once(self, db, tmp_path):
        url = f"sqlite:///{tmp_path / 'desk.db'}"
        setup = db.connect(url)
        setup.execute("CREATE TABLE t (n INTEGER)")
        errors = []

        def write(start):
            connection = db.connect(url)
            try:
                for n in range(start, start + 50):
                    connection.execute("INSERT INTO t (n) VALUES (?)", (n,))
            except sqlite3.Error as error:
                errors.append(error)

        threads = [threading.Thread(target=write, args=(i * 100,)) for i in range(4)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        assert errors == []
        assert setup.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 200


class TestAdapt:
    def test_sqlite_unchanged(self, db):
        sql = "SELECT * FROM notes WHERE user = ? AND title = ?"
        assert db.adapt(sql, "sqlite") == sql

    def test_postgres_parameters(self, db):
        assert db.adapt("SELECT * FROM notes WHERE user = ? AND title = ?", "postgres") == (
            "SELECT * FROM notes WHERE user = %s AND title = %s")

    def test_a_question_mark_inside_quotes_is_text(self, db):
        assert db.adapt("SELECT 'why?' FROM t WHERE id = ?", "postgres") == (
            "SELECT 'why?' FROM t WHERE id = %s")


class TestDockerfile:
    def test_shape(self, source):
        lines = content(source("Dockerfile"), "Dockerfile")
        assert lines[0].startswith("FROM python:3.12")
        text = "\n".join(lines)
        assert "--no-cache-dir" in text
        assert "0.0.0.0" in text and "PORT" in text

    def test_requirements_before_the_code(self, source):
        lines = content(source("Dockerfile"), "Dockerfile")
        install = next(i for i, ln in enumerate(lines) if "pip install" in ln)
        copy_requirements = next(i for i, ln in enumerate(lines)
                                 if ln.startswith("COPY") and "requirements.txt" in ln)
        copy_all = next(i for i, ln in enumerate(lines) if ln.strip().startswith("COPY . "))
        assert copy_requirements < install < copy_all, (
            "Copy the requirements and install them before copying the code. "
            "Otherwise every one-line change reinstalls every package."
        )

    def test_not_root(self, source):
        lines = content(source("Dockerfile"), "Dockerfile")
        users = [ln for ln in lines if ln.startswith("USER ")]
        assert users and users[-1].split()[1] != "root"


class TestCompose:
    def test_two_services_one_volume(self, source):
        text = "\n".join(content(source("compose.yaml"), "compose.yaml"))
        assert "api:" in text and "worker:" in text
        assert "volumes:" in text and "/data" in text
        assert "run_worker.py" in text

    def test_no_secrets_in_the_file(self, source):
        text = source("compose.yaml")
        for line in text.splitlines():
            if "KEY" in line and ":" in line and not line.strip().startswith("#"):
                value = line.split(":", 1)[1].strip()
                assert value.startswith("${") or not value, (
                    f"A secret is written in compose.yaml: {line.strip()}. "
                    "Use ${NAME} and set it in the environment."
                )

    def test_restarts_and_a_healthcheck(self, source):
        text = "\n".join(content(source("compose.yaml"), "compose.yaml"))
        assert "restart:" in text and "healthcheck:" in text and "/health" in text

    def test_database_url(self, source):
        assert "DATABASE_URL" in source("compose.yaml")


class TestDockerignore:
    def test_keeps_secrets_out(self, source):
        lines = content(source(".dockerignore"), ".dockerignore")
        for must in (".env", ".venv", ".git", "instructor"):
            assert any(must in line for line in lines), f".dockerignore does not exclude {must}"

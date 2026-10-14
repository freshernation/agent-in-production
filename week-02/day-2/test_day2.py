"""Week 2, Day 2 - migrations.

Run me:  pytest week-02/day-2 -v
"""

import sqlite3

import pytest


@pytest.fixture
def migrate(load):
    return load("migrate.py")


@pytest.fixture
def db(tmp_path):
    return sqlite3.connect(str(tmp_path / "desk.db"), isolation_level=None)


def columns(db, table):
    names = []
    for row in db.execute(f"PRAGMA table_info({table})"):
        names.append(row[1])
    return names


class TestVersion:
    def test_a_new_database_is_version_zero(self, migrate, db):
        assert migrate.current_version(db) == 0

    def test_after_migrating(self, migrate, db):
        migrate.migrate(db, migrate.MIGRATIONS)
        assert migrate.current_version(db) == len(migrate.MIGRATIONS)


class TestMigrate:
    def test_runs_them_all_and_says_how_many(self, migrate, db):
        assert migrate.migrate(db, migrate.MIGRATIONS) == 3
        assert columns(db, "notes") == ["user", "title", "body", "created"]
        assert columns(db, "conversations") == ["user", "id", "history"]

    def test_running_twice_does_nothing(self, migrate, db):
        migrate.migrate(db, migrate.MIGRATIONS)
        assert migrate.migrate(db, migrate.MIGRATIONS) == 0, (
            "The second run tried to create the tables again. A migration that "
            "cannot run twice will one day run twice."
        )

    def test_only_the_new_ones_run(self, migrate, db):
        migrate.migrate(db, migrate.MIGRATIONS[:2])
        db.execute("INSERT INTO notes (user, title) VALUES ('alice', 'milk')")
        assert migrate.migrate(db, migrate.MIGRATIONS) == 1
        assert db.execute("SELECT title, created FROM notes").fetchall() == [("milk", "")], (
            "Adding a column must keep the rows that are already there."
        )

    def test_a_failing_migration_changes_nothing(self, migrate, db):
        broken = migrate.MIGRATIONS[:2] + ["ALTER TABLE nowhere ADD COLUMN x TEXT"]
        with pytest.raises(sqlite3.Error):
            migrate.migrate(db, broken)
        assert migrate.current_version(db) == 2

    def test_a_failure_halfway_rolls_back(self, migrate, db):
        """The bad one creates a table and then fails. The table must not stay."""
        migrate.migrate(db, migrate.MIGRATIONS[:1])
        bad = migrate.MIGRATIONS[:1] + ["CREATE TABLE half (x TEXT); SELECT nonsense FROM nowhere"]
        with pytest.raises(sqlite3.Error):
            migrate.migrate(db, bad)
        tables = []
        for row in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
            tables.append(row[0])
        assert "half" not in tables
        assert migrate.current_version(db) == 1

    def test_the_list_is_three_long(self, migrate):
        assert len(migrate.MIGRATIONS) == 3

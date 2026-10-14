"""Week 2, Day 1 - notes in a database.

Run me:  pytest week-02/day-1 -v
"""

import pytest


@pytest.fixture
def store(load):
    return load("store.py")


@pytest.fixture
def db(store, tmp_path):
    connection = store.connect(str(tmp_path / "desk.db"))
    store.create_tables(connection)
    return connection


class TestNotes:
    def test_add_and_list(self, store, db):
        assert store.add_note(db, "alice", "milk", "two litres") == "Saved 'milk'."
        store.add_note(db, "alice", "eggs")
        assert store.list_titles(db, "alice") == "1. milk\n2. eggs"

    def test_nothing_yet(self, store, db):
        assert store.list_titles(db, "alice") == "No notes yet."

    def test_a_title_is_needed(self, store, db):
        assert store.add_note(db, "alice", "   ") == "A note needs a title."

    def test_a_duplicate_ignoring_capitals(self, store, db):
        store.add_note(db, "alice", "milk")
        assert store.add_note(db, "alice", "Milk") == "There is already a note called 'Milk'."

    def test_find(self, store, db):
        store.add_note(db, "alice", "milk", "two litres")
        store.add_note(db, "alice", "dentist", "Friday")
        assert store.find_notes(db, "alice", "LITRES") == "milk: two litres"
        assert store.find_notes(db, "alice", "car") == "No notes mention 'car'."

    def test_delete(self, store, db):
        store.add_note(db, "alice", "milk")
        assert store.delete_note(db, "alice", "MILK") == "Deleted 'milk'."
        assert store.list_titles(db, "alice") == "No notes yet."
        assert store.delete_note(db, "alice", "milk") == "No note called 'milk'."


class TestWhoseNotes:
    def test_two_users_two_lists(self, store, db):
        store.add_note(db, "alice", "milk")
        store.add_note(db, "bob", "bike")
        assert store.list_titles(db, "alice") == "1. milk"
        assert store.list_titles(db, "bob") == "1. bike"

    def test_the_same_title_for_two_users(self, store, db):
        assert store.add_note(db, "alice", "milk") == "Saved 'milk'."
        assert store.add_note(db, "bob", "milk") == "Saved 'milk'."

    def test_bob_cannot_find_alices_notes(self, store, db):
        store.add_note(db, "alice", "bank", "sort code 12-34-56")
        assert store.find_notes(db, "bob", "sort") == "No notes mention 'sort'."

    def test_bob_cannot_delete_alices_notes(self, store, db):
        store.add_note(db, "alice", "milk")
        assert store.delete_note(db, "bob", "milk") == "No note called 'milk'."
        assert store.list_titles(db, "alice") == "1. milk"


class TestSafety:
    def test_a_title_that_looks_like_sql(self, store, db):
        title = "x'); DROP TABLE notes; --"
        assert store.add_note(db, "alice", title) == f"Saved '{title}'."
        store.add_note(db, "alice", "milk")
        assert "milk" in store.list_titles(db, "alice")

    def test_a_user_name_that_looks_like_sql(self, store, db):
        store.add_note(db, "alice", "milk")
        assert store.list_titles(db, "x' OR '1'='1") == "No notes yet.", (
            "A user name turned into SQL and matched every row. Pass values as "
            "? parameters, always."
        )

    def test_no_sql_built_from_strings(self, store, source):
        code = source("store.py", code_only=True)
        for line in code.splitlines():
            if "execute(" in line:
                assert 'f"' not in line.split("execute(", 1)[1][:3] and "+" not in line, (
                    f"This builds SQL from a string: {line.strip()}"
                )


class TestTwoWriters:
    def test_a_second_connection_sees_the_first_ones_note(self, store, tmp_path):
        path = str(tmp_path / "desk.db")
        first, second = store.connect(path), store.connect(path)
        store.create_tables(first)
        store.add_note(first, "alice", "milk")
        assert store.list_titles(second, "alice") == "1. milk", (
            "The second connection cannot see the first one's note, so it was "
            "never saved. Connect with isolation_level=None."
        )

    def test_both_adding_the_same_title(self, store, tmp_path):
        path = str(tmp_path / "desk.db")
        first, second = store.connect(path), store.connect(path)
        store.create_tables(first)
        store.add_note(first, "alice", "milk")
        assert store.add_note(second, "alice", "milk") == "There is already a note called 'milk'."

    def test_it_survives_closing(self, store, tmp_path):
        path = str(tmp_path / "desk.db")
        db = store.connect(path)
        store.create_tables(db)
        store.add_note(db, "alice", "milk")
        db.close()
        assert store.list_titles(store.connect(path), "alice") == "1. milk"

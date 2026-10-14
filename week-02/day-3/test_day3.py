"""Week 2, Day 3 - many users.

Run me:  pytest week-02/day-3 -v
"""

import pytest

from desk.agent import run_agent
from desk.kit import SCHEMAS
from llm import FakeModel, say, use


@pytest.fixture
def tenancy(load):
    return load("tenancy.py")


@pytest.fixture
def db(load, tmp_path):
    store, migrate = load("store.py"), load("migrate.py")
    connection = store.connect(str(tmp_path / "desk.db"))
    migrate.migrate(connection, migrate.MIGRATIONS)
    return connection


class TestBound:
    def test_passes_db_and_user_first(self, tenancy):
        def record(db, user, title):
            return f"{db}/{user}/{title}"
        assert tenancy.bound(record, "D", "alice")(title="milk") == "D/alice/milk"

    def test_each_one_keeps_its_own_user(self, tenancy):
        def who(db, user):
            return user
        for_alice, for_bob = tenancy.bound(who, None, "alice"), tenancy.bound(who, None, "bob")
        assert for_alice() == "alice" and for_bob() == "bob"


class TestToolsFor:
    def test_the_same_names_as_the_schemas(self, tenancy, db):
        names = set()
        for schema in SCHEMAS:
            names.add(schema["name"])
        tools = tenancy.tools_for(db, "alice")
        assert set(tools) == names - {"share_note"}

    def test_each_user_gets_their_own_notes(self, tenancy, db):
        alice, bob = tenancy.tools_for(db, "alice"), tenancy.tools_for(db, "bob")
        alice["add_note"](title="bank", body="sort code 12-34-56")
        assert bob["list_titles"]() == "No notes yet."
        assert bob["find_notes"](word="sort") == "No notes mention 'sort'."
        assert alice["list_titles"]() == "1. bank"

    def test_calculate_still_works(self, tenancy, db):
        assert tenancy.tools_for(db, "alice")["calculate"](expression="6*7") == "42"


class TestInTheAgent:
    def test_a_model_cannot_name_another_user(self, tenancy, db):
        """The model asks to delete 'bank' with a made-up user argument."""
        tenancy.tools_for(db, "alice")["add_note"](title="bank")
        model = FakeModel([
            use("delete_note", {"title": "bank", "user": "alice"}, id="c1"),
            say("Done."),
        ])
        run_agent(model, "Delete the bank note.", SCHEMAS, tenancy.tools_for(db, "bob"))
        assert tenancy.tools_for(db, "alice")["list_titles"]() == "1. bank", (
            "Bob's agent deleted Alice's note. The user must come from who is "
            "logged in, never from anything the model wrote."
        )

    def test_bobs_agent_works_on_bobs_notes(self, tenancy, db):
        model = FakeModel([use("add_note", {"title": "bike"}, id="c1"), say("Saved.")])
        run_agent(model, "Remember my bike.", SCHEMAS, tenancy.tools_for(db, "bob"))
        assert tenancy.tools_for(db, "bob")["list_titles"]() == "1. bike"
        assert tenancy.tools_for(db, "alice")["list_titles"]() == "No notes yet."


HISTORY = [
    {"role": "user", "content": "Remember milk"},
    {"role": "assistant", "content": "", "tool_calls": [
        {"id": "c1", "name": "add_note", "args": {"title": "milk"}}], "_raw": object()},
    {"role": "tool", "tool_call_id": "c1", "content": "Saved 'milk'."},
    {"role": "assistant", "content": "Saved."},
]


class TestHistory:
    def test_clean(self, tenancy):
        cleaned = tenancy.clean(HISTORY)
        assert "_raw" not in cleaned[1]
        assert cleaned[1]["tool_calls"][0]["name"] == "add_note"
        assert "_raw" in HISTORY[1], "clean changed the original."

    def test_save_and_load(self, tenancy, db):
        tenancy.save_history(db, "alice", "c-1", HISTORY)
        loaded = tenancy.load_history(db, "alice", "c-1")
        assert loaded == tenancy.clean(HISTORY)

    def test_saving_again_replaces_it(self, tenancy, db):
        tenancy.save_history(db, "alice", "c-1", HISTORY[:1])
        tenancy.save_history(db, "alice", "c-1", HISTORY)
        assert len(tenancy.load_history(db, "alice", "c-1")) == 4

    def test_unknown_is_none(self, tenancy, db):
        assert tenancy.load_history(db, "alice", "nope") is None

    def test_another_users_conversation_is_none(self, tenancy, db):
        tenancy.save_history(db, "alice", "c-1", HISTORY)
        assert tenancy.load_history(db, "bob", "c-1") is None

    def test_conversation_ids(self, tenancy, db):
        tenancy.save_history(db, "alice", "b", HISTORY)
        tenancy.save_history(db, "alice", "a", HISTORY)
        tenancy.save_history(db, "bob", "c", HISTORY)
        assert tenancy.conversation_ids(db, "alice") == ["a", "b"]

    def test_a_loaded_history_is_a_legal_conversation(self, tenancy, db):
        tenancy.save_history(db, "alice", "c-1", HISTORY)
        history = tenancy.load_history(db, "alice", "c-1")
        history.append({"role": "user", "content": "And now?"})
        FakeModel([say("ok")]).chat(history)

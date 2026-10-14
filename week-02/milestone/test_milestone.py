"""Week 2 milestone - Desk for many users, on a database.

Run me:  pytest week-02/milestone -v
"""

import pytest
from fastapi.testclient import TestClient

from llm import FakeModel, say, use

KEYS = {"k-alice-0123456789": "alice", "k-bob-0123456789": "bob", "k-carol-0123456789": "carol"}
ROLES = {"alice": "owner", "bob": "reader"}
ALICE = {"Authorization": "Bearer k-alice-0123456789"}
BOB = {"Authorization": "Bearer k-bob-0123456789"}
CAROL = {"Authorization": "Bearer k-carol-0123456789"}


@pytest.fixture
def app(load):
    return load("app.py")


@pytest.fixture
def path(tmp_path):
    return str(tmp_path / "desk.db")


def client(app, model, path):
    return TestClient(app.create_app(model, KEYS, ROLES, path))


def contents(model, index):
    found = []
    for message in model.requests[index]["messages"]:
        found.append(message["content"])
    return found


class TestParseRoles:
    def test_two(self, app):
        assert app.parse_roles("alice:owner, bob:reader,") == {"alice": "owner", "bob": "reader"}

    @pytest.mark.parametrize("text", ["alice", "alice:admin", "bob:Owner"])
    def test_refuses(self, app, text):
        with pytest.raises(ValueError):
            app.parse_roles(text)


class TestSurvivesARestart:
    def test_the_conversation_carries_on(self, app, path):
        first = client(app, FakeModel([say("Hello, Alice.")]), path)
        cid = first.post("/chat", json={"message": "Hi, I'm Alice"}, headers=ALICE).json()["conversation_id"]

        model = FakeModel([say("You said you were Alice.")])
        second = client(app, model, path)
        response = second.post("/chat", json={"message": "Who am I?", "conversation_id": cid},
                               headers=ALICE)
        assert response.status_code == 200, (
            "The conversation did not survive the restart. It has to be in the "
            "database, not in a dictionary inside create_app."
        )
        assert "Hi, I'm Alice" in contents(model, 0)

    def test_notes_carry_on(self, app, path):
        writer = client(app, FakeModel([use("add_note", {"title": "milk"}, id="c1"), say("Saved.")]), path)
        writer.post("/chat", json={"message": "Remember milk"}, headers=ALICE)
        model = FakeModel([use("list_titles", {}, id="c1"), say("You have milk.")])
        client(app, model, path).post("/chat", json={"message": "What do I have?"}, headers=ALICE)
        assert "1. milk" in contents(model, 1)

    def test_conversations_are_listed_after_a_restart(self, app, path):
        cid = client(app, FakeModel([say("ok")]), path).post(
            "/chat", json={"message": "hi"}, headers=ALICE).json()["conversation_id"]
        assert client(app, FakeModel(), path).get("/conversations", headers=ALICE).json() == [cid]


class TestManyUsers:
    def test_bob_cannot_continue_alices_conversation(self, app, path):
        cid = client(app, FakeModel([say("ok")]), path).post(
            "/chat", json={"message": "secret"}, headers=ALICE).json()["conversation_id"]
        response = client(app, FakeModel(), path).post(
            "/chat", json={"message": "?", "conversation_id": cid}, headers=BOB)
        assert response.status_code == 404

    def test_bob_does_not_see_alices_notes(self, app, path):
        client(app, FakeModel([use("add_note", {"title": "bank", "body": "12-34-56"}, id="c1"),
                               say("Saved.")]), path).post("/chat", json={"message": "save"}, headers=ALICE)
        model = FakeModel([use("find_notes", {"word": "12"}, id="c1"), say("Nothing.")])
        client(app, model, path).post("/chat", json={"message": "find 12"}, headers=BOB)
        assert "No notes mention '12'." in contents(model, 1)


class TestRoles:
    def test_a_reader_is_not_offered_add_note(self, app, path):
        model = FakeModel([say("ok")])
        client(app, model, path).post("/chat", json={"message": "hi"}, headers=BOB)
        offered = []
        for schema in model.requests[0]["tools"]:
            offered.append(schema["name"])
        assert "add_note" not in offered and "delete_note" not in offered

    def test_a_reader_cannot_add_even_if_asked(self, app, path):
        model = FakeModel([use("add_note", {"title": "x"}, id="c1"), say("Done.")])
        client(app, model, path).post("/chat", json={"message": "add x"}, headers=BOB)
        assert "Refused: the reader role cannot use add_note." in contents(model, 1)

    def test_a_user_with_no_role_is_offered_nothing(self, app, path):
        model = FakeModel([say("I cannot do anything for you.")])
        client(app, model, path).post("/chat", json={"message": "hi"}, headers=CAROL)
        assert not model.requests[0]["tools"]


class TestOverHttp:
    def test_a_delete_needs_a_yes_and_nobody_can_give_one(self, app, path):
        c = client(app, FakeModel([use("add_note", {"title": "milk"}, id="c1"), say("Saved."),
                                   use("delete_note", {"title": "milk"}, id="c2"), say("Done.")]), path)
        c.post("/chat", json={"message": "save milk"}, headers=ALICE)
        c.post("/chat", json={"message": "delete milk"}, headers=ALICE)
        model = FakeModel([use("list_titles", {}, id="c1"), say("ok")])
        client(app, model, path).post("/chat", json={"message": "list"}, headers=ALICE)
        assert "1. milk" in contents(model, 1)

    def test_the_reply_is_the_answer(self, app, path):
        body = client(app, FakeModel([say("Hello.")]), path).post(
            "/chat", json={"message": "hi"}, headers=ALICE).json()
        assert body["reply"] == "Hello."

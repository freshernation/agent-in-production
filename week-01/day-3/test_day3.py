"""Week 1, Day 3 - Desk behind POST /chat.

Run me:  pytest week-01/day-3 -v
"""

import re

import pytest
from fastapi.testclient import TestClient

from llm import FakeModel, say, use


def echo_turn(model, history, task):
    """A fake turn: remembers everything it was told."""
    history = history + [{"role": "user", "content": task},
                         {"role": "assistant", "content": f"heard {task}"}]
    return {"text": f"heard {task} ({len(history) // 2} so far)", "history": history}


def broken_turn(model, history, task):
    raise RuntimeError("model on fire at /Users/someone/secret/path.py line 12")


@pytest.fixture
def chat(load):
    return load("chat.py")


@pytest.fixture
def client(chat):
    return TestClient(chat.create_app(FakeModel(), turn=echo_turn))


class TestNewId:
    def test_shape(self, chat):
        assert re.fullmatch(r"[0-9a-f]{12}", chat.new_id())

    def test_different_every_time(self, chat):
        assert chat.new_id() != chat.new_id()


class TestChat:
    def test_a_new_conversation(self, client):
        response = client.post("/chat", json={"message": "hello"})
        assert response.status_code == 200
        body = response.json()
        assert re.fullmatch(r"[0-9a-f]{12}", body["conversation_id"])
        assert body["reply"] == "heard hello (1 so far)"

    def test_continuing_it(self, client):
        first = client.post("/chat", json={"message": "one"}).json()
        second = client.post("/chat", json={"message": "two",
                                            "conversation_id": first["conversation_id"]})
        assert second.json()["reply"] == "heard two (2 so far)", (
            "The second message started from nothing. Store the history the turn "
            "handed back, under the conversation's id."
        )
        assert second.json()["conversation_id"] == first["conversation_id"]

    def test_two_conversations_do_not_mix(self, client):
        a = client.post("/chat", json={"message": "a1"}).json()["conversation_id"]
        client.post("/chat", json={"message": "b1"})
        reply = client.post("/chat", json={"message": "a2", "conversation_id": a}).json()["reply"]
        assert reply == "heard a2 (2 so far)"

    def test_an_unknown_conversation_is_404(self, client):
        response = client.post("/chat", json={"message": "hi", "conversation_id": "nope"})
        assert response.status_code == 404

    @pytest.mark.parametrize("payload", [{}, {"message": ""}, {"message": "x" * 2001}])
    def test_bad_input_is_422(self, client, payload):
        assert client.post("/chat", json=payload).status_code == 422


class TestFailure:
    def test_a_broken_turn_is_503(self, chat):
        client = TestClient(chat.create_app(FakeModel(), turn=broken_turn),
                            raise_server_exceptions=False)
        response = client.post("/chat", json={"message": "hi"})
        assert response.status_code == 503
        assert "secret" not in response.text and "Traceback" not in response.text, (
            "The error reached the caller with your file paths in it. Say "
            "something true and short; the detail belongs in your logs."
        )


class TestWithTheRealDesk:
    def test_take_turn_is_the_default(self, chat):
        model = FakeModel([use("add_note", {"title": "milk"}, id="c1"), say("Saved milk.")])
        client = TestClient(chat.create_app(model))
        body = client.post("/chat", json={"message": "Remember milk"}).json()
        assert body["reply"].startswith("Saved milk.")

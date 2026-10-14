"""Week 1 milestone - Desk behind an API.

Run me:  pytest week-01/milestone -v
"""

import pytest
from fastapi.testclient import TestClient

from llm import FakeModel, say, use

GOOD = "alice:k-alice-0123456789, bob:k-bob-0123456789"
ALICE = {"Authorization": "Bearer k-alice-0123456789"}


@pytest.fixture
def app(load):
    return load("app.py")


class TestParseKeys:
    def test_two_users(self, app):
        assert app.parse_keys(GOOD) == {"k-alice-0123456789": "alice", "k-bob-0123456789": "bob"}

    def test_a_trailing_comma_is_fine(self, app):
        assert len(app.parse_keys(GOOD + ",")) == 2

    @pytest.mark.parametrize("text", [
        "", " , ", "alice", "alice:short", ":k-alice-0123456789",
        "alice:k-same-0123456789,bob:k-same-0123456789",
    ])
    def test_refuses_to_start_on_a_bad_setting(self, app, text):
        with pytest.raises(ValueError):
            app.parse_keys(text)

    def test_the_message_says_what_is_wrong(self, app):
        with pytest.raises(ValueError) as caught:
            app.parse_keys("alice:short")
        assert "16" in str(caught.value)


class TestTheService:
    def test_end_to_end_with_the_real_desk(self, app):
        model = FakeModel([use("add_note", {"title": "milk"}, id="c1"), say("Saved milk."),
                           say("You have one note: milk.")])
        client = TestClient(app.create_app(model, app.parse_keys(GOOD)))
        first = client.post("/chat", json={"message": "Remember milk"}, headers=ALICE)
        assert first.status_code == 200
        cid = first.json()["conversation_id"]
        second = client.post("/chat", json={"message": "What do I have?", "conversation_id": cid},
                             headers=ALICE)
        assert second.json()["reply"].startswith("You have one note")
        assert len(model.requests[2]["messages"]) > 1, (
            "The second message reached the model without the first. The "
            "conversation was not carried."
        )

    def test_no_key_no_answer(self, app):
        client = TestClient(app.create_app(FakeModel(), app.parse_keys(GOOD)))
        assert client.post("/chat", json={"message": "hi"}).status_code == 401

    def test_from_environment(self, app, monkeypatch):
        monkeypatch.setenv("DESK_KEYS", GOOD)
        monkeypatch.setenv("AGENT_PROVIDER", "fake")
        client = TestClient(app.from_environment())
        assert client.get("/health").json() == {"status": "ok"}

    def test_from_environment_refuses_no_keys(self, app, monkeypatch):
        monkeypatch.delenv("DESK_KEYS", raising=False)
        monkeypatch.setenv("AGENT_PROVIDER", "fake")
        with pytest.raises(ValueError):
            app.from_environment()


class TestTheWriteUp:
    HEADINGS = ["What arrives", "Who is asking", "What Desk does with it",
                "What goes back, and what does not"]

    @pytest.mark.parametrize("heading", HEADINGS)
    def test_section_is_written(self, source, heading):
        text = source("A_REQUEST.md")
        assert "<!--" not in text, "Delete the instructions comment."
        assert f"## {heading}" in text
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 40, f"'{heading}' is {len(body.split())} words."

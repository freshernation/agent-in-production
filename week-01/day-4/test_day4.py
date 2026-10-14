"""Week 1, Day 4 - a key per caller.

Run me:  pytest week-01/day-4 -v
"""

import pytest
from fastapi.testclient import TestClient

from llm import FakeModel

KEYS = {"k-alice-123": "alice", "k-bob-456": "bob"}
ALICE = {"Authorization": "Bearer k-alice-123"}
BOB = {"Authorization": "Bearer k-bob-456"}


def counting_turn():
    calls = []

    def turn(model, history, task):
        calls.append(task)
        history = history + [{"role": "user", "content": task},
                             {"role": "assistant", "content": "ok"}]
        return {"text": f"turn {len(history) // 2}", "history": history}

    return turn, calls


@pytest.fixture
def keys(load):
    return load("keys.py")


@pytest.fixture
def app_and_calls(keys):
    turn, calls = counting_turn()
    return TestClient(keys.create_app(FakeModel(), KEYS, turn=turn)), calls


class TestUserFor:
    def test_a_good_key(self, keys):
        assert keys.user_for("Bearer k-alice-123", KEYS) == "alice"

    @pytest.mark.parametrize("header", [
        "", "k-alice-123", "Bearer ", "Bearer k-alice-12", "Bearer k-alice-1234",
        "bearer k-alice-123", "Basic k-alice-123",
    ])
    def test_everything_else_is_nobody(self, keys, header):
        assert keys.user_for(header, KEYS) is None

    def test_compares_in_constant_time(self, keys, source):
        code = source("keys.py", code_only=True)
        assert "compare_digest" in code, (
            "Use secrets.compare_digest. == stops at the first character that "
            "differs, so the time it takes says how much of a key was right."
        )


class TestTheKey:
    def test_health_needs_no_key(self, app_and_calls):
        client, _ = app_and_calls
        assert client.get("/health").status_code == 200

    def test_no_key_is_401(self, app_and_calls):
        client, calls = app_and_calls
        response = client.post("/chat", json={"message": "hi"})
        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
        assert calls == [], "The model was called for somebody with no key."

    def test_a_wrong_key_is_401(self, app_and_calls):
        client, _ = app_and_calls
        response = client.post("/chat", json={"message": "hi"},
                               headers={"Authorization": "Bearer guess"})
        assert response.status_code == 401
        assert "k-alice" not in response.text

    def test_a_good_key_gets_an_answer(self, app_and_calls):
        client, _ = app_and_calls
        response = client.post("/chat", json={"message": "hi"}, headers=ALICE)
        assert response.status_code == 200
        assert response.json()["reply"] == "turn 1"


class TestWhoseConversation:
    def test_continuing_your_own(self, app_and_calls):
        client, _ = app_and_calls
        cid = client.post("/chat", json={"message": "one"}, headers=ALICE).json()["conversation_id"]
        reply = client.post("/chat", json={"message": "two", "conversation_id": cid},
                            headers=ALICE).json()["reply"]
        assert reply == "turn 2"

    def test_somebody_elses_is_404(self, app_and_calls):
        client, calls = app_and_calls
        cid = client.post("/chat", json={"message": "secret"}, headers=ALICE).json()["conversation_id"]
        response = client.post("/chat", json={"message": "what did she say?",
                                              "conversation_id": cid}, headers=BOB)
        assert response.status_code == 404, (
            f"Got {response.status_code}. A 403 would tell Bob the conversation "
            "exists. To him it does not."
        )
        assert calls == ["secret"]

    def test_listing_shows_only_your_own(self, app_and_calls):
        client, _ = app_and_calls
        a = client.post("/chat", json={"message": "a"}, headers=ALICE).json()["conversation_id"]
        client.post("/chat", json={"message": "b"}, headers=BOB)
        assert client.get("/conversations", headers=ALICE).json() == [a]

    def test_listing_needs_a_key(self, app_and_calls):
        client, _ = app_and_calls
        assert client.get("/conversations").status_code == 401

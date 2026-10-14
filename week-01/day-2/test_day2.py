"""Week 1, Day 2 - the smallest service.

Run me:  pytest week-01/day-2 -v

TestClient runs the app in this process. No server, no port, no network.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(load):
    return TestClient(load("service.py").create_app())


class TestHealth:
    def test_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestNotes:
    def test_create(self, client):
        response = client.post("/notes", json={"title": "milk", "body": "two litres"})
        assert response.status_code == 201, (
            f"Got {response.status_code}. Something was created, and 201 says so."
        )
        assert response.json() == {"title": "milk", "body": "two litres"}

    def test_list(self, client):
        client.post("/notes", json={"title": "milk"})
        client.post("/notes", json={"title": "eggs"})
        assert client.get("/notes").json() == ["eggs", "milk"]

    def test_read_one(self, client):
        client.post("/notes", json={"title": "milk", "body": "two litres"})
        response = client.get("/notes/MILK")
        assert response.status_code == 200
        assert response.json()["body"] == "two litres"

    def test_missing_is_404(self, client):
        response = client.get("/notes/nothing")
        assert response.status_code == 404
        assert "nothing" in response.json()["detail"]

    def test_duplicate_is_409(self, client):
        client.post("/notes", json={"title": "milk"})
        response = client.post("/notes", json={"title": "Milk"})
        assert response.status_code == 409, (
            f"Got {response.status_code}. The request was fine; it conflicts with "
            "something that exists. That is 409, and it is the caller's to fix."
        )
        assert "detail" in response.json()

    def test_delete(self, client):
        client.post("/notes", json={"title": "milk"})
        response = client.delete("/notes/milk")
        assert response.status_code == 204
        assert response.content == b""
        assert client.get("/notes").json() == []

    def test_delete_missing_is_404(self, client):
        assert client.delete("/notes/nothing").status_code == 404


class TestValidation:
    @pytest.mark.parametrize("payload", [{}, {"title": ""}, {"title": "x" * 81}, {"title": 5}])
    def test_bad_input_never_reaches_your_code(self, client, payload):
        response = client.post("/notes", json=payload)
        assert response.status_code == 422
        assert client.get("/notes").json() == []

    def test_the_error_names_the_field(self, client):
        detail = client.post("/notes", json={}).json()["detail"]
        assert "title" in str(detail)


class TestEachAppIsItsOwn:
    def test_two_apps_two_sets_of_notes(self, load):
        mod = load("service.py")
        first, second = TestClient(mod.create_app()), TestClient(mod.create_app())
        first.post("/notes", json={"title": "milk"})
        assert second.get("/notes").json() == [], (
            "A note added to one app appeared in the other. The notes must be "
            "made inside create_app, not at the top of the file."
        )

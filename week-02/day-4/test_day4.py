"""Week 2, Day 4 - per-user permissions.

Run me:  pytest week-02/day-4 -v
"""

import pytest

from desk.agent import run_agent
from desk.kit import SCHEMAS
from llm import FakeModel, say, use


@pytest.fixture
def permissions(load):
    return load("permissions.py")


def names(schemas):
    found = []
    for schema in schemas:
        found.append(schema["name"])
    return found


def recording_tools():
    calls = []

    def tool(name):
        def run(**args):
            calls.append(name)
            return f"{name} ran"
        return run

    table = {}
    for name in ("add_note", "list_titles", "find_notes", "delete_note", "share_note", "calculate"):
        table[name] = tool(name)
    return table, calls


class TestRoles:
    def test_each_role_includes_the_one_below(self, permissions):
        assert permissions.READER < permissions.WRITER < permissions.OWNER

    def test_reader(self, permissions):
        assert permissions.allowed("reader") == {"list_titles", "find_notes", "calculate"}

    def test_owner_can_delete(self, permissions):
        assert "delete_note" in permissions.allowed("owner")

    def test_an_unknown_role_may_do_nothing(self, permissions):
        assert permissions.allowed("admin") == set()
        assert permissions.allowed("") == set()

    def test_allowed_is_a_copy(self, permissions):
        permissions.allowed("reader").add("delete_note")
        assert "delete_note" not in permissions.allowed("reader")


class TestSchemasFor:
    def test_a_reader_is_told_about_three(self, permissions):
        assert names(permissions.schemas_for("reader", SCHEMAS)) == [
            "list_titles", "find_notes", "calculate"]

    def test_order_is_kept(self, permissions):
        assert names(permissions.schemas_for("owner", SCHEMAS)) == names(SCHEMAS)

    def test_nobody_is_told_about_nothing(self, permissions):
        assert permissions.schemas_for("stranger", SCHEMAS) == []


class TestGuard:
    def test_refusal(self, permissions):
        refuse = permissions.refusal("delete_note", "reader")
        assert refuse(title="milk") == "Refused: the reader role cannot use delete_note."

    def test_every_name_is_still_there(self, permissions):
        tools, _ = recording_tools()
        assert set(permissions.guard(tools, "reader")) == set(tools)

    def test_allowed_tools_run(self, permissions):
        tools, calls = recording_tools()
        assert permissions.guard(tools, "reader")["find_notes"](word="x") == "find_notes ran"
        assert calls == ["find_notes"]

    def test_forbidden_tools_do_not(self, permissions):
        tools, calls = recording_tools()
        guarded = permissions.guard(tools, "writer")
        assert guarded["delete_note"](title="x") == "Refused: the writer role cannot use delete_note."
        assert calls == []

    def test_the_original_table_is_untouched(self, permissions):
        tools, calls = recording_tools()
        permissions.guard(tools, "reader")
        tools["delete_note"](title="x")
        assert calls == ["delete_note"]


class TestInTheAgent:
    def test_a_reader_whose_model_asks_to_delete(self, permissions):
        """It was never offered delete_note. It asks anyway."""
        tools, calls = recording_tools()
        model = FakeModel([use("delete_note", {"title": "milk"}, id="c1"), say("Done.")])
        result = run_agent(model, "Delete the milk note.",
                           permissions.schemas_for("reader", SCHEMAS),
                           permissions.guard(tools, "reader"))
        assert calls == [], "A reader's agent deleted a note."
        offered = names(model.requests[0]["tools"])
        assert "delete_note" not in offered
        contents = []
        for event in result["trace"]:
            if event["kind"] == "result":
                contents.append(event["content"])
        assert contents == ["Refused: the reader role cannot use delete_note."]

    def test_an_owner_can(self, permissions):
        tools, calls = recording_tools()
        model = FakeModel([use("delete_note", {"title": "milk"}, id="c1"), say("Done.")])
        run_agent(model, "Delete the milk note.", permissions.schemas_for("owner", SCHEMAS),
                  permissions.guard(tools, "owner"))
        assert calls == ["delete_note"]

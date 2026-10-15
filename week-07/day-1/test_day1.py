"""Week 7, Day 1 - an MCP server.

Run me:  pytest week-07/day-1 -v

The tests connect a real MCP client to your server in this process: no
subprocess, no port.
"""

import anyio
import pytest

from mcp import Client


def tools(server):
    async def go():
        async with Client(server) as client:
            return (await client.list_tools()).tools
    return anyio.run(go)


def call(server, name, args=None):
    async def go():
        async with Client(server) as client:
            return await client.call_tool(name, args or {})
    return anyio.run(go)


def text(result):
    return result.content[0].text


@pytest.fixture
def desk(load):
    return load("desk_mcp.py")


@pytest.fixture
def alice(desk, tmp_path):
    return desk.build_server(str(tmp_path / "d.db"), "alice")


class TestTheTools:
    def test_exactly_three(self, alice):
        names = sorted(tool.name for tool in tools(alice))
        assert names == ["add_note", "find_notes", "list_titles"], (
            f"Served {names}. delete_note must not be one: nothing on the other "
            "side of MCP can approve a deletion."
        )

    def test_described(self, alice):
        for tool in tools(alice):
            assert tool.description and len(tool.description.split()) >= 8, (
                f"{tool.name}'s description is too short to choose by."
            )

    def test_the_schema_comes_from_the_hints(self, alice):
        add = [tool for tool in tools(alice) if tool.name == "add_note"][0]
        assert add.input_schema["required"] == ["title"]
        assert add.input_schema["properties"]["title"]["maxLength"] == 100

    def test_instructions(self, desk):
        assert len(desk.INSTRUCTIONS.split()) >= 15
        assert "instruction" in desk.INSTRUCTIONS.lower()


class TestCallingThem:
    def test_add_then_list(self, alice):
        assert text(call(alice, "add_note", {"title": "dentist", "body": "Tuesday 3pm"})) == "Saved 'dentist'."
        assert text(call(alice, "list_titles")) == "1. dentist"
        assert "Tuesday 3pm" in text(call(alice, "find_notes", {"word": "dentist"}))

    def test_one_users_server_cannot_see_anothers(self, desk, tmp_path):
        path = str(tmp_path / "d.db")
        call(desk.build_server(path, "alice"), "add_note", {"title": "bank", "body": "secret"})
        assert text(call(desk.build_server(path, "bob"), "list_titles")) == "No notes yet."

    def test_a_long_title_is_refused_before_your_code(self, alice):
        result = call(alice, "add_note", {"title": "x" * 101})
        assert result.is_error
        assert text(call(alice, "list_titles")) == "No notes yet."

    def test_a_missing_argument_is_an_error(self, alice):
        assert call(alice, "find_notes", {}).is_error

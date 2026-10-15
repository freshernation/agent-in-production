"""Week 7, Day 3 - a trace across the boundary.

Run me:  pytest week-07/day-3 -v
"""

import anyio
import pytest

from mcp import Client

TRACE = "4bf92f3577b34da6a3ce929d0e0e4736"
SPAN = "00f067aa0ba902b7"


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        self.now = self.now + 1
        return self.now


@pytest.fixture
def crossing(load):
    return load("crossing.py")


class TestTraceparent:
    def test_make(self, crossing):
        assert crossing.traceparent(TRACE, SPAN) == f"00-{TRACE}-{SPAN}-01"

    def test_round_trip(self, crossing):
        assert crossing.parse_traceparent(crossing.traceparent(TRACE, SPAN)) == (TRACE, SPAN)

    @pytest.mark.parametrize("value", [
        None, 42, "", "nonsense", f"01-{TRACE}-{SPAN}-01", f"00-{TRACE[:-1]}-{SPAN}-01",
        f"00-{TRACE.upper()}-{SPAN}-01", f"00-{'0' * 32}-{SPAN}-01", f"00-{TRACE}-{'0' * 16}-01",
    ])
    def test_refuses(self, crossing, value):
        assert crossing.parse_traceparent(value) is None, (
            f"{value!r} was accepted. Anything a caller sends is untrusted - a "
            "malformed header must not become a trace id."
        )


def traced_call(crossing, server, trace_id=TRACE):
    client_spans = []

    async def go():
        async with Client(server) as client:
            return await crossing.call_traced(client, "lookup", {"word": "desk"}, trace_id,
                                              client_spans, Clock())
    return anyio.run(go), client_spans


class TestAcrossTheBoundary:
    def test_the_server_joins_the_trace(self, crossing):
        server_spans = []
        text, client_spans = traced_call(crossing, crossing.build_server(server_spans, Clock()))
        assert text == "desk: a word worth knowing."
        assert server_spans[0]["trace_id"] == TRACE
        assert server_spans[0]["parent"] == client_spans[0]["span_id"], (
            "The server's span does not point at the client span that called it, "
            "so the two halves cannot be joined."
        )

    def test_the_client_span(self, crossing):
        _, client_spans = traced_call(crossing, crossing.build_server([], Clock()))
        span = client_spans[0]
        assert span["type"] == "tool" and span["name"] == "lookup"
        assert span["args"] == {"word": "desk"} and len(span["span_id"]) == 16
        assert span["ended"] > span["started"]

    def test_no_traceparent_is_an_orphan(self, crossing):
        server_spans = []
        server = crossing.build_server(server_spans, Clock())

        async def go():
            async with Client(server) as client:
                await client.call_tool("lookup", {"word": "desk"})
        anyio.run(go)
        assert server_spans[0]["trace_id"] is None and server_spans[0]["parent"] is None
        assert crossing.orphans(server_spans) == 1

    def test_an_error_is_recorded(self, crossing):
        spans = []

        async def go():
            async with Client(crossing.build_server([], Clock())) as client:
                await crossing.call_traced(client, "lookup", {}, TRACE, spans, Clock())
        anyio.run(go)
        assert "error" in spans[0]


class TestStitch:
    def test_one_picture(self, crossing):
        server_spans = []
        _, client_spans = traced_call(crossing, crossing.build_server(server_spans, Clock()))
        server_spans.append({"trace_id": "f" * 32, "parent": "a" * 16, "name": "lookup",
                             "started": 0, "ended": 1})
        joined = crossing.stitch(client_spans, server_spans, TRACE)
        assert len(joined) == 2, "Only this trace's server spans belong in it."
        assert joined[1]["type"] == "server"
        assert joined[1]["parent"] == client_spans[0]["span_id"]

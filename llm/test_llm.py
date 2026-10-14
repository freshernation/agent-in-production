"""Tests for the course's own model layer.

Students never need to run these. Instructors do, after touching llm/.
The real SDK clients are replaced with stand-ins shaped like their responses,
so nothing here touches the network.
"""

from types import SimpleNamespace as NS

import pytest

from llm import FakeModel, InvalidRequest, ModelError, connect, say, use, use_many
from llm.claude_model import ClaudeModel
from llm.openai_model import OpenAIModel
from llm.wire import claude_messages, claude_tool, openai_messages, openai_tool

SCHEMA = {
    "name": "add_note",
    "description": "Save a note.",
    "parameters": {
        "type": "object",
        "properties": {"title": {"type": "string"}},
        "required": ["title"],
    },
}

CALL = {"id": "c1", "name": "add_note", "args": {"title": "milk"}}

ROUND_TRIP = [
    {"role": "user", "content": "Remember milk"},
    {"role": "assistant", "content": "", "tool_calls": [CALL]},
    {"role": "tool", "tool_call_id": "c1", "content": "Saved."},
]


class TestFake:
    def test_scripted_replies_come_back_in_order(self):
        model = FakeModel([say("one"), say("two")])
        ask = [{"role": "user", "content": "hi"}]
        assert model.chat(ask)["text"] == "one"
        assert model.chat(ask)["text"] == "two"
        assert model.call_count == 2

    def test_running_out_of_script_is_an_error(self):
        model = FakeModel([say("one")])
        ask = [{"role": "user", "content": "hi"}]
        model.chat(ask)
        with pytest.raises(AssertionError):
            model.chat(ask)

    def test_single_reply_repeats(self):
        model = FakeModel(say("same"))
        ask = [{"role": "user", "content": "hi"}]
        assert [model.chat(ask)["text"] for _ in range(3)] == ["same"] * 3

    def test_unscripted_echoes(self):
        reply = FakeModel().chat([{"role": "user", "content": "hello"}])
        assert "hello" in reply["text"]
        assert reply["stop"] == "done"

    def test_tool_reply_shape(self):
        reply = use("add_note", {"title": "milk"})
        assert reply["stop"] == "tools"
        assert reply["tool_calls"] == [
            {"id": "call_1", "name": "add_note", "args": {"title": "milk"}}
        ]
        assert reply["message"]["tool_calls"] == reply["tool_calls"]

    def test_use_many_numbers_its_ids(self):
        reply = use_many([("a", {}), ("b", {}, "mine")])
        assert [call["id"] for call in reply["tool_calls"]] == ["call_1", "mine"]

    def test_scripted_error_is_raised(self):
        model = FakeModel([ModelError("down", retryable=True)])
        with pytest.raises(ModelError) as caught:
            model.chat([{"role": "user", "content": "hi"}])
        assert caught.value.retryable

    def test_replies_are_copies(self):
        model = FakeModel(say("same"))
        ask = [{"role": "user", "content": "hi"}]
        model.chat(ask)["message"]["content"] = "changed"
        assert model.chat(ask)["text"] == "same"

    def test_requests_are_snapshots(self):
        model = FakeModel(say("ok"))
        history = [{"role": "user", "content": "hi"}]
        model.chat(history)
        history.append({"role": "assistant", "content": "ok"})
        assert len(model.requests[0]["messages"]) == 1

    def test_accepts_a_full_round_trip(self):
        FakeModel(say("ok")).chat(ROUND_TRIP)

    @pytest.mark.parametrize("messages,fragment", [
        ([], "at least one"),
        ([{"role": "assistant", "content": "hi"}], "start with a user"),
        ([{"role": "system", "content": "x"}], "system="),
        ([{"role": "user", "content": 3}], "always a string"),
        ([{"role": "user", "content": "a"}, {"role": "user", "content": "b"}],
         "in a row"),
        ([{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}],
         "nothing to reply to"),
        (ROUND_TRIP[:2], "no result"),
        ([ROUND_TRIP[0], ROUND_TRIP[2]], "asked for no tools"),
        ([ROUND_TRIP[0], ROUND_TRIP[1],
          {"role": "tool", "tool_call_id": "wrong", "content": "x"}],
         "still waiting"),
        ([ROUND_TRIP[0], ROUND_TRIP[1], {"role": "user", "content": "and?"}],
         "have no result"),
    ])
    def test_rejects_illegal_conversations(self, messages, fragment):
        with pytest.raises(InvalidRequest) as caught:
            FakeModel(say("ok")).chat(messages)
        assert fragment in str(caught.value)

    @pytest.mark.parametrize("tools,fragment", [
        ([len], "not the functions"),
        ([{"name": "x", "description": "y"}], "parameters"),
        ([SCHEMA, SCHEMA], "both called"),
        ([{**SCHEMA, "parameters": {"type": "object", "properties": {},
                                    "required": ["title"]}}], "no such property"),
    ])
    def test_rejects_malformed_tools(self, tools, fragment):
        with pytest.raises(InvalidRequest) as caught:
            FakeModel(say("ok")).chat([{"role": "user", "content": "hi"}], tools=tools)
        assert fragment in str(caught.value)


class TestConnect:
    def test_default_is_fake(self, monkeypatch):
        monkeypatch.delenv("AGENT_PROVIDER", raising=False)
        assert isinstance(connect(), FakeModel)

    def test_unknown_provider(self):
        with pytest.raises(ValueError):
            connect("nonsense")


class TestClaudeWire:
    def test_tool(self):
        assert claude_tool(SCHEMA) == {
            "name": "add_note",
            "description": "Save a note.",
            "input_schema": SCHEMA["parameters"],
        }

    def test_results_travel_in_a_user_message(self):
        assert claude_messages(ROUND_TRIP) == [
            {"role": "user", "content": "Remember milk"},
            {"role": "assistant", "content": [
                {"type": "tool_use", "id": "c1", "name": "add_note",
                 "input": {"title": "milk"}},
            ]},
            {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "c1", "content": "Saved."},
            ]},
        ]

    def test_several_results_share_one_user_message(self):
        messages = [
            {"role": "user", "content": "go"},
            {"role": "assistant", "content": "", "tool_calls": [
                CALL, {"id": "c2", "name": "add_note", "args": {"title": "eggs"}},
            ]},
            {"role": "tool", "tool_call_id": "c1", "content": "one"},
            {"role": "tool", "tool_call_id": "c2", "content": "two"},
        ]
        out = claude_messages(messages)
        assert len(out) == 3
        assert [block["tool_use_id"] for block in out[2]["content"]] == ["c1", "c2"]

    def test_raw_turn_is_replayed_untouched(self):
        raw = [object()]
        messages = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello", "_raw": raw},
            {"role": "user", "content": "again"},
        ]
        assert claude_messages(messages)[1]["content"] is raw
        assert claude_messages(messages, use_raw=False)[1]["content"] == [
            {"type": "text", "text": "hello"},
        ]


class TestOpenAIWire:
    def test_tool(self):
        assert openai_tool(SCHEMA) == {
            "type": "function",
            "function": {
                "name": "add_note",
                "description": "Save a note.",
                "parameters": SCHEMA["parameters"],
            },
        }

    def test_system_becomes_the_first_message(self):
        out = openai_messages([{"role": "user", "content": "hi"}], system="Be brief.")
        assert out[0] == {"role": "system", "content": "Be brief."}

    def test_arguments_travel_as_a_json_string(self):
        out = openai_messages(ROUND_TRIP)
        call = out[1]["tool_calls"][0]
        assert call["function"]["arguments"] == '{"title": "milk"}'
        assert out[1]["content"] is None
        assert out[2] == {"role": "tool", "tool_call_id": "c1", "content": "Saved."}


class _Recorder:
    """Stands in for an SDK client: records the request, returns what it was given."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []
        self.messages = self
        self.chat = NS(completions=self)

    def create(self, **request):
        self.requests.append(request)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def _claude_response(blocks, stop_reason="end_turn"):
    return NS(content=blocks, stop_reason=stop_reason,
              usage=NS(input_tokens=11, output_tokens=7))


class TestClaudeModel:
    def test_text_reply(self):
        client = _Recorder(_claude_response([
            NS(type="thinking", thinking="", signature="sig"),
            NS(type="text", text="Hello."),
        ]))
        reply = ClaudeModel(client=client).chat(
            [{"role": "user", "content": "hi"}], system="Be brief.",
        )
        assert reply["text"] == "Hello."
        assert reply["stop"] == "done"
        assert reply["usage"] == {"input": 11, "output": 7}
        request = client.requests[0]
        assert request["model"] == "claude-opus-5-5"
        assert request["system"] == "Be brief."
        assert "tools" not in request

    def test_tool_reply_and_replay(self):
        blocks = [NS(type="tool_use", id="toolu_1", name="add_note",
                     input={"title": "milk"})]
        client = _Recorder(
            _claude_response(blocks, "tool_use"),
            _claude_response([NS(type="text", text="Saved.")]),
        )
        model = ClaudeModel(client=client)
        messages = [{"role": "user", "content": "Remember milk"}]

        reply = model.chat(messages, tools=[SCHEMA])
        assert reply["stop"] == "tools"
        assert reply["tool_calls"] == [
            {"id": "toolu_1", "name": "add_note", "args": {"title": "milk"}}
        ]
        assert client.requests[0]["tools"][0]["input_schema"] == SCHEMA["parameters"]

        messages.append(reply["message"])
        messages.append({"role": "tool", "tool_call_id": "toolu_1", "content": "ok"})
        assert model.chat(messages, tools=[SCHEMA])["text"] == "Saved."
        sent = client.requests[1]["messages"]
        assert sent[1]["content"] is blocks, "the model's own turn goes back untouched"
        assert sent[2]["content"][0]["tool_use_id"] == "toolu_1"

    @pytest.mark.parametrize("stop_reason,stop", [
        ("max_tokens", "length"), ("refusal", "refused"), ("end_turn", "done"),
    ])
    def test_stop_reasons(self, stop_reason, stop):
        client = _Recorder(_claude_response([NS(type="text", text="x")], stop_reason))
        reply = ClaudeModel(client=client).chat([{"role": "user", "content": "hi"}])
        assert reply["stop"] == stop

    def test_sdk_errors_become_model_errors(self):
        import anthropic
        import httpx2 as httpx

        request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
        client = _Recorder(anthropic.APIConnectionError(request=request))
        with pytest.raises(ModelError) as caught:
            ClaudeModel(client=client).chat([{"role": "user", "content": "hi"}])
        assert caught.value.retryable


def _openai_response(content=None, tool_calls=None, finish_reason="stop"):
    return NS(
        choices=[NS(finish_reason=finish_reason,
                    message=NS(content=content, tool_calls=tool_calls))],
        usage=NS(prompt_tokens=11, completion_tokens=7),
    )


class TestOpenAIModel:
    def test_text_reply(self):
        client = _Recorder(_openai_response("Hello."))
        reply = OpenAIModel(client=client).chat(
            [{"role": "user", "content": "hi"}], system="Be brief.", max_tokens=50,
        )
        assert reply["text"] == "Hello."
        assert reply["stop"] == "done"
        assert reply["usage"] == {"input": 11, "output": 7}
        request = client.requests[0]
        assert request["messages"][0]["role"] == "system"
        assert request["max_completion_tokens"] == 50

    def test_tool_reply_parses_the_argument_string(self):
        call = NS(id="call_9", function=NS(name="add_note",
                                           arguments='{"title": "milk"}'))
        client = _Recorder(_openai_response(None, [call], "tool_calls"))
        reply = OpenAIModel(client=client).chat(
            [{"role": "user", "content": "Remember milk"}], tools=[SCHEMA],
        )
        assert reply["stop"] == "tools"
        assert reply["text"] == ""
        assert reply["tool_calls"] == [
            {"id": "call_9", "name": "add_note", "args": {"title": "milk"}}
        ]
        assert client.requests[0]["tools"][0]["type"] == "function"

    def test_unparseable_arguments_do_not_crash(self):
        call = NS(id="call_9", function=NS(name="add_note", arguments='{"title": '))
        client = _Recorder(_openai_response(None, [call], "tool_calls"))
        reply = OpenAIModel(client=client).chat([{"role": "user", "content": "x"}])
        assert reply["tool_calls"][0]["args"] == {"_unparsed_arguments": '{"title": '}

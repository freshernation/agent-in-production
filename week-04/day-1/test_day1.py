"""Week 4, Day 1 - a trace of every request.

Run me:  pytest week-04/day-1 -v
"""

import pytest

from desk.agent import run_agent
from desk.kit import SCHEMAS, TOOLS
from llm import FakeModel, ModelError, say, use

PRICE = {"input": 3.0, "output": 15.0}


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        self.now += 0.5
        return self.now


@pytest.fixture
def rec(load):
    return load("recorder.py")


class TestRecorder:
    def test_passes_the_reply_through(self, rec):
        recorder = rec.Recorder(FakeModel([say("Hello.")]), Clock())
        reply = recorder.chat([{"role": "user", "content": "hi"}])
        assert reply["text"] == "Hello."

    def test_records_a_generation(self, rec):
        recorder = rec.Recorder(FakeModel([say("Hello.", input=12, output=3)]), Clock())
        recorder.chat([{"role": "user", "content": "hi"}], system="Be brief.")
        assert recorder.spans == [{
            "type": "generation", "name": "model", "started": 0.5, "ended": 1.0,
            "input_messages": 1, "output": "Hello.", "tool_calls": [],
            "usage": {"input": 12, "output": 3}, "stop": "done",
        }]

    def test_passes_every_argument_on(self, rec):
        model = FakeModel([say("ok")])
        rec.Recorder(model, Clock()).chat([{"role": "user", "content": "hi"}],
                                          system="S", tools=SCHEMAS)
        assert model.last_request["system"] == "S"
        assert model.last_request["tools"]

    def test_a_failure_is_recorded_and_raised(self, rec):
        recorder = rec.Recorder(FakeModel([ModelError("overloaded")]), Clock())
        with pytest.raises(ModelError):
            recorder.chat([{"role": "user", "content": "hi"}])
        assert recorder.spans[0]["error"] == "ModelError: overloaded"


class TestTools:
    def test_a_recorded_tool(self, rec):
        recorder = rec.Recorder(FakeModel(), Clock())
        tools = rec.record_tools(TOOLS, recorder)
        assert tools["calculate"](expression="6*7") == "42"
        assert recorder.spans == [{"type": "tool", "name": "calculate",
                                   "args": {"expression": "6*7"}, "result": "42",
                                   "started": 0.5, "ended": 1.0}]

    def test_each_wrapper_keeps_its_own_name(self, rec):
        recorder = rec.Recorder(FakeModel(), Clock())
        tools = rec.record_tools(TOOLS, recorder)
        tools["list_titles"]()
        tools["calculate"](expression="1+1")
        names = []
        for span in recorder.spans:
            names.append(span["name"])
        assert names == ["list_titles", "calculate"]


class TestInTheAgent:
    def test_a_whole_run_becomes_spans(self, rec):
        recorder = rec.Recorder(FakeModel([use("calculate", {"expression": "2+2"}, id="c1"),
                                           say("It is 4.")]), Clock())
        run_agent(recorder, "What is 2+2?", SCHEMAS, rec.record_tools(TOOLS, recorder))
        kinds = []
        for span in recorder.spans:
            kinds.append((span["type"], span["name"]))
        assert kinds == [("generation", "model"), ("tool", "calculate"), ("generation", "model")]


class TestCost:
    def test_per_million(self, rec):
        assert rec.cost({"input": 1_000_000, "output": 0}, PRICE) == 3.0
        assert rec.cost({"input": 1000, "output": 1000}, PRICE) == pytest.approx(0.018)


class TestBuildTrace:
    def spans(self):
        return [
            {"type": "generation", "name": "model", "started": 1.0, "ended": 2.0,
             "usage": {"input": 1000, "output": 100}},
            {"type": "tool", "name": "calculate", "started": 2.0, "ended": 2.1},
            {"type": "generation", "name": "model", "started": 2.1, "ended": 3.5,
             "usage": {"input": 1200, "output": 40}},
        ]

    def test_the_whole_trace(self, rec):
        trace = rec.build_trace("t1", "alice", "c1", "What is 2+2?", "4", self.spans(), PRICE)
        assert trace["usage"] == {"input": 2200, "output": 140}
        assert trace["cost"] == 0.0087
        assert trace["duration"] == 2.5
        assert trace["error"] is False
        assert trace["user"] == "alice" and trace["session"] == "c1"
        assert trace["input"] == "What is 2+2?" and trace["output"] == "4"

    def test_an_error_anywhere(self, rec):
        spans = self.spans() + [{"type": "generation", "name": "model", "started": 4.0,
                                 "ended": 4.1, "error": "ModelError: x"}]
        assert rec.build_trace("t", "a", "s", "q", "", spans, PRICE)["error"] is True

    def test_no_spans(self, rec):
        trace = rec.build_trace("t", "a", "s", "q", "", [], PRICE)
        assert trace["duration"] == 0.0 and trace["cost"] == 0.0

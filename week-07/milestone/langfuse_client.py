"""Sends traces and scores to Langfuse - given.

The one file in this course that talks to a tracing platform. It is written
against the Langfuse Python SDK, version 4, and checked against its documentation
on 2026-10-14. It is not exercised by the tests: they use a fake client with the
same three methods. Run it once, by hand, against your own project:

    pip install "langfuse>=4,<5"
    export LANGFUSE_PUBLIC_KEY=pk-lf-...  LANGFUSE_SECRET_KEY=sk-lf-...
    export LANGFUSE_BASE_URL=https://cloud.langfuse.com

Your trace ids are 32 hex characters (uuid4().hex), which is exactly the form
Langfuse uses, so they are passed through as the trace id. The id in your
database and the id on the platform are the same id.
"""


class LangfuseClient:
    def __init__(self):
        from langfuse import get_client, propagate_attributes

        self.langfuse = get_client()
        self.propagate_attributes = propagate_attributes

    def trace(self, trace: dict) -> None:
        with self.langfuse.start_as_current_observation(
            as_type="span", name="chat", input=trace["input"],
            trace_context={"trace_id": trace["id"]},
        ) as root:
            with self.propagate_attributes(user_id=trace["user"], session_id=trace["session"]):
                for span in trace["spans"]:
                    if span["type"] == "generation":
                        with self.langfuse.start_as_current_observation(
                            as_type="generation", name=span["name"],
                        ) as generation:
                            generation.update(
                                output=span.get("output", span.get("error", "")),
                                usage_details={
                                    "input_tokens": span.get("usage", {}).get("input", 0),
                                    "output_tokens": span.get("usage", {}).get("output", 0),
                                },
                            )
                    else:
                        with self.langfuse.start_as_current_observation(
                            as_type="span", name=span["name"], input=span.get("args"),
                        ) as tool:
                            tool.update(output=span.get("result"))
            root.update(output=trace["output"])

    def score(self, trace_id: str, name: str, value: int, comment: str) -> None:
        self.langfuse.create_score(name=name, value=float(value), trace_id=trace_id,
                                   comment=comment or None, data_type="NUMERIC")

    def flush(self) -> None:
        self.langfuse.flush()

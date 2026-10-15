# Week 4 — Concept fence

## Allowed

**Everything from weeks 1 to 3**, plus:

- A class that stands in for another (`Recorder` in place of the model)
- SQL: `GROUP BY`, `SUM`, `COUNT`, `COALESCE`, `JOIN`
- `uuid.uuid4().hex` as a trace id
- The Langfuse Python SDK, through the given `langfuse_client.py` only
- `json` for storing a whole record in one column

## Not yet

OpenTelemetry directly · dashboards and alerts (week 6) · storing full prompts ·
sampling · Docker and deployment (week 5) · model-graded evaluation of traces

---

## Why you do not store the full prompts

A trace that holds every message a user sent is a copy of everything they ever told
Desk, in a second system, readable by whoever can open the dashboard. Some teams do
it, deliberately and with a retention rule. This week you record counts, names,
timings and costs, and the user's own words only where they rated an answer. Storing
more is a decision, not a default.

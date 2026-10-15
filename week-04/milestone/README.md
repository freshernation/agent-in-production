# Week 4 Milestone — Every request traced

> Every chat and every background task leaves a trace with its spans and cost, users can
> rate answers, and both reach Langfuse without slowing anyone down.

---

## The files

| File | Where it comes from |
|---|---|
| `store.py`, `migrate.py`, `tenancy.py`, `permissions.py`, `jobs.py`, `worker.py`, `limits.py` | **copy from your week 3 milestone** |
| `recorder.py`, `tracestore.py`, `feedback.py`, `exporter.py` | **copy from this week's days** |
| `langfuse_client.py`, `run_exporter.py` | given |
| `app.py` | your week 3 milestone, traced |
| `FIND_IT.md` | how you find one request |

## `app.py`

| Change | What it means |
|---|---|
| `PRICE` | your model's price per million tokens, input and output |
| `take_turn(...)` returns `(answer, trace)` | the model wrapped in a `Recorder`, the tools in `record_tools`, the trace built and **saved even when the run fails** |
| `ChatOut.trace_id`, and the `X-Trace-Id` header | the id a user quotes when something goes wrong |
| `POST /feedback` | `{"trace_id", "score", "comment"}`; 422 for a score that is not 1 or -1; 404 for somebody else's trace |
| `export_once(db_path, client)` | what `run_exporter.py` calls every thirty seconds |

Three processes now: the server, the worker, and the exporter.

## `FIND_IT.md`

A user says Desk deleted the wrong note at about 3pm yesterday. Four sections, forty
words or more each: how you narrow it down, what the trace shows, what it cannot
show, and what happens next.

---

## Check it

```bash
pytest week-04/milestone -v
```

## Friday

Your instructor makes three requests and asks you to find the second one.

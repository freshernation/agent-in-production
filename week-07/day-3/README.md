# Day 3 — One trace, two processes

> **By the end of today** a tool call that crosses into an MCP server shows up as one
> trace, with the server's work nested under the call that caused it.

---

## Read first

- [ ] W3C — [Trace Context](https://www.w3.org/TR/trace-context/), sections 3.2 and 3.3 · 15 min
- [ ] MCP Python SDK — [OpenTelemetry](https://py.sdk.modelcontextprotocol.io/run/opentelemetry/) · 10 min

---

## What you need to know

### The problem

Week 4's trace stops at the edge of your process. When Desk calls a tool on another
server, the trace says "called lookup, took 2 seconds" — and the server's own record
of those 2 seconds is somewhere else, with nothing to join them.

### One header joins them

The caller sends `traceparent`: the trace id and the id of the span making the call.
The server records its work under that trace id, pointing at that span. Afterwards
the two halves stitch into one picture. In MCP the header travels in the request's
`_meta`.

### The far side does not trust it

A traceparent comes from a caller, so it is input. A malformed one is not a trace id;
it is a reason to start the server's record without one. A server span with no trace
is an **orphan**, and counting orphans tells you how much of the server's work you
cannot explain.

### You are building what the SDK does

The MCP SDK already sends and reads trace context, through OpenTelemetry, once an
OpenTelemetry SDK is installed. Today you do it by hand, so that when the automatic
version shows you a nested span, you know what it is made of. Use one or the other:
with both, two traceparents compete.

---

## Exercises

```bash
pytest week-07/day-3 -v
```

Write `crossing.py`. One function is `async` — read the client example in the
day 1 links again first.

---

## Predict-then-run

Call `lookup` once with `call_traced` and once with a plain `client.call_tool`.
Predict what `orphans` says. Then send a traceparent with capital letters.

---

## Before you close the laptop

Commit, push, fill in the signal log.

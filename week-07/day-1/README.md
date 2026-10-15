# Day 1 — Desk's tools, over MCP

> **By the end of today** any MCP host can list and use Desk's notes, the SDK
> refuses bad arguments before your code runs, and the one dangerous tool is not
> on offer.

---

## Read first

- [ ] MCP — [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture) · 15 min
- [ ] MCP Python SDK — [Get started](https://py.sdk.modelcontextprotocol.io/get-started/) and [Testing](https://py.sdk.modelcontextprotocol.io/get-started/testing/) · 20 min

---

## What you need to know

### What MCP is

A standard way for an AI application (the host) to find and call tools that live in
another process (the server). You have been writing tools since the agent course;
MCP is the agreement on how one program offers them to another.

### The function is the tool

With `MCPServer`, a function's name is the tool's name, its docstring is the
description and its type hints are the schema. `Annotated[str, Field(max_length=100)]`
puts a limit in the schema, and the SDK refuses a call that breaks it before your
function runs.

### Choose what not to serve

Desk asks a person before it deletes a note. An MCP server has no way to ask that
person — the host might, or might not. So `delete_note` is not served. Deciding
what a server **does not** offer is the most important line in it.

### Who is the user?

This server runs on your machine, started by your MCP host, and acts as whoever
`DESK_USER` names. That is fine locally, where the person who starts it is the
person whose notes they are. On the internet it would be a hole: see the deep track.

### Testing without a process

`Client(server)` connects to a server object in the same process, with no subprocess
and no port. The tests do it; so can you, in a Python shell.

---

## Exercises

```bash
pytest week-07/day-1 -v
```

Copy `store.py`, then write `desk_mcp.py`. `run_mcp.py` is given.

---

## Predict-then-run

Add the server to an MCP host — for Claude Code:

```bash
claude mcp add desk -e DESK_USER=you -e DESK_DB=/full/path/desk.db -- python3 /full/path/week-07/day-1/run_mcp.py
```

Predict which tools the host lists. Ask it to delete a note. What happens?

---

## Before you close the laptop

Commit, push, fill in the signal log.

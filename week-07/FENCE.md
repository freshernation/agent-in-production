# Week 7 — Concept fence

## Allowed

**Everything from weeks 1 to 6**, plus:

- The MCP Python SDK: `MCPServer`, `@server.tool()`, `Context`, `Client`
- `Annotated[...]` with Pydantic's `Field` for a tool's argument limits
- `async def`, `await` and `async with` — for the MCP client only
- `anyio.run`
- The W3C `traceparent` format, and a regular expression to check it
- A GitHub Actions job with `env` from `secrets`, and `needs` with a list

## Not yet

MCP over HTTP with OAuth (deep track) · resources, prompts, sampling and
elicitation · connecting an untrusted MCP server to the deployed Desk · an
OpenTelemetry SDK and exporter · red-teaming tools and generated attacks

---

## Why the MCP server is local

Serving Desk's tools over HTTP means another way in, with its own authentication,
and the MCP authorization specification is a week on its own. A local server over
stdio runs as the person who started it, against their own notes, with no network
in between. It is the right first server; putting it behind your API key on the
live service is the deep track.

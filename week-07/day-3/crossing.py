# Day 3 - one trace, two processes.
#
# A W3C traceparent is one string: "00-<trace id>-<span id>-01"
#   trace id   32 lowercase hex characters (your week 4 trace ids already are)
#   span id    16 lowercase hex characters
#
#   traceparent(trace_id, span_id) -> str
#
#   parse_traceparent(value) -> (trace_id, span_id) | None
#       None for anything that is not exactly that shape - not a string, the
#       wrong version, wrong lengths, capitals - and for an all-zero trace id
#       or span id, which the standard says is invalid.
#
#   build_server(spans, clock) -> MCPServer
#       the far side. A server named "Lookup" with one tool:
#           lookup(word, ctx: Context) -> f"{word}: a word worth knowing."
#       (from mcp.server.mcpserver import Context; ctx is not part of the
#       tool's schema - the SDK fills it in). The request's metadata is
#       ctx.request_context.meta (it may be None). Parse its "traceparent" and
#       append to `spans`:
#           {"trace_id": ..., "parent": <the span id>, "name": "lookup",
#            "started": ..., "ended": ...}
#       with trace_id and parent both None when there was no valid traceparent.
#
#   async call_traced(client, name, args, trace_id, spans, clock) -> str
#       the near side. Make a new span id (secrets.token_hex(8)), call the tool
#       with meta={"traceparent": ...}, and append to `spans`:
#           {"type": "tool", "name": name, "span_id": ..., "args": dict(args),
#            "result": <text>, "started": ..., "ended": ...}
#       plus "error": <text> if result.is_error. Return the text of the
#       result's first content block.
#
#   stitch(client_spans, server_spans, trace_id) -> list
#       the client's spans, then each server span with this trace_id as
#           {"type": "server", "name", "parent", "started", "ended"}
#
#   orphans(server_spans) -> int
#       how many server spans could not be placed in any trace

# Day 4 - send it to the platform, and turn a bad trace into an eval case.
#
# Copy tracestore.py and feedback.py from days 2 and 3.
#
# A `client` is anything with three methods. In the tests it is a fake. In real
# use it is langfuse_client.LangfuseClient (given):
#     client.trace(trace)                              send one trace
#     client.score(trace_id, name, value, comment)     attach a score to one
#     client.flush()                                   send what is buffered
#
#   export_pending(db, client) -> {"traces": n, "scores": n, "failed": n}
#       1. Every trace with exported = 0, oldest first: client.trace(the trace
#          as a dict). Mark it exported = 1. If the client raises, count it as
#          failed, leave it at 0 for next time, and carry on with the rest.
#       2. Every feedback row with exported = 0 WHOSE TRACE HAS BEEN EXPORTED:
#          client.score(trace_id, "user-feedback", score, comment), then mark
#          it 1. A score for a trace the platform has not seen goes nowhere.
#          Same rule for failures.
#       3. client.flush(), always.
#
#   to_case(trace, comment) -> dict
#       a DRAFT eval case for Agent From Zero's week 8 suite:
#         {"name": "from trace <id>", "task": <trace input>, "notes": [],
#          "expect": {},
#          "seen": {"calls": <each tool used, once, first-use order>,
#                   "answer": <trace output>},
#          "why": <the user's comment>}
#       "expect" is empty on purpose. What SHOULD have happened is a judgement,
#       and it is yours to write.

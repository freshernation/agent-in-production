# Day 1 - a trace of every request: what the model was asked, what it did, what it cost.
#
#   class Recorder(model, clock)
#       Stands in for the model. run_agent calls recorder.chat(...) exactly as it
#       would call model.chat(...), and never knows the difference.
#       .spans                    a list, empty to start with
#       .chat(messages, system=None, tools=None, max_tokens=None)
#           call the real model with the same arguments, append one span, and
#           return the reply unchanged:
#             {"type": "generation", "name": "model", "started": <clock()>,
#              "ended": <clock()>, "input_messages": <len(messages)>,
#              "output": <reply text>, "tool_calls": [<names>],
#              "usage": <copy of reply["usage"]>, "stop": <reply["stop"]>}
#           If the model raises: append {"type": "generation", "name": "model",
#           "started", "ended", "error": "<ErrorType>: <message>"} and re-raise.
#
#   recorded(function, name, recorder)
#       a function that runs the tool and appends
#         {"type": "tool", "name", "args": <copy>, "result": <str(result)>,
#          "started", "ended"}
#       then returns the result. (Agent From Zero week 8's `watched`, again.)
#   record_tools(tools, recorder)   a new table, every tool recorded
#
#   cost(usage, price) -> float
#       usage {"input": tokens, "output": tokens}; price {"input": $, "output": $}
#       per MILLION tokens. Dollars.
#
#   build_trace(trace_id, user, session, task, answer, spans, price) -> dict
#       {"id", "user", "session", "input": task, "output": answer, "spans",
#        "usage": <generation usage added up>, "cost": <rounded to 6 places>,
#        "duration": <last span's end minus first span's start, to 3 places;
#                     0.0 with no spans>,
#        "error": <True if any span has an "error">}

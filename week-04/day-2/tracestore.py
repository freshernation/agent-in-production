# Day 2 - traces you can search: one person's afternoon, the dearest user, the slowest request.
#
#   SCHEMA      CREATE TABLE IF NOT EXISTS traces:
#                 id TEXT PRIMARY KEY, user TEXT, session TEXT, started REAL,
#                 duration REAL, cost REAL, tokens INTEGER, error INTEGER,
#                 body TEXT (the whole trace as JSON),
#                 exported INTEGER NOT NULL DEFAULT 0
#               every column not null
#
#   create_tables(db)
#   save(db, trace, started)       a trace from day 1's build_trace. tokens is
#                                  input + output; error is 0 or 1.
#   get(db, trace_id) -> dict | None
#
# The questions an incident asks. Every list is of trace ids.
#   for_user(db, user, start, end)       that user's traces with
#                                        start <= started < end, oldest first
#   session(db, user, session_id)        one conversation's traces, oldest first
#   costs_by_user(db, start, end)        {user: total cost, rounded to 6}, for
#                                        traces in that window
#   slowest(db, n)                       the n longest, longest first; ties by
#                                        earlier start
#   error_rate(db, start, end) -> float  errors / traces in the window, to 3
#                                        places; 0.0 when there are none
#
# The columns pulled out of the JSON are the ones you search by. The body keeps
# everything else.

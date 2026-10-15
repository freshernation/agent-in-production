# Day 3 - what the user thought, tied to the trace it is about.
#
# Copy tracestore.py from day 2 into this folder.
#
#   SCHEMA      CREATE TABLE IF NOT EXISTS feedback:
#                 trace_id TEXT PRIMARY KEY, user TEXT, score INTEGER,
#                 comment TEXT default '', exported INTEGER default 0
#               every column not null
#   create_tables(db)
#
#   rate(db, user, trace_id, score, comment="") -> str
#       score must be 1 or -1: anything else is a ValueError.
#       A trace that does not exist, or belongs to somebody else:
#       "No such trace." - the same words for both.
#       Otherwise store it and return "Thanks." Rating the same trace again
#       replaces the score and the comment, and sets exported back to 0 so the
#       change is sent again. The comment is stripped of surrounding spaces.
#
#   summary(db) -> {"up": <count of 1s>, "down": <count of -1s>}
#
#   bad_traces(db) -> list[str]
#       the ids of every trace rated -1, newest trace first

# Day 1 - what to wake somebody up for, and how not to cry wolf.
#
# Copy tracestore.py from week 4 day 2 into this folder.
#
#   percentile(values, p) -> float
#       nearest rank: sort the values, take the one at position ceil(p/100 * n),
#       counting from 1 (and never below 1). 0.0 for no values.
#       percentile([1, 2, 3, 4], 50) is 2. percentile([1, 2, 3, 4], 95) is 4.
#
#   measure(db, start, end) -> dict
#       over the traces with start <= started < end:
#       {"requests": n, "error_rate": errors / n to 3 places (0.0 for none),
#        "p95_seconds": percentile of the durations, "cost": total to 6 places}
#
#   A rule is a dict:
#       {"name": "errors", "metric": "error_rate", "above": 0.05, "min_requests": 20}
#
#   firing(rules, measured) -> list[str]
#       the names, in order, of the rules whose metric is ABOVE its threshold -
#       skipping any rule whose min_requests (default 1) is more than the number
#       of requests measured. One failure in two requests is 50%, and not news.
#
#   class Pager(send, cooldown)
#       send(message) is how a message reaches a person - injected.
#       .alert(name, message, now) -> bool
#           send "[name] message" and return True - unless the same alert was
#           sent less than `cooldown` seconds ago, in which case send nothing
#           and return False. An alert repeated every minute gets muted, and
#           then the real one is missed.
#       .resolve(name)
#           forget that alert, so the next time it fires it is sent at once

# Day 4 - a daily cost budget per user.
#
# Copy tracestore.py from week 4 day 2 into this folder.
#
#   day_start(now) -> float
#       the most recent midnight UTC at or before `now` (a Unix time).
#       There are 86400 seconds in a day, and Unix time 0 was a midnight.
#
#   spent_today(db, user, now) -> float
#       the total cost of this user's traces from day_start(now) up to and
#       including now, rounded to 6 places. 0.0 for none.
#
#   check_budget(db, user, limit, now) -> str | None
#       None while they have spent less than `limit` today.
#       Otherwise the message they are shown, exactly:
#           "You have used today's budget of $1.00. It resets at midnight UTC."
#       (the limit to two decimal places)
#
#   overshoot(token_budget, price) -> float
#       The check runs BEFORE a turn, so one turn can still go over. How far?
#       At most every token in Desk's token budget, priced as output:
#       token_budget * price["output"] / 1,000,000.

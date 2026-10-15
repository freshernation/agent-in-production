"""The numbers for your cost review, from a trace store - given.

    python3 numbers.py path/to/desk.db

Run it on a copy of your production database (take one from your host's shell,
or a backup), or on a week of your own use if production is quiet. It reads the
traces table from week 4 and nothing else.
"""

import sqlite3
import sys


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(1, -(-len(ordered) * p // 100))
    return ordered[int(rank) - 1]


def summarise(db: sqlite3.Connection) -> dict:
    rows = db.execute("SELECT user, started, duration, cost, tokens, error FROM traces").fetchall()
    if not rows:
        return {"requests": 0}
    durations = [row[2] for row in rows]
    costs = [row[3] for row in rows]
    per_user_day: dict[tuple, float] = {}
    for user, started, _, cost, _, _ in rows:
        key = (user, int(started // 86400))
        per_user_day[key] = per_user_day.get(key, 0.0) + cost
    days = len({key[1] for key in per_user_day})
    return {
        "requests": len(rows),
        "days": days,
        "error_rate": round(sum(row[5] for row in rows) / len(rows), 3),
        "p50_seconds": round(percentile(durations, 50), 2),
        "p95_seconds": round(percentile(durations, 95), 2),
        "cost_per_request": round(sum(costs) / len(rows), 5),
        "p95_cost_per_request": round(percentile(costs, 95), 5),
        "tokens_per_request": round(sum(row[4] for row in rows) / len(rows)),
        "cost_per_day": round(sum(costs) / days, 4),
        "most_one_user_spent_in_a_day": round(max(per_user_day.values()), 4),
    }


def main() -> None:
    db = sqlite3.connect(sys.argv[1] if len(sys.argv) > 1 else "desk.db")
    for name, value in summarise(db).items():
        print(f"{name:32} {value}")


if __name__ == "__main__":
    main()

# Week 2 — Concept fence

## Allowed

**Everything from week 1**, plus:

- `sqlite3`: `connect`, `execute`, `fetchone`, `fetchall`, `isolation_level=None`
- SQL: `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `WHERE`, `ORDER BY`,
  `PRIMARY KEY`, `COLLATE NOCASE`, `LIKE`, `ALTER TABLE ... ADD COLUMN`,
  `INSERT ... ON CONFLICT ... DO UPDATE`
- `BEGIN`, `COMMIT`, `ROLLBACK`
- `?` parameters — always
- A FastAPI dependency that `yield`s
- Sets: `<` and `|`

## Not yet

Postgres and Docker (week 5) · an ORM such as SQLAlchemy · `async` · background
work · indexes and query plans · sharing a connection between requests

---

## Why no ORM

An ORM writes the SQL for you. That is useful once you can read the SQL it writes,
and dangerous before. Every query this week is one line you can read, and every one
of them says whose data it touches. When you meet an ORM at work, you will know what
it is doing.

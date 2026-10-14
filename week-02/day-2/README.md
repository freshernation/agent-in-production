# Day 2 — Changing the shape without losing anything

> **By the end of today** you can add a table or a column to a database that already
> has people's data in it, and a failure halfway leaves nothing broken.

---

## Read first

- [ ] SQLite — [Transactions](https://www.sqlite.org/lang_transaction.html) · 10 min
- [ ] SQLite — [ALTER TABLE](https://www.sqlite.org/lang_altertable.html), the part on ADD COLUMN · 5 min

---

## What you need to know

### The database outlives the code

Yesterday's `CREATE TABLE IF NOT EXISTS` works once. The day you need a new column,
`IF NOT EXISTS` sees the table and does nothing, and your code asks for a column
that is not there.

### A migration is one change, numbered

```python
MIGRATIONS = [
    "CREATE TABLE notes (...)",
    "CREATE TABLE conversations (...)",
    "ALTER TABLE notes ADD COLUMN created TEXT NOT NULL DEFAULT ''",
]
```

The database remembers how many have run, in a table called `schema_version`. On
start, run the ones after that. **Never edit a migration that has run anywhere.**
Somebody's database already has it. Add a new one at the end.

### All of it, or none of it

```python
db.execute("BEGIN")
try:
    db.execute(migration)
    db.execute("INSERT INTO schema_version (version) VALUES (?)", (number,))
    db.execute("COMMIT")
except Exception:
    db.execute("ROLLBACK")
    raise
```

A transaction makes two statements one. The migration and the record that it ran
either both happen or neither does. Without it, a migration that ran but was not
recorded runs again tomorrow, and fails. SQLite can roll back `CREATE TABLE` and
`ALTER TABLE` too, which not every database can.

### Running it twice does nothing

Every server start runs `migrate`. That is the point: the second run finds nothing
new and returns 0.

---

## Exercises

```bash
pytest week-02/day-2 -v
```

Write `migrate.py`: `MIGRATIONS`, `current_version(db)` and `migrate(db, migrations)`.

---

## Predict-then-run

Run your three migrations on a database. Now edit the first one to add a column and
run `migrate` again. Predict what happens to the database — and to a teammate's
database that already ran the old first migration.

---

## Before you close the laptop

Commit, push, fill in the signal log.

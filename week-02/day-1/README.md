# Day 1 — Every query says whose

> **By the end of today** Desk's notes live in a database, two users' notes never
> mix, and two writers at once do not corrupt anything.

---

## Read first

- [ ] Python — [`sqlite3`](https://docs.python.org/3/library/sqlite3.html), the tutorial and "How to use placeholders" · 25 min
- [ ] SQLite — [SQL as understood by SQLite: CREATE TABLE](https://www.sqlite.org/lang_createtable.html), the parts on PRIMARY KEY and COLLATE · 10 min

---

## What you need to know

### A JSON file has one writer

Desk's notes were a JSON file: read it all, change it, write it all back. Two
requests at the same moment both read, both write, and one of them wins. The other's
note is gone and nothing said so. A database exists to make that impossible.

### A table, and whose each row is

```sql
CREATE TABLE IF NOT EXISTS notes (
    user  TEXT NOT NULL,
    title TEXT NOT NULL COLLATE NOCASE,
    body  TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (user, title)
)
```

`(user, title)` together are the key: Alice can have a note called *milk*, and so can
Bob, but Alice cannot have two. `COLLATE NOCASE` makes *Milk* and *milk* the same
title, as the old kit did.

### Every query says whose

```python
db.execute("SELECT title FROM notes WHERE user = ? ORDER BY rowid", (user,))
```

Every single one. A query without `WHERE user = ?` is the most common way a
many-user system shows one person another's data.

### Values go in as `?`, always

```python
db.execute("INSERT INTO notes (user, title, body) VALUES (?, ?, ?)", (user, title, body))
```

Never `f"... WHERE user = '{user}'"`. A user called `x' OR '1'='1` turns that into a
query that matches everyone. With `?`, the value is a value and cannot become SQL.
This is **SQL injection**, and it is the same lesson as prompt injection: text from
outside must never be treated as instructions.

### Let the database catch the duplicate

You could check whether *milk* exists, then insert. Between the check and the insert,
another request can insert it. Instead, insert, and let the primary key refuse:

```python
try:
    db.execute("INSERT ...", ...)
except sqlite3.IntegrityError:
    return f"There is already a note called '{title}'."
```

### Saved when it runs

`sqlite3.connect(path, isolation_level=None)` saves each statement as soon as it
runs. Tomorrow you take control of that with `BEGIN` and `COMMIT`.

---

## Exercises

```bash
pytest week-02/day-1 -v
```

Write `store.py`: `SCHEMA`, `connect`, `create_tables`, and the four tools with a
`user` argument. The sentences are the old kit's; the rules are in the file.

---

## Predict-then-run

Open the database with `sqlite3 desk.db` and run `SELECT * FROM notes;`. Add a note
for a user called `x' OR '1'='1` through your code. Predict what the table shows.

---

## Before you close the laptop

Commit, push, fill in the signal log.

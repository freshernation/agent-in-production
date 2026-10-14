# Week 2 — State that survives

> **Destination**
> Many people use Desk at once, each with their own notes and conversations, each
> allowed to do only what their role allows — and restarting the server loses
> nothing.

On Friday your instructor restarted your server and every conversation vanished.
This week they go into a database.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Keep notes in SQLite, where every query says whose they are |
| Tue | `day-2/` | Change a database's shape without losing what is in it |
| Wed | `day-3/` | Give each user tools that cannot reach anyone else's notes, and store conversations |
| Thu | `day-4/` | Decide what each user may make Desk do |
| Fri | `milestone/` | Ship Desk for many users, and survive a restart in front of an audience |

---

## Why SQLite, and not Postgres

SQLite is a database in one file, built into Python. Nothing to install, nothing to
run, and the SQL is the same SQL. Everything you learn this week carries straight
across. Postgres arrives in week 5, when Docker does, because that is when you need
a database that runs somewhere other than your laptop.

---

## The rule of the week

**Every query says whose.** A note belongs to somebody. A conversation belongs to
somebody. There is no query in this course without `WHERE user = ?` — and the user
always comes from the key, never from anything the model wrote.

---

## Outside-view question

> *A bank keeps two copies of every account and still knows which one is right. How,
> and what happens when they disagree?*

# Day 1 — The Python you skipped

> **By the end of today** you can read FastAPI code, because you can write the three
> things it is built from: classes, type hints and decorators.

Agent From Zero cut classes, type hints and decorators on purpose, and said why: your
`run_agent` grew to fourteen arguments so you would feel the need for something
better. FastAPI uses all three on every line. Today is the catch-up, and it is one
day because you already know the hard part.

---

## Read first

- [ ] Python tutorial — [Classes](https://docs.python.org/3/tutorial/classes.html), sections 9.3 and 9.4 · 25 min
- [ ] FastAPI — [Python types intro](https://fastapi.tiangolo.com/python-types/) · 15 min

---

## What you need to know

### A class is a dictionary with functions attached

You have been passing dictionaries around for nine weeks:

```python
note = {"title": "milk", "body": "two litres"}
```

A class gives that shape a name, and puts the functions that work on it next to it:

```python
class Note:
    def __init__(self, title, body=""):
        self.title = title
        self.body = body

    def summary(self):
        return f"{self.title}: {self.body}"

note = Note("milk", "two litres")
note.summary()            # "milk: two litres"
```

`__init__` runs when you write `Note(...)`. `self` is the note being made, or the
note a method was called on. Store things on `self`, not on the class, or every note
shares them.

### Type hints say what goes in and what comes out

```python
def summary(self, width: int = 30) -> str:
```

Python does not check them when your code runs. Two things do: your editor, and
FastAPI — which reads them to decide what a request must contain. That is why this
course needs them.

### A decorator is a function that wraps a function

You wrote one in Agent From Zero week 8 without the name: `watched` took a tool and
returned a new function that did something first, then called it. A decorator is
exactly that, with a shorter way to apply it:

```python
@logged
def add_note(title):
    ...
```

means `add_note = logged(add_note)`. `functools.wraps` copies the original's name
onto the wrapper — FastAPI uses names to label routes, so it matters.

### Pydantic: a class that checks itself

```python
class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=80)
```

Make one with bad data and it raises, saying which field and why. Tomorrow FastAPI
does that for every request, before your code runs.

---

## Exercises

```bash
pytest week-01/day-1 -v
```

Write `basics.py`:

| Name | What it is |
|---|---|
| `Note(title, body="")` | a class; `title` stripped of surrounding spaces |
| `.summary(width=30)` | `"milk: two litres"`, or the body cut to `width` characters and `...` |
| `.matches(word)` | `True` when the word is in the title or body, ignoring capitals |
| `CALLS` | an empty list |
| `logged(function)` | a decorator: appends the function's name to `CALLS`, then calls it. Use `functools.wraps` |
| `NoteIn` | pydantic: `title` 1–80 characters, `body` up to 2000, default `""` |

Every method has type hints. A test checks.

---

## Predict-then-run

Make two `Note`s, then add `count = 0` inside the class and `Note.count += 1` in
`__init__`. Predict what `Note("a").count` is after making three notes. Then try it.

---

## Before you close the laptop

Commit, push, fill in the signal log.

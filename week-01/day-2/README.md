# Day 2 — The smallest service

> **By the end of today** you have a service that answers HTTP requests, refuses bad
> ones before your code runs, and chooses its status codes on purpose.

---

## Read first

- [ ] FastAPI — [First steps](https://fastapi.tiangolo.com/tutorial/first-steps/) and [Request body](https://fastapi.tiangolo.com/tutorial/body/) · 25 min
- [ ] MDN — [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) — skim the list, read 200, 201, 204, 401, 404, 409, 422, 503 · 10 min

---

## What you need to know

### A route is a function with a decorator

```python
app = FastAPI()

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
```

Run it with `uvicorn service:app --reload` and open `http://127.0.0.1:8000/health`.
Then open `/docs`: FastAPI built that page from your type hints.

### A request body is a pydantic model

```python
@app.post("/notes", status_code=201)
def add(note: NoteIn) -> dict:
    ...
```

FastAPI reads `note: NoteIn`, parses the JSON, and validates it. A missing title is a
**422** with the field named, and **your function never runs.** You wrote no code for
that.

### Choose the status code

| Code | Means | Here |
|---|---|---|
| 201 | created | a new note |
| 204 | done, nothing to send back | a delete |
| 404 | no such thing | an unknown title |
| 409 | conflicts with what is there | a duplicate title |
| 422 | the request itself is wrong | FastAPI, from your model |

4xx means the caller has something to fix. 5xx means you do. Choosing right is what
lets the caller handle errors sensibly.

```python
raise HTTPException(status_code=409, detail="There is already a note called 'milk'.")
```

### Make the app in a function

```python
def create_app() -> FastAPI:
    app = FastAPI()
    notes = {}
    ...
    return app
```

Each call makes a new app with its own notes. That is what lets every test start
clean — and tomorrow it is how you hand the app a model.

### Testing without a server

```python
client = TestClient(create_app())
client.post("/notes", json={"title": "milk"})
```

No port, no network. Every test in this course works this way.

---

## Exercises

```bash
pytest week-01/day-2 -v
```

Write `service.py`. The routes, and what each returns, are in the file's comments.
Titles are matched ignoring capitals.

---

## Predict-then-run

Start the server and `curl -i -X POST localhost:8000/notes -H 'content-type: application/json' -d '{}'`.
Predict the status code and the body before you press enter. Then read the body: who
wrote that message?

---

## Before you close the laptop

Commit, push, fill in the signal log.

# Week 1 — Concept fence

## Allowed

**Everything from Agent From Zero**, plus:

- Classes: `class`, `__init__`, `self`, methods
- Type hints on arguments and return values, including `str | None` and `dict[str, str]`
- Decorators, and `functools.wraps`
- Pydantic: `BaseModel`, `Field`
- FastAPI: `FastAPI()`, `@app.get`, `@app.post`, `@app.delete`, `HTTPException`,
  `Header`, `Depends`, `Response`, `status_code=`
- `fastapi.testclient.TestClient`
- `uuid`, `secrets.compare_digest`
- `uvicorn` to run it

## Not yet

Databases — conversations live in a dictionary this week, and are lost on restart ·
`async` · background work · streaming · logging and tracing · Docker · deploying
anywhere · per-user permissions on tools

---

## Why a dictionary, when it is lost on restart

Because you should feel the restart lose everything before you are handed the fix.
On Friday someone will restart your server during the defence. Next week is the
answer.

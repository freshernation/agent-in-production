# Week 7 Milestone — Connected, and attacked

> Desk's notes through MCP, and no deploy without the attack suite's rate.

---

## The files

| File | Where it comes from |
|---|---|
| everything from your week 6 milestone | **copy** |
| `desk_mcp.py`, `attacks.py` | **copy from this week's days** |
| `run_mcp.py`, `run_attacks.py` | given |
| `ci.yml` | week 6's, with an `attacks` job the deploy waits for |
| `ATTACKS.md` | new |

`app.py` does not change this week.

## `ci.yml`

Three jobs. `checks` on every push. `attacks` on a push to `main`, with your
provider's key from a secret and `ATTACK_LIMIT` set. `deploy` with
`needs: [checks, attacks]`.

## `ATTACKS.md`

Run the suite with your real provider and write down the rate. Make one change you
expect to lower it, run it again, and write that down too.

| Section | What goes in it |
|---|---|
| The suite | what you attack, how many times |
| Before | the rate, and which attacks did harm |
| The defence | the one change, and why there |
| After | the rate, and what it does and does not prove |
| What still gets through | what the suite does not try |

---

## Check it

```bash
pytest week-07/milestone -v
AGENT_PROVIDER=claude python3 week-07/milestone/run_attacks.py
```

## Friday

The defence starts in your repository's Actions tab.

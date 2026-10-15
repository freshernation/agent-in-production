# Day 4 — Rehearse the demo

> **By the end of today** you have run your Friday demo from start to finish, on the
> live service, at least twice — once with something going wrong.

---

## Read first

- [ ] Your `DEMO.md` draft, and `week-08/DEFEND.md`, so nothing on Friday is a surprise

---

## What you need to know

### Live, through the pipeline

Friday's demo is on your public URL, and any change you show goes through CI. No local
server, no slides of screenshots. If it only works on your laptop, it does not work.

### Break something on purpose

The most convincing minute of any demo is a failure you cause and the system handles:
the model switched off and the fallback answering, the alert arriving, a rollback
against a timer. Choose one and rehearse it.

### Plan for it going wrong

The host is slow, the alert is late, the Wi-Fi is down. Write down what you do in each
case. A demo that recovers from a real failure is better than one that never had one.

### Time it

Fifteen minutes. Run it with a timer twice. Cut whatever overruns.

---

## Exercises

```bash
pytest week-08/day-4 -v
```

Write `DEMO.md`, then rehearse — once for someone who has not seen Desk.

---

## Before you close the laptop

Commit, push, fill in the signal log. Check both model keys are ready to paste back.

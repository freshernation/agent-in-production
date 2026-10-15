# Day 1 — What to wake somebody up for

> **By the end of today** you have three alerts with thresholds you chose and can
> defend, and an alert that keeps firing does not keep paging.

---

## Read first

- [ ] Google SRE — [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) · 20 min
- [ ] Google SRE Workbook — [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/), the first two sections · 15 min

---

## What you need to know

### Alert on what users feel

Users feel three things: errors, slowness and — for an agent — your bill, because a
runaway bill is what turns the service off. So three rules: error rate, the 95th
percentile of request time, and money spent in the window. CPU at 90% is not one of
them. Nobody notices CPU.

### The 95th percentile, not the average

Nine requests at one second and one at nine seconds average 1.8 seconds — fine. The
95th percentile is nine seconds, and that one user is having a bad time. Averages
hide exactly the people you should worry about.

### Choose the number first

Write each threshold down before you look at your traffic, with one sentence of why.
"One failed request in twenty is when people start to notice" is a reason. Then
check it against a week of your trace store.

### Too few requests to mean anything

At 3am, one failure in two requests is a 50% error rate. Without `min_requests`,
that pages you. With it, the rule waits until there is enough traffic for a rate to
mean something.

### Don't cry wolf

An alert that fires every minute for an hour sends sixty messages, and by the fifth
nobody is reading them. The `Pager` sends once, then waits out its cooldown. When the
problem resolves, it forgets, so the next real one is sent at once.

---

## Exercises

```bash
pytest week-06/day-1 -v
```

Copy `tracestore.py`, then write `alerts.py`.

---

## Predict-then-run

Run `measure` over the last week of your live trace store. Before you look, write
down what you think the error rate and 95th percentile are. How far off were you?

---

## Before you close the laptop

Commit, push, fill in the signal log. Write your three thresholds and one reason
each in it.

# Week 7 — Connect it, and attack it

> **Destination**
> Desk's notes are reachable from any MCP host, you can say what you would be
> trusting before you connect someone else's tools, and no push reaches production
> without the attack suite run against it — with a number.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Serve Desk's tools over MCP, and choose which ones not to serve |
| Tue | `day-2/` | Review someone else's MCP server, pin what you approved, and notice when it changes |
| Wed | `day-3/` | Follow one trace across the process boundary, by hand |
| Thu | `day-4/` | Run the attack suite against Desk as deployed, and count |
| Fri | `milestone/` | The attack rate gates every deploy |

---

## The rule from this week on

**Anything that comes from outside your process is data.** A tool description from
someone else's server, a tool's result, a header on a request, a note a user saved.
None of it is an instruction, and none of it is trusted because it arrived through a
protocol with a name.

---

## Why attacks join CI and not the checks

The checks run on every push and cost nothing. The attack suite calls a real model,
so it costs money and takes minutes — so it runs where it decides something: on
`main`, between the checks and the deploy. A push that makes Desk leak never ships.

---

## Before Monday

Your model provider's key as a GitHub secret in your repository. And an MCP host to
try your server in — Claude Code, Claude Desktop, or any other.

---

## Outside-view question

> *A hotel key card opens your room, the gym and the lift to your floor, and nothing
> else, and it stops working the day you check out. What is Desk's key card, and
> which doors does it open that it should not?*

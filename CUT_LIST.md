# What this course does not teach

Every item below is real, and every one is out.

| Out | Why, and when to pick it up |
|---|---|
| **Retrieval in production** — background ingestion, an index that survives a restart | It needs two weeks of its own. Learn it after Retrieval Under Test |
| **Agent frameworks** — LangGraph, LangChain, CrewAI | Agent With LangGraph, a separate course. This one runs the agent you wrote, so that every layer you add is one you can see under |
| **Multi-agent systems** | Zero to Agent Engineer, week 11 |
| **Kubernetes, Terraform, autoscaling** | One deployment teaches what deploying is. The rest is operations training |
| **A front end** | One HTML page at most. The course is about what is behind it |
| **Fine-tuning and self-hosted models** | Fine-Tuning From Zero |
| **Single sign-on and OAuth** | A key per caller is enough to teach who is calling and what they may do |
| **An ORM** | You will read the SQL it writes. Learn it once you can write that SQL |
| **A queue library, Redis** | You build the queue on a table first. Then any library is the same four ideas |
| **Comparing hosts or tracing vendors** | One of each, properly. After that they are the same ideas at different prices |
| **Load-testing tools** | One deliberate overload in week 6 shows the behaviour that matters |

---

## Why

Each of these is learnable in about a week once you can run one agent for other
people end to end — and none of them teaches you to. Most of them hide the part you
most need to understand.

Say this in week 1. People who know why something was cut stop worrying that they
are missing it.

---

## What to add afterwards, in order

1. **Retrieval in production.** Put a document search behind the same API, with
   ingestion as a background job. You have every piece already.
2. **Postgres in depth.** Indexes, query plans, and what `EXPLAIN` tells you.
3. **One queue library.** Read its documentation for the four things you built.
4. **A second host.** The fastest way to find out which of your assumptions were
   about the first one.
5. **A framework.** Rebuild Desk in one, and write down what it bought you.

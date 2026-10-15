# Day zero

About an hour. Do it before week 1, not on Monday morning.

---

## 1. Python 3.12 or newer

```bash
python3 --version
```

If that prints 3.12 or higher, skip ahead. Otherwise install it from
[python.org](https://www.python.org/downloads/) or, on macOS, `brew install python@3.12`.

## 2. Your own repository

Make your own copy of this repository on GitHub (**Use this template**), then clone
your copy:

```bash
git clone https://github.com/YOUR-USERNAME/agent-in-production.git
cd agent-in-production
```

You push to your copy every day. From week 5, GitHub runs your tests on every push.

## 3. The environment

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 4. Check it

```bash
python3 check_setup.py
pytest llm -q
```

Every line of `check_setup.py` should say OK except the last one, about your
baseline — that is step 5.

## 5. Your baseline interview

Open a fresh chat with any capable AI. Paste the whole of `ai/advisor.md`. Answer its
questions honestly; it will ask you to do small things rather than rate yourself. At
the end it prints a `BASELINE` block. Paste it into `logs/baseline.md`, replacing the
bracketed lines, and push.

Your instructor reads every baseline before Monday.

## 6. Before week 4: a model key and a tracing account

Weeks 1 to 3 use the fake model and need no key. Week 4 needs:

- a key for Claude or OpenAI in `.env` — copy `.env.example` and fill in one provider
- a free [Langfuse Cloud](https://cloud.langfuse.com) account on the Hobby plan, with one
  project. Put its keys in `.env` as `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` and
  `LANGFUSE_HOST`. The Hobby plan keeps traces for a limited time, so export the
  screenshots your reports need in the week you make them

## 7. Before week 5: Docker and a host

Week 5 builds a container and deploys it. You need Docker running on your laptop, and
a free account on the host your instructor names — one that builds from a Dockerfile,
gives you a deploy hook URL, and can attach a persistent disk. If Docker will not run
on your machine, tell your instructor in week 3, not in week 5.

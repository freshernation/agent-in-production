"""Day-zero environment check.

Run this with:  python3 check_setup.py

Every line should say OK. If one says FAIL, it tells you what to do about it.
You are not expected to understand this file.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

GREEN = "\033[32m"
RED = "\033[31m"
DIM = "\033[2m"
OFF = "\033[0m"

results = []


def check(name, ok, fix=""):
    results.append((name, ok, fix))
    tag = f"{GREEN}OK  {OFF}" if ok else f"{RED}FAIL{OFF}"
    print(f"  {tag}  {name}")
    if not ok and fix:
        print(f"        {DIM}-> {fix}{OFF}")


def note(text):
    print(f"  {DIM}--    {text}{OFF}")


def main():
    print("\nChecking your setup\n" + "-" * 46)

    v = sys.version_info
    check(
        f"Python {v.major}.{v.minor}.{v.micro}",
        (v.major, v.minor) >= (3, 12),
        "Install Python 3.12 or newer - see SETUP.md step 1.",
    )

    in_venv = sys.prefix != sys.base_prefix
    check(
        "Virtual environment is active",
        in_venv,
        "Run:  source .venv/bin/activate   (Windows: .venv\\Scripts\\Activate.ps1)",
    )
    if in_venv:
        check(
            "Virtual environment belongs to this repo",
            Path(sys.prefix).resolve().parent == ROOT,
            f"You are in a venv, but not this project's. Expected {ROOT / '.venv'}.",
        )

    try:
        import pytest  # noqa: F401
        has_pytest = True
    except ImportError:
        has_pytest = False
    check("pytest is installed", has_pytest, "Run:  pip install -r requirements.txt")

    try:
        from llm import connect
        has_llm = True
    except ImportError:
        has_llm = False
    check("The course's llm package is installed", has_llm,
          "Run:  pip install -r requirements.txt   (from the repo root)")

    try:
        from desk.app import take_turn  # noqa: F401
        has_desk = True
    except ImportError:
        has_desk = False
    check("The desk package is installed", has_desk,
          "Run:  pip install -r requirements.txt   (from the repo root)")

    try:
        import fastapi  # noqa: F401
        import httpx  # noqa: F401
        has_web = True
    except ImportError:
        has_web = False
    check("FastAPI and httpx are installed", has_web, "Run:  pip install -r requirements.txt")

    check("git is installed", shutil.which("git") is not None,
          "Install git - see SETUP.md step 4.")

    name = email = ""
    if shutil.which("git"):
        def cfg(key):
            r = subprocess.run(["git", "config", "--global", key],
                               capture_output=True, text=True)
            return r.stdout.strip()
        name, email = cfg("user.name"), cfg("user.email")
    check(
        f"git knows who you are{f' ({name})' if name else ''}",
        bool(name and email),
        'Run:  git config --global user.name "Your Name"  and the same for user.email',
    )

    if shutil.which("git"):
        tracked = subprocess.run(["git", "ls-files", ".env"], cwd=ROOT,
                                 capture_output=True, text=True).stdout.strip()
        check(".env is not tracked by git", not tracked,
              "Your key file is in git. Run:  git rm --cached .env   then rotate the key.")

    if has_llm:
        provider = "fake"
        try:
            model = connect()
            provider = model.name
            ok = True
            fix = ""
        except Exception as error:  # a missing key or package - report it plainly
            ok = False
            fix = f"{error}  - check AGENT_PROVIDER and the key in .env (SETUP.md, 'Before week 4')."
        check(f"Model provider: {os.environ.get('AGENT_PROVIDER', 'fake')}", ok, fix)
        if ok and provider == "fake":
            note("Using the fake model. That is all you need until week 4.")

    baseline = ROOT / "logs" / "baseline.md"
    written = baseline.exists() and "_(" not in baseline.read_text()
    check("Your baseline is written (logs/baseline.md)", written,
          "Run the advisor (ai/advisor.md) and paste its summary into logs/baseline.md.")

    print("-" * 46)
    failed = [r for r in results if not r[1]]
    if failed:
        print(f"\n{RED}{len(failed)} check(s) failed.{OFF} Fix the ones above, "
              f"then run this again.\n"
              f"Stuck for more than 20 minutes? Message your instructor - "
              f"setup is the one place struggling teaches you nothing.\n")
        return 1

    print(f"\n{GREEN}All checks passed.{OFF} You are ready.\n"
          f"Next: open week-01/README.md\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

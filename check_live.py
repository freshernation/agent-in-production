"""Check a live deployment from the outside - given.

    python3 check_live.py https://your-desk.example.com [expected-version]

Three things must be true of any release: /health answers 200 (and reports the
expected version, if you give one), and /chat refuses a request with no key.
Exits 0 when they are, 1 when not. CI runs it after every deploy.
"""

import json
import sys
import urllib.error
import urllib.request


def fetch(method: str, url: str, headers: dict) -> tuple[int, dict]:
    request = urllib.request.Request(url, method=method, headers=headers, data=b"{}"
                                     if method == "POST" else None)
    request.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        return error.code, {}
    except (urllib.error.URLError, TimeoutError) as error:
        return 0, {"error": str(error)}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    base = sys.argv[1].rstrip("/")
    expected = sys.argv[2] if len(sys.argv) > 2 else None
    problems = []
    status, body = fetch("GET", base + "/health", {})
    if status != 200:
        problems.append(f"/health answered {status}")
    elif expected and body.get("version") != expected:
        problems.append(f"/health reports {body.get('version')!r}, expected {expected!r}")
    status, _ = fetch("POST", base + "/chat", {})
    if status != 401:
        problems.append(f"/chat without a key answered {status}, not 401")
    for problem in problems:
        print("FAIL", problem)
    print("live ok" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

# Day 2 - one command that says yes or no.
#
#   CHECKS      a list of (name, command) pairs, run in this order:
#                 ("tests",   [sys.executable, "-m", "pytest", "-q"])
#                 ("smoke",   [sys.executable, "smoke.py"])
#               smoke.py is given in the milestone: it starts the app in-process
#               and checks /health, a refused request, and an answer.
#               Your evals and attack suite join this list in week 7, when they
#               can run against a real model with a key kept in CI secrets.
#
#   run_check(name, command, runner=subprocess.run, clock=time.perf_counter) -> dict
#       run the command with runner(command) and read .returncode.
#       {"name", "passed": <code == 0>, "code", "seconds": <rounded to 1 place>}
#       A command that does not exist (FileNotFoundError): code 127, failed.
#
#   run_all(checks, runner=subprocess.run, clock=time.perf_counter) -> list
#       EVERY check, even after one fails - you want to see all of what is
#       wrong in one run, not one thing per push.
#
#   summary(results) -> str
#       PASS tests (12.3s)
#       FAIL evals (exit 1, 40.1s)
#       PASS attacks (8.0s)
#       2/3 passed
#
#   exit_code(results) -> 0 when every check passed, otherwise 1
#
#   if __name__ == "__main__": run_all(CHECKS), print the summary, sys.exit
#   with the exit code. That exit code is the only thing CI reads.

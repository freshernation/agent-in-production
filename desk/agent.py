import time

from desk.guards import clip, is_repeating, signature
from desk.kit import run_tool
from llm import ModelError
from desk.retry import call_with_retry


def finish(run, answer, stopped):
    """Fill in how the run ended and hand it back."""
    if stopped != "done":
        run["trace"].append({"step": run["steps"], "kind": "stop", "reason": stopped})
    run["answer"] = answer
    run["stopped"] = stopped
    return run


def is_allowed(call, dangerous, approve):
    """Safe tools always run. Dangerous ones need a yes - and no asker means no."""
    if not dangerous or call["name"] not in dangerous:
        return True
    if approve is None:
        return False
    return approve(call) is True


def run_agent(model, task, schemas, tools, system=None,
              max_steps=10, repeat_limit=3, result_limit=2000,
              dangerous=None, approve=None, history=None,
              token_budget=None, retries=2, wait=time.sleep):
    messages = list(history or [])
    messages.append({"role": "user", "content": task})
    trace = []
    signatures = []
    run = {"answer": "", "stopped": "", "steps": 0,
           "usage": {"input": 0, "output": 0}, "trace": trace, "messages": messages}

    while run["steps"] < max_steps:
        try:
            reply = call_with_retry(model, messages, system=system, tools=schemas,
                                    retries=retries, wait=wait)
        except ModelError as error:
            return finish(run, f"The model is unavailable: {error}", "error")

        run["steps"] = run["steps"] + 1
        step = run["steps"]
        run["usage"]["input"] = run["usage"]["input"] + reply["usage"]["input"]
        run["usage"]["output"] = run["usage"]["output"] + reply["usage"]["output"]
        messages.append(reply["message"])

        if reply["stop"] == "length":
            return finish(run, reply["text"] + " [cut off]", "length")
        if reply["stop"] == "refused":
            return finish(run, "The model declined this request.", "refused")
        if reply["stop"] != "tools":
            trace.append({"step": step, "kind": "answer", "text": reply["text"]})
            return finish(run, reply["text"], "done")

        spent = run["usage"]["input"] + run["usage"]["output"]
        if token_budget is not None and spent > token_budget:
            return finish(run, "I reached my token budget before finishing.", "budget")

        if reply["text"]:
            trace.append({"step": step, "kind": "say", "text": reply["text"]})
        for call in reply["tool_calls"]:
            trace.append({"step": step, "kind": "call",
                          "name": call["name"], "args": call["args"]})
            signatures.append(signature(call))
            if is_repeating(signatures, repeat_limit):
                return finish(run, "I kept repeating the same step, so I stopped.",
                              "repeating")

        results = []
        for call in reply["tool_calls"]:
            if is_allowed(call, dangerous, approve):
                content = clip(run_tool(tools, call["name"], call["args"]), result_limit)
            else:
                content = f"Refused: the user did not approve {call['name']}."
            results.append({"role": "tool", "tool_call_id": call["id"], "content": content})
            trace.append({"step": step, "kind": "result",
                          "name": call["name"], "content": content})
        messages.extend(results)

    return finish(run, "I ran out of steps before finishing.", "max_steps")

def allowed_recipient(to, allowed):
    wanted = to.strip().lower()
    for address in allowed:
        if address.strip().lower() == wanted:
            return True
    return False


def watched(function, name, readers, state):
    def run(**args):
        if name in readers:
            state["tainted"] = True
        return function(**args)
    return run


def watch(tools, readers, state):
    table = {}
    for name in tools:
        table[name] = watched(tools[name], name, readers, state)
    return table


def make_approver(allowed, state, ask=None):
    def approve(call):
        if call["name"] == "share_note":
            if not allowed_recipient(call["args"].get("to", ""), allowed):
                return False
            if not state["tainted"]:
                return True
        if ask is None:
            return False
        return ask(call) is True
    return approve

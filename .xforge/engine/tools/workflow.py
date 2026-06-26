"""
Workflow tools - list, validate, run workflows (YAML).

Extraido de xforge_engine.py em v3.10.2 per DR-0089.
"""
import re
import yaml
from .common import _ok, _err, WORKFLOWS

def tool_workflow_list(args):
    if not WORKFLOWS.exists():
        return _ok(workflows=[])
    out = []
    for yml in sorted(WORKFLOWS.glob("W*.yaml")):
        try:
            d = yaml.safe_load(yml.read_text(encoding="utf-8"))
        except Exception as e:
            out.append({"file": yml.name, "error": str(e)})
            continue
        out.append({
            "file": yml.name, "id": d.get("id"), "name": d.get("name"),
            "version": d.get("version"), "description": d.get("description"),
            "trustScore": d.get("trustScore") if False else None,
            "states": len(d.get("states", [])),
            "transitions": len(d.get("transitions", [])),
        })
    return _ok(count=len(out), workflows=out)


def _validate_workflow(wf):
    errors = []
    required = ["id", "version", "name", "states", "transitions", "entrypoint", "terminalStates"]
    for r in required:
        if r not in wf:
            errors.append("missing required field: " + r)
    if "id" in wf and not re.match(r"^W\d{3}$", str(wf["id"])):
        errors.append("id must match W<3digits>, got " + str(wf["id"]))
    if "version" in wf and not re.match(r"^\d+\.\d+\.\d+$", str(wf["version"])):
        errors.append("version must be semver, got " + str(wf["version"]))
    states = set(wf.get("states", []))
    for s in states:
        if not isinstance(s, str) or not s:
            errors.append("invalid state: " + repr(s))
    if wf.get("entrypoint") not in states:
        errors.append("entrypoint '" + str(wf.get("entrypoint")) + "' not in states")
    for ts in wf.get("terminalStates", []):
        if ts not in states:
            errors.append("terminalState '" + ts + "' not in states")
    transitions = wf.get("transitions", [])
    for i, t in enumerate(transitions):
        if "from" not in t or "to" not in t or "event" not in t:
            errors.append("transition[" + str(i) + "] missing from/to/event")
            continue
        if t["from"] != "*" and t["from"] not in states:
            errors.append("transition[" + str(i) + "].from '" + str(t["from"]) + "' not in states")
        if t["to"] not in states:
            errors.append("transition[" + str(i) + "].to '" + str(t["to"]) + "' not in states")
    targets = {t.get("to") for t in transitions if t.get("to")}
    for ts in wf.get("terminalStates", []):
        if ts not in targets:
            errors.append("terminalState '" + ts + "' is unreachable (no transition lands on it)")
    sources = {t.get("from") for t in transitions if t.get("from")}
    has_global = "*" in sources
    for s in states:
        if s in wf.get("terminalStates", []):
            continue
        if s not in sources and not has_global:
            errors.append("state '" + s + "' is a dead-end (no outgoing transition, not terminal, no global)")
    return errors


def tool_workflow_validate(args):
    wid = (args.get("id") or "").upper()
    if not wid:
        return _err("id required")
    matches = list(WORKFLOWS.glob(wid + "-*.yaml")) if WORKFLOWS.exists() else []
    if not matches:
        return _err("workflow '" + wid + "' not found")
    path = matches[0]
    try:
        wf = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return _err("YAML parse error: " + str(e))
    errors = _validate_workflow(wf)
    return _ok(file=path.name, id=wf.get("id"), valid=len(errors) == 0, errors=errors,
               states=wf.get("states"), entrypoint=wf.get("entrypoint"),
               terminalStates=wf.get("terminalStates"),
               transitions=len(wf.get("transitions", [])))


def _apply_event(wf, current, event):
    for t in wf.get("transitions", []):
        f = t.get("from")
        if (f == current or f == "*") and t.get("event") == event:
            return t.get("to")
    return None


def tool_workflow_run(args):
    wid = (args.get("id") or "").upper()
    if not wid:
        return _err("id required")
    matches = list(WORKFLOWS.glob(wid + "-*.yaml")) if WORKFLOWS.exists() else []
    if not matches:
        return _err("workflow '" + wid + "' not found")
    path = matches[0]
    try:
        wf = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return _err("YAML parse error: " + str(e))
    events = args.get("events") or []
    if isinstance(events, str):
        events = [e.strip() for e in events.split(",") if e.strip()]
    state = wf.get("entrypoint")
    history = [{"step": 0, "state": state, "event": None}]
    for ev in events:
        next_state = _apply_event(wf, state, ev)
        if next_state is None:
            return _err("no transition from '" + str(state) + "' with event '" + str(ev) + "'", history=history)
        history.append({"step": len(history), "state": next_state, "event": ev})
        state = next_state
        if state in wf.get("terminalStates", []):
            break
    return _ok(id=wf.get("id"), file=path.name, currentState=state,
               terminal=state in wf.get("terminalStates", []),
               steps=len(history) - 1, history=history)

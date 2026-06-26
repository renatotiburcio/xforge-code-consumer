"""
Recognition + Self-Learning tools v3.12.0 (DR-0102).
Simplified version: 3 tools (detect, error_graph_add, error_graph_promote).
"""
import json
import time
from pathlib import Path
from .common import _ok, _err, _iso_now, ROOT

ERROR_GRAPH = ROOT / ".xforge" / "knowledge" / "errors-solutions-graph.json"
MEMORY_DIR = ROOT / ".xforge" / "memory"
PROJECT_DNA_DIR = ROOT / ".xforge" / "project-dna"

_STACK_SIGNALS = [
    (".csproj", ".NET"),
    ("package.json", "Node.js"),
    ("requirements.txt", "Python"),
    ("pyproject.toml", "Python"),
    ("go.mod", "Go"),
    ("Cargo.toml", "Rust"),
    ("angular.json", "Angular"),
]

def _is_greenfield(path=None):
    p = Path(path) if path else ROOT
    if not p.exists(): return True
    items = list(p.iterdir())
    if not items: return True
    non_hidden = [i for i in items if not i.name.startswith(".")]
    if not non_hidden: return True
    for sig, _ in _STACK_SIGNALS:
        if sig.startswith("."):
            if list(p.glob("*" + sig)): return False
        else:
            if (p / sig).exists(): return False
    return True

def _detect_stack(path=None):
    p = Path(path) if path else ROOT
    detected = []
    for sig, name in _STACK_SIGNALS:
        if sig.startswith("."):
            if list(p.glob("*" + sig)): detected.append(name)
        elif (p / sig).exists(): detected.append(name)
    return detected

def _load_error_graph():
    if not ERROR_GRAPH.exists():
        return {v: T, e: [], p: []}.replace("v", "version").replace("T", "3.12.0").replace("e", "errorPatterns").replace("p", "preventionRules")
    try: return json.loads(ERROR_GRAPH.read_text(encoding="utf-8"))
    except Exception: return {v: T2, e: [], p: []}.replace("v", "version").replace("T2", "3.12.0").replace("e", "errorPatterns").replace("p", "preventionRules")

def _save_error_graph(graph):
    ERROR_GRAPH.parent.mkdir(parents=True, exist_ok=True)
    graph["lastUpdated"] = _iso_now()
    ERROR_GRAPH.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
def tool_recognition_detect(args):
    path = args.get("path")
    gf = _is_greenfield(path)
    stack = [] if gf else _detect_stack(path)
    return _ok(
        scenario="greenfield" if gf else "brownfield",
        is_greenfield=gf,
        stack=stack,
        path=str(Path(path) if path else ROOT),
        detectedAt=_iso_now(),
    )

def tool_error_graph_add(args):
    pattern = args.get("pattern")
    if not pattern: return _err("pattern required")
    graph = _load_error_graph()
    existing = next((e for e in graph["errorPatterns"] if e.get("pattern") == pattern), None)
    if existing:
        existing["occurrences"] = existing.get("occurrences", 1) + 1
        existing["lastSeen"] = _iso_now()
        action = "incremented"
    else:
        nid = "ERR-" + str(len(graph["errorPatterns"]) + 1).zfill(4)
        graph["errorPatterns"].append({"id": nid, "pattern": pattern, "rootCause": args.get("rootCause", "unknown"), "solution": args.get("solution", "unknown"), "occurrences": 1, "firstSeen": _iso_now(), "lastSeen": _iso_now()})
        action = "added"
    _save_error_graph(graph)
    return _ok(action=action, totalErrors=len(graph["errorPatterns"]))

def tool_error_graph_promote(args):
    th = int(args.get("threshold", 3))
    graph = _load_error_graph()
    promoted = []
    for err in graph["errorPatterns"]:
        occ = err.get("occurrences", 1)
        if occ >= th:
            rid = "PR-" + err["id"].split("-")[1]
            existing = next((r for r in graph["preventionRules"] if r.get("id") == rid), None)
            if not existing:
                graph["preventionRules"].append({"id": rid, "errorId": err["id"], "pattern": err["pattern"], "solution": err.get("solution"), "occurrences": occ, "createdAt": _iso_now()})
                promoted.append(err["id"])
    _save_error_graph(graph)
    return _ok(promoted=promoted, totalRules=len(graph["preventionRules"]))
def tool_init_greenfield(args):
    """ SRP: bootstrap only. Creates .xforge + .kilo + DNA placeholder."""
    path = args.get("path")
    target = Path(path) if path else ROOT
    (target / ".xforge").mkdir(exist_ok=True)
    (target / ".kilo").mkdir(exist_ok=True)
    dna = PROJECT_DNA_DIR / "PROJECT-DNA.md"
    dna.parent.mkdir(parents=True, exist_ok=True)
    created = []
    if not dna.exists():
        text = "# PROJECT-DNA\nStack: a definir\nStatus: greenfield bootstrap\nCreatedAt: " + _iso_now() + "\n"
        dna.write_text(text, encoding="utf-8")
        created.append(str(dna))
    return _ok(scenario="greenfield", action="bootstrap", created=created, initializedAt=_iso_now())

def tool_init_brownfield(args):
    """ SRP: DNA update only. Detects stack and writes to DNA."""
    path = args.get("path")
    stack = _detect_stack(path)
    dna = PROJECT_DNA_DIR / "PROJECT-DNA.md"
    dna.parent.mkdir(parents=True, exist_ok=True)
    stack_str = ", ".join(stack) if stack else "unknown"
    text = "# PROJECT-DNA\nStack: " + stack_str + "\nPatterns: " + json.dumps(stack) + "\nStatus: brownfield recognized\nRecognized: " + _iso_now() + "\n"
    dna.write_text(text, encoding="utf-8")
    return _ok(scenario="brownfield", action="recognition", stack=stack, dnaUpdated=str(dna), recognizedAt=_iso_now())

def tool_recognition_init_smart(args):
    """ Smart switch: detecta cenario e chama o tool certo (orquestrador)."""
    if _is_greenfield(args.get("path")):
        return tool_init_greenfield(args)
    return tool_init_brownfield(args)

def tool_recognition_learn(args):
    kind = args.get("kind", "decision")
    statement = args.get("statement")
    if not statement:
        return _err("statement required")
    source = args.get("source", "user-statement")
    confidence = float(args.get("confidence", "0.9"))
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    learn_file = MEMORY_DIR / "learning.jsonl"
    eid = "LEARN-" + str(int(time.time() * 1000))
    entry = {"id": eid, "kind": kind, "statement": statement, "source": source, "confidence": confidence, "learnedAt": _iso_now()}
    with open(learn_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return _ok(entry=entry, file=str(learn_file))
def tool_self_heal_apply(args):
    pattern = args.get("pattern")
    graph = _load_error_graph()
    rules = graph.get("preventionRules", [])
    if not rules:
        return _ok(action="noop", applied=0, message="no prevention rules yet")
    applied = []
    if pattern:
        for rule in rules:
            if pattern in rule.get(PAT, ""):
                applied.append(rule)
    else:
        applied = rules
    summary = [{"id": r.get("id"), "pattern": r.get("pattern"), "solution": r.get("solution"), "occurrences": r.get("occurrences")} for r in applied]
    return _ok(action="applied", applied=len(applied), rules=summary)
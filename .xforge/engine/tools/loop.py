"""
Loop Engineer v3.19.0 (decree number 109).
ReAct loop: Thought -> Action -> Observation.
Includes: max_steps, confidence threshold, anti-drift.
"""
from .common import _ok, _iso_now

_MAX_STEPS_DEFAULT = 10
_CONFIDENCE_THRESHOLD = 0.7
_MAX_RETRIES = 3


def _compute_confidence(observation):
    if not isinstance(observation, dict): return 0.0
    ok = observation.get("ok")
    if ok is False: return 0.1
    if ok is True:
        has_data = any(k for k in observation.keys() if k != "ok")
        return 0.9 if has_data else 0.7
    return 0.5


def _detect_drift(history, threshold=3):
    if len(history) < threshold: return False
    recent = history[-threshold:]
    if not all("action" in step for step in recent): return False
    actions = [step["action"].get("tool") for step in recent]
    return len(set(actions)) == 1


def tool_loop_run(args):
    goal = args.get("goal", "unknown")
    max_steps = int(args.get("max_steps", _MAX_STEPS_DEFAULT))
    threshold = float(args.get("confidence_threshold", _CONFIDENCE_THRESHOLD))
    max_retries = int(args.get("max_retries", _MAX_RETRIES))
    history = []
    confidence = 1.0
    import xforge_engine as xe
    for step in range(max_steps):
        thought = {"step": step, "goal": goal}
        action = {"tool": "xforge_knowledge_search", "args": {"query": goal}}
        observation = None
        for retry in range(max_retries):
            try:
                if action["tool"] in xe.TOOLS:
                    observation = xe.TOOLS[action["tool"]](action.get("args", {}))
                else:
                    observation = {"ok": False, "error": "tool not found"}
                break
            except Exception as e:
                if retry == max_retries - 1:
                    observation = {"ok": False, "error": str(e)[:80]}
        history.append({"thought": thought, "action": action, "observation": observation})
        confidence = _compute_confidence(observation)
        if confidence < threshold: break
        if _detect_drift(history): break
    return _ok(
        goal=goal,
        steps=len(history),
        maxSteps=max_steps,
        finalConfidence=confidence,
        stopped=confidence < threshold or _detect_drift(history),
        history=history[-3:],
        completedAt=_iso_now(),
    )


def tool_loop_detect_drift(args):
    history = args.get("history", [])
    threshold = int(args.get("threshold", 3))
    is_drift = _detect_drift(history, threshold)
    return _ok(drift=is_drift, historyLen=len(history), threshold=threshold)


def tool_loop_confidence(args):
    observation = args.get("observation", {})
    score = _compute_confidence(observation)
    return _ok(score=score, threshold=_CONFIDENCE_THRESHOLD, above=score >= _CONFIDENCE_THRESHOLD)


def tool_loop_state(args):
    return _ok(maxStepsDefault=_MAX_STEPS_DEFAULT, confidenceThreshold=_CONFIDENCE_THRESHOLD, maxRetries=_MAX_RETRIES, stateMachine="Thought -> Action -> Observation")


# ============= v3.24.0: Loop Engineer v2 =============

def _summarize_history(history, max_steps=3):
    """ Progressive summarization: condensa history antiga em resumo."""
    if len(history) <= max_steps:
        return history, ""
    old_steps = history[:-max_steps]
    recent = history[-max_steps:]
    # Build summary of old steps
    summary = {
        "summarizedCount": len(old_steps),
        "toolsUsed": list(set(s.get("action", {}).get("tool", "unknown") for s in old_steps if s.get("action"))),
        "outcomes": [s.get("observation", {}).get("ok", False) for s in old_steps if s.get("observation")],
        "firstSpan": old_steps[0].get("spanId") if old_steps else None,
        "lastSpan": old_steps[-1].get("spanId") if old_steps else None,
    }
    return recent, summary


def _gen_span_id():
    """ Generate unique span_id for observability."""
    import uuid
    return "span-" + str(uuid.uuid4())[:8]


def tool_loop_run_v2(args):
    """ Loop Engineer v2: ReAct with progressive summarization + span_id."""
    goal = args.get("goal", "unknown")
    max_steps = int(args.get("max_steps", _MAX_STEPS_DEFAULT))
    threshold = float(args.get("confidence_threshold", _CONFIDENCE_THRESHOLD))
    max_retries = int(args.get("max_retries", _MAX_RETRIES))
    summarize_after = int(args.get("summarize_after", 3))
    parent_span = args.get("parent_span")
    full_history = []
    summary = None
    confidence = 1.0
    import xforge_engine as xe
    for step in range(max_steps):
        span_id = _gen_span_id()
        thought = {"step": step, "goal": goal, "spanId": span_id, "parentSpan": parent_span}
        action = {"tool": "xforge_knowledge_search", "args": {"query": goal}, "spanId": span_id}
        observation = None
        for retry in range(max_retries):
            try:
                if action["tool"] in xe.TOOLS:
                    observation = xe.TOOLS[action["tool"]](action.get("args", {}))
                else:
                    observation = {"ok": False, "error": "tool not found", "spanId": span_id}
                break
            except Exception as e:
                if retry == max_retries - 1:
                    observation = {"ok": False, "error": str(e)[:80], "spanId": span_id}
        step_record = {"spanId": span_id, "parentSpan": parent_span, "thought": thought, "action": action, "observation": observation, "ts": _iso_now()}
        full_history.append(step_record)
        confidence = _compute_confidence(observation)
        if confidence < threshold: break
        if _detect_drift(full_history): break
    # Apply progressive summarization
    if len(full_history) > summarize_after:
        full_history, summary = _summarize_history(full_history, summarize_after)
    return _ok(
        goal=goal,
        steps=len(full_history),
        maxSteps=max_steps,
        finalConfidence=confidence,
        stopped=confidence < threshold,
        history=full_history[-3:],
        summary=summary,
        totalSpans=len(full_history) + (summary.get("summarizedCount", 0) if summary else 0),
        completedAt=_iso_now(),
    )


def tool_loop_summarize(args):
    """ Standalone progressive summarization of a history."""
    history = args.get("history", [])
    max_steps = int(args.get("max_steps", 3))
    recent, summary = _summarize_history(history, max_steps)
    return _ok(recentCount=len(recent), summary=summary, recent=recent)


def tool_loop_span_id(args):
    """ Generate a new span_id for trace correlation."""
    return _ok(spanId=_gen_span_id(), generatedAt=_iso_now())
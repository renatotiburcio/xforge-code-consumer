"""
Policy tool - OPA-style policy check (RBAC + policies).

Extraido de xforge_engine.py em v3.10.3 per DR-0090.
Importa tool_rbac_check via lazy import (break circular).
"""
import json
import re
from .common import _ok, _err, POLICY_ENGINE, RBAC_CONFIG


def tool_policy_check(args):
    # Lazy import para evitar circular dependency
    from .rbac import tool_rbac_check, _role_chain
    actor_role = (args.get("actor_role") or args.get("role") or "").lower()
    action = (args.get("action") or "").lower()
    resource = args.get("resource") or ""
    context = args.get("context") or {}
    if not actor_role or not action:
        return _err("actor_role and action required")
    if not POLICY_ENGINE.exists() or not RBAC_CONFIG.exists():
        return _err("policy or rbac config missing")
    try:
        engine = json.loads(POLICY_ENGINE.read_text(encoding="utf-8"))
        rbac = json.loads(RBAC_CONFIG.read_text(encoding="utf-8-sig"))
    except Exception as e:
        return _err("config invalid: " + str(e))
    rbac_res = tool_rbac_check({"role": actor_role, "action": action})
    if not rbac_res.get("allowed"):
        return _ok(allowed=False, decision="denied", stage="rbac",
                   reason="RBAC denied role '" + actor_role + "' for action '" + action + "'",
                   rbac=rbac_res, applied_policies=[])
    applied, requirements = [], []
    for pol in engine.get("policies", []):
        pol_actions = [a.lower() for a in pol.get("action", [])]
        if action not in pol_actions:
            continue
        if pol.get("appliesTo") and actor_role not in [x.lower() for x in pol["appliesTo"]]:
            continue
        pattern = pol.get("resourcePattern", ".*")
        if not re.match(pattern, resource):
            continue
        applied.append({"id": pol["id"], "name": pol["name"], "effect": pol.get("effect"),
                        "reason": pol.get("reason", "")})
        if pol.get("effect") == "deny":
            allow_roles = [x.lower() for x in pol.get("allowRoles", [])]
            if actor_role in allow_roles:
                continue
            return _ok(allowed=False, decision="denied", stage="policy:" + pol["id"],
                       reason=pol.get("reason", "denied by policy"),
                       rbac=rbac_res, applied_policies=applied, policy=pol)
        if pol.get("effect") == "require":
            req = pol.get("requiredRole")
            req_provider = pol.get("requiredProvider")
            if req and req.lower() not in _role_chain(rbac, actor_role):
                requirements.append({"type": "role", "required": req, "policy": pol["id"]})
            if req_provider and context.get("provider") not in (None, req_provider, "human"):
                requirements.append({"type": "provider", "required": req_provider, "policy": pol["id"]})
    if requirements:
        return _ok(allowed=True, decision="allowed_with_requirements", stage="policy",
                   reason="allowed but requires: " + "; ".join(
                       r["type"] + "=" + str(r["required"]) for r in requirements),
                   rbac=rbac_res, applied_policies=applied, requirements=requirements)
    return _ok(allowed=True, decision="allowed", stage="policy",
               reason="allowed by RBAC and no policy required escalation",
               rbac=rbac_res, applied_policies=applied)

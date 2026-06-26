"""
RBAC tool - role-based access control check.

Extraido de xforge_engine.py em v3.10.3 per DR-0090.
"""
import json
from .common import _ok, _err, RBAC_CONFIG


def tool_rbac_check(args):
    role = (args.get("role") or "").lower()
    action = (args.get("action") or "").lower()
    if not role or not action:
        return _err("role and action required")
    if not RBAC_CONFIG.exists():
        return _err("rbac.json not found")
    try:
        cfg = json.loads(RBAC_CONFIG.read_text(encoding="utf-8-sig"))
    except Exception as e:
        return _err("rbac.json invalid: " + str(e))
    if role not in cfg.get("roles", {}):
        return _err("unknown role: " + role, available=list(cfg.get("roles", {}).keys()))
    r = cfg["roles"][role]
    granted, denied = set(), set()
    cur, seen = role, set()
    while cur and cur not in seen:
        seen.add(cur)
        rdef = cfg["roles"].get(cur, {})
        for p in rdef.get("permissions", []):
            granted.add(p.lower())
        for p in rdef.get("denied", []):
            denied.add(p.lower())
        if rdef.get("permissions") == ["*"]:
            granted, denied = {"*"}, set()
            break
        parents = rdef.get("inherits", [])
        cur = parents[0] if parents else None
    allowed = (action in granted) or ("*" in granted and action not in denied)
    return _ok(role=role, action=action, allowed=allowed, level=r.get("level"),
               granted=sorted(granted), denied=sorted(denied),
               reason=("explicitly allowed" if allowed else "denied by RBAC"))


def _role_chain(rbac, role):
    chain, cur, seen = set(), role, set()
    while cur and cur not in seen:
        seen.add(cur)
        chain.add(cur)
        parents = rbac.get("roles", {}).get(cur, {}).get("inherits", [])
        cur = parents[0] if parents else None
    return chain

#!/usr/bin/env python3
"""XForge Engine - facade for tools package v3.9.1 per DR-0083.

Common helpers + cache state foram extraidos para tools/common.py.
Este arquivo mantem todas as tool_* functions e atua como facade.
MCP server (server.js) importa tool_X deste modulo.
Backwards compat: tool_X(args) ainda funciona (re-exports via tools.common)."""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure tools package is importable quando engine e chamado via subprocess (test_doctor_cache etc)
import os as _os_eng
import sys as _sys_eng
_ENGINE_DIR = _os_eng.path.dirname(_os_eng.path.abspath(__file__))
if _ENGINE_DIR not in _sys_eng.path:
    _sys_eng.path.insert(0, _ENGINE_DIR)

# Re-exports de tools.common para backward compat
from tools.common import (
    ROOT, WORKFLOWS, KNOWLEDGE, BUSINESS, INDEX_JSON,
    _INDEX_CACHE, _INDEX_TTL_SEC,
    _DOCTOR_CACHE, _DOCTOR_TTL_SEC,
    _PYTEST_CACHE, _PYTEST_TTL_SEC,
    _ok, _err, _iso_now,
    _load_index_cached, _invalidate_index_cache, _index_cache_stats,
)

# Re-exports de tools.doctor + tools.validate (DR-0084, v3.9.2)
from tools.doctor import tool_doctor_run, _run_doctor_cached
from tools.validate import (
    tool_validate_all,
    _run_knowledge_cached, _run_pytest_cached,
    _run_workflow_validate_parallel,
)

# Re-export knowledge tools (DR-0085, v3.9.3)
from tools.knowledge import tool_knowledge_search, tool_index_cache_stats

# Re-export workflow tools (DR-0089, v3.10.2)
from tools.workflow import (tool_workflow_list, tool_workflow_validate, tool_workflow_run, _validate_workflow, _apply_event)

# Re-export rbac + policy tools (DR-0090, v3.10.3)
from tools.rbac import tool_rbac_check, _role_chain
from tools.policy import tool_policy_check

# Re-export tenant tools (DR-0091, v3.10.4)
from tools.tenant import tool_tenant_list, tool_tenant_create, tool_tenant_use

# Re-export pack tools (DR-0092, v3.10.5)
from tools.pack import (tool_pack_list, tool_pack_install, tool_pack_uninstall, tool_pack_create)

# Re-export autoresearch tools (DR-0093, v3.10.6 ULTIMO)
from tools.autoresearch import (tool_autoresearch_run, tool_autoresearch_run_mutate, tool_autoresearch_daemon)

# Re-export knowledge graph tools (DR-0097, v3.11.3)
from tools.kg import (tool_graph_query, tool_graph_related, tool_graph_path)

# Re-export recognition tools (DR-0102, v3.12.0)
from tools.recognition import (tool_recognition_detect, tool_error_graph_add, tool_error_graph_promote, tool_recognition_init_smart, tool_recognition_learn, tool_self_heal_apply, tool_init_greenfield, tool_init_brownfield)
from tools.loop import (tool_loop_run, tool_loop_detect_drift, tool_loop_confidence, tool_loop_state, tool_loop_run_v2, tool_loop_summarize, tool_loop_span_id)


import yaml
import shutil


# Path constants (eram inline apos tool_doctor_run)
SCHEMA_KNOWLEDGE = ROOT / ".xforge" / "schemas" / "knowledge.schema.json"
SCHEMA_WORKFLOW = ROOT / ".xforge" / "workflows" / "workflow.schema.json"
POLICY_ENGINE = ROOT / ".xforge" / "policy" / "engine.json"
RBAC_CONFIG = ROOT / ".xforge" / "policy" / "rbac.json"
TENANTS_DIR = ROOT / ".xforge" / "tenants"
MARKETPLACE = ROOT / ".xforge" / "marketplace" / "packs"
PACKS_INSTALLED = ROOT / ".xforge" / "packs" / "installed.json"
AUTORESEARCH_CFG = ROOT / ".xforge" / "autoresearch" / "config.json"
AUTORESEARCH_RESULTS = ROOT / ".xforge" / "autoresearch" / "results.tsv"
AUTORESEARCH_EXPERIMENTS = ROOT / ".xforge" / "autoresearch" / "experiments"
AUTORESEARCH_SANDBOX = ROOT / ".xforge" / "autoresearch" / "sandbox"
SCORING_RULE = ROOT / ".kilo" / "rules" / "immutable-scoring.md"
SCHEMAS_DIR = ROOT / ".xforge" / "schemas"

# ============================================================== DOCTOR + KNOWLEDGE + WORKFLOWS

























def _exp_count_knowledge():
    kcount = sum(1 for _ in KNOWLEDGE.rglob("*.md")) if KNOWLEDGE.exists() else 0
    return "knowledge_files", kcount


def _exp_count_transitions():
    total = 0
    for yml in (WORKFLOWS.glob("W*.yaml") if WORKFLOWS.exists() else []):
        try:
            d = yaml.safe_load(yml.read_text(encoding="utf-8"))
            total += len(d.get("transitions", []))
        except Exception:
            pass
    return "transitions", total


def _exp_check_documented():
    if not (KNOWLEDGE.exists() and WORKFLOWS.exists()):
        return "undocumented", []
    klow = {p.name.lower() for p in KNOWLEDGE.rglob("*.md")}
    missing = []
    for yml in WORKFLOWS.glob("W*.yaml"):
        wf_id = yml.stem.split("-")[0].lower()
        if not any(wf_id in n for n in klow):
            missing.append(yml.name)
    return "undocumented_workflows", missing


def _exp_check_empty_dirs():
    if not (ROOT / ".xforge").exists():
        return "empty_dirs", []
    empties = []
    for d in (ROOT / ".xforge").rglob("*"):
        if d.is_dir() and not any(d.iterdir()):
            empties.append(str(d.relative_to(ROOT)))
    return "empty_dirs", empties


def _exp_check_dup_types():
    if not KNOWLEDGE.exists():
        return "duplicates", []
    seen = {}
    dups = []
    for f in KNOWLEDGE.rglob("*.md"):
        c = f.read_text(encoding="utf-8", errors="ignore")
        m = re.match(r"(?s)^---\r?\n(.+?)\r?\n---", c)
        if not m:
            continue
        fm = m.group(1)
        fid, ftype = "", ""
        for ln in fm.splitlines():
            if ln.startswith("id:"):
                fid = ln.split(":", 1)[1].strip()
            if ln.startswith("type:"):
                ftype = ln.split(":", 1)[1].strip()
        if fid and ftype:
            key = (ftype, fid)
            if key in seen:
                dups.append({"id": fid, "type": ftype,
                             "files": [seen[key], str(f.relative_to(ROOT))]})
            else:
                seen[key] = str(f.relative_to(ROOT))
    return "duplicates", dups


    invalid_wf = []
    def _validate_one(w):
        v = tool_workflow_validate({"id": w["id"]})
        return w["id"], v.get("valid", False), v.get("errors", [])
    with ThreadPoolExecutor(max_workers=min(8, len(workflows))) as pool:
        for wf_id, valid, errs in pool.map(_validate_one, workflows):
            if valid:
                valid_wf += 1
            else:
                invalid_wf.append({"id": wf_id, "errors": errs})
    return valid_wf, invalid_wf








TOOLS = {
    "xforge_doctor": tool_doctor_run,
    "xforge_knowledge_search": tool_knowledge_search,
    "xforge_workflow_list": tool_workflow_list,
    "xforge_workflow_validate": tool_workflow_validate,
    "xforge_workflow_run": tool_workflow_run,
    "xforge_rbac_check": tool_rbac_check,
    "xforge_policy_check": tool_policy_check,
    "xforge_tenant_list": tool_tenant_list,
    "xforge_tenant_create": tool_tenant_create,
    "xforge_tenant_use": tool_tenant_use,
    "xforge_pack_list": tool_pack_list,
    "xforge_pack_install": tool_pack_install,
    "xforge_pack_uninstall": tool_pack_uninstall,
    "xforge_pack_create": tool_pack_create,
    "xforge_index_cache_stats": tool_index_cache_stats,
    "xforge_autoresearch_run": tool_autoresearch_run,
    "xforge_autoresearch_run_mutate": tool_autoresearch_run_mutate,
    "xforge_autoresearch_daemon": tool_autoresearch_daemon,
    "xforge_validate_all": tool_validate_all,
    "xforge_graph_query": tool_graph_query,
    "xforge_graph_related": tool_graph_related,
    "xforge_graph_path": tool_graph_path,
    "xforge_recognition_detect": tool_recognition_detect,
    "xforge_error_graph_add": tool_error_graph_add,
    "xforge_error_graph_promote": tool_error_graph_promote,
    "xforge_recognition_init_smart": tool_recognition_init_smart,
    "xforge_loop_run": tool_loop_run,
    "xforge_loop_detect_drift": tool_loop_detect_drift,
    "xforge_loop_confidence": tool_loop_confidence,
    "xforge_loop_state": tool_loop_state,
    "xforge_loop_run_v2": tool_loop_run_v2,
    "xforge_loop_summarize": tool_loop_summarize,
    "xforge_loop_span_id": tool_loop_span_id,
    "xforge_init_greenfield": tool_init_greenfield,
    "xforge_init_brownfield": tool_init_brownfield,
    "xforge_recognition_learn": tool_recognition_learn,
    "xforge_self_heal_apply": tool_self_heal_apply,
}

def main():
    if len(sys.argv) < 2:
        print(json.dumps(_err("usage: xforge_engine.py <tool> [json-args]"), ensure_ascii=False))
        sys.exit(1)
    tool = sys.argv[1]
    args = {}
    if len(sys.argv) >= 3 and sys.argv[2]:
        raw = sys.argv[2]
        if raw.startswith("@"):
            try:
                raw = Path(raw[1:]).read_text(encoding="utf-8")
            except Exception as e:
                print(json.dumps(_err("cannot read args file: " + str(e)), ensure_ascii=False))
                sys.exit(1)
        try:
            args = json.loads(raw)
        except Exception as e:
            print(json.dumps(_err("invalid args JSON: " + str(e)), ensure_ascii=False))
            sys.exit(1)
    if tool not in TOOLS:
        print(json.dumps(_err("unknown tool: " + tool, available=list(TOOLS.keys())), ensure_ascii=False))
        sys.exit(1)
    try:
        result = TOOLS[tool](args)
    except Exception as e:
        import traceback
        result = _err("tool crashed: " + str(e), traceback=traceback.format_exc())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("ok") else 1)



if __name__ == "__main__":
    main()

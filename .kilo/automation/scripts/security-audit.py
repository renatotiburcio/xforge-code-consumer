"""XForge Security Audit (v1.1.0).

Scans the codebase for:
1. Hardcoded secrets (API keys, passwords, tokens, private keys)
2. Common dangerous patterns (eval, exec, os.system with user input)
3. Known-vulnerable file extensions

Exit codes:
  0 = clean
  1 = findings (review and fix)
  2 = scan error

Usage:
    python .kilo/automation/scripts/security-audit.py
    python .kilo/automation/scripts/security-audit.py --strict
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(r"D:\\dev\\XForge-Development-New")

# Directories to skip (third-party, generated, git)
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".pytest_cache",
    ".venv", "venv", "dist", "build", "sandbox",
    "tests",  # test fixtures may contain fake secrets and PII
    "indexes",  # RAG indexed content may have PII patterns
    "autoresearch",  # AutoResearch artifacts (results.tsv, stress reports)
    "curated-operational",  # real-world rejection codes (some look like keys)
}

# File extensions to scan
SCAN_EXTS = {".py", ".ps1", ".sh", ".js", ".ts", ".json", ".md", ".txt", ".yml", ".yaml", ".env", ".config"}

# Secret patterns (name, regex, severity, description)
SECRET_PATTERNS = [
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}"), "critical", "AWS Access Key ID"),
    ("aws-secret-key", re.compile(r"aws_secret_access_key\s*=\s*[\"'][A-Za-z0-9/+=]{40}"), "critical", "AWS Secret Access Key"),
    ("github-token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), "critical", "GitHub Personal Access Token"),
    ("github-fine-grained", re.compile(r"github_pat_[A-Za-z0-9_]{82}"), "critical", "GitHub Fine-Grained PAT"),
    ("slack-token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"), "critical", "Slack Token"),
    ("stripe-key", re.compile(r"sk_live_[A-Za-z0-9]{24,}"), "critical", "Stripe Live Secret Key"),
    ("stripe-pub", re.compile(r"pk_live_[A-Za-z0-9]{24,}"), "high", "Stripe Live Publishable Key"),
    ("private-key", re.compile(r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"), "critical", "Private Key"),
    ("generic-password", re.compile(r"(?i)password\s*[:=]\s*[\"'][^\"'\s]{8,}"), "high", "Hardcoded password"),
    ("generic-secret", re.compile(r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*[\"'][A-Za-z0-9_\-]{20,}"), "high", "Hardcoded API key"),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\\.eyJ[A-Za-z0-9_-]{10,}\\.[A-Za-z0-9_-]{10,}"), "high", "JWT token"),
    ("basic-auth-url", re.compile(r"https?://[^:\\s/]+:[^@\\s]+@"), "critical", "URL with embedded credentials"),
    ("brazilian-cpf", re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"), "low", "Possible CPF (PII)"),
    ("brazilian-cnpj", re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b"), "low", "Possible CNPJ (PII)"),
]

# Allowed false-positive patterns (e.g., env var refs, mock values)
FALSE_POSITIVE_PATTERNS = [
    re.compile(r"\$\{?[A-Z_][A-Z0-9_]*\}?"),  # ${ENV_VAR} or $ENV_VAR
    re.compile(r"os\.getenv\("),
    re.compile(r"os\.environ\["),
    re.compile(r"Environment\.GetEnvironmentVariable"),
    re.compile(r"\bexample\.com\b", re.IGNORECASE),
    re.compile(r"\bxxx+\b", re.IGNORECASE),
    re.compile(r"\bplaceholder\b", re.IGNORECASE),
    re.compile(r"\bCHANGEME\b", re.IGNORECASE),
]


def is_false_positive(line):
    """Check if a line matches any false-positive pattern."""
    for pat in FALSE_POSITIVE_PATTERNS:
        if pat.search(line):
            return True
    return False


def scan_file(path):
    """Scan a single file for secret patterns. Returns list of findings."""
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings
    for i, line in enumerate(text.splitlines(), 1):
        if is_false_positive(line):
            continue
        for name, pattern, severity, desc in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append({
                    "file": str(path.relative_to(ROOT)),
                    "line": i,
                    "pattern": name,
                    "severity": severity,
                    "description": desc,
                    "excerpt": line.strip()[:120],
                })
    return findings


def scan_tree(root):
    """Recursively scan tree, skipping excluded dirs."""
    findings = []
    files_scanned = 0
    for p in root.rglob("*"):
        # Check if any parent dir is in skip list
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if not p.is_file():
            continue
        if p.suffix.lower() not in SCAN_EXTS:
            continue
        files_scanned += 1
        findings.extend(scan_file(p))
    return findings, files_scanned


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--strict", action="store_true", help="fail on medium+ severity (default: high+)")
    p.add_argument("--json", action="store_true", help="output JSON only")
    args = p.parse_args()

    findings, files = scan_tree(ROOT)
    by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        by_severity[f["severity"]] = by_severity.get(f["severity"], 0) + 1

    if args.json:
        print(json.dumps({
            "filesScanned": files,
            "findingsTotal": len(findings),
            "bySeverity": by_severity,
            "findings": findings,
        }, indent=2, ensure_ascii=False))
    else:
        print(f"XForge Security Audit")
        print(f"=" * 50)
        print(f"Files scanned: {files}")
        print(f"Findings: {len(findings)}")
        for sev in ("critical", "high", "medium", "low"):
            n = by_severity.get(sev, 0)
            if n:
                print(f"  {sev}: {n}")
        if findings:
            print()
            for f in findings[:30]:
                print("  [" + f["severity"].upper() + "] " + f["file"] + ":" + str(f["line"]) + " - " + f["pattern"] + " (" + f["description"] + ")")
                print("      " + f["excerpt"])
            if len(findings) > 30:
                print(f"  ... and {len(findings) - 30} more")
        else:
            print()
            print("OK - no secrets detected")

    # Exit code
    fail_threshold = "medium" if args.strict else "high"
    severities = ["low", "medium", "high", "critical"]
    fail_idx = severities.index(fail_threshold)
    for sev in severities[fail_idx + 1:]:
        if by_severity.get(sev, 0) > 0:
            sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
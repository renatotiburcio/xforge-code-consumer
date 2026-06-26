"""
LGPD Compliance Scanner for XForge.
Scans generated code for personal data handling, consent mechanisms, and data protection.
"""
import os
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

PERSONAL_DATA_PATTERNS = {
    "cpf": r"\bCPF\b|\bCpf\b|\b[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}\b",
    "rg": r"\bRG\b|\bRg\b",
    "email": r"\bemail\b|\bEmail\b|\bEMail\b|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "telefone": r"\btelefone\b|\bTelefone\b|\bcelular\b|\bCelular\b|\bphone\b|\bPhone\b",
    "endereco": r"\bendereco\b|\bEndereco\b|\baddress\b|\bAddress\b|\blogradouro\b",
    "cep": r"\bCEP\b|\bCep\b|\b[0-9]{5}-[0-9]{3}\b",
    "datanascimento": r"\bdatanascimento\b|\bDataNascimento\b|\bdata_nascimento\b|\bbirthdate\b|\bBirthDate\b",
    "genero": r"\bgenero\b|\bGenero\b|\bgender\b|\bGender\b",
    "raca": r"\braca\b|\bRaca\b|\brace\b|\bRace\b",
    "saude": r"\bsaude\b|\bSaude\b|\bhealth\b|\bHealth\b|\bdoenca\b|\bDoenca\b",
    "biometria": r"\bbiometria\b|\bBiometria\b|\bbiometric\b|\bBiometric\b",
    "religiao": r"\breligiao\b|\bReligiao\b|\breligion\b|\bReligion\b",
}

SENSITIVE_ENCRYPTION_REQUIRED = ["cpf", "rg", "biometria", "saude"]

REQUIRED_LGPD_ENDPOINTS = [
    r"GET.*dados.*pessoais|GET.*personal.*data",
    r"DELETE.*dados.*pessoais|DELETE.*personal.*data",
    r"PUT.*dados.*pessoais|PUT.*personal.*data",
    r"consentimento|consent",
    r"portabilidade|portability",
]

def scan_for_personal_data(root_dir: str) -> List[Dict]:
    findings = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ("node_modules", "bin", "obj", ".git", "packages")]
        for f in files:
            if f.endswith((".cs", ".ts", ".js", ".py", ".md", ".json")):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()
                    for field_name, pattern in PERSONAL_DATA_PATTERNS.items():
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for m in matches:
                            findings.append({
                                "field": field_name,
                                "file": os.path.relpath(path, root_dir),
                                "line": content[:m.start()].count("\n") + 1,
                                "match": m.group(),
                                "context": content[max(0,m.start()-30):m.end()+30].replace("\n"," ").strip()
                            })
                except Exception:
                    pass
    return findings

def check_encryption(root_dir: str, findings: List[Dict]) -> List[Dict]:
    encryption_issues = []
    sensitive_files = set()
    for f in findings:
        if f["field"] in SENSITIVE_ENCRYPTION_REQUIRED:
            sensitive_files.add(f["file"])
    for sf in sorted(sensitive_files):
        path = os.path.join(root_dir, sf)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            has_encrypt = bool(re.search(r"Encrypt|encrypt|Protected|protected|HashSet|hash", content))
            if not has_encrypt:
                encryption_issues.append({
                    "file": sf,
                    "issue": "Sensitive personal data without encryption"
                })
        except:
            pass
    return encryption_issues

def check_lgpd_endpoints(root_dir: str) -> List[Dict]:
    missing = []
    cmd_dir = os.path.join(root_dir, ".kilo", "commands")
    api_files = []
    for root, dirs, files in os.walk(cmd_dir):
        for f in files:
            if f.endswith(".md"):
                api_files.append(os.path.join(root, f))
    content = " ".join(open(f, "r", encoding="utf-8", errors="ignore").read() for f in api_files if os.path.exists(f))
    for endpoint_pattern in REQUIRED_LGPD_ENDPOINTS:
        if not re.search(endpoint_pattern, content, re.IGNORECASE):
            desc = endpoint_pattern.replace("|", " or ")
            missing.append({
                "required_endpoint": "Endpoint for: " + desc,
                "status": "NOT FOUND"
            })
    return missing

def check_consent(root_dir: str) -> List[Dict]:
    consent_issues = []
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith(("Request.cs", "Dto.cs", "DTO.cs", "Command.cs")):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()
                    has_personal_data = bool(re.search(r"CPF|Cpf|Email|email|Telefone|telefone", content))
                    has_consent = bool(re.search(r"Consentimento|consentimento|Consent|consent|Autorizacao|autorizacao", content))
                    if has_personal_data and not has_consent:
                        consent_issues.append({
                            "file": os.path.relpath(path, root_dir),
                            "issue": "Has personal data fields but no consent mechanism"
                        })
                except:
                    pass
    return consent_issues

def generate_report(root_dir: str) -> Dict:
    personal_data = scan_for_personal_data(root_dir)
    encryption = check_encryption(root_dir, personal_data)
    endpoints = check_lgpd_endpoints(root_dir)
    consent = check_consent(root_dir)

    report = {
        "summary": {
            "personal_data_fields_found": len(personal_data),
            "encryption_issues": len(encryption),
            "missing_endpoints": len(endpoints),
            "consent_issues": len(consent),
            "overall_score": "PASS" if len(personal_data) < 10 and len(encryption) == 0 else "WARN" if len(personal_data) < 50 else "FAIL"
        },
        "findings": {
            "personal_data": personal_data[:30],
            "encryption": encryption,
            "missing_lgpd_endpoints": endpoints,
            "consent": consent[:20]
        },
        "recommendations": []
    }

    if encryption:
        report["recommendations"].append("Add encryption attributes to all sensitive personal data fields")
    if endpoints:
        report["recommendations"].append("Implement missing LGPD data subject rights endpoints")
    if consent:
        report["recommendations"].append("Add consent collection to all APIs handling personal data")
    if personal_data:
        report["recommendations"].append("Review all personal data fields for LGPD compliance (legal basis, purpose, retention)")

    return report

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    report = generate_report(root)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    grade = report["summary"]["overall_score"]
    if grade == "FAIL":
        sys.exit(2)
    elif grade == "WARN":
        sys.exit(1)
    sys.exit(0)

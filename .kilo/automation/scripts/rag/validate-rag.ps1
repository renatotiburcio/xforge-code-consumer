$ErrorActionPreference = "Stop"

Write-Host "Validating local RAG..."

if (!(Test-Path ".xforge/rag/config.json")) { throw "Missing .xforge/rag/config.json" }
if (!(Test-Path ".kilo/automation/scripts/rag/rag_local.py")) { throw "Missing rag_local.py" }

if (!(Test-Path ".xforge/rag/indexes/lexical.json") -or !(Test-Path ".xforge/rag/chunks/chunks.jsonl")) {
  Write-Host "[INFO] RAG index missing. Creating index..."
  & ./.kilo/automation/scripts/rag/index-local.ps1
}

& ./.kilo/automation/scripts/rag/status-index.ps1
if ($LASTEXITCODE -ne 0) {
  throw "RAG index is stale. Run .\.kilo\automation\scripts\rag\index-local.ps1"
}

if (!(Test-Path ".kilo/automation/scripts/rag/validate-no-secrets.ps1")) {
  throw "Missing .kilo/automation/scripts/rag/validate-no-secrets.ps1"
}
& ./.kilo/automation/scripts/rag/validate-no-secrets.ps1
if ($LASTEXITCODE -ne 0) {
  throw "Potential secrets found in RAG sources. Review .xforge/rag/reports/secret-scan-report.md"
}

Write-Host "Local RAG validation passed."

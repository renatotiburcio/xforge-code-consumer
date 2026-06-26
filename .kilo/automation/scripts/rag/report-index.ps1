$ErrorActionPreference = "Stop"

if (Test-Path ".xforge/rag/reports/index-report.md") {
  Get-Content ".xforge/rag/reports/index-report.md"
} else {
  Write-Host "No RAG index report found. Run .\.kilo\automation\scripts\rag\index-local.ps1"
}

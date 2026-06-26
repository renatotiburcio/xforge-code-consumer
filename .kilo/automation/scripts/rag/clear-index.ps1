$ErrorActionPreference = "Stop"

$paths = @(
  ".xforge/rag/chunks/chunks.jsonl",
  ".xforge/rag/indexes/lexical.json",
  ".xforge/rag/reports/index-report.md"
)

foreach ($path in $paths) {
  if (Test-Path $path) {
    Remove-Item $path -Force
    Write-Host "[REMOVE] $path"
  }
}

Write-Host "Local RAG index cleared."


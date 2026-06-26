$ErrorActionPreference = "Stop"

Write-Host "Indexing local XForge RAG..."
py ./.kilo/automation/scripts/rag/rag_local.py index


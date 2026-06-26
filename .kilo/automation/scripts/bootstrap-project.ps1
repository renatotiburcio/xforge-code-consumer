$ErrorActionPreference = "Stop"

Write-Host "XForge Project Bootstrap"
Write-Host "========================"

$root = (Get-Location).Path
Write-Host "Project root: $root"

$requiredDirs = @(
  ".xforge",
  ".xforge/memory",
  ".xforge/knowledge",
  ".xforge/project-dna",
  ".xforge/decisions",
  ".xforge/rag",
  ".xforge/rag/sources",
  ".xforge/rag/chunks",
  ".xforge/rag/indexes",
  ".xforge/rag/queries",
  ".xforge/rag/reports"
)

foreach ($dir in $requiredDirs) {
  if (!(Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    Write-Host "[CREATE] $dir"
  }
}

if (!(Test-Path ".xforge/project-dna/PROJECT-DNA.md")) {
  @"
# Project DNA

## Status

Pending project recognition.
"@ | Set-Content ".xforge/project-dna/PROJECT-DNA.md" -Encoding UTF8
  Write-Host "[CREATE] .xforge/project-dna/PROJECT-DNA.md"
}

Write-Host ""
Write-Host "Running doctor..."
& ./.kilo/automation/scripts/doctor.ps1

Write-Host ""
Write-Host "Running validate-engineer..."
& ./.kilo/automation/scripts/validate-engineer.ps1

Write-Host ""
Write-Host "Bootstrap completed."
Write-Host "Next command in KiloCode: /analisar-projeto"

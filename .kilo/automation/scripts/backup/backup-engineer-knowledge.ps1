$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = ".engineer-backups"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
$out = Join-Path $backupDir "engineer-knowledge-$timestamp.zip"
$items = @(
  ".xforge/memory",
  ".xforge/knowledge",
  ".xforge/project-dna",
  ".xforge/decisions",
  ".xforge/customizations",
  ".xforge/engineer/persistent-memory",
  ".xforge/engineer/knowledge",
  ".xforge/engineer/knowledge-packs",
  ".xforge/engineer/knowledge-graph",
  ".xforge/engineer/curated-operational-knowledge",
  ".xforge/engineer/market-intelligence",
  ".xforge/engineer/expert-evolution",
  ".xforge/engineer/support-learning",
  ".xforge/engineer/production-learning",
  ".xforge/engineer/known-errors",
  ".xforge/engineer/audit-trail",
  ".xforge/engineer/why-memory",
  ".kilo/custom"
)
$temp = Join-Path $backupDir "tmp-knowledge-$timestamp"
New-Item -ItemType Directory -Path $temp -Force | Out-Null
foreach ($item in $items) {
  if (Test-Path $item) { Copy-Item $item (Join-Path $temp $item) -Recurse -Force }
}
Compress-Archive -Path (Join-Path $temp "*") -DestinationPath $out -Force
Remove-Item $temp -Recurse -Force
Write-Host "Knowledge backup created: $out"

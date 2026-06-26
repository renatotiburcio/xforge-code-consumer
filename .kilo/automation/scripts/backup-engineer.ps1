$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupRoot = ".engineer-backups/$timestamp"
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null

$items = @(
  "AGENTS.md",
  "kilo.jsonc",
  ".kilocodeignore",
  ".kilo",
  ".xforge",
  "README.md",
  ".xforge/docs/INSTALL.md"
)

foreach ($item in $items) {
  if (Test-Path $item) {
    $target = Join-Path $backupRoot $item
    New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
    Copy-Item $item $target -Recurse -Force
    Write-Host "[BACKUP] $item"
  }
}

Write-Host "Backup created at: $backupRoot"

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = ".engineer-backups"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
$out = Join-Path $backupDir "engineer-full-$timestamp.zip"
$items = @("AGENTS.md","kilo.jsonc",".kilo",".xforge/engineer","docs","docs-html","scripts","operations","xforge-engineer.config.json","engineer.config.json")
$temp = Join-Path $backupDir "tmp-full-$timestamp"
New-Item -ItemType Directory -Path $temp -Force | Out-Null
foreach ($item in $items) {
  if (Test-Path $item) {
    Copy-Item $item (Join-Path $temp $item) -Recurse -Force
  }
}
Compress-Archive -Path (Join-Path $temp "*") -DestinationPath $out -Force
Remove-Item $temp -Recurse -Force
Write-Host "Backup full created: $out"

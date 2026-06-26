param([Parameter(Mandatory=$true)][string]$BackupZip,[switch]$Force)
$ErrorActionPreference = "Stop"
if (!(Test-Path $BackupZip)) { throw "BackupZip not found: $BackupZip" }
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$temp = ".engineer-restore-temp/$timestamp"
$review = ".engineer-restore-review/$timestamp"
New-Item -ItemType Directory -Path $temp -Force | Out-Null
New-Item -ItemType Directory -Path $review -Force | Out-Null
Expand-Archive -Path $BackupZip -DestinationPath $temp -Force
Get-ChildItem $temp -Recurse -File | ForEach-Object {
  $relative = $_.FullName.Substring((Resolve-Path $temp).Path.Length).TrimStart('\','/').Replace('\','/')
  if ($relative -notmatch "^(\.kilo|\.xforge|AGENTS\.md|kilo\.jsonc|README\.md|INSTALL\.md|\.kilocodeignore)") {
    Write-Host "[SKIP] Unexpected restore path: $relative"
    return
  }
  if (Test-Path $relative) {
    if ($Force) { Copy-Item $_.FullName $relative -Force }
    else {
      $target = Join-Path $review $relative
      New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
      Copy-Item $_.FullName $target -Force
    }
  } else {
    New-Item -ItemType Directory -Path (Split-Path $relative -Parent) -Force | Out-Null
    Copy-Item $_.FullName $relative -Force
  }
}
Remove-Item $temp -Recurse -Force
Write-Host "Restore completed. Review conflicts in: $review"

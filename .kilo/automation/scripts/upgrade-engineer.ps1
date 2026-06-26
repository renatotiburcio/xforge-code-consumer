param(
  [Parameter(Mandatory=$true)][string]$NewEngineerRoot,
  [switch]$ForceSystemFiles
)
$ErrorActionPreference = "Stop"
if (!(Test-Path $NewEngineerRoot)) { throw "NewEngineerRoot not found: $NewEngineerRoot" }

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$mergeReview = ".engineer-merge-review/$timestamp"
New-Item -ItemType Directory -Path $mergeReview -Force | Out-Null

$preservePrefixes = @(
 ".xforge/memory",".xforge/knowledge",".xforge/project-dna",
 ".xforge/engineer/persistent-memory",".xforge/engineer/knowledge",".xforge/engineer/knowledge-packs",
 ".xforge/engineer/known-errors",".xforge/engineer/audit-trail",".xforge/engineer/why-memory",
 ".xforge/engineer/ecosystem-consolidation",".xforge/engineer/dotnet-standards/studied",".xforge/engineer/customers",
 ".xforge/customizations",".xforge/decisions"
)

function Should-Preserve($path) {
  $n = $path.Replace('\','/')
  foreach ($prefix in $preservePrefixes) { if ($n.StartsWith($prefix)) { return $true } }
  return $false
}

& ./.kilo/automation/scripts/backup-engineer.ps1

Get-ChildItem $NewEngineerRoot -Recurse -File | ForEach-Object {
  $relative = $_.FullName.Substring((Resolve-Path $NewEngineerRoot).Path.Length).TrimStart('\','/').Replace('\','/')
  if (Should-Preserve $relative) { Write-Host "[PRESERVE] $relative"; return }
  if (Test-Path $relative) {
    if ($ForceSystemFiles) {
      Copy-Item $_.FullName $relative -Force
      Write-Host "[UPDATE] $relative"
    } else {
      $reviewTarget = Join-Path $mergeReview $relative
      New-Item -ItemType Directory -Path (Split-Path $reviewTarget -Parent) -Force | Out-Null
      Copy-Item $_.FullName $reviewTarget -Force
      Write-Host "[REVIEW] $relative"
    }
  } else {
    New-Item -ItemType Directory -Path (Split-Path $relative -Parent) -Force | Out-Null
    Copy-Item $_.FullName $relative -Force
    Write-Host "[ADD] $relative"
  }
}
Write-Host "Upgrade completed. Review conflicts in: $mergeReview"

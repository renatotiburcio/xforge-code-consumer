param(
  [Parameter(Mandatory=$false)]
  [string]$Destination = "C:\tmp\xforge-terminal-copy-test"
)

$ErrorActionPreference = "Stop"

$source = (Resolve-Path ".").Path
if (!(Test-Path ".kilo") -or !(Test-Path ".xforge")) {
  throw "Run this script from the root of an installed XForge terminal template."
}

if (Test-Path $Destination) {
  Remove-Item $Destination -Recurse -Force
}

New-Item -ItemType Directory -Path $Destination -Force | Out-Null

$items = @("AGENTS.md", "kilo.jsonc", ".kilocodeignore", ".kilo", ".xforge", "README.md", ".xforge/docs/INSTALL.md")
foreach ($item in $items) {
  if (Test-Path $item) {
    Copy-Item $item (Join-Path $Destination $item) -Recurse -Force
    Write-Host "[COPY] $item"
  }
}

Push-Location $Destination
try {
  & ./.kilo/automation/scripts/doctor.ps1
  & ./.kilo/automation/scripts/validate-engineer.ps1
  & ./.kilo/automation/scripts/final-doctor.ps1
} finally {
  Pop-Location
}

Write-Host "Template copy test passed: $Destination"

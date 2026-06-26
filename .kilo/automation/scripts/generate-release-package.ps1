param(
  [Parameter(Mandatory=$false)]
  [string]$OutputDir = "dist"
)

$ErrorActionPreference = "Stop"

Write-Host "Generating XForge terminal release package..."

$sevenZip = (Get-Command 7z.exe -ErrorAction SilentlyContinue).Source
if (-not $sevenZip) {
  $defaultSevenZip = "C:\Program Files\7-Zip\7z.exe"
  if (Test-Path $defaultSevenZip) {
    $sevenZip = $defaultSevenZip
  }
}
if (-not $sevenZip) {
  $defaultSevenZipX86 = "C:\Program Files (x86)\7-Zip\7z.exe"
  if (Test-Path $defaultSevenZipX86) {
    $sevenZip = $defaultSevenZipX86
  }
}
if (-not $sevenZip) {
  throw "7-Zip not found. Install 7-Zip or add 7z.exe to PATH."
}

& ./.kilo/automation/scripts/doctor.ps1
& ./.kilo/automation/scripts/validate-engineer.ps1
& ./.kilo/automation/scripts/final-doctor.ps1
& ./.kilo/automation/scripts/rag/validate-rag.ps1

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$outputFull = Join-Path (Get-Location) $OutputDir
$zip = Join-Path $outputFull "xforge-terminal-$timestamp.zip"
New-Item -ItemType Directory -Path $outputFull -Force | Out-Null

$items = @("AGENTS.md", ".xforge/docs/INSTALL.md", "README.md", "kilo.jsonc", ".kilocodeignore", ".kilo", ".xforge")
$zipArgs = @(
  "a",
  "-tzip",
  $zip,
  "-mx=5"
)
foreach ($item in $items) {
  $zipArgs += $item
}
$zipArgs += @(
  "-xr!.xforge\rag\chunks\*",
  "-xr!.xforge\rag\indexes\*",
  "-xr!.xforge\rag\reports\*",
  "-xr!.xforge\reports\*",
  "-xr!.xforge\backlog\*",
  "-xr!.xforge\audits\*",
  "-xr!.xforge\docs-html-audits\*",
  "-xr!.xforge\testing\*",
  "-xr!.xforge\changelog\*",
  "-xr!.xforge\incidents\*",
  "-xr!.xforge\legacy\*",
  "-xr!.xforge\legacy-skills\*",
  "-xr!.xforge\roadmap\*",
  "-xr!.xforge\sprints\*",
  "-xr!.xforge\backups\*",
  "-xr!.xforge\temp\*",
  "-xr!dist\*",
  "-xr!node_modules",
  "-xr!.git"
)

if (Test-Path $zip) {
  Remove-Item $zip -Force
}

& $sevenZip @zipArgs | Out-Host

Write-Host "Release package created: $zip"

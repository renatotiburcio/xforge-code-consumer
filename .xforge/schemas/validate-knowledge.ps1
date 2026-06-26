#!/usr/bin/env pwsh
# Validate .xforge/knowledge/**/*.md frontmatter against knowledge.schema.json
# Rules:
#   - Frontmatter is OPTIONAL (loose files are valid)
#   - If frontmatter is present: id and type are REQUIRED
#   - All other fields are optional
[CmdletBinding()]
param(
  [string]$Root = "D:\dev\XForge-Development-New",
  [string]$KnowledgeDir = ".xforge\knowledge",
  [string]$Schema = ".xforge\schemas\knowledge.schema.json"
)
$ErrorActionPreference = "Stop"
$KnowledgeAbs = Join-Path $Root $KnowledgeDir
$SchemaAbs    = Join-Path $Root $Schema
$SchemaJson   = Get-Content -LiteralPath $SchemaAbs -Raw | ConvertFrom-Json
$Req          = $SchemaJson.required

$files   = Get-ChildItem -LiteralPath $KnowledgeAbs -Recurse -File -Filter "*.md"
$total   = $files.Count
$valid   = 0
$loose   = 0
$invalid = 0
$errors  = New-Object System.Collections.Generic.List[object]

foreach ($f in $files) {
  $content = Get-Content -LiteralPath $f.FullName -Raw
  $fmMatch = [regex]::Match($content, '(?s)^---\r?\n(.+?)\r?\n---')
  if (-not $fmMatch.Success) {
    $loose++
    continue
  }
  $fm = $fmMatch.Groups[1].Value
  $props = @{}
  foreach ($line in ($fm -split "`r?`n")) {
    if ($line -match '^\s*#') { continue }
    if ($line -match '^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$') {
      $props[$matches[1]] = $matches[2].Trim()
    }
  }
  $missing = @()
  foreach ($r in $Req) { if (-not $props.ContainsKey($r) -or [string]::IsNullOrWhiteSpace($props[$r])) { $missing += $r } }
  if ($missing.Count -eq 0) { $valid++ } else {
    $invalid++
    $errors.Add([pscustomobject]@{ File = $f.Name; Reason = ("missing: " + ($missing -join ", ")) }) | Out-Null
  }
}

Write-Host ""
Write-Host "Knowledge Validation Report" -ForegroundColor Cyan
Write-Host ("=" * 50)
Write-Host ("Total:   $total")
Write-Host ("Valid:   $valid   (with frontmatter + required fields)") -ForegroundColor Green
Write-Host ("Loose:   $loose   (no frontmatter, accepted as free-form)") -ForegroundColor DarkGray
Write-Host ("Invalid: $invalid  (frontmatter present but missing required fields)") -ForegroundColor $(if ($invalid -gt 0) { "Red" } else { "Green" })
Write-Host ""
if ($errors.Count -gt 0) {
  Write-Host "Errors:" -ForegroundColor Yellow
  $errors | ForEach-Object { Write-Host ("  {0,-60} {1}" -f $_.File, $_.Reason) }
  exit 1
}
Write-Host "All knowledge files valid." -ForegroundColor Green
exit 0
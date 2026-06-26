param([Parameter(Mandatory=$true)][string]$NewEngineerRoot)
$ErrorActionPreference = "Stop"
if (!(Test-Path $NewEngineerRoot)) { throw "NewEngineerRoot not found: $NewEngineerRoot" }
New-Item -ItemType Directory -Path "engineer/migrations" -Force | Out-Null
$report = "engineer/migrations/COMPARE-ENGINEER-VERSION.md"
"# Engineer Version Compare" | Out-File $report -Encoding utf8
Get-ChildItem $NewEngineerRoot -Recurse -File | ForEach-Object {
  $relative = $_.FullName.Substring((Resolve-Path $NewEngineerRoot).Path.Length).TrimStart('\','/').Replace('\','/')
  if (!(Test-Path $relative)) { "- NEW: $relative" | Out-File $report -Append }
  else { "- EXISTS: $relative" | Out-File $report -Append }
}
Write-Host "Compare report: $report"

$ErrorActionPreference = "Stop"

Write-Host "XForge Engineer Final Doctor"

$required = @(
  "AGENTS.md",
  "kilo.jsonc",
  ".kilo/commands",
  ".kilo/skills",
  ".kilo/rules",
  ".kilo/docs-html",
  ".xforge",
  ".xforge/engineer",
  ".xforge/project-dna",
  ".xforge/memory",
  ".xforge/knowledge"
)

$errors = 0
foreach($item in $required){
  if(Test-Path $item){ Write-Host "[OK] $item" }
  else {
    Write-Host "[MISSING] $item"
    $errors++
  }
}

Write-Host "Checking standardized commands..."
$standard = @(
  "xforge","xforge-reconhecer-projeto","xforge-criar-projeto-dotnet","xforge-dev",
  "xforge-validar-qualidade","xforge-memoria","xforge-docs","xforge-gerar-release"
)

foreach($cmd in $standard){
  $path = ".kilo/commands/$cmd.md"
  if(Test-Path $path){ Write-Host "[OK] /$cmd" }
  else {
    Write-Host "[MISSING] /$cmd"
    $errors++
  }
}

Write-Host "Final doctor completed."
if ($errors -gt 0) { exit 1 }

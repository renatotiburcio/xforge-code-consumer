# XForge Init — Golden Command
# Ponto de entrada único: inicializa + valida + onboarding
# Uso: .\.kilo\automation\scripts\xforge-init.ps1

param(
    [switch]$SkipIntro,
    [switch]$Force
)

$ErrorActionPreference = "Continue"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
Push-Location $Root

$startTime = Get-Date
$checks = @()

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       BEM-VINDO AO XFORGE v54.0                        ║" -ForegroundColor Cyan
Write-Host "║       Split Architecture · AutoResearch · IA Local      ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check 1: Ollama availability
Write-Host "[1/8] Verificando Ollama..." -ForegroundColor Yellow
try {
    $ollamaTest = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 3
    $checks += @{ Name = "Ollama"; Status = "PASS"; Detail = "Online" }
    Write-Host "  Ollama online" -ForegroundColor Green
} catch {
    $checks += @{ Name = "Ollama"; Status = "WARN"; Detail = "Offline" }
    Write-Host "  Ollama offline" -ForegroundColor Yellow
}

# Check 2: Doctor
Write-Host "[2/8] Rodando Doctor..." -ForegroundColor Yellow
$doctorOutput = powershell -ExecutionPolicy Bypass -File ".\.kilo\automation\scripts\doctor.ps1" 2>&1 | Out-String
$doctorErrors = ([regex]::Matches($doctorOutput, "\[ERROR\]")).Count
$doctorOk = ([regex]::Matches($doctorOutput, "\[OK\]")).Count
if ($doctorErrors -eq 0) {
    $checks += @{ Name = "Doctor"; Status = "PASS"; Detail = "$doctorOk OK, 0 errors" }
    Write-Host "  ✅ $doctorOk OK, 0 errors" -ForegroundColor Green
} else {
    $checks += @{ Name = "Doctor"; Status = "FAIL"; Detail = "$doctorErrors errors" }
    Write-Host "  ❌ $doctorErrors errors encontrados" -ForegroundColor Red
}

# Check 3: Knowledge
Write-Host "[3/8] Verificando Knowledge..." -ForegroundColor Yellow
$knowledgeFiles = (Get-ChildItem -Path ".xforge/knowledge" -Recurse -Filter "*.md" -ErrorAction SilentlyContinue).Count
$indexExists = Test-Path ".xforge/knowledge/INDEX.json"
if ($knowledgeFiles -ge 170 -and $indexExists) {
    $checks += @{ Name = "Knowledge"; Status = "PASS"; Detail = "$knowledgeFiles files + INDEX" }
    Write-Host "  ✅ $knowledgeFiles files + INDEX.json" -ForegroundColor Green
} else {
    $checks += @{ Name = "Knowledge"; Status = "WARN"; Detail = "$knowledgeFiles files" }
    Write-Host "  ⚠️ Knowledge: $knowledgeFiles files" -ForegroundColor Yellow
}

# Check 4: Error Graph
Write-Host "[4/8] Verificando Error Graph..." -ForegroundColor Yellow
$graphFile = ".xforge\knowledge\errors-solutions-graph.json"
if (Test-Path $graphFile) {
    try {
        $graph = Get-Content $graphFile -Raw -Encoding UTF8 | ConvertFrom-Json
        $errorCount = $graph.errorPatterns.Count
        $ruleCount = $graph.preventionRules.Count
        $checks += @{ Name = "Error Graph"; Status = "PASS"; Detail = "$errorCount errors, $ruleCount rules" }
        Write-Host "  ✅ Error Graph: $errorCount errors, $ruleCount prevention rules" -ForegroundColor Green
    } catch {
        $checks += @{ Name = "Error Graph"; Status = "WARN"; Detail = "JSON parse error" }
        Write-Host "  ⚠️ Error Graph: erro ao ler JSON" -ForegroundColor Yellow
    }
} else {
    $checks += @{ Name = "Error Graph"; Status = "WARN"; Detail = "Não encontrado em .xforge\knowledge\" }
    Write-Host "  ⚠️ Error Graph não encontrado em .xforge\knowledge\errors-solutions-graph.json" -ForegroundColor Yellow
}

# Check 5: Scripts
Write-Host "[5/8] Verificando Scripts..." -ForegroundColor Yellow
$requiredScripts = @("doctor.ps1", "score.ps1", "pre-commit.ps1", "live-dashboard.ps1", "knowledge-validation.ps1", "dependency-check.ps1", "proactive-intelligence.ps1")
$scriptsOk = 0
foreach ($script in $requiredScripts) {
    if (Test-Path ".\.kilo\automation\scripts\$script") { $scriptsOk++ }
}
if ($scriptsOk -eq $requiredScripts.Count) {
    $checks += @{ Name = "Scripts"; Status = "PASS"; Detail = "$scriptsOk scripts" }
    Write-Host "  ✅ $scriptsOk/$($requiredScripts.Count) scripts" -ForegroundColor Green
} else {
    $checks += @{ Name = "Scripts"; Status = "WARN"; Detail = "$scriptsOk/$($requiredScripts.Count)" }
    Write-Host "  ⚠️ $scriptsOk/$($requiredScripts.Count) scripts" -ForegroundColor Yellow
}

# Check 6: Rules
Write-Host "[6/8] Verificando Rules..." -ForegroundColor Yellow
$rulesCount = (Get-ChildItem -Path ".kilo/rules" -Filter "*.md" -ErrorAction SilentlyContinue).Count
if ($rulesCount -ge 28) {
    $checks += @{ Name = "Rules"; Status = "PASS"; Detail = "$rulesCount rules" }
    Write-Host "  ✅ $rulesCount rules" -ForegroundColor Green
} else {
    $checks += @{ Name = "Rules"; Status = "WARN"; Detail = "$rulesCount rules" }
    Write-Host "  ⚠️ $rulesCount rules" -ForegroundColor Yellow
}

# Check 7: Manual
Write-Host "[7/8] Verificando Manual..." -ForegroundColor Yellow
if (Test-Path "docs/index.html") {
    $manualLines = (Get-Content "docs/index.html" | Measure-Object).Count
    $checks += @{ Name = "Manual"; Status = "PASS"; Detail = "$manualLines lines" }
    Write-Host "  ✅ docs/index.html ($manualLines lines)" -ForegroundColor Green
} else {
    $checks += @{ Name = "Manual"; Status = "WARN"; Detail = "Não encontrado" }
    Write-Host "  ⚠️ Manual não encontrado" -ForegroundColor Yellow
}

# Check 8: Knowledge Validation
Write-Host "[8/8] Validando Knowledge..." -ForegroundColor Yellow
if (Test-Path ".\.kilo\automation\scripts\knowledge-validation.ps1") {
    $validationOutput = powershell -ExecutionPolicy Bypass -File ".\.kilo\automation\scripts\knowledge-validation.ps1" 2>&1 | Out-String
    $validated = ([regex]::Matches($validationOutput, "OK")).Count
    if ($validated -ge 5) {
        $checks += @{ Name = "Validation"; Status = "PASS"; Detail = "$validated areas" }
        Write-Host "  ✅ $validated areas validated" -ForegroundColor Green
    } else {
        $checks += @{ Name = "Validation"; Status = "WARN"; Detail = "$validated areas" }
        Write-Host "  ⚠️ $validated areas validated" -ForegroundColor Yellow
    }
} else {
    $checks += @{ Name = "Validation"; Status = "SKIP"; Detail = "Script não encontrado" }
    Write-Host "  ⚠️ Script de validação não encontrado" -ForegroundColor Yellow
}

# Calculate score
$totalChecks = $checks.Count
$passedChecks = ($checks | Where-Object { $_.Status -eq "PASS" }).Count
$score = [Math]::Round(($passedChecks / $totalChecks) * 100)
$elapsed = [Math]::Round(((Get-Date) - $startTime).TotalSeconds, 1)

# Final Report
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              XFORGE INIT — RESULTADO                   ║" -ForegroundColor Cyan
Write-Host "╠══════════════════════════════════════════════════════════╣" -ForegroundColor Cyan

foreach ($check in $checks) {
    $icon = switch ($check.Status) { "PASS" { "✅" } "WARN" { "⚠️" } "FAIL" { "❌" } "SKIP" { "⏭️" } }
    $color = switch ($check.Status) { "PASS" { "Green" } "WARN" { "Yellow" } "FAIL" { "Red" } "SKIP" { "Gray" } }
    Write-Host ("║  {0,-12} {1} {2,-35} ║" -f $check.Name, $icon, $check.Detail) -ForegroundColor $color
}

Write-Host "║                                                        ║" -ForegroundColor Cyan
$scoreColor = if ($score -ge 80) { "Green" } elseif ($score -ge 50) { "Yellow" } else { "Red" }
Write-Host ("║  SCORE: {0}% ({1}/{2} checks passed)                       ║" -f $score, $passedChecks, $totalChecks) -ForegroundColor $scoreColor
Write-Host ("║  TIME:  {0}s                                           ║" -f $elapsed) -ForegroundColor Cyan
Write-Host "╠══════════════════════════════════════════════════════════╣" -ForegroundColor Cyan

if ($score -ge 80) {
    Write-Host "║  ✅ XForge pronto! Comece com: /xforge [tarefa]        ║" -ForegroundColor Green
} elseif ($score -ge 50) {
    Write-Host "║  ⚠️ Sistema parcialmente pronto. Corrija warnings.     ║" -ForegroundColor Yellow
} else {
    Write-Host "║  ❌ Sistema com problemas. Veja doctor.ps1.            ║" -ForegroundColor Red
}

Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

Pop-Location

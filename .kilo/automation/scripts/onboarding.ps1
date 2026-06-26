# XForge First-Run Onboarding
# Executa na primeira vez que o usuário usa o XForge
# Uso: .\.kilo\automation\scripts\onboarding.ps1

param(
    [switch]$SkipIntro
)

$ErrorActionPreference = "Continue"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
Push-Location $Root

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       BEM-VINDO AO XFORGE ENTERPRISE DEVELOPMENT OS    ║" -ForegroundColor Cyan
Write-Host "║       v54.0 — Split Architecture · AutoResearch        ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

if (!$SkipIntro) {
    Write-Host "O que é o XForge?" -ForegroundColor Yellow
    Write-Host "Template operacional que transforma KiloCode em assistente enterprise completo." -ForegroundColor White
    Write-Host "148 skills, 43 agents, 132 commands, 30 rules, 173 knowledge files." -ForegroundColor White
    Write-Host ""
    Write-Host "Pressione ENTER para continuar..." -ForegroundColor Gray
    Read-Host
}

# Step 1: Doctor
Write-Host "[1/4] Validando sistema..." -ForegroundColor Yellow
powershell -ExecutionPolicy Bypass -File ".\.kilo\automation\scripts\doctor.ps1"
Write-Host ""

# Step 2: Ollama
Write-Host "[2/4] Verificando Ollama..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5
    Write-Host "  Ollama rodando ($($response.models.Count) models)" -ForegroundColor Green
} catch {
    Write-Host "  Ollama nao esta rodando" -ForegroundColor Yellow
    Write-Host "  Para modo offline: instale Ollama" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Quick test
Write-Host "[3/4] Teste rapido..." -ForegroundColor Yellow
Write-Host "  No KiloCode, digite:" -ForegroundColor White
Write-Host "  /xforge ola! estou comecando. me mostre o que voce pode fazer" -ForegroundColor Cyan
Write-Host ""

# Step 4: Next steps
Write-Host "[4/4] Proximos passos..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Teste: /xforge [sua tarefa]" -ForegroundColor White
Write-Host "  2. Veja o manual: docs/index.html" -ForegroundColor White
Write-Host "  3. Valide sempre: .\.kilo\automation\scripts\doctor.ps1" -ForegroundColor White
Write-Host ""

Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ XForge pronto! Comece com: /xforge [tarefa]        ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green

Pop-Location

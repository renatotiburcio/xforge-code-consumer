<#
xforge install (Windows PowerShell)
Instala xforge CLI no PATH do usuario.

Uso:
  powershell -ExecutionPolicy Bypass -File install.ps1
#>

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CliPath = Join-Path $ScriptDir "cli.py"

if (-not (Test-Path $CliPath)) {
    Write-Error "[XForge] ERRO: cli.py nao encontrado em $ScriptDir"
    exit 1
}

# Criar wrapper .cmd
$BinDir = Join-Path $env:USERPROFILE ".local\bin"
if (-not (Test-Path $BinDir)) {
    New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
}

$WrapperPath = Join-Path $BinDir "xforge.cmd"
@"
@echo off
python "$CliPath" %*
"@ | Out-File -Encoding ASCII $WrapperPath

Write-Host "[XForge] Instalado em: $WrapperPath" -ForegroundColor Green

# Adicionar ao PATH se necessario
$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($CurrentPath -notlike "*$BinDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$CurrentPath;$BinDir", "User")
    Write-Host "[XForge] PATH atualizado (reinicie o terminal)" -ForegroundColor Yellow
}

# Verificar
Write-Host ""
Write-Host "[XForge] Testando instalacao..." -ForegroundColor Cyan
& python $CliPath --version

Write-Host ""
Write-Host "[XForge] Pronto! Use 'xforge --help' para comecar." -ForegroundColor Green
Write-Host "[XForge] Para usar em qualquer projeto:" -ForegroundColor Cyan
Write-Host "  cd meu-projeto"
Write-Host "  xforge init --analyze"
Write-Host "  xforge recognize"
Write-Host "  xforge doctor"

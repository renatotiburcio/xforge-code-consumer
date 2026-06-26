<#
.SYNOPSIS
diff-consumer.ps1 - xforge diff consumer. Mostra template-only paths que ainda existem no projeto.

.DESCRIPTION
DR-0180 Fase 0. Para usuarios que ja clonaram o template, mostra quais paths
template-only (definidos em .xforge/template-only.json) ainda estao presentes
e deveriam ter sido removidos.

Exit codes:
- 0: projeto esta clean (nenhum template-only path encontrado)
- 1: dirty (template-only paths encontrados)

.EXAMPLE
.xforge/scripts/diff-consumer.ps1
$LASTEXITCODE  # 0 ou 1
#>

[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$manifestPath = Join-Path $ProjectRoot '.xforge/template-only.json'
if (-not (Test-Path -LiteralPath $manifestPath)) {
    Write-Error "Manifesto nao encontrado em $manifestPath"
    exit 2
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json

$dirty = @()
foreach ($pattern in $manifest.templateOnly.paths) {
    $full = Join-Path $ProjectRoot $pattern
    if (Test-Path -LiteralPath $full) {
        $dirty += $pattern
    }
}

if ($dirty.Count -eq 0) {
    Write-Host "OK - projeto clean. Nenhum template-only path encontrado." -ForegroundColor Green
    exit 0
} else {
    Write-Host "DIRTY - $($dirty.Count) template-only paths encontrados:" -ForegroundColor Yellow
    foreach ($p in $dirty) {
        Write-Host "  - $p" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Para limpar:" -ForegroundColor Cyan
    Write-Host "  .xforge/scripts/reset-memory.ps1            # Remove template-only paths + purifica memory"
    Write-Host "  .xforge/scripts/reset-memory.ps1 -WhatIf    # Preview"
    exit 1
}

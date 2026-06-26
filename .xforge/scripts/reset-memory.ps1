<#
.SYNOPSIS
reset-memory.ps1 - xforge reset memory. Aplica template-only.json em projeto ja clonado.

.DESCRIPTION
DR-0180 Fase 0. Para usuarios que ja clonaram o template XForge mas nao usaram
init-consumer.ps1. Remove paths template-only (audit, decisions internas, sessions,
learning) e purifica memory.

Suporta:
- -ProjectRoot <path>: projeto alvo (default: cwd)
- -WhatIf: mostra o que seria removido
- -BackupDir <path>: backup custom (default: .xforge-backups/reset-YYYYMMDD-HHmm/)
- -Force: nao pede confirmacao
- -SkipPurify: nao roda purify.ps1 apos reset (so remove template-only paths)

.EXAMPLE
.xforge/scripts/reset-memory.ps1 -WhatIf
.xforge/scripts/reset-memory.ps1 -Force
.xforge/scripts/reset-memory.ps1 -ProjectRoot ../my-project -Force
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$BackupDir,
    [switch]$Force,
    [switch]$SkipPurify
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$manifestPath = Join-Path $ProjectRoot '.xforge/template-only.json'
if (-not (Test-Path -LiteralPath $manifestPath)) {
    throw "Manifesto nao encontrado em $manifestPath. Este projeto nao foi inicializado com init-consumer.ps1. Use purify.ps1 para purificacao basica."
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json

# Backup
$timestamp = Get-Date -Format 'yyyyMMdd-HHmm'
if (-not $BackupDir) {
    $BackupDir = Join-Path $ProjectRoot ".xforge-backups/reset-$timestamp"
}
if ($WhatIfPreference) {
    Write-Host "[WhatIf] Backup seria criado em: $BackupDir" -ForegroundColor Cyan
} else {
    if (-not (Test-Path -LiteralPath $BackupDir)) {
        New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
        Write-Host "Backup criado em: $BackupDir" -ForegroundColor Green
    }
}

# Identifica template-only paths que existem no projeto
$toRemove = @()
foreach ($pattern in $manifest.templateOnly.paths) {
    $full = Join-Path $ProjectRoot $pattern
    if (Test-Path -LiteralPath $full) {
        $toRemove += @{ Pattern = $pattern; FullPath = $full }
    }
}

if ($toRemove.Count -eq 0) {
    Write-Host "Nenhum template-only path encontrado. Projeto ja esta limpo." -ForegroundColor Green
} else {
    Write-Host "Template-only paths encontrados: $($toRemove.Count)" -ForegroundColor Cyan
    foreach ($item in $toRemove) {
        $relativePath = $item.Pattern
        if ($WhatIfPreference) {
            Write-Host "  [WhatIf] Removeria: $relativePath" -ForegroundColor Yellow
        } else {
            # Backup antes de remover
            $backupDst = Join-Path $BackupDir $relativePath
            $backupDstDir = Split-Path -Parent $backupDst
            if (-not (Test-Path -LiteralPath $backupDstDir)) {
                New-Item -ItemType Directory -Path $backupDstDir -Force | Out-Null
            }
            if (Test-Path -LiteralPath $item.FullPath -PathType Container) {
                Copy-Item -LiteralPath $item.FullPath -Destination $backupDst -Recurse -Force
                Remove-Item -LiteralPath $item.FullPath -Recurse -Force
            } else {
                Copy-Item -LiteralPath $item.FullPath -Destination $backupDst -Force
                Remove-Item -LiteralPath $item.FullPath -Force
            }
            Write-Host "  Removido: $relativePath (backup: $backupDst)" -ForegroundColor Yellow
        }
    }
}

# Purify
if (-not $SkipPurify -and -not $WhatIfPreference) {
    Write-Host ""
    Write-Host "Rodando purify.ps1..." -ForegroundColor Cyan
    $purifyScript = Join-Path $ProjectRoot '.xforge/scripts/purify.ps1'
    if (Test-Path -LiteralPath $purifyScript) {
        & $purifyScript -ProjectRoot $ProjectRoot -Force
    } else {
        Write-Warning "purify.ps1 nao encontrado em $ProjectRoot. Pulando purify."
    }
}

Write-Host ""
Write-Host "[DONE] Reset memory completo." -ForegroundColor Green
if (Test-Path -LiteralPath $BackupDir) {
    Write-Host "Backup em: $BackupDir"
}

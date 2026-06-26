<#
.SYNOPSIS
init-consumer.ps1 - xforge init --consumer. Cria projeto limpo copiando apenas paths user-facing.

.DESCRIPTION
DR-0180 Fase 0. Quando o usuario clona o template XForge-Development-New, este script
cria um novo projeto consumidor copiando APENAS os paths declarados em
.xforge/template-only.json como `userFacing`. Paths `templateOnly` (audit, decisions
internas, sessions, learning) NAO sao copiados.

Suporta:
- -TargetDir <path>: diretorio destino (obrigatorio)
- -SourceDir <path>: diretorio origem (default: cwd)
- -Stack <name>: stack manual (default: auto-detect via stack-detector)
- -WhatIf: mostra o que seria copiado sem copiar
- -Force: sobrescreve target dir se existir

.EXAMPLE
.xforge/scripts/init-consumer.ps1 -TargetDir ../my-saas -Stack dotnet
.xforge/scripts/init-consumer.ps1 -TargetDir ../my-saas -WhatIf
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)][string]$TargetDir,
    [string]$SourceDir = (Get-Location).Path,
    [string]$Stack,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Resolve paths
$SourceDir = (Resolve-Path -LiteralPath $SourceDir).Path
$manifestPath = Join-Path $SourceDir '.xforge/template-only.json'
if (-not (Test-Path -LiteralPath $manifestPath)) {
    throw "Manifesto nao encontrado em $manifestPath. Este script deve ser rodado de dentro do template XForge-Development-New."
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json

# Resolve target
if (Test-Path -LiteralPath $TargetDir) {
    if (-not $Force) {
        $existing = Get-ChildItem -LiteralPath $TargetDir -Force | Measure-Object
        if ($existing.Count -gt 0) {
            throw "TargetDir nao vazio: $TargetDir. Use -Force para sobrescrever."
        }
    }
} else {
    if ($WhatIfPreference) {
        Write-Host "[WhatIf] Criaria diretorio: $TargetDir" -ForegroundColor Cyan
    } else {
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    }
}
$TargetDir = (Resolve-Path -LiteralPath $TargetDir).Path

# Stack detection
if (-not $Stack) {
    . (Join-Path $SourceDir '.xforge/scripts/lib/stack-detector.ps1')
    $info = Get-ProjectStack -ProjectRoot $SourceDir -AllowAmbiguous
    $Stack = $info.stack
    Write-Host "Stack detectado: $Stack (confidence $($info.confidence))" -ForegroundColor Green
}

# Copy user-facing paths
$copied = 0
$skipped = 0
$patterns = $manifest.userFacing.paths
foreach ($pattern in $patterns) {
    $src = Join-Path $SourceDir $pattern
    $dst = Join-Path $TargetDir $pattern
    if (Test-Path -LiteralPath $src -PathType Container) {
        # Diretorio
        if ($WhatIfPreference) {
            Write-Host "[WhatIf] Copiaria diretorio: $pattern" -ForegroundColor Cyan
        } else {
            $dstParent = Split-Path -Parent $dst
            if (-not (Test-Path -LiteralPath $dstParent)) {
                New-Item -ItemType Directory -Path $dstParent -Force | Out-Null
            }
            # Copy excluding node_modules and .git
            $exclude = @('node_modules', '.git', '__pycache__', '.next', 'dist', 'build', 'bin', 'obj', 'target', 'vendor')
            $items = Get-ChildItem -LiteralPath $src -Force | Where-Object { $exclude -notcontains $_.Name }
            foreach ($item in $items) {
                $itemDst = Join-Path $dst $item.Name
                if ($item.PSIsContainer) {
                    Copy-Item -LiteralPath $item.FullName -Destination $itemDst -Recurse -Force
                } else {
                    Copy-Item -LiteralPath $item.FullName -Destination $itemDst -Force
                }
            }
            $copied++
        }
    } elseif (Test-Path -LiteralPath $src -PathType Leaf) {
        # Arquivo
        if ($WhatIfPreference) {
            Write-Host "[WhatIf] Copiaria arquivo: $pattern" -ForegroundColor Cyan
        } else {
            $dstParent = Split-Path -Parent $dst
            if (-not (Test-Path -LiteralPath $dstParent)) {
                New-Item -ItemType Directory -Path $dstParent -Force | Out-Null
            }
            Copy-Item -LiteralPath $src -Destination $dst -Force
            $copied++
        }
    } else {
        $skipped++
        Write-Verbose "Pattern nao encontrado (skipped): $pattern"
    }
}

# Copia o proprio manifesto para o target (para auditoria futura)
if ($WhatIfPreference) {
    Write-Host "[WhatIf] Copiaria manifesto para target" -ForegroundColor Cyan
} else {
    $manifestDst = Join-Path $TargetDir '.xforge/template-only.json'
    $manifestDstDir = Split-Path -Parent $manifestDst
    if (-not (Test-Path -LiteralPath $manifestDstDir)) {
        New-Item -ItemType Directory -Path $manifestDstDir -Force | Out-Null
    }
    Copy-Item -LiteralPath $manifestPath -Destination $manifestDst -Force
}

# Purifica memory do target com stack detectado
if (-not $WhatIfPreference) {
    Write-Host ""
    Write-Host "Purificando memory do target com stack=$Stack..." -ForegroundColor Cyan
    & (Join-Path $SourceDir '.xforge/scripts/purify.ps1') -ProjectRoot $TargetDir -Force
}

Write-Host ""
Write-Host "[DONE] Init consumer completo." -ForegroundColor Green
Write-Host "  Target: $TargetDir"
Write-Host "  Stack: $Stack"
Write-Host "  Paths copiados: $copied"
Write-Host "  Paths skipped (nao existem): $skipped"
Write-Host ""
Write-Host "Proximos passos:"
Write-Host "  cd $TargetDir"
Write-Host "  git init"
Write-Host "  # Customize AGENTS.md, README.md, kilo.jsonc conforme o projeto"

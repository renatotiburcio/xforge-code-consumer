<#
.SYNOPSIS
purify.ps1 - Purifica .xforge/memory/ e .xforge/project-dna/ do projeto alvo.

.DESCRIPTION
DR-0180 Fase 1. Detecta stack do projeto, reescreve project-preferences.md
e PROJECT-DNA.md com stack correto, dedupa learning.jsonl, remove lixo.

Suporta:
- -WhatIf: mostra o que mudaria sem alterar nada
- -ProjectRoot <path>: purifica subprojeto (default: cwd)
- -BackupDir <path>: diretorio de backup custom (default: .xforge-backups/purify-YYYYMMDD-HHmm/)
- -Force: nao pede confirmacao
- -SkipBackup: NAO cria backup (USE COM CUIDADO)
- -DryRunProjectDna: so mostra, nao escreve

.EXAMPLE
.\purify.ps1 -WhatIf
.\purify.ps1 -ProjectRoot src/sales-erp
.\purify.ps1 -ProjectRoot src/fastapi-fiscal-demo -Force
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$BackupDir,
    [switch]$Force,
    [switch]$SkipBackup,
    [switch]$DryRunProjectDna
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Carrega lib
$libPath = Join-Path $PSScriptRoot 'lib/stack-detector.ps1'
$rewriterPath = Join-Path $PSScriptRoot 'lib/memory-rewriter.ps1'
if (-not (Test-Path -LiteralPath $libPath)) { throw "Lib nao encontrada: $libPath" }
. $libPath
if (Test-Path -LiteralPath $rewriterPath) { . $rewriterPath }

# Resolve paths
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$xforgeDir = Join-Path $ProjectRoot '.xforge'
if (-not (Test-Path -LiteralPath $xforgeDir)) {
    throw ".xforge nao encontrado em $ProjectRoot. Use -ProjectRoot para apontar para o projeto correto."
}

# Output helper
function Write-Phase {
    param([string]$Phase, [string]$Message)
    Write-Host "[$Phase] $Message" -ForegroundColor Cyan
}

# === STEP 0: Validacoes ===
Write-Phase "0/5" "Projeto alvo: $ProjectRoot"

# === STEP 1: Stack detection ===
Write-Phase "1/5" "Detectando stack..."
$stackInfo = Get-ProjectStack -ProjectRoot $ProjectRoot -AllowAmbiguous
Write-Host "  Stack: $($stackInfo.stack)"
Write-Host "  Confidence: $($stackInfo.confidence)"
Write-Host "  Signals: $($stackInfo.signals -join ', ')"
if ($stackInfo.ambiguous -and -not $Force) {
    Write-Warning "Stack ambiguo. Use -Force para prosseguir mesmo assim."
    if (-not $WhatIfPreference -and -not $Force) {
        $confirm = Read-Host "Prosseguir mesmo assim? (y/N)"
        if ($confirm -ne 'y' -and $confirm -ne 'Y') { exit 1 }
    }
}

# === STEP 2: Backup ===
$timestamp = Get-Date -Format 'yyyyMMdd-HHmm'
if (-not $BackupDir) {
    $BackupDir = Join-Path $ProjectRoot ".xforge-backups/purify-$timestamp"
}
if (-not $SkipBackup) {
    if ($WhatIfPreference) {
        Write-Phase "2/5" "[WhatIf] Backup seria criado em: $BackupDir"
    } else {
        if (Test-Path -LiteralPath $BackupDir) {
            Write-Warning "Backup ja existe em $BackupDir. Use -BackupDir para forcar novo."
        } else {
            New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
            $itemsToBackup = @(
                'memory/project-preferences.md',
                'memory/learning.jsonl',
                'memory/current-context.md',
                'memory/known-decisions.md',
                'memory/known-errors.md',
                'project-dna/PROJECT-DNA.md'
            )
            foreach ($item in $itemsToBackup) {
                $src = Join-Path $xforgeDir $item
                if (Test-Path -LiteralPath $src) {
                    $dst = Join-Path $BackupDir $item
                    $dstDir = Split-Path -Parent $dst
                    if (-not (Test-Path -LiteralPath $dstDir)) { New-Item -ItemType Directory -Path $dstDir -Force | Out-Null }
                    Copy-Item -LiteralPath $src -Destination $dst -Force
                }
            }
            Write-Phase "2/5" "Backup criado em: $BackupDir"
        }
    }
} else {
    Write-Phase "2/5" "Backup SKIPADO (use -SkipBackup=false para habilitar)"
}

# === STEP 3: Rewrite project-preferences.md ===
Write-Phase "3/5" "Reescrevendo project-preferences.md..."
if (Get-Command -Name 'Rewrite-ProjectPreferences' -ErrorAction SilentlyContinue) {
    $newContent = Rewrite-ProjectPreferences -StackInfo $stackInfo
    $targetFile = Join-Path $xforgeDir 'memory/project-preferences.md'
    if ($WhatIfPreference) {
        Write-Host "  [WhatIf] Reescreveria: $targetFile"
        Write-Host "  [WhatIf] Preview:"
        $newContent -split "`n" | Select-Object -First 10 | ForEach-Object { Write-Host "    $_" }
    } else {
        if (Test-Path -LiteralPath $targetFile) {
            $existing = Get-Content -LiteralPath $targetFile -Raw -Encoding UTF8
            if ($existing -ne $newContent) {
                Set-Content -LiteralPath $targetFile -Value $newContent -Encoding UTF8 -NoNewline
                Write-Host "  Atualizado: $targetFile"
            } else {
                Write-Host "  Ja estava correto: $targetFile"
            }
        } else {
            Set-Content -LiteralPath $targetFile -Value $newContent -Encoding UTF8 -NoNewline
            Write-Host "  Criado: $targetFile"
        }
    }
} else {
    Write-Warning "Rewrite-ProjectPreferences nao disponivel (lib/memory-rewriter.ps1 nao carregada). Pulando."
}

# === STEP 4: Rewrite PROJECT-DNA.md ===
Write-Phase "4/5" "Reescrevendo PROJECT-DNA.md..."
if (-not $DryRunProjectDna) {
    if (Get-Command -Name 'Rewrite-ProjectDna' -ErrorAction SilentlyContinue) {
        $newDna = Rewrite-ProjectDna -StackInfo $stackInfo -ProjectRoot $ProjectRoot
        $dnaFile = Join-Path $xforgeDir 'project-dna/PROJECT-DNA.md'
        if ($WhatIfPreference) {
            Write-Host "  [WhatIf] Reescreveria: $dnaFile"
            Write-Host "  [WhatIf] Preview:"
            $newDna -split "`n" | Select-Object -First 15 | ForEach-Object { Write-Host "    $_" }
        } else {
            $dnaDir = Split-Path -Parent $dnaFile
            if (-not (Test-Path -LiteralPath $dnaDir)) { New-Item -ItemType Directory -Path $dnaDir -Force | Out-Null }
            if (Test-Path -LiteralPath $dnaFile) {
                $existingDna = Get-Content -LiteralPath $dnaFile -Raw -Encoding UTF8
                if ($existingDna -ne $newDna) {
                    Set-Content -LiteralPath $dnaFile -Value $newDna -Encoding UTF8 -NoNewline
                    Write-Host "  Atualizado: $dnaFile"
                } else {
                    Write-Host "  Ja estava correto: $dnaFile"
                }
            } else {
                Set-Content -LiteralPath $dnaFile -Value $newDna -Encoding UTF8 -NoNewline
                Write-Host "  Criado: $dnaFile"
            }
        }
    } else {
        Write-Warning "Rewrite-ProjectDna nao disponivel. Pulando."
    }
} else {
    Write-Host "  DryRun: pulando rewrite de PROJECT-DNA.md"
}

# === STEP 5: Dedupe learning.jsonl ===
Write-Phase "5/5" "Deduplicando learning.jsonl..."
$learningFile = Join-Path $xforgeDir 'memory/learning.jsonl'
if (Test-Path -LiteralPath $learningFile) {
    if ($WhatIfPreference) {
        Write-Host "  [WhatIf] Analisaria: $learningFile"
    } else {
        $lines = Get-Content -LiteralPath $learningFile -Encoding UTF8
        $seen = @{}
        $deduped = @()
        $removed = 0
        $removedTest = 0
        $removedLowConf = 0
        foreach ($line in $lines) {
            if ([string]::IsNullOrWhiteSpace($line)) { continue }
            try {
                $entry = $line | ConvertFrom-Json -ErrorAction Stop
            } catch {
                continue
            }
            if ($entry.statement -eq 'test' -or $entry.statement -eq 'test learning') {
                $removedTest++
                $removed++
                continue
            }
            if ($entry.confidence -and $entry.confidence -lt 0.5) {
                $removedLowConf++
                $removed++
                continue
            }
            $key = "$($entry.kind)|$($entry.statement)"
            if ($seen.ContainsKey($key)) {
                $removed++
                continue
            }
            $seen[$key] = $true
            $deduped += $line
        }
        Set-Content -LiteralPath $learningFile -Value $deduped -Encoding UTF8
        Write-Host "  Entradas originais: $($lines.Count)"
        Write-Host "  Entradas finais: $($deduped.Count)"
        Write-Host "  Removidas: $removed (test=$removedTest, lowConf=$removedLowConf, duplicatas=$(($removed - $removedTest - $removedLowConf)))"
    }
} else {
    Write-Host "  learning.jsonl nao existe em $ProjectRoot"
}

Write-Host ""
Write-Phase "DONE" "Purificacao concluida."
if ($BackupDir -and (Test-Path -LiteralPath $BackupDir)) {
    Write-Host "Backup em: $BackupDir"
    Write-Host "Para reverter: Copy-Item -Recurse -Force '$BackupDir\*' '$xforgeDir\'"
}

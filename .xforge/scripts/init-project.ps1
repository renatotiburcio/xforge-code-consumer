<#
.SYNOPSIS
init-project.ps1 - Cria projeto consumidor completo, separando do template.

.DESCRIPTION
DR-0211. Resolve o problema Template vs Consumer:
- Remove .git remote do template
- Inicializa novo repositorio git no projeto
- Copia apenas paths user-facing do template
- Remove paths template-only
- Purifica memory com stack detectada
- Cria commit inicial
- Atualiza .gitignore para o projeto

Suporta:
- -TargetDir <path>: diretorio destino (obrigatorio)
- -SourceDir <path>: diretorio origem (default: cwd)
- -Stack <name>: stack manual (default: auto-detect)
- -Remote <url>: URL do remote do projeto (opcional)
- -WhatIf: mostra o que seria feito
- -Force: sobrescreve target dir se existir
- -SkipPurify: nao roda purify.ps1
- -SkipGit: nao faz operacoes git

.EXAMPLE
.xforge/scripts/init-project.ps1 -TargetDir ../meu-projeto -Stack dotnet
.xforge/scripts/init-project.ps1 -TargetDir ../meu-projeto -Stack dotnet -Remote https://github.com/user/repo.git
.xforge/scripts/init-project.ps1 -TargetDir ../meu-projeto -WhatIf
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)][string]$TargetDir,
    [string]$SourceDir = (Get-Location).Path,
    [string]$Stack,
    [string]$Remote,
    [switch]$Force,
    [switch]$SkipPurify,
    [switch]$SkipGit
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# === STEP 0: Validacoes ===
Write-Host "[0/8] Validando..." -ForegroundColor Cyan

$SourceDir = (Resolve-Path -LiteralPath $SourceDir).Path
$manifestPath = Join-Path $SourceDir '.xforge/template-only.json'
if (-not (Test-Path -LiteralPath $manifestPath)) {
    throw "Manifesto nao encontrado em $manifestPath. Este script deve ser rodado de dentro do template XForge-Development-New."
}
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json

$gitDir = Join-Path $SourceDir '.git'
if (-not (Test-Path -LiteralPath $gitDir)) {
    throw ".git nao encontrado em $SourceDir. Este script deve ser rodado de dentro do template XForge."
}

# === STEP 1: Backup ===
$timestamp = Get-Date -Format "yyyyMMdd-HHmm"
$backupDir = Join-Path $TargetDir ".xforge-backups/init-project-$timestamp"
if (-not $SkipGit) {
    Write-Host "[1/8] Backup do source em: $backupDir" -ForegroundColor Cyan
    if (-not $WhatIfPreference) {
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        $gitConfig = Join-Path $gitDir "config"
        if (Test-Path -LiteralPath $gitConfig) {
            Copy-Item -LiteralPath $gitConfig -Destination (Join-Path $backupDir "git-config-backup") -Force
        }
    }
}

# === STEP 2: Copia paths user-facing ===
Write-Host "[2/8] Copiando paths user-facing..." -ForegroundColor Cyan
if (Test-Path -LiteralPath $TargetDir) {
    if (-not $Force) {
        $existing = Get-ChildItem -LiteralPath $TargetDir -Force -ErrorAction SilentlyContinue | Measure-Object
        if ($existing.Count -gt 0) {
            throw "TargetDir nao vazio: $TargetDir. Use -Force para sobrescrever."
        }
    }
} else {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}
if (Test-Path -LiteralPath $TargetDir) { $TargetDir = (Resolve-Path -LiteralPath $TargetDir).Path } else { $TargetDir = [System.IO.Path]::GetFullPath($TargetDir) }

$copied = 0
$patterns = $manifest.userFacing.paths
foreach ($pattern in $patterns) {
    $src = Join-Path $SourceDir $pattern
    $dst = Join-Path $TargetDir $pattern
    if (Test-Path -LiteralPath $src -PathType Container) {
        if ($WhatIfPreference) {
            Write-Host "  [WhatIf] Copiaria diretorio: $pattern" -ForegroundColor Cyan
        } else {
            $dstParent = Split-Path -Parent $dst
            if (-not (Test-Path -LiteralPath $dstParent)) { New-Item -ItemType Directory -Path $dstParent -Force | Out-Null }
            Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
            $copied++
        }
    } elseif (Test-Path -LiteralPath $src -PathType Leaf) {
        if ($WhatIfPreference) {
            Write-Host "  [WhatIf] Copiaria arquivo: $pattern" -ForegroundColor Cyan
        } else {
            $dstParent = Split-Path -Parent $dst
            if (-not (Test-Path -LiteralPath $dstParent)) { New-Item -ItemType Directory -Path $dstParent -Force | Out-Null }
            Copy-Item -LiteralPath $src -Destination $dst -Force
            $copied++
        }
    }
}
Write-Host "  Paths copiados: $copied" -ForegroundColor Green

# === STEP 3: Copia manifesto ===
Write-Host "[3/8] Copiando manifesto template-only..." -ForegroundColor Cyan
if (-not $WhatIfPreference) {
    $manifestDst = Join-Path $TargetDir ".xforge/template-only.json"
    $manifestDstDir = Split-Path -Parent $manifestDst
    if (-not (Test-Path -LiteralPath $manifestDstDir)) { New-Item -ItemType Directory -Path $manifestDstDir -Force | Out-Null }
    Copy-Item -LiteralPath $manifestPath -Destination $manifestDst -Force
}

# === STEP 4: Remove paths template-only ===
Write-Host "[4/8] Removendo paths template-only..." -ForegroundColor Cyan
$toRemove = @()
foreach ($pattern in $manifest.templateOnly.paths) {
    $full = Join-Path $TargetDir $pattern
    if (Test-Path -LiteralPath $full) {
        $toRemove += @{ Pattern = $pattern; FullPath = $full }
    }
}
if ($toRemove.Count -gt 0) {
    foreach ($item in $toRemove) {
        if ($WhatIfPreference) {
            Write-Host "  [WhatIf] Removeria: $($item.Pattern)" -ForegroundColor Yellow
        } else {
            if (Test-Path -LiteralPath $item.FullPath -PathType Container) {
                Remove-Item -LiteralPath $item.FullPath -Recurse -Force
            } else {
                Remove-Item -LiteralPath $item.FullPath -Force
            }
            Write-Host "  Removido: $($item.Pattern)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "  Nenhum template-only path encontrado (ja limpo)." -ForegroundColor Green
}

# === STEP 5: Detecta stack ===
Write-Host "[5/8] Detectando stack..." -ForegroundColor Cyan
if (-not $Stack) {
    $libPath = Join-Path $SourceDir ".xforge/scripts/lib/stack-detector.ps1"
    if (Test-Path -LiteralPath $libPath) {
        . $libPath
        $stackInfo = Get-ProjectStack -ProjectRoot $TargetDir -AllowAmbiguous
        $Stack = $stackInfo.stack
        Write-Host "  Stack detectado: $Stack (confidence: $($stackInfo.confidence))" -ForegroundColor Green
    } else {
        Write-Warning "stack-detector.ps1 nao encontrado. Usando stack=unknown"
        $Stack = "unknown"
    }
} else {
    Write-Host "  Stack informado: $Stack" -ForegroundColor Green
}

# === STEP 6: Purifica memory ===
if (-not $SkipPurify) {
    Write-Host "[6/8] Purificando memory..." -ForegroundColor Cyan
    if ($WhatIfPreference) {
        Write-Host "  [WhatIf] Rodaria purify.ps1 -ProjectRoot $TargetDir -Force" -ForegroundColor Cyan
    } else {
        $purifyScript = Join-Path $SourceDir ".xforge/scripts/purify.ps1"
        if (Test-Path -LiteralPath $purifyScript) {
            & $purifyScript -ProjectRoot $TargetDir -Force
        } else {
            Write-Warning "purify.ps1 nao encontrado. Pulando purify."
        }
    }
} else {
    Write-Host "[6/8] Purify SKIPADO (-SkipPurify)" -ForegroundColor Yellow
}

# === STEP 7: Git init + commit ===
if (-not $SkipGit) {
    Write-Host "[7/8] Inicializando git..." -ForegroundColor Cyan
    
    $targetGit = Join-Path $TargetDir ".git"
    if (Test-Path -LiteralPath $targetGit) {
        if ($WhatIfPreference) {
            Write-Host "  [WhatIf] Removeria .git do target" -ForegroundColor Cyan
        } else {
            Remove-Item -LiteralPath $targetGit -Recurse -Force
            Write-Host "  .git do template removido" -ForegroundColor Yellow
        }
    }
    
    if ($WhatIfPreference) {
        Write-Host "  [WhatIf] Executaria: git init" -ForegroundColor Cyan
        Write-Host "  [WhatIf] Executaria: git add ." -ForegroundColor Cyan
        Write-Host "  [WhatIf] Executaria: git commit" -ForegroundColor Cyan
    } else {
        Push-Location $TargetDir
        try {
            git init
            Write-Host "  git init criado" -ForegroundColor Green
            
            git add .
            Write-Host "  git add . concluido" -ForegroundColor Green
            
            git commit -m "Initial commit from XForge template (DR-0211)"
            Write-Host "  Commit inicial criado" -ForegroundColor Green
            
            if ($Remote) {
                git remote add origin $Remote
                Write-Host "  Remote adicionado: $Remote" -ForegroundColor Green
            }
        } finally {
            Pop-Location
        }
    }
} else {
    Write-Host "[7/8] Git SKIPADO (-SkipGit)" -ForegroundColor Yellow
    Write-Host "  Para inicializar manualmente:" -ForegroundColor Cyan
    Write-Host "    cd $TargetDir" -ForegroundColor Cyan
    Write-Host "    git init" -ForegroundColor Cyan
    Write-Host "    git add ." -ForegroundColor Cyan
    Write-Host "    git commit -m 'Initial commit'" -ForegroundColor Cyan
    Write-Host "    git remote add origin <seu-repo>" -ForegroundColor Cyan
}

# === STEP 8: .gitignore para o projeto ===
Write-Host "[8/8] Atualizando .gitignore..." -ForegroundColor Cyan
$gitignorePath = Join-Path $TargetDir ".gitignore"
if (Test-Path -LiteralPath $gitignorePath) {
    if ($WhatIfPreference) {
        Write-Host "  [WhatIf] Atualizaria .gitignore do projeto" -ForegroundColor Cyan
    } else {
        $gitignoreContent = Get-Content -LiteralPath $gitignorePath -Raw -Encoding UTF8
        $lines = $gitignoreContent -split "`n"
        $filtered = @()
        foreach ($line in $lines) {
            $trimmed = $line.Trim()
            if ($trimmed -eq "CHANGELOG.md" -or 
                $trimmed -eq "STATUS.md" -or 
                $trimmed -eq "ARCHITECTURE.md" -or
                $trimmed -eq "CLAUDE.md" -or
                $trimmed -match "^\.xforge/decisions/" -or
                $trimmed -match "^docs/decisions/" -or
                $trimmed -match "^docs/manual/") {
                continue
            }
            $filtered += $line
        }
        
        $header = @(
            "# =============================================================================="
            "# .gitignore - Projeto consumidor do template XForge"
            "# Gerado por init-project.ps1 (DR-0211 - Template vs Consumer)"
            "# Data: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
            "# Stack: $Stack"
            "# =============================================================================="
            ""
        )
        
        $newContent = ($header + $filtered) -join "`n"
        Set-Content -LiteralPath $gitignorePath -Value $newContent -Encoding UTF8 -NoNewline
        
        Write-Host "  .gitignore atualizado" -ForegroundColor Green
    }
}

# === RESUMO ===
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  INIT PROJECT CONCLUIDO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Target: $TargetDir" -ForegroundColor White
Write-Host "  Stack: $Stack" -ForegroundColor White
Write-Host "  Paths copiados: $copied" -ForegroundColor White
Write-Host "  Template-only removidos: $($toRemove.Count)" -ForegroundColor White
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "  cd $TargetDir" -ForegroundColor Cyan
if ($Remote) {
    Write-Host "  # Remote ja configurado: $Remote" -ForegroundColor Green
} else {
    Write-Host "  git remote add origin <seu-repo-url>" -ForegroundColor Cyan
}
Write-Host "  git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para voltar ao template:" -ForegroundColor DarkGray
Write-Host "  cd $SourceDir" -ForegroundColor DarkGray


<#
.SYNOPSIS
add-applicability-scope.ps1 - Adiciona campo applicabilityScope em cada entry do INDEX.json.

.DESCRIPTION
DR-0180 Fase 1. Processa .xforge/knowledge/INDEX.json e adiciona campo
`applicabilityScope` em cada entry baseado em heuristica do path:
- path contem 'dotnet', 'blazor', 'ef-core', 'automapper', 'xforge-mediatr', 'csharp', 'aspnet' -> ["dotnet"]
- path contem 'python', 'fastapi', 'django', 'pydantic', 'pytest' -> ["python"]
- path contem 'react', 'next', 'remix' -> ["react"]
- path contem 'angular' -> ["angular"]
- path contem 'vue', 'nuxt' -> ["vue"]
- path contem 'svelte' -> ["svelte"]
- path contem 'go', 'gin', 'fiber' -> ["go"]
- path contem 'rust', 'tauri' -> ["rust"]
- path contem 'java', 'spring', 'kotlin' -> ["java"]
- path contem 'fiscal', 'nfe', 'nfce', 'nfse', 'icms', 'pis', 'cofins', 'sped' -> ["fiscal"]
- path contem 'contabil', 'ecd', 'ecf', 'plano-contas' -> ["contabil"]
- path contem 'trabalhista', 'esocial', 'clt', 'folha', 'fgts' -> ["trabalhista"]
- path contem 'rh', 'beneficios' -> ["rh"]
- path contem 'lgpd', 'gdpr', 'privacy', 'compliance' (isolado) -> ["lgpd"]
- default -> ["*"]

Heuristicas NAO sao mutualmente exclusivas (entry pode ter ["dotnet","python"]).

Suporta:
- -WhatIf: mostra diff proposto sem gravar
- -Backup: cria backup antes de gravar
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$IndexPath = (Join-Path (Get-Location) '.xforge/knowledge/INDEX.json'),
    [switch]$Backup
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $IndexPath)) {
    throw "INDEX.json nao encontrado: $IndexPath"
}

Write-Host "Lendo $IndexPath..."
$json = Get-Content -LiteralPath $IndexPath -Raw -Encoding UTF8
$index = $json | ConvertFrom-Json
$heuristics = @{
    'dotnet'      = @('dotnet', 'blazor', 'ef-core', 'automapper', 'xforge-mediatr', 'csharp', 'aspnet', 'maui', 'wpf', 'winforms', 'minimal-apis', 'signalr', 'grpc-dotnet')
    'python'      = @('python', 'fastapi', 'django', 'flask', 'pydantic', 'pytest', 'ruff', 'sqlalchemy')
    'react'       = @('react', 'next-', 'remix', 'tanstack', 'vite-react')
    'angular'     = @('angular')
    'vue'         = @('vue', 'nuxt', 'pinia')
    'svelte'      = @('svelte')
    'go'          = @('golang', 'gin', 'fiber', 'echo', 'chi', 'sqlc')
    'rust'        = @('rust', 'tauri', 'axum', 'actix')
    'java'        = @('java', 'spring', 'kotlin', 'quarkus', 'micronaut', 'jvm')
    'fiscal'      = @('fiscal', 'nfe', 'nfce', 'nfse', 'icms', 'ipi', 'pis', 'cofins', 'irpj', 'csll', 'sped', 'sefaz', 'rejeicao')
    'contabil'    = @('contabil', 'contabeis', 'ecd', 'ecf', 'plano-de-contas', 'centro-de-custo', 'avaliacao-estoque', 'escrituracao', 'lancamentos', 'demonstracoes', 'lcpr', 'normas-contabeis')
    'trabalhista' = @('trabalhista', 'esocial', 'clt', 'folha-pagamento', 'calculos-folha', 'afastamentos', 'beneficios', 'inss', 'fgts', 'ferias', 'decimo', 'rescisao')
    'rh'          = @('rh', 'recursos-humanos')
    'lgpd'        = @('lgpd', 'gdpr', 'privacy', 'consent-management', 'data-classification', 'data-protection', 'breach-notification', 'direitos-titular', 'dpia', 'ripd')
}

$updated = 0
$skipped = 0
foreach ($entry in $index.entries) {
    $hasScope = $entry.PSObject.Properties.Name -contains 'applicabilityScope'
    if ($hasScope -and $null -ne $entry.applicabilityScope) {
        $skipped++
        continue
    }
    $pathLower = $entry.path.ToString().ToLower()
    $tags = if ($entry.tags) { @($entry.tags | ForEach-Object { $_.ToString().ToLower() }) } else { @() }
    $haystack = "$pathLower $($tags -join ' ')"

    $scopes = New-Object System.Collections.Generic.List[string]
    foreach ($key in $heuristics.Keys) {
        foreach ($pattern in $heuristics[$key]) {
            if ($haystack -match [regex]::Escape($pattern)) {
                $scopes.Add($key)
                break
            }
        }
    }
    if ($scopes.Count -eq 0) {
        $entry | Add-Member -NotePropertyName 'applicabilityScope' -NotePropertyValue @('*') -Force
    } else {
        $entry | Add-Member -NotePropertyName 'applicabilityScope' -NotePropertyValue @($scopes) -Force
    }
    $updated++
}

if ($Backup) {
    $backupPath = "$IndexPath.bak-$(Get-Date -Format 'yyyyMMdd-HHmm')"
    Copy-Item -LiteralPath $IndexPath -Destination $backupPath -Force
    Write-Host "Backup criado: $backupPath"
}

if ($WhatIfPreference) {
    Write-Host "[WhatIf] Atualizaria $updated entries (skipadas: $skipped ja tinham applicabilityScope)" -ForegroundColor Cyan
    Write-Host "Sample (primeiras 5):" -ForegroundColor Cyan
    $index.entries | Select-Object -First 5 | ForEach-Object {
        Write-Host "  $($_.id): $($_.applicabilityScope -join ', ')"
    }
} else {
    # Salva preservando formatacao
    $newJson = $index | ConvertTo-Json -Depth 10
    Set-Content -LiteralPath $IndexPath -Value $newJson -Encoding UTF8
    Write-Host "[DONE] $updated entries atualizadas com applicabilityScope ($skipped ja tinham)" -ForegroundColor Green
}

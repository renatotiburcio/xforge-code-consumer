# stack-detector.ps1 - Stack detection library
# DR-0180 Fase 1. Detecta stack do projeto ativo via sinais (package.json, *.csproj, etc).
# Nao assume .NET por padrao. Stack-agnostic por design (Regra 0).
# Retorna hashtable com stack, signals, confidence.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-ManifestPath {
    <#
    .SYNOPSIS
    Retorna o caminho do manifesto template-only.json a partir de um ProjectRoot.
    .PARAMETER ProjectRoot
    Diretorio raiz do projeto alvo.
    #>
    param([Parameter(Mandatory = $true)][string]$ProjectRoot)
    return (Join-Path $ProjectRoot '.xforge/template-only.json')
}

function Read-Manifest {
    <#
    .SYNOPSIS
    Le o manifesto template-only.json. Retorna $null se nao existir.
    #>
    param([Parameter(Mandatory = $true)][string]$ProjectRoot)
    $manifestPath = Get-ManifestPath -ProjectRoot $ProjectRoot
    if (-not (Test-Path -LiteralPath $manifestPath)) { return $null }
    try {
        $json = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8
        return ($json | ConvertFrom-Json)
    } catch {
        Write-Warning "Manifesto invalido em $manifestPath : $_"
        return $null
    }
}

function Get-SkipDirectories {
    <#
    .SYNOPSIS
    Retorna lista de diretorios a serem ignorados na deteccao (node_modules, bin, obj, etc).
    #>
    param([Parameter(Mandatory = $false)][string]$ProjectRoot)
    $default = @('node_modules', 'bin', 'obj', 'dist', 'build', '.next', '.venv', 'venv', '__pycache__', '.git', 'target', 'vendor', '.pytest_cache')
    if ($ProjectRoot) {
        $manifest = Read-Manifest -ProjectRoot $ProjectRoot
        if ($manifest -and ($manifest.PSObject.Properties.Name -contains 'stacks') -and $manifest.stacks -and ($manifest.stacks.PSObject.Properties.Name -contains 'skipDirectories')) {
            return @($manifest.stacks.skipDirectories)
        }
    }
    return $default
}

function Test-SignalExists {
    <#
    .SYNOPSIS
    Verifica se um sinal (arquivo ou pattern) existe dentro do ProjectRoot, ignorando diretorios de skip.
    .PARAMETER ProjectRoot
    Diretorio raiz.
    .PARAMETER Pattern
    Pattern glob (ex: '*.csproj', 'package.json', 'pyproject.toml').
    .PARAMETER SkipDirs
    Diretorios a ignorar.
    #>
    param(
        [Parameter(Mandatory = $true)][string]$ProjectRoot,
        [Parameter(Mandatory = $true)][string]$Pattern,
        [Parameter(Mandatory = $false)][string[]]$SkipDirs
    )
    if (-not (Test-Path -LiteralPath $ProjectRoot)) { return $false }
    if (-not $SkipDirs) { $SkipDirs = Get-SkipDirectories }
    try {
        $found = Get-ChildItem -LiteralPath $ProjectRoot -Filter $Pattern -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object { $_.DirectoryName -notmatch ($SkipDirs -join '|') } |
            Select-Object -First 1
        return ($null -ne $found)
    } catch {
        return $false
    }
}

function Get-DetectionRules {
    <#
    .SYNOPSIS
    Retorna lista de regras de deteccao (signal, stack, weight) ordenadas por precisao.
    .PARAMETER ProjectRoot
    Diretorio raiz (para carregar manifest customizado se existir).
    #>
    param([Parameter(Mandatory = $false)][string]$ProjectRoot)
    $rules = @(
        @{ signal = '*.csproj';     stack = 'dotnet';  weight = 100; precise = $true }
        @{ signal = '*.sln';        stack = 'dotnet';  weight = 90;  precise = $true }
        @{ signal = '*.slnx';       stack = 'dotnet';  weight = 90;  precise = $true }
        @{ signal = 'package.json'; stack = 'node';    weight = 80;  precise = $false }
        @{ signal = 'angular.json'; stack = 'angular'; weight = 100; precise = $true }
        @{ signal = 'next.config.js'; stack = 'next';  weight = 100; precise = $true }
        @{ signal = 'next.config.ts'; stack = 'next';  weight = 100; precise = $true }
        @{ signal = 'nuxt.config.ts'; stack = 'nuxt';  weight = 100; precise = $true }
        @{ signal = 'nuxt.config.js'; stack = 'nuxt';  weight = 100; precise = $true }
        @{ signal = 'svelte.config.js'; stack = 'svelte'; weight = 100; precise = $true }
        @{ signal = 'pyproject.toml'; stack = 'python'; weight = 100; precise = $true }
        @{ signal = 'requirements.txt'; stack = 'python'; weight = 90; precise = $true }
        @{ signal = 'setup.py';     stack = 'python';  weight = 70;  precise = $true }
        @{ signal = 'go.mod';       stack = 'go';      weight = 100; precise = $true }
        @{ signal = 'Cargo.toml';   stack = 'rust';    weight = 100; precise = $true }
        @{ signal = 'pom.xml';      stack = 'java';    weight = 100; precise = $true }
        @{ signal = 'build.gradle'; stack = 'java';    weight = 100; precise = $true }
        @{ signal = 'Gemfile';      stack = 'ruby';    weight = 100; precise = $true }
        @{ signal = 'composer.json'; stack = 'php';    weight = 100; precise = $true }
        @{ signal = 'mix.exs';      stack = 'elixir';  weight = 100; precise = $true }
        @{ signal = 'index.html';   stack = 'html';    weight = 60;  precise = $false }
    )
    return $rules
}

function Get-ProjectStack {
    <#
    .SYNOPSIS
    Detecta o stack do projeto via sinais. Retorna hashtable: stack, signals[], confidence (0-1), ambiguous (bool).
    .DESCRIPTION
    Algoritmo:
    1. Para cada regra ordenada por weight DESC, verifica se signal existe
    2. Soma pesos por stack
    3. Stack vencedor = maior soma
    4. Confidence = soma_vencedor / soma_total
    5. Se 2+ stacks empatados com weight >= 100, marca ambiguous = $true
    #>
    param(
        [Parameter(Mandatory = $true)][string]$ProjectRoot,
        [Parameter(Mandatory = $false)][switch]$AllowAmbiguous
    )
    if (-not (Test-Path -LiteralPath $ProjectRoot)) {
        throw "ProjectRoot nao existe: $ProjectRoot"
    }
    $rules = Get-DetectionRules -ProjectRoot $ProjectRoot
    $skipDirs = Get-SkipDirectories -ProjectRoot $ProjectRoot
    $stackScores = @{}
    $signalsFound = @()

    foreach ($rule in $rules) {
        $exists = Test-SignalExists -ProjectRoot $ProjectRoot -Pattern $rule.signal -SkipDirs $skipDirs
        if ($exists) {
            $signalsFound += $rule.signal
            if (-not $stackScores.ContainsKey($rule.stack)) {
                $stackScores[$rule.stack] = 0
            }
            $stackScores[$rule.stack] += $rule.weight
        }
    }

    if ($signalsFound.Count -eq 0) {
        return @{
            stack = 'unknown'
            signals = @()
            confidence = 0.0
            ambiguous = $false
            scores = @{}
        }
    }

    $sortedStacks = $stackScores.GetEnumerator() | Sort-Object -Property Value -Descending
    $topStack = $sortedStacks[0].Key
    $topScore = $sortedStacks[0].Value
    $totalScore = ($stackScores.Values | Measure-Object -Sum).Sum
    $confidence = [math]::Round($topScore / $totalScore, 2)

    $ambiguous = $false
    if ($sortedStacks.Count -gt 1) {
        $secondScore = $sortedStacks[1].Value
        if ($secondScore -ge 80 -and ($topScore - $secondScore) -le 10) {
            $ambiguous = $true
        }
    }

    $result = @{
        stack = $topStack
        signals = $signalsFound
        confidence = $confidence
        ambiguous = $ambiguous
        scores = $stackScores
    }

    if ($ambiguous -and -not $AllowAmbiguous) {
        Write-Warning "Stack ambiguo detectado em $ProjectRoot. Candidatos: $($sortedStacks[0..1] | ForEach-Object { "$($_.Key)=$($_.Value)" } | Join-String -Separator ', '). Use -AllowAmbiguous para forcar."
    }

    return $result
}

function Format-StackReport {
    <#
    .SYNOPSIS
    Formata o resultado de Get-ProjectStack para exibicao humana.
    #>
    param([Parameter(Mandatory = $true)]$Result)
    $lines = @()
    $lines += "Stack: $($Result.stack)"
    $lines += "Confidence: $($Result.confidence)"
    $lines += "Ambiguous: $($Result.ambiguous)"
    $lines += "Signals: $($Result.signals -join ', ')"
    $lines += "Scores:"
    foreach ($k in ($Result.scores.Keys | Sort-Object)) {
        $lines += "  $k = $($Result.scores[$k])"
    }
    return ($lines -join "`n")
}

function Get-MultiStack {
    <#
    .SYNOPSIS
    Detecta multiplos stacks em um workspace (ex: .NET backend + React frontend).
    DR-0181: Heuristica aprimorada para multi-stack workspace.

    Algoritmo:
    1. Detecta stacks usando Get-ProjectStack
    2. Se confidence < 0.7 ou ambiguous, busca stacks em subdiretorios
    3. Retorna lista de stacks detectados com seus niveis (primary, secondary)
    #>
    param(
        [Parameter(Mandatory = $true)][string]$ProjectRoot,
        [Parameter(Mandatory = $false)][switch]$AllowAmbiguous
    )

    # First pass: root detection
    $rootResult = Get-ProjectStack -ProjectRoot $ProjectRoot -AllowAmbiguous:$AllowAmbiguous

    # If high confidence and not ambiguous, single stack
    if ($rootResult.confidence -ge 0.7 -and -not $rootResult.ambiguous) {
        return @{
            stacks = @(
                @{ stack = $rootResult.stack; level = "primary"; confidence = $rootResult.confidence; path = $ProjectRoot }
            )
            multiStack = $false
            rootDetection = $rootResult
        }
    }

    # Second pass: search in common subdirectories
    $subDirs = @('frontend', 'backend', 'api', 'app', 'web', 'mobile', 'server', 'client')
    $detectedStacks = @()

    foreach ($subDir in $subDirs) {
        $subPath = Join-Path $ProjectRoot $subDir
        if (Test-Path $subPath -PathType Container) {
            $subResult = Get-ProjectStack -ProjectRoot $subPath -AllowAmbiguous:$AllowAmbiguous
            if ($subResult.confidence -ge 0.5 -and $subResult.stack -ne 'unknown') {
                $detectedStacks += @{
                    stack = $subResult.stack
                    level = if ($detectedStacks.Count -eq 0) { "primary" } else { "secondary" }
                    confidence = $subResult.confidence
                    path = $subPath
                }
            }
        }
    }

    # If we found stacks in subdirs, use them
    if ($detectedStacks.Count -gt 0) {
        return @{
            stacks = $detectedStacks
            multiStack = $detectedStacks.Count -gt 1
            rootDetection = $rootResult
        }
    }

    # Fallback: root result even with low confidence
    return @{
        stacks = @(
            @{ stack = $rootResult.stack; level = "primary"; confidence = $rootResult.confidence; path = $ProjectRoot }
        )
        multiStack = $false
        rootDetection = $rootResult
    }
}

if ($MyInvocation.MyCommand.ScriptBlock.Module) {
    Export-ModuleMember -Function @(
        'Get-ManifestPath',
        'Read-Manifest',
        'Get-SkipDirectories',
        'Test-SignalExists',
        'Get-DetectionRules',
        'Get-ProjectStack',
        'Get-MultiStack',
        'Format-StackReport'
    )
}
# Em dot-source (sem .psm1), funcoes ficam disponiveis no escopo do chamador.

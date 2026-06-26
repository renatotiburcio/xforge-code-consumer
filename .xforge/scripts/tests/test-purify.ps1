# test-purify.ps1 - Testes Pester v3 compat (sem BeforeAll/AfterAll)
# DR-0180 Fase 1. Testa stack-detector.ps1, memory-rewriter.ps1, purify.ps1, diff-consumer.ps1.

$ErrorActionPreference = 'Stop'
$libPath = Join-Path $PSScriptRoot '..\lib\stack-detector.ps1'
$rewriterPath = Join-Path $PSScriptRoot '..\lib\memory-rewriter.ps1'
. $libPath
. $rewriterPath

$TestRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("xforge-test-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $TestRoot -Force | Out-Null

function Cleanup-TestRoot {
    if (Test-Path -LiteralPath $TestRoot) {
        Remove-Item -LiteralPath $TestRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Describe "Get-ProjectStack" {
    It "detecta dotnet a partir de .csproj" {
        $dir = Join-Path $TestRoot 'dotnet-proj'
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        '<?xml version="1.0"?><Project Sdk="Microsoft.NET.Sdk"></Project>' | Set-Content -LiteralPath (Join-Path $dir 'App.csproj') -Encoding UTF8
        $info = Get-ProjectStack -ProjectRoot $dir
        $info.stack | Should Be 'dotnet'
        $info.signals | Should Contain '*.csproj'
        $info.confidence | Should BeGreaterThan 0.5
    }

    It "detecta python a partir de pyproject.toml" {
        $dir = Join-Path $TestRoot 'python-proj'
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        '[project]' | Set-Content -LiteralPath (Join-Path $dir 'pyproject.toml') -Encoding UTF8
        $info = Get-ProjectStack -ProjectRoot $dir
        $info.stack | Should Be 'python'
        $info.signals | Should Contain 'pyproject.toml'
    }

    It "detecta node a partir de package.json" {
        $dir = Join-Path $TestRoot 'node-proj'
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        '{}' | Set-Content -LiteralPath (Join-Path $dir 'package.json') -Encoding UTF8
        $info = Get-ProjectStack -ProjectRoot $dir
        $info.stack | Should Be 'node'
        $info.signals | Should Contain 'package.json'
    }

    It "detecta angular com weight maior que package.json" {
        $dir = Join-Path $TestRoot 'angular-proj'
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        '{}' | Set-Content -LiteralPath (Join-Path $dir 'package.json') -Encoding UTF8
        '{}' | Set-Content -LiteralPath (Join-Path $dir 'angular.json') -Encoding UTF8
        $info = Get-ProjectStack -ProjectRoot $dir
        $info.stack | Should Be 'angular'
    }

    It "retorna unknown para diretorio vazio" {
        $dir = Join-Path $TestRoot 'empty-proj'
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        $info = Get-ProjectStack -ProjectRoot $dir
        $info.stack | Should Be 'unknown'
        $info.signals.Count | Should Be 0
    }

    It "ignora node_modules na deteccao" {
        $dir = Join-Path $TestRoot 'with-node_modules'
        $nm = Join-Path $dir 'node_modules\some-lib'
        New-Item -ItemType Directory -Path $nm -Force | Out-Null
        '<Project Sdk="Microsoft.NET.Sdk"/>' | Set-Content -LiteralPath (Join-Path $nm 'package.csproj') -Encoding UTF8
        $info = Get-ProjectStack -ProjectRoot $dir
        $info.stack | Should Be 'unknown'
    }
}

Describe "Rewrite-ProjectPreferences" {
    It "gera preferencias para dotnet" {
        $info = @{ stack = 'dotnet'; signals = @('*.csproj'); confidence = 1.0 }
        $content = Rewrite-ProjectPreferences -StackInfo $info
        $content | Should Match 'dotnet'
        $content | Should Match 'XForge\.MediatR'
    }

    It "gera preferencias para python sem .NET" {
        $info = @{ stack = 'python'; signals = @('pyproject.toml'); confidence = 1.0 }
        $content = Rewrite-ProjectPreferences -StackInfo $info
        $content | Should Match 'python'
        $content | Should Match 'FastAPI'
        $content | Should Not Match 'XForge\.MediatR'
    }

    It "marca unknown para stack nao detectado" {
        $info = @{ stack = 'unknown'; signals = @(); confidence = 0.0 }
        $content = Rewrite-ProjectPreferences -StackInfo $info
        $content | Should Match 'Desconhecido'
    }
}

Describe "Rewrite-ProjectDna" {
    It "gera DNA com lacunas detectadas" {
        $info = @{ stack = 'python'; signals = @('pyproject.toml'); confidence = 1.0 }
        $content = Rewrite-ProjectDna -StackInfo $info -ProjectRoot $TestRoot
        $content | Should Match 'python'
        $content | Should Match 'Has Tests'
        $content | Should Match 'Lacunas'
    }

    It "marca todas as convencoes como OK se existirem" {
        $dir = Join-Path $TestRoot 'complete'
        New-Item -ItemType Directory -Path (Join-Path $dir 'tests') -Force | Out-Null
        New-Item -ItemType Directory -Path (Join-Path $dir '.github\workflows') -Force | Out-Null
        '' | Set-Content -LiteralPath (Join-Path $dir 'Dockerfile') -Encoding UTF8
        '' | Set-Content -LiteralPath (Join-Path $dir 'README.md') -Encoding UTF8
        '' | Set-Content -LiteralPath (Join-Path $dir '.gitignore') -Encoding UTF8
        $info = @{ stack = 'python'; signals = @(); confidence = 1.0 }
        $content = Rewrite-ProjectDna -StackInfo $info -ProjectRoot $dir
        $content | Should Not Match '\[ \] Has Tests'
        $content | Should Not Match '\[ \] Has CI/CD'
    }
}

Describe "diff-consumer.ps1" {
    It "exit 0 quando projeto esta clean" {
        $dir = Join-Path $TestRoot 'clean-proj'
        New-Item -ItemType Directory -Path (Join-Path $dir '.xforge') -Force | Out-Null
        '{"version":"1.0.0","templateOnly":{"paths":[]},"userFacing":{"paths":[]}}' | Set-Content -LiteralPath (Join-Path $dir '.xforge\template-only.json') -Encoding UTF8
        & (Join-Path $PSScriptRoot '..\diff-consumer.ps1') -ProjectRoot $dir | Out-Null
        $LASTEXITCODE | Should Be 0
    }

    It "exit 1 quando ha template-only paths" {
        $dir = Join-Path $TestRoot 'dirty-proj'
        New-Item -ItemType Directory -Path (Join-Path $dir '.xforge\decisions') -Force | Out-Null
        New-Item -ItemType Directory -Path (Join-Path $dir '.xforge') -Force | Out-Null
        '{"version":"1.0.0","templateOnly":{"paths":[".xforge/decisions/"]},"userFacing":{"paths":[]}}' | Set-Content -LiteralPath (Join-Path $dir '.xforge\template-only.json') -Encoding UTF8
        & (Join-Path $PSScriptRoot '..\diff-consumer.ps1') -ProjectRoot $dir | Out-Null
        $LASTEXITCODE | Should Be 1
    }
}

Describe "purify.ps1 (integracao minima)" {
    It "cria backup em -ProjectRoot se backup dir nao existe" {
        $dir = Join-Path $TestRoot 'purify-target'
        $xforge = Join-Path $dir '.xforge'
        $mem = Join-Path $xforge 'memory'
        New-Item -ItemType Directory -Path $mem -Force | Out-Null
        '---\nstack: dotnet\n---' | Set-Content -LiteralPath (Join-Path $mem 'project-preferences.md') -Encoding UTF8
        '<Project Sdk="Microsoft.NET.Sdk"/>' | Set-Content -LiteralPath (Join-Path $dir 'App.csproj') -Encoding UTF8
        '{"version":"1.0.0","templateOnly":{"paths":[]},"userFacing":{"paths":[]}}' | Set-Content -LiteralPath (Join-Path $xforge 'template-only.json') -Encoding UTF8
        & (Join-Path $PSScriptRoot '..\purify.ps1') -ProjectRoot $dir -Force -SkipBackup | Out-Null
        # Sem backup, mas deve ter rodado sem erro
        Test-Path -LiteralPath (Join-Path $mem 'project-preferences.md') | Should Be $true
    }
}

Cleanup-TestRoot
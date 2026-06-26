# memory-rewriter.ps1 - Memory/DNA rewrite library
# DR-0180 Fase 1. Gera novo conteudo para project-preferences.md e PROJECT-DNA.md
# baseado no stack detectado. Aplica stack-agnostic (Regra 0).

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Rewrite-ProjectPreferences {
    <#
    .SYNOPSIS
    Gera novo conteudo para project-preferences.md com stack correto.
    .PARAMETER StackInfo
    Hashtable retornado por Get-ProjectStack.
    .PARAMETER Template
    Opcional: caminho para template customizado. Default: embutido.
    #>
    param(
        [Parameter(Mandatory = $true)]$StackInfo,
        [string]$Template
    )
    $stack = $StackInfo.stack
    $signals = $StackInfo.signals -join ', '
    $today = Get-Date -Format 'yyyy-MM-dd'

    $stackDescription = switch ($stack) {
        'dotnet'  { '.NET (C# / F# / VB) - opt-in para XForge.MediatR, AutoMapper, EF Core' }
        'node'    { 'Node.js (Express, Fastify, NestJS, Hono, Prisma, Drizzle)' }
        'python'  { 'Python (FastAPI, Django, Flask, Pydantic, pytest, ruff)' }
        'angular' { 'Angular (CLI, standalone components, signals)' }
        'next'    { 'Next.js (App Router, Server Components, Server Actions)' }
        'nuxt'    { 'Nuxt 3 (SSR/SSG)' }
        'svelte'  { 'Svelte/SvelteKit' }
        'go'      { 'Go (Gin, Echo, Fiber, sqlc, testify)' }
        'rust'    { 'Rust (Axum, Actix, sqlx, tokio)' }
        'java'    { 'Java/Kotlin (Spring Boot, Quarkus, Micronaut)' }
        'ruby'    { 'Ruby (Rails)' }
        'php'     { 'PHP (Laravel, Symfony)' }
        'elixir'  { 'Elixir (Phoenix)' }
        'html'    { 'HTML estatico (Tailwind via CDN ou build)' }
        default   { 'Desconhecido - requer revisao manual' }
    }

    $content = @"
---
id: project-preferences
type: memoria
tags: [memoria, preferencias, config, padroes]
trust: high
updated: $today
generated-by: purify.ps1 (DR-0180)
---

# Preferencias do Projeto

## Stack Detectado
- **Stack primario**: $stack
- **Confidence**: $($StackInfo.confidence)
- **Signals**: $signals
- **Descricao**: $stackDescription

> Este arquivo foi gerado/atualizado por `purify.ps1` (DR-0180 Fase 1).
> O stack NAO e .NET por default. Cada projeto tem seu proprio stack.
> Para mais detalhes sobre stack detection, ver: .kilo/skills/stack-aware-context/SKILL.md

## Idioma
- Interface de comandos: Portugues
- Documentacao tecnica: Portugues
- Codigo: Ingles (padrao)

## Stack (Multi-stack, sem default) - Adicionado 2026-06-14
- **SEM default de stack**: o sistema NAO deve assumir .NET, C#, Blazor, EF Core, MediatR, AutoMapper por padrao.
- Stack eh detectado por sinais do projeto: package.json, *.csproj, requirements.txt, go.mod, angular.json, next.config.js, pyproject.toml, Cargo.toml, mix.exs, pom.xml, build.gradle, Gemfile, composer.json, *.html, *.tsx, *.vue, etc.
- Diretores especialistas por stack sao OPT-IN.
- Diretorios especialistas por stack sao OPT-IN (Regra 0). Aplicam-se apenas ao stack detectado.
- Comandos genericos (create-project, create-api, analyze-project) DEVEM perguntar ou detectar stack antes de sugerir patterns.

## Estilo de Codigo
- Agentes: YAML frontmatter (name, description, mode, permission, color)
- Skills: SKILL.md com YAML frontmatter
- Comandos: Markdown com frontmatter (description, agent)
- Scripts: PowerShell (.ps1) para automacao, Python para RAG

## Encoding
- Todos os arquivos: UTF-8 sem BOM
- Scripts PS1: WriteAllText(Encoding.UTF8)
- Leitura: StreamReader(UTF8)
- Detecao mojibake: [regex]::IsMatch() (nao usar -match)

## Fluxo de Trabalho
- Validar com doctor.ps1 antes de commit
- Usar /provider para trocar modelo
- Usar /buscar para pesquisa combinada
- Usar /memoria para gerenciar contexto
- Em QUALQUER projeto novo, PRIMEIRO detectar o stack antes de sugerir patterns
- Em projetos multi-stack, validar cada subprojeto independentemente

## Organizacao
- .kilo/ = operacional (pode ser substituido)
- .xforge/ = persistente (nunca deletar, mas pode ser purificado via purify.ps1)
- scripts/ = utilitarios
- tests/ = testes unitarios
"@

    return $content
}

function Rewrite-ProjectDna {
    <#
    .SYNOPSIS
    Gera novo conteudo para PROJECT-DNA.md com stack correto e lacunas detectadas.
    .PARAMETER StackInfo
    Hashtable retornado por Get-ProjectStack.
    .PARAMETER ProjectRoot
    Diretorio raiz do projeto (para detectar lacunas como has-tests, has-ci, has-docker).
    #>
    param(
        [Parameter(Mandatory = $true)]$StackInfo,
        [Parameter(Mandatory = $true)][string]$ProjectRoot
    )
    $stack = $StackInfo.stack
    $signals = $StackInfo.signals -join ', '
    $today = Get-Date -Format 'yyyy-MM-dd HH:mm'

    # Detecta lacunas comuns
    $hasTests = Test-Path -LiteralPath (Join-Path $ProjectRoot 'tests')
    $hasCi = (Test-Path -LiteralPath (Join-Path $ProjectRoot '.github/workflows')) -or (Test-Path -LiteralPath (Join-Path $ProjectRoot '.gitlab-ci.yml')) -or (Test-Path -LiteralPath (Join-Path $ProjectRoot 'azure-pipelines.yml'))
    $hasDocker = Test-Path -LiteralPath (Join-Path $ProjectRoot 'Dockerfile')
    $hasReadme = Test-Path -LiteralPath (Join-Path $ProjectRoot 'README.md')
    $hasGitignore = Test-Path -LiteralPath (Join-Path $ProjectRoot '.gitignore')

    $gaps = @()
    if (-not $hasTests) { $gaps += 'Has Tests' }
    if (-not $hasCi) { $gaps += 'Has CI/CD' }
    if (-not $hasDocker) { $gaps += 'Has Docker' }
    if (-not $hasReadme) { $gaps += 'Has README' }
    if (-not $hasGitignore) { $gaps += 'Has .gitignore' }
    $gapsList = if ($gaps.Count -gt 0) { $gaps | ForEach-Object { "- [ ] $_" } } else { '- Nenhuma lacuna critica detectada.' }

    $conventions = switch ($stack) {
        'dotnet'  { '- **Naming**: PascalCase para classes, camelCase para metodos/variaveis`n- **ORM**: provavel Entity Framework Core (verificar .csproj)' }
        'node'    { '- **Naming**: camelCase para variaveis/funcoes, PascalCase para classes`n- **Module System**: ESM ou CommonJS (verificar package.json type)' }
        'python'  { '- **Naming**: snake_case para modulos/funcoes, PascalCase para classes`n- **Type Hints**: obrigatorios em modulos publicos' }
        'angular' { '- **Naming**: kebab-case para selectors, PascalCase para classes`n- **Standalone**: true (Angular 17+ default)' }
        'next'    { '- **Naming**: kebab-case para arquivos, PascalCase para componentes`n- **Server Components**: default em App Router' }
        'go'      { '- **Naming**: PascalCase para exported, camelCase para unexported`n- **Idioms**: erros como valores, contexto primeiro' }
        'rust'    { '- **Naming**: snake_case para variaveis/funcoes, PascalCase para tipos`n- **Idioms**: Result<T,E> em vez de panic' }
        default   { '- **Naming**: a definir com base em patterns do projeto' }
    }

    $signalsList = $signals -split ',' | ForEach-Object { '- **' + $_.Trim() + '**' }
    $signalsListStr = $signalsList -join "`n"
    $projectName = Split-Path -Leaf $ProjectRoot
    $checkOk = '[OK]'
    $checkNo = '[ ]'
    $hasTestsMd = if ($hasTests) { $checkOk } else { $checkNo }
    $hasCiMd = if ($hasCi) { $checkOk } else { $checkNo }
    $hasDockerMd = if ($hasDocker) { $checkOk } else { $checkNo }
    $hasReadmeMd = if ($hasReadme) { $checkOk } else { $checkNo }
    $hasGitignoreMd = if ($hasGitignore) { $checkOk } else { $checkNo }

    $content = "# PROJECT-DNA`n`n" +
        "**Gerado em**: $today`n" +
        "**Gerado por**: purify.ps1 (DR-0180 Fase 1)`n" +
        "**Stack detectado**: $stack`n" +
        "**Confidence**: $($StackInfo.confidence)`n" +
        "**Signals**: $signals`n" +
        "**Projeto**: $projectName`n`n" +
        "## Visao Geral`n`n" +
        "Projeto analisado automaticamente por `purify.ps1` (DR-0180).`n`n" +
        "- **Nome**: $projectName`n" +
        "- **Tipo**: $stack`n" +
        "- **Stack**: $stack (confidence $($StackInfo.confidence))`n`n" +
        "## Stack Detectado`n`n" +
        "$signalsListStr`n`n" +
        "## Convencoes Detectadas`n`n" +
        "$conventions`n" +
        "- $hasTestsMd Has Tests`n" +
        "- $hasCiMd Has CI/CD`n" +
        "- $hasDockerMd Has Docker`n" +
        "- $hasReadmeMd Has README`n" +
        "- $hasGitignoreMd Has .gitignore`n`n" +
        "## Lacunas (Gaps)`n`n" +
        "$gapsList`n`n" +
        "## Proximos Passos Recomendados`n`n" +
        "1. **Validar PROJECT-DNA**: revisar e ajustar com o time`n" +
        "2. **Rodar Doctor**: `xforge doctor` para validar setup`n" +
        "3. **Adotar Skills gradualmente**: instalar 1 skill por semana`n" +
        "4. **Aplicar GCF**: usar Conselho dos Genios para decisoes`n" +
        "5. **Documentar Decisoes**: cada DR em `.xforge/decisions/` `n`n" +
        "## Referencias`n`n" +
        "- GCF (Regra de Ouro Suprema): `.kilo/rules/02-genius-council-framework.md` `n" +
        "- Stack detection: `.kilo/skills/stack-aware-context/SKILL.md` `n" +
        "- DR-0180 (este template): `.xforge/decisions/DR-0180-stack-aware-context-and-memory-namespace.md` `n`n" +
        "## Comandos Uteis`n`n" +
        "````n" +
        "# Re-rodar deteccao`n" +
        ".xforge/scripts/purify.ps1 -ProjectRoot .`n`n" +
        "# Ver o que mudaria (sem alterar)`n" +
        ".xforge/scripts/purify.ps1 -WhatIf`n`n" +
        "# Limpar template-only paths`n" +
        ".xforge/scripts/reset-memory.ps1`n`n" +
        "# Diff contra manifest`n" +
        ".xforge/scripts/diff-consumer.ps1`n" +
        "````n"

    return $content
}

if ($MyInvocation.MyCommand.ScriptBlock.Module) {
    Export-ModuleMember -Function @(
        'Rewrite-ProjectPreferences',
        'Rewrite-ProjectDna'
    )
}
# Em dot-source (sem .psm1), funcoes ficam disponiveis no escopo do chamador.

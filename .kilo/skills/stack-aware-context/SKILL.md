---
name: stack-aware-context
description: Use when detecting project stack, filtering skills/agents/knowledge by stack, or applying ACL on cross-project contamination. Loads applicabilityScope from INDEX.json and filters out incompatible entries.
when_to_use: Detecting stack, filtering knowledge/skill/agent loads, applying cross-project isolation, running purify.ps1
when_not_to_use: When stack is already known and stable, when project has no .xforge/
inputs:
  - ProjectRoot (default: cwd)
  - Stack (optional override)
outputs:
  - Filtered list of applicable skills/agents/knowledge
  - Stack detection report
  - Recommendations for memory cleanup
related_rules:
  - .kilo/rules/memory-namespace.md
  - .kilo/rules/knowledge-rules.md
  - .kilo/rules/01-xforge-golden-rules.md (Regra 0 stack-agnostic)
related_dr:
  - DR-0180 (Stack-Aware Context + Memory Namespace)
---

# Stack-Aware Context Skill

> Skill canonica para deteccao de stack + filtragem de contexto (DR-0180).

## 1. O que faz

Esta skill implementa o **ACL (Anti-Corruption Layer)** do XForge:

1. **Detecta o stack** do projeto ativo via sinais (package.json, *.csproj, etc)
2. **Carrega o manifesto** `.xforge/template-only.json` para saber o que e template-only vs user-facing
3. **Filtra knowledge entries** por `applicabilityScope` vs stack detectado
4. **Filtra skills/agents** por aplicabilidade
5. **Reporta contaminacao** (ex: learning.jsonl com preferencias .NET em projeto Python)
6. **Sugere limpeza** via `purify.ps1` ou `reset-memory.ps1`

## 2. Quando usar

```powershell
# Stack detection simples
. .xforge/scripts/lib/stack-detector.ps1
$info = Get-ProjectStack -ProjectRoot .
Format-StackReport $info

# Stack detection com ambiguous warning
$info = Get-ProjectStack -ProjectRoot .  # warns if ambiguous
```

## 3. Quando NAO usar

- Stack ja foi detectado e validado na sessao atual (cache)
- Projeto nao tem `.xforge/` (greenfield, antes do init)
- Stack e unico e estavel (1 *.csproj ou 1 package.json, sem ambiguity)

## 4. Algoritmo de deteccao

15 sinais ordenados por precisao (peso):

| Peso | Sinal | Stack | Precisao |
|-----:|-------|-------|----------|
| 100 | `*.csproj`, `*.sln`, `*.slnx` | dotnet | alta |
| 100 | `angular.json` | angular | alta |
| 100 | `next.config.{js,ts}` | next | alta |
| 100 | `nuxt.config.{js,ts}` | nuxt | alta |
| 100 | `svelte.config.js` | svelte | alta |
| 100 | `pyproject.toml` | python | alta |
| 100 | `go.mod` | go | alta |
| 100 | `Cargo.toml` | rust | alta |
| 100 | `pom.xml`, `build.gradle` | java | alta |
| 100 | `Gemfile` | ruby | alta |
| 100 | `composer.json` | php | alta |
| 100 | `mix.exs` | elixir | alta |
| 90 | `*.sln*`, `requirements.txt` | dotnet/python | alta |
| 80 | `package.json` | node | media (precisa verificar angular.json, next.config.*, etc) |
| 60 | `index.html` | html | baixa |

**Algoritmo**: para cada regra (ordenada por peso DESC), verificar se signal existe. Soma pesos por stack. Stack vencedor = maior soma. Confidence = soma_vencedor / soma_total. Se 2+ stacks empatam com peso >= 80 e diferenca <= 10, marca ambiguous.

## 5. Stack-aware filtering (ACL)

Para cada knowledge entry em `.xforge/knowledge/INDEX.json`:

```json
{
  "id": "xforge-mediatr-cqrs-completo",
  "applicabilityScope": ["dotnet"],
  ...
}
```

**Regras**:

- `["*"]` -> sempre incluido
- `["dotnet"]` -> incluir apenas se stack detectado = `dotnet`
- `["python"]` -> incluir apenas se stack detectado = `python`
- Multi-scope `["dotnet", "python"]` -> incluir se stack = `dotnet` OU `python`
- Sem campo `applicabilityScope` -> tratar como `["*"]` (compatibilidade retroativa)

## 6. Comandos

```powershell
# Detect + report
.xforge/scripts/purify.ps1 -WhatIf

# Detect + rewrite memory
.xforge/scripts/purify.ps1

# Detect + rewrite for subproject
.xforge/scripts/purify.ps1 -ProjectRoot src/my-module

# Init clean consumer
.xforge/scripts/init-consumer.ps1 -TargetDir ../my-new-project

# Reset memory of existing clone
.xforge/scripts/reset-memory.ps1 -WhatIf

# Diff against manifest
.xforge/scripts/diff-consumer.ps1
```

## 7. Integracao com agent router

Quando um agente (orchestrator) carrega contexto:

```
1. Detectar stack (Get-ProjectStack)
2. Carregar knowledge INDEX
3. Filtrar entries por applicabilityScope
4. Carregar apenas skills/agents compativeis
5. Reportar ao usuario: "Stack X detectado, carregados N skills, M knowledge entries"
```

## 8. Limites conhecidos

- **Stack multi (1 projeto com backend .NET + frontend React)**: detecta o stack primario (maior peso), mas pode ser refinado em Fase 2 com deteccao por subdiretorio.
- **Stack sem manifest customizado**: usa regras embutidas no `stack-detector.ps1`.
- **Mono-repo**: detecta o stack do root, mas usuario pode precisar rodar `purify.ps1 -ProjectRoot services/foo` para cada subprojeto.

## 9. Referencias

- DR-0180 - design completo
- `.kilo/rules/memory-namespace.md` - regra canonica
- `.kilo/rules/01-xforge-golden-rules.md` - Regra 0 (stack-agnostic)
- `.kilo/skills/project-recognition/SKILL.md` - skill relacionada (reconhecimento de projeto)

## 10. Changelog

- v1.0.0 (2026-06-21): criacao inicial (DR-0180)

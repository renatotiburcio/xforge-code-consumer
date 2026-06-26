# Immutable Scoring System - XForge Engineer (Stack-Aware)

## Visao Geral

Sistema de pontuacao que o agente **NAO pode modificar ou manipular**. A pontuacao eh calculada por um processo externo (validador) que o agente nao controla. A unica excecao eh quando o humano solicita alteracao explicitamente.

## Regra Fundamental

```
╔══════════════════════════════════════════════════════════════╗
║  O AGENTE NUNCA PODE MODIFICAR O SISTEMA DE PONTUACAO.     ║
║  A pontuacao eh calculada por um processo separado.          ║
║  A unica excecao eh solicitacao humana explicita.            ║
╚══════════════════════════════════════════════════════════════╝
```

## Como Funciona

### 1. Metrica Unica: XForge Score (xfs)

O **XForge Score** eh uma metrica composta de 5 dimensoes, cada uma com peso fixo:

```
xfs = (correctness * 0.30) + (performance * 0.20) + (quality * 0.20) + (simplicity * 0.15) + (prevention * 0.15)
```

| Dimensao | Peso | O que mede | Como mede |
|----------|------|------------|-----------|
| **Correctness** | 30% | O codigo funciona? Testes passam? | stack-specific test runner exit code |
| **Performance** | 20% | Eh rapido? Sem N+1, sem memory leaks? | Analise estatica + metricas |
| **Quality** | 20% | Codigo limpo? Padroes seguidos? | stack-specific formatter + lint |
| **Simplicity** | 15% | Mudanca minima? Sem over-engineering? | Analise de diff |
| **Prevention** | 15% | Erros prevenidos? Padroes aprendidos? | Error graph matches |

### 2. Validacao Independente

O scoring eh executado por um **validador separado** que o agente nao controla:

```
+-----------------+     +------------------+     +-----------------+
|   Agente XForge |---->|  Scoring Script  |---->|  results.tsv    |
|   (modifica     |     |  (calcula xfs)   |     |  (log imutavel) |
|    codigo)      |     |  (agente NAO     |     |                 |
|                 |     |   controla)      |     |                 |
+-----------------+     +------------------+     +-----------------+
```

### 3. Protecoes

| Protecao | Descricao |
|----------|-----------|
| **Script read-only** | `score.sh` tem permissao 555 (execute-only) |
| **Resultados append-only** | `results.tsv` so permite append, nunca overwrite |
| **Hash de integridade** | Cada linha tem hash SHA256 do conteudo |
| **Validador externo** | Scoring roda em processo separado |
| **Auditoria** | Qualquer tentativa de modificacao eh logada |

## Metricas Detalhadas

### Correctness (30%)

Stack-specific test runner:

```python
# .NET: tests_passed = dotnet test exit code 0
# Node:  tests_passed = vitest/jest exit code 0
# Python: tests_passed = pytest exit code 0
# Go:    tests_passed = go test ./... exit code 0
# Rust:  tests_passed = cargo test exit code 0
# HTML+Tailwind: tests_passed = htmlhint + pa11y exit code 0

correctness = (
    tests_passed / total_tests * 0.5 +        # 50%: testes passam
    build_success * 0.3 +                       # 30%: build limpo
    (1 - runtime_errors) * 0.2                  # 20%: sem erros de runtime
)
```

### Performance (20%)

```python
# Calculado por analise estatica stack-aware
performance = (
    (1 - n_plus_one_queries) * 0.3 +           # 30%: sem N+1
    (1 - sync_over_async) * 0.3 +               # 30%: sem sync-over-async
    (1 - memory_leaks) * 0.2 +                  # 20%: sem memory leaks
    response_time_score * 0.2                    # 20%: tempo de resposta
)
```

### Quality (20%)

```python
# Stack-specific:
# .NET:    dotnet format + dotnet format --verify-no-changes
# Node:    prettier --check + eslint
# Python:  ruff check + ruff format --check
# Go:      gofmt -l + golangci-lint
# Rust:    cargo fmt --check + cargo clippy
# HTML:    htmlhint + tailwindcss-classnames --check

quality = (
    format_compliance * 0.4 +                    # 40%: formatacao
    (1 - warnings) * 0.3 +                       # 30%: sem warnings
    naming_convention * 0.15 +                   # 15%: padroes de nomes
    documentation * 0.15                         # 15%: documentacao
)
```

### Simplicity (15%)

```python
# Calculado por analise de diff
simplicity = (
    lines_added_ratio * 0.4 +                    # 40%: poucas linhas adicionadas
    (1 - files_changed_ratio) * 0.3 +            # 30%: poucos arquivos alterados
    (1 - new_dependencies) * 0.3                 # 30%: sem novas dependencias
)
```

### Prevention (15%)

```python
# Calculado por error graph
prevention = (
    errors_prevented * 0.5 +                     # 50%: erros prevenidos
    patterns_applied * 0.3 +                     # 30%: padroes aplicados
    knowledge_gaps_filled * 0.2                  # 20%: gaps preenchidos
)
```

## Formato do results.tsv

```
commit  xfs     correctness     performance      quality  simplicity      prevention      status  description     timestamp
a1b2c3d 0.875   0.92    0.85    0.90    0.88    0.82    keep    Adicionado FluentValidation   2026-06-11T10:30:00Z
b2c3d4e 0.750   0.80    0.70    0.85    0.60    0.78    discard Mudanca radical de arquitetura  2026-06-11T10:35:00Z
c3d4e5f 0.000   0.00    0.00    0.00    0.00    0.00    crash   Build falhou - null reference 2026-06-11T10:40:00Z
```

## Script de Validacao

O script `score.ps1` eh o unico que calcula a pontuacao (stack-aware):

```powershell
# score.ps1 - Execute-only, agente nao pode modificar
# Detecta stack e calcula XForge Score para a ultima mudanca
# Uso: .\.kilo\automation\scripts\score.ps1
# Saida: linha para results.tsv
```

## Regras para o Agente

1. **NUNCA** tentar modificar `score.ps1`
2. **NUNCA** tentar modificar `results.tsv` diretamente
3. **NUNCA** tentar manipular a pontuacao de alguma forma
4. **SEMPRE** aguardar o resultado do scoring antes de decidir keep/discard
5. **SEMPRE** respeitar o resultado do scoring (mesmo que discorde)
6. **SEMPRE** registrar o stack detectado no results.tsv

## Integracao com o Loop

```
1. Agente faz mudanca no codigo
2. Agente faz commit
3. Scoring script detecta stack e roda gates apropriados
4. Scoring calcula xfs
5. Scoring registra em results.tsv (com campo `stack`)
6. Agente le resultado
7. Agente decide: keep (avanca) ou discard (reverte)
8. Repete
```

## Excecoes

A unica forma de modificar o sistema de pontuacao eh:

1. **Solicitacao humana explicita**: "Altere o peso de correctness para 40%"
2. **Auditoria humana**: Humano revisa e ajusta periodicamente
3. **Evolucao controlada**: Mudancas so passam apos review humano

## Multi-Stack Scoring

Quando o projeto tem mais de um stack (ex: Next.js + Node backend):
- O scoring roda gates de TODOS os stacks detectados
- O xfs final eh a media ponderada pelo numero de arquivos de cada stack
- Cada stack contribui com seu proprio subset das 5 dimensoes
- Weighted formula:

```
xfs_multi = sum(xfs_stack * files_stack) / total_files
```

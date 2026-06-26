---
name: xforge-init
description: Golden Command — ativa e valida TODO o sistema XForge de uma vez. Roda doctor, Ollama, knowledge, error graph, scripts, rules, manual e validation. Mostra score de prontidão.
category: xforge-public
agent: code
---

# /xforge-init

## Objetivo
Ativar e validar TODO o sistema XForge de uma vez. Mostra score de prontidão (0-100%).

## Modos de Operacao

| Modo | Flag | Quando usar |
|------|------|-------------|
| **Consumer** (padrao) | nenhuma flag | Preparar o template para usar em um projeto (remove .git, purifica memory, cria novo repo) |
| **Template** | `--template` | Manter o template XForge para manutencao (valida, mostra score, NAO modifica nada) |

## Procedimento

### Modo Consumer (padrao — sem flag)

Quando o usuario roda `/xforge-init` sem flags, o sistema prepara o template para ser usado em um projeto:

1. **Validar que esta no template** — verificar que `.xforge/template-only.json` existe
2. **Copiar paths user-facing** — usar `template-only.json` como referencia
3. **Remover paths template-only** — DR-0211
4. **Atualizar .gitignore** — remover regras template-only
5. **Purificar memory** — rodar `purify.ps1` com stack detectada
6. **Git reset** — remover `.git` do template, `git init` novo, commit inicial
7. **Instrucoes** — mostrar proximos passos (git remote add, etc)

**Script:** `.xforge/scripts/init-project.ps1` implementa este fluxo.
```powershell
.xforge/scripts/init-project.ps1 -TargetDir <dir> -Stack <stack>
```

### Modo Template (flag `--template`)

Quando o usuario passa `--template`, o sistema valida o template para manutencao:

#### 1. Doctor Check
Execute:
```powershell
.\.kilo\automation\scripts\doctor.ps1
```
Verifique: 0 errors, todos os [OK] presentes.

#### 2. Ollama Status
Execute:
```powershell
try { Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5 } catch { "Ollama not running" }
```
Verifique: modelos instalados (gemma4-26b, qwen3-coder-30b, qwen3.6-27b, nomic-embed-text).

#### 3. Knowledge Base
Verifique:
- `.xforge/knowledge/INDEX.json` existe
- 173 knowledge files presentes
- `errors-solutions-graph.json` com 20 patterns

#### 4. Scripts
Verifique que estes scripts existem:
- `doctor.ps1`
- `xforge-init.ps1`
- `score.ps1`
- `pre-commit.ps1`
- `live-dashboard.ps1`
- `knowledge-validation.ps1`
- `dependency-check.ps1`
- `proactive-intelligence.ps1`

#### 5. Rules
Verifique que `.kilo/rules/` tem 30 arquivos .md.

#### 6. Manual
Verifique que `docs/index.html` existe com ~1700 linhas.

#### 7. Knowledge Validation
Execute:
```powershell
.\.kilo\automation\scripts\knowledge-validation.ps1
```
Verifique: 6 áreas validadas (INSS, IRRF, eSocial, NF-e, Reforma, CNPJ).

#### 8. Score Final
Calcule:
```
score = (checks_passing / 8) * 100
```

## Saida Esperada

### Modo Consumer
```
╔══════════════════════════════════════════════════════════╗
║              XFORGE INIT — CONSUMER MODE                ║
╠══════════════════════════════════════════════════════════╣
║  Paths copiados: 15                                      ║
║  Template-only removidos: 0                              ║
║  Memory purificada: dotnet                               ║
║  Git init: novo repo criado                              ║
║                                                          ║
║  Proximos passos:                                        ║
║    git remote add origin <seu-repo>                      ║
║    git push -u origin main                               ║
╚══════════════════════════════════════════════════════════╝
```

### Modo Template
```
╔══════════════════════════════════════════════════════════╗
║              XFORGE INIT — TEMPLATE MODE                ║
╠══════════════════════════════════════════════════════════╣
║  Doctor:      PASS (24 OK, 0 errors)                   ║
║  Ollama:      PASS (4 models)                          ║
║  Knowledge:   PASS (173 files)                         ║
║  Error Graph: PASS (20 patterns)                       ║
║  Scripts:     PASS (31 available)                      ║
║  Rules:       PASS (30 loaded)                         ║
║  Manual:      PASS (1741 lines)                        ║
║  Validation:  PASS (6 areas)                           ║
║                                                        ║
║  SCORE: 100% (8/8 checks passed)                       ║
╚══════════════════════════════════════════════════════════╝
```

## Se Algo Falhar

1. Rode `doctor.ps1` para detalhes
2. Corrija os issues encontrados
3. Rode `/xforge-init` novamente

## Uso
```
/xforge-init              # Modo consumer (padrao) — prepara para projeto
/xforge-init --template   # Modo template — valida para manutencao
```

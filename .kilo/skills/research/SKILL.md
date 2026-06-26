---
name: research
description: FASE 1 — Analisa fontes (URLs, pastas, PDFs, repos) e gera documentação padronizada: BACKLOG.md, SPRINTS.md, ROADMAP.md, TASKS/, ARCHITECTURE.md, DECISIONS.md, STATUS.md. Use IA ROBUSTA (paga). Formato OBRIGATÓRIO — não adicione nada além do template.
---

# research — Fase 1: Análise Padronizada

## OBJETIVO

Analisar fontes e gerar documentação padronizada em `.xforge/project/`.

**Formato OBRIGATÓRIO.** O agente DEVE gerar EXATAMENTE os 7 arquivos abaixo, sem exceção, sem adições.

## PROCESSO OBRIGATÓRIO

### Passo 1: Coletar fontes
```
1. Identificar TODAS as fontes (URL, pasta, PDF, repo)
2. Para cada fonte, usar o método correto:
   - URL/webpage → playwright-mcp (SEMPRE, nunca webfetch)
   - Pasta → glob + read
   - PDF → pdf skill
   - Repo → git clone + read
   - XML/JSON → read + parse
```

### Passo 2: Extrair conteúdo (OTIMIZADO)
```
Para CADA fonte, extrair APENAS:
- Nome e tipo do arquivo
- Resumo executivo (3-5 bullets)
- Funcionalidades principais (lista)
- Stack tecnológico
- Pontos de atenção

MÁXIMO: 500 tokens por fonte. NUNCA copiar código completo.
```

### Passo 3: Gerar 7 arquivos padronizados
```
CRIAR na ordem exata:
1. .xforge/project/BACKLOG.md
2. .xforge/project/SPRINTS.md
3. .xforge/project/ROADMAP.md
4. .xforge/project/ARCHITECTURE.md
5. .xforge/project/DECISIONS.md
6. .xforge/project/STATUS.md
7. .xforge/project/TASKS/T001-nome.md (uma por tarefa)
```

## TEMPLATES OBRIGATÓRIOS

### BACKLOG.md
```markdown
# Backlog — [Nome do Projeto]

Gerado em: [data]
Fontes analisadas: [quantidade]

## P0 — Crítico (fazer primeiro)
| ID | Título | Estimativa | Dependências |
|----|--------|-----------|--------------|
| T001 | [título] | [tempo] | nenhuma |

## P1 — Importante
| ID | Título | Estimativa | Dependências |
|----|--------|-----------|--------------|
| T010 | [título] | [tempo] | T001 |

## P2 — Desejável
| ID | Título | Estimativa | Dependências |
|----|--------|-----------|--------------|
| T020 | [título] | [tempo] | T010 |

## P3 — Baixa prioridade
| ID | Título | Estimativa | Dependências |
|----|--------|-----------|--------------|
| T030 | [título] | [tempo] | nenhuma |

## Resumo
- Total: X tarefas (P0: Y, P1: Z, P2: W, P3: V)
- Estimativa total: Xh
- Tarefas sem dependência: N
```

### SPRINTS.md
```markdown
# Sprints — [Nome do Projeto]

## Sprint 1 (semana 1-2) — Fundação
| ID | Título | Dias |
|----|--------|------|
| T001 | [título] | 2 |
| T002 | [título] | 3 |

## Sprint 2 (semana 3-4) — Core
| ID | Título | Dias |
|----|--------|------|
| T010 | [título] | 3 |
| T011 | [título] | 2 |

## Sprint 3 (semana 5-6) — Features
...

## Milestones
| Milestone | Sprint | Data estimada |
|-----------|--------|---------------|
| MVP funcional | Sprint 2 | [data] |
| Beta | Sprint 4 | [data] |
| Release | Sprint 6 | [data] |
```

### ROADMAP.md
```markdown
# Roadmap — [Nome do Projeto]

## Timeline

```
Mês 1        Mês 2        Mês 3        Mês 4        Mês 5        Mês 6
├─ Sprint 1 ─┼─ Sprint 2 ─┼─ Sprint 3 ─┼─ Sprint 4 ─┼─ Sprint 5 ─┼─ Sprint 6 ─┤
│  Fundação   │   Core     │  Features  │  Integração │   QA       │  Release   │
│  T001-T009  │  T010-T019 │  T020-T029 │  T030-T039 │  T040-T049 │  T050-T059 │
└─────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘
```

## Fases
| Fase | Período | Entregável |
|------|---------|-----------|
| Fundação | Mês 1 | Setup, entidades, testes base |
| Core | Mês 2 | Services, repositories, API |
| Features | Mês 3 | Funcionalidades principais |
| Integração | Mês 4 | APIs externas, pagamentos |
| QA | Mês 5 | Testes, performance, segurança |
| Release | Mês 6 | Deploy, docs, launch |
```

### ARCHITECTURE.md
```markdown
# Arquitetura — [Nome do Projeto]

## Stack
| Camada | Tecnologia |
|--------|-----------|
| Frontend | [tecnologia] |
| Backend | [tecnologia] |
| Banco | [tecnologia] |
| Infra | [tecnologia] |

## Diagrama
```
[Frontend] → [API] → [Services] → [Repository] → [Database]
```

## Padrões
| Padrão | Onde usar |
|--------|----------|
| CQRS | Commands/Queries separados |
| Repository | Acesso a dados |
| FluentValidation | Validações |

## Componentes
| Componente | Responsabilidade | Arquivos |
|-----------|-----------------|----------|
| [nome] | [descrição] | [lista] |
```

### DECISIONS.md
```markdown
# Decisões Técnicas — [Nome do Projeto]

## D001: [Título da Decisão]
- **Contexto**: [situação]
- **Opções**: [A, B, C]
- **Escolha**: [opção escolhida]
- **Rationale**: [por quê]
- **Tradeoffs**: [o que perdeu]

## D002: [Título]
...
```

### STATUS.md
```markdown
# Status — [Nome do Projeto]

## Progresso
| Métrica | Valor |
|---------|-------|
| Tarefas totais | X |
| Concluídas | Y |
| Em andamento | Z |
| Bloqueadas | W |
| Progresso | Y/X (percentual) |

## Última atualização
[data]

## Próximas tarefas
| ID | Título | Prioridade |
|----|--------|-----------|
| T001 | [título] | P0 |

## Bloqueios
| ID | Título | Motivo |
|----|--------|--------|
| (nenhum) | | |
```

### TASKS/TXXX-nome.md
```markdown
---
id: T001
title: [Título claro]
priority: P0
status: pending
estimated_time: [tempo]
dependencies: nenhuma
---

# T001: [Título]

## Objetivo
[1 frase clara]

## Passos
1. [passo específico e acionável]
2. [passo específico]
3. [passo específico]

## Arquivos
- Criar: `src/path/novo.cs`
- Modificar: `src/path/existente.cs`

## Critérios de Aceite
- [ ] [critério verificável]
- [ ] [critério verificável]

## Notas
- [qualquer observação relevante]
```

## ECONOMIA DE TOKENS

| Regra | Limite |
|-------|--------|
| Por fonte | 500 tokens |
| Por arquivo gerado | 200 tokens |
| Total BACKLOG.md | 500 tokens |
| Total TASKS/ (todas) | 200 tokens por tarefa |
| Total por análise | 5000 tokens |

**Formato comprimido — tabelas e listas, nunca parágrafos.**

## CHECKPOINT

Após gerar TODOS os 7 arquivos:
```
Salve .xforge/checkpoints/research.json:
{
  "source": "[URL/pasta analisada]",
  "filesGenerated": ["BACKLOG.md", "SPRINTS.md", ...],
  "taskCount": X,
  "priorityBreakdown": {"P0": Y, "P1": Z, ...},
  "timestamp": "ISO 8601"
}
```

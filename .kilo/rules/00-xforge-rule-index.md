# Rules Index — XForge Engineer

Guia rápido para encontrar a rule correta. O agente deve ler este arquivo PRIMEIRO antes de carregar qualquer rule.

## Como Usar

1. Identificar a situação
2. Encontrar a rule correspondente nesta tabela
3. Ler APENAS a rule necessária (não todas)

## Regra de Ouro Suprema (LEIA PRIMEIRO)

| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| **GCF (Genius Council Framework)** | `02-genius-council-framework.md` | **SEMPRE antes de qualquer decisao nao-trivial** |

O GCF tem precedencia absoluta. Sem ele, nenhuma outra rule se aplica em decisao arquitetural.

## Rules por Categoria

### Core
| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| Golden Rules | `01-xforge-golden-rules.md` | Sempre — regras fundamentais |
| **GCF (Regra de Ouro)** | `02-genius-council-framework.md` | **Sempre antes de decisao nao-trivial** |
| Active Project | `active-project-root-rules.md` | Ao iniciar sessão |

### Memória & Aprendizado
| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| Session Memory | `session-memory.md` | Preferências, decisões, histórico do usuário |
| Memory Rules | `memory-rules.md` | Regras básicas de memória |

### Inteligência & Qualidade
| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| Self-Healing | `self-healing-rules.md` | Correção automática de erros |
| Quality Gates | `proactive-quality-gates.md` | Checks automáticos pré-commit/push |
| Dependency Intelligence | `dependency-intelligence.md` | Monitoramento de pacotes (NuGet/npm/PyPI/Go/Cargo) |

### Decisao & Governanca
| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| Audit Trail | `audit-trail-rules.md` | Toda mudanca relevante deve registrar |
| Cost Rules | `cost-rules.md` | Tracking de custo de providers |
| Event Bus | `event-bus-rules.md` | Eventos internos (PROJECT_RECOGNIZED, etc) |
| Policy Rules | `policy-rules.md` | Politicas obrigatorias antes da execucao |
| RBAC Rules | `rbac-rules.md` | Permissoes para acoes criticas |
| Promotion Rules | `promotion-rules.md` | Pipeline experimental → enterprise-standard |
| Human Review | `human-review-rules.md` | Aprovacao humana obrigatoria |
| State Machine | `state-machine-rules.md` | Transicoes de workflow |

### Documentacao & Conhecimento
| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| Knowledge Rules | `knowledge-rules.md` | Origem, confianca, rastreabilidade |
| Curation Rules | `curation-rules.md` | Curadoria de memoria |
| Legacy Import | `legacy-import-rules.md` | Conteudo legado deve ser inventariado |
| Trust Score | `trust-score-rules.md` | Score de confianca |
| TTL Rules | `ttl-rules.md` | Conhecimento com validade |
| Documentation Clarity | `documentation-clarity-rules.md` | Regras de clareza |
| Fullstack Analysis | `fullstack-analysis-rules.md` | Pipeline 11 estagios |
| SDD Authoring | `sdd-authoring-rules.md` | Template canonico de SDD |
| Handoff Readiness | `handoff-readiness-rules.md` | Bloqueios para handoff |

### UI/UX & Arquitetura
| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| Diagram Quality | `diagram-quality-rules.md` | Limites de diagramas |
| Enterprise Architecture | `enterprise-architecture-rules.md` | Bounded contexts, eventos, DDD |
| Multi-Agent Orchestration | `multi-agent-orchestration.md` | Orquestracao multi-agente |

### Sistema & Memoria
| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| Session Memory | `session-memory.md` | Memoria de longo prazo |
| Memory Rules | `memory-rules.md` | Regras basicas |
| Self-Healing | `self-healing-rules.md` | Correcao automatica |
| Quality Gates | `proactive-quality-gates.md` | Checks pre-commit/push |
| Simplicity Criterion | `simplicity-criterion.md` | Matriz vale-a-pena |

### Outros
| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| Provider Routing | `provider-routing-rules.md` | Context-based provider selection |
| Security Rules | `security-rules.md` | Segredos, LGPD, dados sensiveis |
| Cost Rules | `cost-rules.md` | Custo de providers |
| Manual Sync | `manual-sync-rules.md` | Sync docs/index.html apos mudancas |
| Immutable Scoring | `immutable-scoring.md` | xfs score (read-only) |
| Auto Retry Recovery | `auto-retry-recovery.md` | Recuperacao automatica |
| Checkpoint Resume | `checkpoint-resume.md` | Salvar checkpoint em limit |
| Autonomous Experiment | `autonomous-experiment-loop.md` | Loop de experimentos |

## Workflow Recomendado

1. **Recebeu pedido nao-trivial?** -> Leia `02-genius-council-framework.md` (GCF) PRIMEIRO.
2. **Precisa de clarificacao?** -> Use `interaction-intelligence.md`.
3. **Implementando codigo?** -> Leia `01-xforge-golden-rules.md` + `dependency-intelligence.md`.
4. **Documentando?** -> Leia `documentation-clarity-rules.md` + `sdd-authoring-rules.md`.
5. **Antes de commit?** -> Leia `proactive-quality-gates.md` + `self-healing-rules.md`.
6. **Decisao critica?** -> Acione o Conselho (GCF + Devil''s Advocate).

### Sistema & Organizacao
| Rule | Arquivo | Quando usar |
|------|---------|-------------|
| **Temp Files Organization** | `temp-files-organization.md` | Sempre - root so tem artefatos canonicos, transient em /temp/ |
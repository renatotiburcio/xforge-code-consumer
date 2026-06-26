# Sprint Planning — Rebrand KiloCode → XForge Code

**Data**: 2026-06-25
**Versao**: 1.0.0

---

## Sprint 0 — Descoberta

**Objetivo**: Imersao completa no projeto antes de qualquer mudanca

**Atividades**:
- [x] Mapeamento arquitetural (src/, packages/, .kilo/, .xforge/)
- [x] Analise de build (scripts, CI/CD, Docker)
- [x] Mapeamento de dominio (session, agent, provider, config, etc.)
- [x] Analise VS Code (APIs, contribution points, gap analysis)
- [x] Mapeamento de naming (10K+ ocorrencias)
- [x] Analise de branding assets
- [ ] Consolidated documentation in `.xforge/project/`

**Status**: CONCLUIDO
**Duracao**: 1 semana
**Resultado**: Relatorio completo disponivel para execucao

---

## Sprint 1 — Brand Abstraction Layer

**Objetivo**: Criar camada de abstracao unica para branding

**Tarefas**:
| ID | Tarefa | Estimativa | Responsavel |
|---|---|---|---|
| S1.1 | Criar `BRAND_CONFIG` em `packages/core/src/constants/brand.ts` | 4h | SWE |
| S1.2 | Criar funcoes helper (command prefix, env vars, headers) | 4h | SWE |
| S1.3 | Adicionar dual-write support (legado + novo) | 8h | SWE |
| S1.4 | Unit tests para brand helpers | 4h | SWE |
| S1.5 | Integrar em core + opencode + kilo-vscode | 8h | SWE |
| S1.6 | Code review + validacao | 4h | Lead |

**Total**: 32h (1 week)
**Criterios de aceite**:
- [ ] Unico arquivo `brand.ts` com todas as constants
- [ ] `bun test packages/core/brand/` 100% pass
- [ ] Dual-write funciona (env vars KILOCODE_ E XFORGE_CODE_ ambos lidos)

**Marco M1**: Brand abstraction complete

---

## Sprint 2 — Package Renaming

**Objetivo**: Renomear escopo npm de @kilocode/* para @xforge-code/*

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S2.1 | Script: rename package.json em 22 pacotes | 2h |
| S2.2 | Script: update root package.json workspaces | 1h |
| S2.3 | Script: update import statements (~500 locais) | 4h |
| S2.4 | Regenerate bun.lock (bun install) | 2h |
| S2.5 | Atualizar turbo.json pipeline keys | 1h |
| S2.6 | Atualizar .github/workflows references | 3h |
| S2.7 | Atualizar build scripts (Dockerfile, docker-compose) | 4h |
| S2.8 | Full build validation (bun run build) | 4h |
| S2.9 | Tests passam (bun test per package) | 8h |
| S2.10 | Code review + ajustes | 4h |

**Total**: 33h
**Criterios de aceite**:
- [ ] `bun install` compila sem erros
- [ ] Zero `@kilocode/` references nos arquivos .ts/.tsx/.js
- [ ] Build completo OK

---

## Sprint 3 — Package Publishing

**Objetivo**: Publicar pacotes npm sob novo escopo

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S3.1 | Criar organizacao `xforge-code` no npm | 2h |
| S3.2 | Configurar tokens de publicacao | 1h |
| S3.3 | Publicar 22 pacotes (beta, --tag beta) | 8h |
| S3.4 | Validar: `npm view @xforge-code/cli` | 2h |
| S3.5 | Configurar deprecation dos pacotes antigos | 2h |

**Total**: 15h

---

## Sprint 4 — Extension Rebrand (Core)

**Objetivo**: Extension standalone sem dependencias Kilo Code

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S4.1 | Atualizar `kilo-vscode/package.json` | 2h |
| S4.2 | Remover `extensionDependencies` | 1h |
| S4.3 | Atualizar activationEvents para `["*"]` | 1h |
| S4.4 | Adicionar capabilities (virtualWorkspaces) | 2h |
| S4.5 | Script: rename `kilo-code.new.*` → `xforge-code.new.*` | 4h |
| S4.6 | Atualizar ~455 locais de source | 8h |
| S4.7 | Adicionar settings migration script | 8h |
| S4.8 | Atualizar config migration | 4h |
| S4.9 | Testes da extensao (bun test + VS Code) | 8h |

**Total**: 38h

---

## Sprint 5 — Extension Rebrand (UI + Assets)

**Objetivo**: Identidade visual completa

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S5.1 | Criar novos icons em todos os tamanhos | 16h (design) |
| S5.2 | Atualizar `package.json` icon field | 1h |
| S5.3 | Atualizar UI labels (4 code actions) | 2h |
| S5.4 | Atualizar system prompts (prompt/*.txt) | 2h |
| S5.5 | Atualizar i18n en + pt-BR | 8h |
| S5.6 | Atualizar i18n em 14+ linguas | 16h |
| S5.7 | Atualizar favicons | 2h |
| S5.8 | Testes de regressao visual | 8h |

**Total**: 55h

---

## Sprint 6 — Template Update (Parte 1)

**Objetivo**: Manual HTML + configs rebrand

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S6.1 | Atualizar 6 primeiras paginas do manual | 16h |
| S6.2 | Atualizar 6 paginas restantes | 16h |
| S6.3 | Atualizar index.html | 4h |
| S6.4 | Atualizar SUMMARY.md | 2h |
| S6.5 | Rotar `check-manual.ps1` | 1h |
| S6.6 | Rotar `check-manual-content.ps1` | 1h |

**Total**: 40h

---

## Sprint 7 — Template Update (Parte 2)

**Objetivo**: Auto-docs + community

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S7.1 | Atualizar AGENTS.md | 4h |
| S7.2 | Atualizar CLAUDE.md | 4h |
| S7.3 | Atualizar ARCHITECTURE.md | 8h |
| S7.4 | Atualizar CHANGELOG.md | 4h |
| S7.5 | Atualizar .kilo/rules references | 8h |
| S7.6 | Atualizar .xforge/config/*.json | 2h |
| S7.7 | Atualizar knowledge base | 8h |

**Total**: 38h

---

## Sprint 8 — Build & CI Validation

**Objetivo**: Build limpo em todos os OS

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S8.1 | Build Windows (0 erros) | 4h |
| S8.2 | Build Linux (0 erros) | 4h |
| S8.3 | Build macOS (0 erros) | 4h |
| S8.4 | 30+ CI workflows green | 8h |
| S8.5 | TypeCheck + Lint + Tests | 8h |
| S8.6 | Security audit (0 CVEs criticos) | 4h |
| S8.7 | CodeQL (0 alertas) | 2h |

**Total**: 34h

---

## Sprint 9 — Testing & Migration

**Objetivo**: Validacao completa de migracao

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S9.1 | Migration test: settings | 8h |
| S9.2 | Migration test: globalStorage | 4h |
| S9.3 | Migration test: MCP servers | 4h |
| S9.4 | Migration test: custom commands | 4h |
| S9.5 | Performance benchmark | 8h |
| S9.6 | E2E test (instalacao → first run) | 8h |
| S9.7 | Bug fixes (variavel) | 8h |

**Total**: 44h

---

## Sprint 10 — Release Candidate

**Objetivo**: RC publicado em staging

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S10.1 | Version bump 8.0.0-rc.1 | 1h |
| S10.2 | CHANGELOG para RC | 2h |
| S10.3 | Migration guide draft | 8h |
| S10.4 | Marketplace preview deploy | 4h |
| S10.5 | Beta tester feedback loop | 8h |
| S10.6 | Ajustes baseados em feedback | 8h |

**Total**: 31h

---

## Sprint 11 — Producao

**Objetivo**: Release final (GA)

**Tarefas**:
| ID | Tarefa | Estimativa |
|---|---|---|
| S11.1 | Version bump 8.0.0 (stable) | 1h |
| S11.2 | Tags Git (v8.0.0) | 1h |
| S11.3 | Publicacao npm + marketplace | 2h |
| S11.4 | Comunicacao + blog post | 4h |
| S11.5 | Depreciation notice Kilo Code | 2h |
| S11.6 | Monitoring pos-release | 4h |

**Total**: 14h

---

## Resumo de Esforco

| Sprint | Esforco | % do Total |
|---|---|---|
| S0 — Descoberta | 16h | 4% |
| S1 — Brand Abstraction | 32h | 8% |
| S2 — Package Renaming | 33h | 8% |
| S3 — Package Publishing | 15h | 4% |
| S4 — Extension Rebrand | 38h | 9% |
| S5 — UI + Assets | 55h | 13% |
| S6 — Template P1 | 40h | 10% |
| S7 — Template P2 | 38h | 9% |
| S8 — Build/CI | 34h | 8% |
| S9 — Testing | 44h | 11% |
| S10 — RC | 31h | 8% |
| S11 — Release | 14h | 3% |
| **Total** | **~420h** | **100%** |

**Equipe estimada**: 2 SWE + 1 Designer + 1 Lead
**Duracao**: 11 sprints x 1 semana = 11 semanas (~3 meses)

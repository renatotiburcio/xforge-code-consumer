# ROADMAP — Rebrand KiloCode → XForge Code

**Data**: 2026-06-25
**Versao**: 1.0.0
**Horizonte**: 3 meses (12 sprints)

---

## Visao Gero

```
Mes 1 (Sprint 0-3): Fundacao
  → Brand abstraction + Package rename + Core rebrand

Mes 2 (Sprint 4-7): Extensao & Template  
  → Extension completa + Template update + Documentacao

Mes 3 (Sprint 8-11): Validacao & Release
  → Testing + QA + Release candidate + Producao
```

---

## Curto Prazo (Sprint 0-3)

### Sprint 0 — Descoberta (completa)
**Status**: CONCLUIDO
- Analise arquitetural completa
- Matriz de VS Code completa
- Mapeamento naming completo (10K+ ocorrencias)
- Plano de migracao aprovado

### Sprint 1 — Brand Abstraction Layer
**Objetivo**: Criar infraestrutura de branding
- [ ] BRAND_CONFIG em `packages/core/`
- [ ] Funcoes helper (command prefix, headers, env vars)
- [ ] Dual-write support
- [ ] Unit tests

**Criterios de aceite**: Brand lookup <1ms, 100% test coverage

### Sprint 2 — Package Renaming
**Objetivo**: Renomear todos os 22 pacotes
- [ ] Script de rename executado
- [ ] Todos os imports atualizados
- [ ] bun.lock regenerado
- [ ] Build sem erros

**Criterios de aceite**: Zero `@kilocode/` references

### Sprint 3 — Package Publishing
**Objetivo**: Publicar novos pacotes
- [ ] npm org `xforge-code` criado
- [ ] 22 pacotes publicados (beta)
- [ ] Tokens configurados

**Criterios de aceite**: `npm install @xforge-code/cli` funciona

---

## Medio Prazo (Sprint 4-7)

### Sprint 4 — Extension Rebrand (Core)
**Objetivo**: Extension standalone sem dependencias
- [ ] package.json atualizado
- [ ] extensionDependencies removido
- [ ] Comandos renomeados
- [ ] Config namespace migrado

**Criterios de aceite**: Extension ativa sem Kilo Code instalado

### Sprint 5 — Extension Rebrand (UI + Assets)
**Objetivo**: Identidade visual completa
- [ ] Icones substituidos
- [ ] UI strings atualizadas
- [ ] i18n en/pt-BR
- [ ] Settings migrados

**Criterios de aceite**: UI 100% "XForge Code", 0 "Kilo Code" visivel

### Sprint 6 — Template Update
**Objetivo**: .kilo/ + .xforge/ rebrand
- [ ] Manual 12 paginas atualizado
- [ ] Docs/SUMMARY.md atualizado
- [ ] Config files atualizados
- [ ] i18n atualizado (16 linguas)

**Criterios de aceite**: Manual valida em check-manual.ps1

### Sprint 7 — Auto-docs & Community
**Objetivo**: Documentacao automatica consistente
- [ ] AGENTS.md, CLAUDE.md, ARCHITECTURE.md
- [ ] CHANGELOG.md
- [ ] GitHub templates
- [ ] CONTRIBUTING.md (se existir)

**Criterios de aceite**: Todos os arquivos .md sem "kilocode"

---

## Longo Prazo (Sprint 8-11)

### Sprint 8 — Build & CI Validation
**Objetivo**: Build limpo em todos os ambientes
- [ ] Windows build 0 erros
- [ ] Linux build 0 erros
- [ ] macOS build 0 erros
- [ ] 30+ CI workflows green

**Criterios de aceite**: Build matrix 100% pass

### Sprint 9 — Testing & Migration
**Objetivo**: Validacao completa e migration testing
- [ ] 100% tests passam
- [ ] Migration script testado
- [ ] Dados preservados
- [ ] Performance equivalent

**Criterios de aceite**: Migration success rate >= 99%

### Sprint 10 — Release Candidate
**Objetivo**: RC publicado em staging
- [ ] v8.0.0-rc.1 publicado
- [ ] Marketplace preview
- [ ] Migration guide disponivel
- [ ] Beta testers feedback

**Criterios de aceite**: RC instalavel e funcional

### Sprint 11 — Producao
**Objetivo**: Release final
- [ ] v8.0.0 publicado
- [ ] Marketplace publico
- [ ] Comunicacao enviada
- [ ] Depreciacao Kilo Code iniciada

**Criterios de aceite**: v8.0.0 em producao

---

## Marcos (Milestones)

| Milestone | Sprint | Data |
|---|---|---|
| **M1**: Brand abstraction complete | S1 | Semana 2 |
| **M2**: Package renaming complete | S2 | Semana 3 |
| **M3**: Extension standalone | S4 | Semana 5 |
| **M4**: Visual identity complete | S5 | Semana 6 |
| **M5**: Documentation updated | S6-S7 | Semana 8 |
| **M6**: Build validated | S8 | Semana 9 |
| **M7**: RC published | S10 | Semana 11 |
| **M8**: GA release | S11 | Semana 12 |

---

## Riscos ao Longo do Tempo

| Risco | Quando | Mitigacao |
|---|---|---|
| Upstream merge quebra | S2-S4 | Testes de merge semanais |
| npm publish rejection | S3 | Publish como novos pacotes, nao updates |
| Marketplace rejection | S10 | Plan B: publicar sob publisher diferente |
| User migration issues | S10-S11 | Migration script com rollback |

---

## KPIs Trimestrais

| KPI | Target |
|---|---|
| Builds limpos (3 OS) | 100% |
| Test coverage | >= 85% |
| Migration success | >= 99% |
| Extention load time | <= 2s |
| User-reported bugs (pos-release) | < 50/semana |
| Docs coverage | 100% dos commands documentados |

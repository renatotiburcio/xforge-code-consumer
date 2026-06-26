# XForge Manual

> **v50.0.0** (DR-0181, 2026-06-21) — Manual Biblioteca v2.0 — Padrao canonico unico

XForge e' **Enterprise Development OS**: template + runtime + knowledge + manual para construir software corporativo com GCF (Genius Council Framework), 38+ genios, 171 skills, 81 agents, 144 commands e 319 knowledge entries.

## Quickstart

1. Abra `docs/getting-started.md` (5 min para rodar)
2. Veja `docs/manual/01-quickstart.html` (versao visual)
3. Decisao nao-trivial? Acione o **Conselho dos Genios** (ver `manual/03-gcf.html`)

## Indice

- **`docs/SUMMARY.md`** — TOC completo (Markdown, GitHub-friendly)
- **`docs/index.html`** — Manual visual entry point (Tailwind CDN, dark mode, mobile)
- **`docs/manual/`** — 11 paginas canonicas (HTML auto-contido)
- **`docs/getting-started.md`** — Quickstart em Markdown

## Estrutura canonica (DR-0181)

```
docs/
|-- README.md                  (este arquivo, landing GitHub)
|-- SUMMARY.md                 (TOC completo, 12 secoes)
|-- getting-started.md         (5 min para rodar)
|-- index.html                 (entry point visual)
|-- decisions/
|   `-- README.md              (stub 12L -> .xforge/decisions/ADR-INDEX.md)
`-- manual/                    (11 paginas HTML canonicas)
    |-- _template.html         (template DRY)
    |-- 01-quickstart.html
    |-- 02-architecture.html
    |-- 03-gcf.html
    |-- 04-skills.html
    |-- 05-agents.html
    |-- 06-commands.html
    |-- 07-rules.html
    |-- 08-knowledge.html
    |-- 09-decisions.html
    |-- 10-extensions.html
    `-- 11-faq.html
```

## Mudancas vs versao anterior

Removidos: 29 `adr-*.md` orfaos + `glossary.md` (DR-0152 + DR-0181).
Adicionados: 11 paginas HTML canonicas + `_template.html`.
Padronizados: nav, footer, hero, dark mode, copy-btn (1 template para todos).

## Referencias canonicas

- `.xforge/decisions/ADR-INDEX.md` — indice oficial de DRs (24 DRs)
- `.xforge/decisions/DR-0181-*.md` — este redesign
- `.kilo/rules/00-xforge-rule-index.md` — indice de regras (41 rules)
- `.kilo/core/registries/` — 17 JSONs com fonte da verdade por dominio

---

**Status**: v50.0.0 stable-final-governed | **Loop discipline**: 6/6 PASS | **Ref-count**: 0 dead refs
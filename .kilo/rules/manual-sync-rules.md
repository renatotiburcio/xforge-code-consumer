# manual-sync-rules (DR-0181 - updated 2026-06-21)

Toda mudanca significativa no Engineer DEVE ser verificada contra o manual canonico em `docs/`.

## Manual Canonico Atual (DR-0181, v50.0.0)

```
docs/
|-- README.md            # Landing GitHub
|-- SUMMARY.md           # TOC Markdown
|-- getting-started.md   # Quickstart
|-- index.html           # Entry point visual (Tailwind CDN)
|-- style.css            # CSS compartilhado
|-- script.js            # JS compartilhado (dark + copy-btn)
|-- decisions/README.md  # Stub 12L
`-- manual/              # 11 paginas HTML canonicas
    |-- _template.html
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

## Gatilhos

Apos QUALQUER uma destas acoes, verificar se o manual precisa de atualizacao:

- Novo skill adicionado ou enriquecido
- Novo agent criado ou modificado
- Novo command criado ou modificado
- Regra adicionada ou alterada
- Configuracao mudada (kilo.jsonc, xforge-engineer.config.json)
- Estrutura de diretorios alterada
- Script de automacao modificado ou criado
- Provider adicionado ou removido
- Feature de seguranca implementada
- Bug fix que afeta comportamento documentado
- Migracao ou upgrade realizada
- Novo caso de uso descoberto

## Procedimento

1. Identificar o que mudou
2. Abrir `docs/index.html` (visual) e/ou `docs/SUMMARY.md` (TOC)
3. Verificar se a pagina afetada existe em `docs/manual/`
4. Se a pagina existe -> atualizar com a mudanca
5. Se a pagina nao existe -> criar nova pagina usando `_template.html`
6. Verificar se a mudanca afeta multiplas paginas (atualizar todas)
7. Manter consistencia: mesma nav, mesmo footer, mesmo design system

## Regras de Formatacao do Manual

- Cada pagina DEVE ter: titulo H1, descricao, secoes H2, exemplos em `<code>` ou `<pre>`
- Nav identica em todas as 11 paginas (6 items: Inicio/Quickstart/Arquitetura/Conselho/Skills/Decisoes)
- Footer canonico 3 linhas (titulo, stats, links)
- 1 hero (NAO 2) - apenas em index.html
- Dark mode via `body.dark` (escopo correto)
- Responsive `@media (max-width: 768px)`
- Copy-btn automatico em todos `<pre>` (via script.js)
- Tailwind via CDN
- Total `docs/` < 500 KB

## Validacao Automatica

Apos atualizar o manual, rodar:

```powershell
.\.kilo\automation\scripts\check-manual.ps1
```

Validacoes:
- 1 `<html>`, 1 `<body>`, 1 `<main>`, 1 `<head>`, 1 `<title>` por HTML
- Nav identica (mesmos 6 items)
- Footer canonico (3 linhas)
- Dark mode presente (`body.dark` no CSS)
- 0 referencias mortas no codigo ativo
- Total `docs/` < 500 KB

Exit 0 = clean, 1 = dirty. Integrado ao `doctor.ps1` Gate 4.

## O que NAO documentar

- Alteracoes internas de implementacao sem impacto no usuario
- Fixes de encoding ou BOM
- Renomeacoes de scripts internos
- Mudancas em testes

## Mudanca vs Versao Anterior

- v3.65.0-v3.66.9: 25 paginas HTML com design system quebrado (DR-0156/0158)
- v50.0.0 (DR-0181): 11 paginas HTML + 1 index.html + 1 style.css + 1 script.js, 1 template canonico, validacao automatica

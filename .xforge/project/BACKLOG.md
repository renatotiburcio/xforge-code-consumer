# BACKLOG — Rebrand KiloCode → XForge Code

**Data**: 2026-06-25
**Versao**: 1.0.0
**Epics**: 5 | **Features**: 18 | **Stories**: 42

---

## EPI-001: Brand Abstraction Layer

### Feature 001.1: Single source of truth for brand
**Stories**:
- [ ] Criar `packages/core/src/constants/brand.ts` com BRAND_CONFIG
- [ ] Criar funcoes helper: getCommandPrefix, getConfigPrefix, getHeaderPrefix
- [ ] Adicionar suporte dual-write (XFORGE_CODE + KILOCODE)
- [ ] Unit tests para brand helpers
- [ ] Documentation inline

**Criterios de aceite**:
- Unico arquivo contem todas as brand strings
- Suporta dual-write durante migracao
- 100% unit test coverage

### Feature 001.2: Brand sfotable infrastructure
**Stories**:
- [ ] Criar modulo `packages/core/src/brand/index.ts` public API
- [ ] Integrar brAND_CONFIG em 3+ pacotes
- [ ] Benchmarks performance (brand lookup <1ms)

**Criterios de aceite**:
- Brand lookup e' constant time
- Integrado em core, opencode, kilo-vscode

---

## EPI-002: Package Renaming

### Feature 002.1: npm scope migration
**Stories**:
- [ ] Script de rename para todos os 22 package.json
- [ ] Atualizar root package.json workspace references
- [ ] Atualizar import statements (~500 locais)
- [ ] Atualizar bun.lock (bun install)
- [ ] Atualizar turbo.json pipeline keys
- [ ] Atualizar .github/workflows references

**Criterios de aceite**:
- `bun install` sem erros
- Zero `@kilocode/` references em source code
- Build completo sem erros

### Feature 002.2: Package publishing setup
**Stories**:
- [ ] Criar organizacao `xforge-code` no npm
- [ ] Configurar tokens de publicacao
- [ ] Publicar primeira versao (beta) de cada pacote
- [ ] Verificar pacotes publicados (npm view)

**Criterios de aceite**:
- Todos os 22 pacotes publicados sob `@xforge-code/*`
- npm install Funciona para cada pacote

---

## EPI-003: Extension Rebrand

### Feature 003.1: Extension manifest changes
**Stories**:
- [ ] Atualizar `kilo-vscode/package.json`: name, displayName, publisher
- [ ] Remover `extensionDependencies: ["kilocode.kilo-code"]`
- [ ] Atualizar `activationEvents` para `["*"]`
- [ ] Adicionar `capabilities.virtualWorkspaces: true`
- [ ] Atualizar repository.url, bugs, homepage

**Criterios de aceite**:
- Extension manifest compila
- Sem dependencias de outros extensions
- VS Code carrega extension standalone

### Feature 003.2: Command + settings namespace migration
**Stories**:
- [ ] Script de rename: `kilo-code.new.*` → `xforge-code.new.*`
- [ ] Atualizar ~455 locais de source code
- [ ] Atualizar package.json contributes.commands
- [ ] Atualizar package.json contributes.keybindings
- [ ] Adicionar migration script para settings antigos

**Criterios de aceite**:
- Todos os comandos usam novo prefixo
- Settings antigos migrados automaticamente
- Keybindings preservados

### Feature 003.3: UI strings update
**Stories**:
- [ ] "Add to Kilo Code" → "Add to XForge Code" (e similares)
- [ ] Update extension command titles
- [ ] Update notification messages
- [ ] Update error messages
- [ ] Update system prompts (prompt/*.txt files)

**Criterios de aceite**:
- Zero "Kilo Code" strings visiveis em UI
- Todas as linguas i18n atualizadas

### Feature 003.4: Visual assets
**Stories**:
- [ ] Criar novos icons (activity bar, extension, command)
- [ ] Atualizar `package.json` icon field
- [ ] Atualizar favicons para UI/docs/console
- [ ] Validar icons em 16x16 ate 512x512

**Criterios de aceite**:
- Icons renderizam corretamente em todos os tamanhos
- Sem assets Kilo Code restantes

---

## EPI-004: Template & Documentation

### Feature 004.1: Manual HTML pages
**Stories**:
- [ ] Atualizar 12 paginas do manual (trocar "Kilo Code" → "XForge Code")
- [ ] Atualizar index.html (landing)
- [ ] Atualizar SUMMARY.md
- [ ] Validar HTML (6 sections per page, content checks)
- [ ] Rodar `check-manual.ps1` e `check-manual-content.ps1`

**Criterios de aceite**:
- Todas as 12 paginas validam em doctor
- Manual content >= 25KB total

### Feature 004.2: auto-documenting files
**Stories**:
- [ ] Atualizar AGENTS.md
- [ ] Atualizar CLAUDE.md
- [ ] Atualizar ARCHITECTURE.md
- [ ] Atualizar CHANGELOG.md
- [ ] Atualizar README.md (root)
- [ ] Atualizar .kilo/rules/*.md (brand references)
- [ ] Atualizar .xforge/config/*.json

**Criterios de aceite**:
- Files principais atualizados
- Zero "kilocode" em .md files ativos

### Feature 004.3: i18n
**Stories**:
- [ ] Atualizar locale en todas as chaves
- [ ] Atualizar locale pt-BR
- [ ] Atualizar 14+ outras linguas
- [ ] Adicionar "xfor" como novo codigo de linguagem (se existir)
- [ ] Validar sem linguas faltando

**Criterios de aceite**:
- 16 linguas completas
- Zero missing keys
- Inglês e portugues 100% corretos

### Feature 004.4: Visual identity
**Stories**:
- [ ] Gerar logo assets em todos os formatos necessarios
- [ ] Criar `assets/icons/` com novo icon set
- [ ] Atualizar `social-share.png` e variantes
- [ ] Criar about page com nova identidade
- [ ] Atualizar favicon set completo

**Criterios de aceite**:
- Todos os assets em `packages/xforge-code/assets/`
- Formatos: SVG (vector), PNG (raster), ICO (favicon), ICNS (macOS)

---

## EPI-005: Validation & Release

### Feature 005.1: Build validation
**Stories**:
- [ ] Build compila em Windows
- [ ] Build compila em Linux
- [ ] Build compila em macOS
- [ ] 0 erros, 0 warnings criticos
- [ ] Pipeline CI/CD 100% green (30+ workflows)
- [ ] Type-check (tsgo) sem erros
- [ ] Lint (oxlint) sem erros
- [ ] Tests (bun test) 100% passam

**Criterios de aceite**:
- Build matrix 3 OS passa
- Coverage >= 85%

### Feature 005.2: Migration validation
**Stories**:
- [ ] Migracao settings testada (Kilo Code → XForge Code)
- [ ] Migracao globalStorage testada
- [ ] Migracao MCP servers testada
- [ ] Migracao custom commands testada
- [ ] Migracao skill/action testada
- [ ] Backup restaura em caso de falha

**Criterios de aceite**:
- Dados de usuario preservados 100%
- Migration script reversivel

### Feature 005.3: Release preparation
**Stories**:
- [ ] Version bump 8.0.0
- [ ] CHANGELOG atualizado
- [ ] Migration guide publicado
- [ ] Rollback plan documentado
- [ ] Comunicacao preparada (blog post)
- [ ] Depreciation notice no Kilo Code marketplace

**Criterios de aceite**:
- v8.0.0 published on npm + marketplace
- Migration guide disponivel
- Rollback plan testado

---

## Resumo

| Epic | Features | Stories | Story Points |
|---|---|---|---|
| EPI-001: Brand Abstraction | 2 | 6 | 13 |
| EPI-002: Package Renaming | 2 | 8 | 21 |
| EPI-003: Extension Rebrand | 4 | 16 | 40 |
| EPI-004: Template & Docs | 4 | 12 | 34 |
| EPI-005: Validation & Release | 3 | 10 | 21 |
| **Total** | **16** | **52** | **129** |

---

## Prioridade

1. **P0** (Must have): EPI-001, EPI-002, EPI-003.1, EPI-003.2, EPI-005.1
2. **P1** (Should have): EPI-003.3, EPI-003.4, EPI-004.1, EPI-004.2, EPI-005.2
3. **P2** (Nice to have): EPI-004.3, EPI-004.4

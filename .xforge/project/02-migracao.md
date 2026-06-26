# Plano de Migracao KiloCode → XForge Code

**Data**: 2026-06-25
**Versao**: 1.0.0
**Status**: Draft
**Tipo**: Phased Migration (7 fases)

---

## 1. Visao Geral

O plano de migracao deve ser **incremental** para evitar breaking changes massivos. Cada fase e' independente e reversivel.

| Fase | Nome | Duracao | Breaking? | Escopo |
|---|---|---|---|---|
| F0 | Descoberta e planejamento | 1 semana | N/A | Documentacao |
| F1 | Brand abstraction layer | 2 semanas | Nao | Infra |
| F2 | Package renaming | 1 semana | Sim (dev) | Source code |
| F3 | Extension rebrand | 1 semana | Sim (users) | VS Code |
| F4 | Rebrand template/docs | 1 semana | Nao | .kilo/ + docs/ |
| F5 | Build validation | 1 semana | Nao | CI/CD |
| F6 | Testing + QA | 2 semanas | Nao | Validacao |
| F7 | Release candidate | 1 semana | Nao | Producao |

---

## 2. Fase 0: Descoberta (Completa)

**Status**: COMPLETO

**Entregaveis**:
- [x] Relatorio arquitetural completo
- [x] Matriz de compatibilidade VS Code
- [x] Mapeamento de naming (10K+ ocorrencias)
- [x] Analise de branding assets
- [x] Gap analysis

---

## 3. Fase 1: Brand Abstraction Layer

**Objetivo**: Criar camada de abstracao de branding para centralizar todos os naming references em 1 ponto.

**Tarefas**:

1. **Criar arquivo `BRAND_CONFIG`**:
   - Local: `packages/core/src/constants/brand.ts`
   - Conteudo: `export const BRAND = { prefix: 'xforge-code', prefixOld: 'kilocode', env: 'XFORGE_CODE', header: 'X-XFORGE-CODE', market: 'xforge-code', publisher: 'xforge-code' }`

2. **Criar funcoes helper**:
   - `getCommandPrefix()` → `xforge-code.new.*`
   - `getConfigPrefix()` → `xforge-code.new.*`
   - `getHeadersPrefix()` → `X-XFORGE-CODE-*`
   - `getEnvPrefix()` → `XFORGE_CODE_*`

3. **Dual-write support**:
   - Environment: processar ambos `KILOCODE_*` e `XFORGE_CODE_*`
   - Headers: enviar ambos headers
   - Settings: ler ambos namespaces
   - Commands: registrar ambos (alias)

**Validacao**:
- [ ] BRAND_CONFIG criado
- [ ] Funcoes helper testadas
- [<longcat_arg_value> com dual-write funcionando
- [ ] Unit tests passam

---

## 4. Fase 2: Package Renaming (mono-repo scope)

**Objetivo**: Renomear pacotes npm de `@kilocode/*` para escopo novo.

**IMPORTANTE**: Nao renomear `packages/opencode/` (upstream constraint). O diretorio interno pode manter o nome, mas o package name muda.

**Tarefas**:

1. **Atualizar todos os 22 package.json**:
   - `@kilocode/cli` → `@xforge-code/cli`
   - `@kilocode/sdk` → `@xforge-code/sdk`
   - `@kilocode/plugin` → `@xforge-code/plugin`
   - ... (todos os 22 pacotes)

2. **Atualizar import statements** (~500+ locais):
   - Automated codemod/script
   - Verificar cada `import ... from '@kilocode/...'`

3. **Atualizar bun.lock**:
   - `bun install` regenera automaticamente

4. **Atualizar turbo.json pipeline keys**

5. **Atualizar build scripts references**

6. **Atualizar CI/CD workflows**

**Validacao**:
- [ ] `bun install` sem erros
- [ ] `bun build` sem erros
- [ ] Zero referencias restantes a `@kilocode` em source
- [ ] Tests passam em todos os pacotes

---

## 5. Fase 3: Extension Rebrand (VS Code)

**Objetivo**: Mudar extension ID, commands, e UI strings.

**Tarefas**:

1. **package.json (kilo-vscode)**:
   - `name`: `xforge-code`
   - `displayName`: `XForge Code: Enterprise AI Coding Agent`
   - `publisher`: `xforge-code`
   - `extensionDependencies`: `[]` (remover Kilo Code dependency)
   - `repository.url`: `github.com/xforge-code/xforge-code`

2. **Atualizar comandos** (~455 locais):
   - `kilo-code.new.*` → `xforge-code.new.*`
   - Usar codemod

3. **Atualizar configuracao**:
   - `contributes.configuration.properties`: `xforge-code.new.*`
   - Migracao de settings antigos

4. **Atualizar brand strings**:
   - `"Add to Kilo Code"` → `"Add to XForge Code"`
   - todas as strings visiveis

5. **Criar migration script**:
   - Migrar globalStorage de `kilocode.kilo-code/` para `xforge-code.xforge-code/`
   - Preservar settings antigos por 30 dias

6. **Atualizar assets**:
   - Novos icones (se fornecidos)
   - Novo logo (XForge All)

**Validacao**:
- [ ] Extension compila
- [ ] Registrada no marketplace como novo item
- [ ] Migration testada (dados preservados)
- [ ] UI mostra "XForge Code" em todos os lugares
- [ ] Sem referencias a "Kilo Code" em UI strings

---

## 6. Fase 4: Template Rebrand (.kilo/ + .xforge/)

**Objetivo**: Atualizar template e documentacao.

**Tarefas**:

1. **`.kilo/` directory**: Renomear para `.xforge-code/` (ou manter `.kilo/` como legacy alias)

2. **`.xforge/vscode-extension/`**:
   - Trocar todas as strings "Kilo Code" → "XForge Code"
   - Atualizar `extension.js` literals
   - Atualizar `package.json`

3. **`kilo.jsonc`**: Renomear para `xforge-code.jsonc` (ou manter nome)

4. **Documentacao**:
   - `docs/manual/*.html` — ~12 paginas, trocar todas as referencias
   - `docs/SUMMARY.md`
   - `CHANGELOG.md`
   - `AGENTS.md`
   - `README.md`
   - 16 linguas em `packages/kilo-i18n/`

5. **Knowledge base**:
   - `.xforge/knowledge/**/*` — trocar referencias
   - `.xforge/decisions/**/*` — trocar referencias

6. **Community files** (se existir):
   - `CONTRIBUTING.md`
   - `CODE_OF_CONDUCT.md`
   - GitHub issue templates
   - GitHub discussions setup

**Validacao**:
- [ ] Todas as 12 paginas do manual atualizadas
- [ ] Knowledge base sem referencias a Kilo Code
- [ ] i18n para ingles e portugues corretos
- [ ] Doctor valida nova estrutura

---

## 7. Fase 5: Build Validation

**Objetivo**: Garantir que o build funciona em todos os ambientes.

**Tarefas**:

1. **Build local (Windows/Linux/macOS)**:
   - `bun install` — 0 erros
   - `bun run build` — 0 erros
   - `bun run typecheck` — 0 erros
   - `bun run lint` — 0 erros
   - `bun run test` — 100% pass

2. **CI/CD pipeline**:
   - 30+ workflows passam sem erro
   - Test coverage >= 85%
   - Security audit 0 CVEs criticos
   - CodeQL 0 alertas

3. **Package publishing**:
   - Novo scope `@xforge-code/*` registrado no npm
   - Publicacao teste em staging
   - Token rotation necessario?

4. **Extension publishing**:
   - Novo publisher `xforge-code` no VS Code Marketplace
   - Publish em modo restrito primeiro
   - Validar instalacao em VS Code

5. **CLI binary**:
   - Novo binario `xforge-code` (ou manter `kilo` como alias)
   - Testar em Windows/Linux/macOS
   - Docker images buildam

**Validacao**:
- [ ] Build limpo (0 erros, 0 warnings)
- [ ] CI/CD green
- [ ] Coverage >= 85%
- [ ] Security 0 issues
- [ ] Publicacao em staging

---

## 8. Fase 6: Testing + QA

**Objetivo**: Validacao completa de funcionalidade e migracao.

**Tarefas**:

1. **Unit tests**: 100% passam
2. **Integration tests**: Fluxos principais testados
3. **E2E tests**: Instacao → onboarding → first run
4. **Migration tests**:
   - Instalar Kilo Code → atualizar para XForge Code → dados preservados
   - Settings migrados
   - Sessions preservadas
   - MCP servers configurados
5. **VS Code tests**:
   - Extensao ativa corretamente
   - Comandos funcionam
   - Settings UI funciona
   - Sidebar rendering OK
   - Agent Manager funciona
6. **Performance tests**:
   - Startup time <= Kilo Code
   - Build time <= Kilo Code
   - Extension load time <= 2s

**Validacao**:
- [ ] 100% unit tests passam
- [ ] E2E scenarios passam
- [ ] Migration testada com sucesso
- [ ] Performance equivalent
- [ ] Sem regressao vs Kilo Code

---

## 9. Fase 7: Release Candidate

**Objetivo**: Preparar release para producao.

**Tarefas**:

1. **Versionamento**: `7.3.54` → `8.0.0` (major version bump = breaking rebrand)
2. **CHANGELOG**: Nova entrada para v8.0.0
3. **Migration guide**: Documento de migracao para usuarios
4. **Rollback plan**: Reverter para v7.x se problemas
5. **Comunicacao**: Blog post + release notes + deprecacao Kilo Code no marketplace
6. **Suporte**: Legacy Kilo Code por 90 dias com security fixes
7. **Launch sequence**:
   - Day 0: Publicacao npm (beta)
   - Day 7: Publicacao marketplace (preview)
   - Day 14: Publicacao producao
   - Day 30: Deprecacao Kilo Code
   - Day 90: Descontinuacao Kilo Code

**Validacao**:
- [ ] RC published
- [ ] Migration guide documented
- [ ] Rollback tested
- [ ] Comunicacao preparada
- [ ] 90-day legacy support plan

---

## 10. Dependencias entre Fases

```
F0 (descoberta)
  → F1 (brand abstraction)
    → F2 (package rename) + F3 (extension) [paralelo]
      → F4 (template/docs) + F5 (build) [paralelo]
        → F6 (testing)
          → F7 (release)
```

---

## 11. Riscos e Mitigacao

| Risco | Probabilidade | Impacto | Mitigacao |
|---|---|---|---|
| Fonte upstream merge quebra | Alta | Alto | Manter `kilocode_change` markers, testar merge semanalmente |
| Extension migration perde dados | Media | Critico | Migration script com backup automatico |
| Marketplace rejection | Baixa | Alto | Publicar como novo extension, nao update |
| npm scope conflict | Baixa | Medio | Registrar `@xforge-code` antecipadamente |
| CI/CD pipeline complexidade | Alta | Medio | Testar em staging primeiro |
| Performance regression | Media | Medio | Benchmark automated testing |

---

## 12. KPIs de Sucesso

| KPI | Meta |
|---|---|
| Build errors | 0 |
| Build warnings (critical) | 0 |
| Test pass rate | >= 99% |
| Test coverage | >= 85% |
| Extension load time | <= 2s |
| Migration success rate | >= 99% |
| User-reported issues (first week) | < 50 |

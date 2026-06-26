# XForge Code — Analise Completa do Projeto Kilo Code

**Data**: 2026-06-25
**Versao**: 1.0.0
**Status**: FASE 1 Completa — Imersao e Aquisicao de Conhecimento

---

## 1. Identidade do Projeto

| Campo | Valor |
|---|---|
| **Nome atual** | Kilo Code |
| **Nome alvo** | XForge Code |
| **Tipo** | AI Coding Agent (CLI + VS Code Extension + JetBrains Plugin) |
| **Stack** | TypeScript/Bun monorepo + PowerShell/Python template |
| **Runtime** | Bun 1.3.14 |
| **Bundler** | esbuild (extension), Bun built-in (CLI) |
| **Type checker** | tsgo |
| **Test runner** | bun test |
| **Linter** | oxlint |
| **UI Framework** | SolidJS + OpenTUI |
| **Orquestracao** | Turborepo |
| **Repositorio** | github.com/Kilo-Org/kilocode |
| **Versao CLI** | 7.3.54 |
| **Versao Template** | 50.0.0 |

---

## 2. Estrutura do Monorepo (src/)

### 2.1 Workspaces (22 pacotes)

| Pacote | Escopo npm | Proposito |
|---|---|---|
| `packages/opencode/` | `@kilocode/cli` | Core CLI — agents, tools, sessions, server, TUI |
| `packages/core/` | `@opencode-ai/core` | Dominio central (session, agent, model, provider, config) |
| `packages/kilo-gateway/` | `@kilocode/kilo-gateway` | Auth, provider routing, API integration |
| `packages/kilo-vscode/` | `kilo-code` | VS Code extension + sidebar + Agent Manager |
| `packages/kilo-ui/` | `@kilocode/kilo-ui` | SolidJS component library (40+ componentes) |
| `packages/kilo-telemetry/` | `@kilocode/kilo-telemetry` | PostHog + OpenTelemetry |
| `packages/kilo-i18n/` | `@kilocode/kilo-i18n` | 16 linguas |
| `packages/kilo-docs/` | `@kilocode/kilo-docs` | Next.js documentation site |
| `packages/kilo-indexing/` | `@kilocode/kilo-indexing` | Codebase indexing (LanceDB) |
| `packages/kilo-sandbox/` | `@kilocode/sandbox` | Sandbox execution environment |
| `packages/kilo-console/` | `@kilocode/kilo-console` | Console UI |
| `packages/kilo-web-ui/` | `@kilocode/kilo-web-ui` | Web UI |
| `packages/kilo-jetbrains/` | `@kilocode/kilo-jetbrains` | JetBrains plugin |
| `packages/sdk/js/` | `@kilocode/sdk` | Auto-generated TypeScript SDK |
| `packages/plugin/` | `@kilocode/plugin` | Plugin/tool interface definitions |
| `packages/plugin-atomic-chat/` | `@kilocode/plugin-atomic-chat` | Atomic chat plugin |
| `packages/ui/` | `@opencode-ai/ui` | Shared UI primitives |
| `packages/script/` | `@opencode-ai/script` | Build/publish scripts |
| `packages/llm/` | `@opencode-ai/llm` | LLM utilities |
| `packages/http-recorder/` | `@opencode-ai/http-recorder` | HTTP recording/replaying |
| `packages/effect-drizzle-sqlite/` | — | Drizzle ORM + SQLite |
| `packages/storybook/` | — | Storybook for UI development |

### 2.2 Dependencias Internas

```
@kilocode/cli (opencode)
  ├── @opencode-ai/core
  ├── @kilocode/kilo-gateway
  ├── @kilocode/kilo-indexing
  ├── @kilocode/kilo-telemetry
  ├── @kilocode/plugin
  ├── @kilocode/plugin-atomic-chat
  ├── @kilocode/sandbox
  ├── @kilocode/sdk
  ├── @opencode-ai/script
  ├── @opencode-ai/ui
  └── @opencode-ai/llm

kilo-vscode
  ├── @kilocode/kilo-gateway
  ├── @kilocode/kilo-i18n
  ├── @kilocode/kilo-indexing
  ├── @kilocode/kilo-ui
  ├── @kilocode/plugin
  ├── @kilocode/sdk
  ├── @opencode-ai/ui
  └── @pierre/diffs
```

### 2.3 Padroes Arquiteturais

1. **Namespace modules** — Codigo organizado como TypeScript namespaces com Zod schemas
2. **`Instance.state(init, dispose?)`** — Per-project lazy singleton via AsyncLocalStorage
3. **`fn(schema, callback)`** — Wrapper com Zod input validation
4. **`Tool.define(id, init)`** — Pattern para todas as ferramentas
5. **`BusEvent.define(type, schema)` + `Bus.publish()`** — In-process pub/sub
6. **Effect system** — Functional effects para DI, state management, error handling
7. **Kilo-specific isolation** — Kilo code em `kilocode/` directories; upstream usa `kilocode_change` markers

---

## 3. Build System

### 3.1 Comandos Principais

| Comando | Proposito |
|---|---|
| `bun run build` (CLI) | Build CLI binary |
| `bun run typecheck` | Type-check (tsgo) |
| `bun run lint` | Lint (oxlint) |
| `bun run test` (per-package) | Run tests |
| `bun run extension` | Build + launch VS Code with extension |
| `bun turbo typecheck` | Type-check entire monorepo |

### 3.2 CI/CD (GitHub Actions)

| Workflow | Trigger | Proposito |
|---|---|---|
| `test.yml` | Push/PR | Unit tests (Linux/macOS/Windows) |
| `test-vscode.yml` | PR | VS Code extension tests |
| `publish.yml` | Manual | Build + publish to marketplace + npm |
| `typecheck.yml` | PR | TypeScript type checking |
| `codeql.yml` | PR | CodeQL security analysis |
| `xforge.yml` | Push/PR | Template validation (doctor.ps1) |
| `ci.yml` | Push/PR | 6-phase pipeline (validate→build→security→docker→staging→prod) |

### 3.3 Build Outputs

| Artefato | Path |
|---|---|
| CLI binary | `packages/opencode/dist/*/bin/kilo` |
| VS Code extension | `packages/kilo-vscode/dist/extension.js` |
| Webview bundle | `packages/kilo-vscode/dist/webview.js` |
| Agent Manager | `packages/kilo-vscode/dist/agent-manager.js` |

---

## 4. VS Code Extension — Analise de Compatibilidade

### 4.1 APIs Utilizadas

| Modulo | Uso |
|---|---|
| `vscode.window` | `createOutputChannel`, `showInformationMessage`, `showInputBox` |
| `vscode.commands` | `registerCommand` — 9 comandos registrados |
| `vscode.workspace` | `getConfiguration("xforge")` |

### 4.2 Command Prefix

O VS Code extension usa prefixo `kilo-code.new.*` em ~455+ localizacoes.

### 4.3 Extension ID

- **Atual**: `kilocode.kilo-code`
- **Publisher**: `kilocode`
- **Display Name**: "Kilo Code: AI Coding Agent, Copilot, and Autocomplete"
- **Activation**: `workspaceContains:.xforge`
- **Dependencies**: `kilocode.kilo-code` (XForge extension depende do Kilo Code)

### 4.4 Config Section

Toda a configuracao do VS Code usa namespace `kilo-code.new.*` (fontSize, autocomplete, browserAutomation, autoApprove, attention, indexing).

---

## 5. Rebranding Surface

### 5.1 Estatisticas

| Padrao | Ocorrencias |
|---|---|
| `kilocode` (case-insensitive) | ~10,905 |
| `KiloCode` | ~1,043 |
| `Kilo Code` | ~2,106 |
| `@kilocode` em package.json | 45 |
| `kilo-code` | ~645 |
| `@kilocode/cli` | ~213 |
| `opencode` | ~4,593 |
| `kilocode_change` markers | ~3,990 |
| `ai.kilocode` (Kotlin namespace) | ~2,990 |

### 5.2 Categorias de Mudanca

| Categoria | Risco | Esforco |
|---|---|---|
| npm scope `@kilocode/*` | CRITICAL | Muito Alto |
| VS Code extension ID | CRITICAL | Alto |
| VS Code command prefix | HIGH | Alto |
| VS Code settings namespace | HIGH | Medio |
| Kotlin namespace | HIGH | Muito Alto |
| HTTP headers `X-KILOCODE-*` | HIGH | Medio |
| Env vars `KILOCODE_*` | MEDIUM | Medio |
| `kilocode_change` markers | MEDIO | Alto (NAO mudar) |
| CLI binary name `kilo` | MEDIUM | Medio |
| Template docs | LOW | Medio |

### 5.3 Assets Visuais

| Asset | Local | Formato |
|---|---|---|
| Logo XForge | `implement/logo/XForge All.svg` | SVG/PNG/ICNS |
| Logo Kilo Code | `src/logo.png` | PNG |
| Extension icon | `src/packages/kilo-vscode/assets/icons/logo-outline-black.png` | PNG |
| Activity bar icons | `src/packages/kilo-vscode/assets/icons/kilo-{light,dark}.png` | PNG |
| Icon font | `src/packages/kilo-vscode/assets/icons/kilo-icon-font.woff2` | WOFF2 |
| Favicons | `src/packages/ui/src/assets/favicon/*` | ICO/SVG/PNG |
| Social share | `src/packages/ui/src/assets/images/social-share*.png` | PNG |

---

## 6. Template XForge (.kilo/ + .xforge/)

### 6.1 Estrutura Canonica

```
.kilo/
  commands/          # Comandos do Kilo Code CLI
  agent/             # Agentes especializados
  rules/             # Regras de engenharia
  skills/            # Skills especializados
  automation/        # Scripts PowerShell/Python
  workflows/         # Workflows FSM
  knowledge/         # Base de conhecimento
  memory/            # Sistema de memoria
  decisions/         # Decision Records
  rag/               # RAG index

.xforge/
  config/            # Configuracao do engine
  knowledge/         # Knowledge packs
  decisions/         # ADRs
  docs/              # Documentacao
  scripts/           # Automacoes
  project/           # Documentacao de projeto
  autoresearch/       # Loop de experimentos
  feedback/          # Error/solution graph
  audit/             # Trilha de auditoria
```

### 6.2 Scripts de Automacao (30+ scripts)

| Script | Proposito |
|---|---|
| `doctor.ps1` | Health check master |
| `score.ps1` | XForge Score (xfs) — imutavel |
| `pre-commit.ps1` | Quality gate |
| `validate-kilo-strict.ps1` | Valida kilo.jsonc |
| `validate-engineer.ps1` | Valida estrutura do template |
| `dependency-check.ps1` | Scanner de vulnerabilidades |
| `security-audit.py` | Scanner de secrets |
| `proactive-intelligence.ps1` | Deteccao de padroes de erro |
| `rag_local.py` | RAG index/query/status |
| `automation-engine.py` | Entry point de automacao |
| `generate-release-package.ps1` | Cria pacote distributable |

---

## 7. Referencia VS Code (referencia/vscode/)

- **Versao**: VS Code 1.127.0 (Code - OSS)
- **Estrutura completa**: src/vs/ (base, platform, editor, workbench, sessions, code, server)
- **Extensions**: ~100+ built-in extensions
- **API**: vscode.d.ts (stable) + vscode.proposed.*.d.ts (200+ proposed APIs)
- **Layers**: base → platform → editor → workbench → sessions (one-way dependencies)
- **New**: `src/vs/sessions/` — Agents Window (new agentic workbench layer)

---

## 8. Descobertas Criticas

1. **O projeto ja e' um fork evoluido**: O Kilo Code ja divergiu significativamente do OpenCode original. O XForge e' mais uma camada de evolucao.

2. **Dual branding existe**: "Kilo Code" (upstream open-source) vs "XForge" (enterprise layer). O rebrand unifica essas marcas.

3. **Extension dependency critica**: A extensao XForge depende da extensao Kilo Code (`extensionDependencies: ["kilocode.kilo-code"]`). No rebrand completo, isso deve ser invertido ou eliminado.

4. **10K+ mudancas de naming**: O esforco de rebranding e' massivo. Nao deve ser big-bang.

5. **Upstream merge constraint**: O `packages/opencode/` e' fork de `anomalyco/opencode`. Renomearia quebra o merge tooling.

6. **3,990 `kilocode_change` markers**: Infraestrutura critica de sync com upstream. NAO mudar.

---

## 9. Proximos Passos

1. **FASE 2** — Analise profunda do VS Code (APIs, contribution points, extension host)
2. **FASE 3** — Plano de rebranding detalhado (phased migration)
3. **FASE 4** — Plano de refatoracao estrutural
4. **FASE 5** — Validacao de build
5. **FASE 6** — Plano de testes
6. **FASE 7** — Documentacao final

---

## 10. Artefatos Gerados

| Artefato | Local |
|---|---|
| Este documento | `.xforge/project/00-arquitetura.md` |
| Matriz de compatibilidade | `.xforge/project/01-compatibilidade.md` |
| Plano de migracao | `.xforge/project/02-migracao.md` |
| Plano de rebranding | `.xforge/project/03-rebranding.md` |
| Backlog | `BACKLOG.md` |
| Roadmap | `ROADMAP.md` |
| ADRs | `.xforge/decisions/` |

# Getting Started - XForge v50.0.0

> **Tempo estimado**: 5 min para rodar, 30 min para dominar.

## Pre-requisitos

- Git 2.40+
- PowerShell 5.1+ (Windows) ou bash (Linux/Mac)
- 16 GB RAM minimo (32 GB recomendado para AI local)
- GPU NVIDIA 16 GB VRAM (opcional, para Ollama local)
- XForge Code CLI 1.0+ ou Claude Code (VS Code extension)

## Instalacao (3 passos)

### Passo 1 — Clonar

```bash
git clone https://github.com/renatotiburcio/xforge.git
cd xforge
```

### Passo 2 — Inicializar

```bash
# Windows
.\.kilo\automation\scripts\xforge-init.ps1

# Linux/Mac (via PowerShell Core)
pwsh ./.kilo/automation/scripts/xforge-init.ps1
```

Saida esperada: stack detectado, project-dna gerado, knowledge INDEX validado.

### Passo 3 — Primeiro Comando

Abra VS Code com XForge Code CLI ou Claude Code e rode:

```
/quickstart
```

## Estrutura (5 min para entender)

```
xforge/
|-- .kilo/              # Operacional (skills/agents/commands/rules) — NAO MEXER
|-- .xforge/            # Runtime (knowledge/decisions/memory) — pode evoluir
|-- docs/               # Manual canonico (este arquivo)
|-- kilo.jsonc          # Config XForgeCode CLI
|-- AGENTS.md           # Instrucoes para AI agents
|-- ARCHITECTURE.md     # Visao arquitetural
|-- CLAUDE.md           # Alias para Claude Code
|-- README.md           # Landing GitHub
|-- CHANGELOG.md        # Release history (immutable per DR-0087)
`-- STATUS.md           # Status master
```

## Decisao nao-trivial? Use o Conselho dos Genios

Qualquer decisao arquitetural, seguranca, UX, produto, refactor, breaking change:

```
# 1. Abrir conselho
/genius-council

# 2. Dar contexto
/topico: "escolha entre X e Y para resolver Z"

# 3. Receber DR
# (automatico, salvo em .xforge/decisions/DR-XXXX-titulo.md)
```

Mais detalhes: `docs/manual/03-gcf.html`.

## Stack Detection (DR-0180)

XForge detecta seu stack via sinais:

| Sinal | Stack |
|---|---|
| `*.csproj`, `*.sln` | .NET |
| `package.json` | Node |
| `pyproject.toml`, `requirements.txt` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `angular.json` | Angular |
| `next.config.*` | Next.js |
| `*.html` standalone | HTML+Tailwind |

Knowledge entries com `applicabilityScope: ["dotnet"]` so serao carregadas em projetos .NET.

## Proximos passos

1. Leia `docs/manual/02-architecture.html` (10 min)
2. Rode `/xforge-health-check` para validar setup
3. Crie seu primeiro projeto: `/create-dotnet-project` (ou equivalente do seu stack)
4. Para decisoes arquiteturais: `/genius-council`

## Suporte

- Issues: https://github.com/renatotiburcio/xforge/issues
- Docs: `docs/index.html` (visual) ou este arquivo (MD)
- DRs: `.xforge/decisions/ADR-INDEX.md`
- Rules: `.kilo/rules/00-xforge-rule-index.md`

---

**Versao**: v50.0.0 | **Status**: stable-final-governed | **Loop discipline**: 6/6 PASS
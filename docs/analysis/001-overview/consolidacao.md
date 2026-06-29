# Consolidação — Visão Geral dos 10 Projetos

## Tabela Comparativa

| Projeto | Tipo | Linguagem | Licença | Status | Versão |
|---------|------|-----------|---------|--------|--------|
| Kilo Code | VS Code + CLI + JetBrains | TypeScript | MIT | Ativo | 7.3.54 |
| Cline | VS Code + CLI + JetBrains | TypeScript | Apache 2.0 | Ativo | — |
| Continue | VS Code + CLI + JetBrains | TypeScript | Apache 2.0 | Read-only | 2.0.0 |
| Goose | Desktop + CLI + API | Rust | Apache 2.0 | Ativo (AAIF) | — |
| Roo-Code | VS Code | TypeScript | Apache 2.0 | Descontinuado | — |
| Aider | CLI | Python | Apache 2.0 | Ativo | — |
| OpenHands | Web App + Backend | Python | MIT | Ativo | — |
| Twinny | VS Code | TypeScript | MIT | Ativo | 3.23.31 |
| MiMo-Code | VS Code | TypeScript | — | Ativo | — |
| OpenCode | CLI/TUI | TypeScript | MIT | Arquivado | — |

## O que cada projeto faz de melhor

### Kilo Code
- Agent Manager com worktree isolation
- 500+ modelos LLM
- 5 agentes especializados (Code, Plan, Ask, Debug, Review)
- MCP marketplace
- Autonomous mode para CI/CD

### Cline
- Checkpoint/restore com estado completo
- Multi-agent teams com persistência
- Scheduled agents (cron jobs)
- Messaging integration (Telegram, Slack, Discord)
- SDK programático com plugins

### Continue
- @context system (@file, @folder, @codebase, @docs)
- RAG local com SQLite
- Inline autocomplete inteligente
- Pioneiro em open-source coding agents

### Goose
- MCP-first architecture (70+ extensões)
- Escrito em Rust (performance)
- Desktop app + CLI + API
- Custom distributions
- Linux Foundation (AAIF)

### Roo-Code
- Sistema de múltiplos modos (Code, Architect, Ask, Debug, Custom)
- Tools especializadas por modo
- Mode detection automático

### Aider
- Git-native workflow
- Repo mapping automático
- Pair programming
- Prompt caching

### OpenHands
- Sandbox Docker para execução segura
- Event-driven architecture
- Web UI acessível
- Planner integrado

### Twinny
- Local-first (Ollama)
- Minimalista e leve
- Máxima privacidade

### MiMo-Code
- Leve e rápido
- Multi-provedor

### OpenCode
- Single-binary
- TUI minimalista
- Rápido

## Padrões Comuns

1. **Tool-Calling Loop** — Todos usam loop de ferramentas
2. **Multi-provedor** — Quase todos suportam múltiplos LLMs
3. **VS Code Extension** — 7 de 10 são extensões VS Code
4. **Git integration** — Integração com git é comum
5. **Rules/AGENTS.md** — Permitem regras de projeto

## Padrões Divergentes

1. **Multi-agentes** — Apenas Kilo Code e Cline
2. **MCP** — Kilo Code, Cline, Goose, Roo-Code
3. **RAG** — Kilo Code (Qdrant), Continue (SQLite), Aider (repo map)
4. **Compactação** — Apenas Kilo Code
5. **Desktop app** — Apenas Goose
6. **Web app** — Apenas OpenHands

## Lacunas — O que NENHUM projeto faz

1. Multi-perspectiva AI (Genius Council)
2. Self-healing automático
3. Living knowledge com TTL
4. Decision records automáticos
5. Stack-agnostic
6. Per-directory rules
7. Error learning entre sessões
8. Memory namespace isolation
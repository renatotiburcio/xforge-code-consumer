# Consolidação — Sistema de Chat dos 10 Projetos

## Tabela Comparativa

| Projeto | UI | Streaming | Multi-sessão | Diff Review |
|---------|----|-----------|--------------|-------------|
| Kilo Code | Webview (SolidJS) | ✅ SSE | ✅ Agent Manager | ✅ |
| Cline | Webview (React) | ❌ | ❌ | ✅ |
| Continue | Webview (React) | ❌ | ❌ | ❌ |
| Goose | Desktop + TUI | ✅ | ❌ | ❌ |
| Roo-Code | Webview (React) | ❌ | ❌ | ❌ |
| Aider | Terminal | ❌ | ❌ | ✅ Git diff |
| OpenHands | Web UI (React) | ✅ WebSocket | ❌ | ❌ |
| Twinny | Webview | ❌ | ❌ | ❌ |
| MiMo-Code | Webview | ❌ | ❌ | ❌ |
| OpenCode | TUI | ❌ | ❌ | ❌ |

## Funcionalidades Únicas

| Projeto | Funcionalidade Única |
|---------|----------------------|
| Kilo Code | Agent Manager com worktree isolation |
| Cline | Diff review com accept/reject/modify |
| Continue | @context system no chat |
| Goose | Desktop app + system tray |
| OpenHands | Streaming via WebSocket |

## Stacks de UI

| Stack | Projetos |
|-------|----------|
| React | Cline, Continue, Goose, Roo-Code, OpenHands |
| SolidJS | Kilo Code |
| Electron | Goose |
| Terminal | Aider, OpenCode |

## Oportunidades para o XForge

1. Agent Manager (inspirado em Kilo Code)
2. Diff review (inspirado em Cline)
3. @context system (inspirado em Continue)
4. Streaming via SSE/WebSocket
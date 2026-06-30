---
id: references-rule
priority: critical
applicabilityScope: ["*"]
status: approved
version: 1.0.0
created: 2026-06-30
updated: 2026-06-30
---

# Regra de Ouro — Consultar Referencias Primeiro

> **obrigatorio**: Antes de implementar QUALQUER funcionalidade, analise TODAS as referencias na pasta `ref/` (Kilocode, Twinny, OpenHands, Roo-Code, xforge-code-template). Elas ja possuem tempo de experiencia e usuarios em producao.

## Referencias disponiveis

- **`ref/kilocode`** — Maior referenciado,Arquitetura completa com React/TanStack, session management, provider switching, slash commands, tools
- **`ref/twinny`** — Focado em Ollama/local models, sessoes simples, comunicacao webview
- **`ref/opencode`** — Opencode CLI com AI providers, session persistence, streaming
- **`ref/openhands`** — OpenHands com tools diferentes, session history
- **`ref/aider`** — Aider code chat, git integration, session resume
- **`ref/Roo-Code`** — Roo code com tool calls, session management
- **`ref/xforge-code-template`** — Template XForge original, arquitetura base

## Procedimento

1. Antes de implementar, identifique a funcionalidade equivalente nas referencias
2. Analise a estrutura: como persistem dados, como comunicam webview<->provider, como gerenciam estado
3. Copie a FUNDAMENTACAO (estrutura, padroes, APIs) da melhor referencia
4. Adapte ao XForge apenas onde necessario
5. Mantenha compatibilidade com APIs existentes das referencias quando possivel

## Quando consultar cada referencia

| Funcionalidade | Referencia primaria | Por que |
|---|---|---|
| Session management | Kilocode | Mais completo, SessionProvider com provider/provider-resolver |
| Webview<->Provider comm | Kilocode | use-extension-state, messages tipados |
| Session persistence (salvar/resumar) | Twinny | Persistencia em arquivo local |
| Provider switching (OpenAI/Anthropic/Ollama) | Kilocode | createProvider com fallback chain |
| Streaming response | Kilocode | StreamingController, abortable |
| UI Components (React) | Kilocode | shadcn/ui com Tailwind, componente reutilizaveis |
| Tool execution | Aider/Roo-Code | Ferramentas locais, permissoes |
| Multi-provider | Kilocode | ProviderList, BaseProvider |
| Message types | Kilocode | ExtensionMessage, ProviderMessage enums |

## Regra de Ouro

SE referencia tem a funcionalidade → copiar fundamentacao.
SE Nao existe em referencia → criar do zero com funcionalidades aprendidas das referencias.

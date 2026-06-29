# Goose

## O que é

Goose é um agente AI open-source (Apache 2.0) escrito em Rust. Funciona como app desktop (Electron), CLI, e API. MCP-first architecture com 70+ extensões e 15+ provedores LLM. Agora é parte da Agentic AI Foundation (AAIF) na Linux Foundation.

## Qual objetivo

Fornecer um agente AI general-purpose que roda na máquina do usuário — não apenas para código, mas para pesquisa, escrita, automação, e análise de dados.

## Como funciona

\\\mermaid
flowchart TD
    U[Usuário] -->|prompt| APP[Desktop App / CLI]
    APP -->|conecta| SRV[goose-server\ncrates/goose-server]
    SRV -->|carrega| AG[Agente\ncrates/goose]
    AG -->|usa| MCP[MCP Extensions\ncrates/goose-mcp\n70+ servers]
    AG -->|chama| PRV[15+ Providers\nAnthropic/OpenAI/Google/Ollama/etc]
    AG -->|executa| CLI[CLI Entry\ncrates/goose-cli]
    APP -->|UI| DESK[Electron App\nui/desktop]
    SRV -->|responde| APP
    APP --> U
\\\

## Estrutura do Projeto (Rust)

| Crate | Propósito |
|-------|-----------|
| goose | Core logic — agente, tools, providers |
| goose-cli | Entry point CLI |
| goose-server | Backend server (binary: goosed) |
| goose-mcp | Extensões MCP (70+ servers) |
| goose-acp-macros | Proc macros para ACP |
| goose-test | Utilitários de teste |
| goose-test-support | Suporte a testes |
| ui/desktop | App Electron |

## Funcionalidades Principais

1. **MCP-first**: 70+ extensões MCP
2. **15+ providers**: Anthropic, OpenAI, Google, Ollama, OpenRouter, Azure, Bedrock
3. **Desktop app**: Electron para macOS, Linux, Windows
4. **CLI**: Terminal interface completa
5. **API**: Embedding em qualquer aplicação
6. **ACP providers**: Claude, ChatGPT, Gemini subscriptions
7. **Custom distributions**: Build your own distro

## Pontos Fortes

1. **MCP-first**: Arquitetura centrada em ferramentas externas
2. **Rust**: Performance e portabilidade
3. **70+ extensões**: Ecossistema MCP rico
4. **Multi-plataforma**: Desktop + CLI + API
5. **Linux Foundation**: Governança aberta

## Limitações

1. **Sem multi-agentes**: Apenas um agente por tarefa
2. **Sem compactação**: Contexto limitado
3. **Sem memória**: Sem persistência entre sessões
4. **Sem error learning**: Sem rastreamento de erros

## Oportunidades para o XForge

1. MCP-first architecture é modelo excelente
2. Rust performance pode inspirar implementação
3. Custom distributions = template system
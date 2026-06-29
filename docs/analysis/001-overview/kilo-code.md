# Kilo Code

## O que é

Kilo Code é um agente de código AI open-source que funciona noBrains e CLI. É um fork do OpenCode aprimorado com sistema de agentes especializados, Agent Manager multi-sessão, 500+ modelos LLM, e suporte a MCP. Versão atual: 7.3.54.

## Qual objetivo

Substituir o desenvolvimento manual por um agente inteligente que entende o contexto do projeto, executa ferramentas, coordena agentes especializados, e aprende com o usuário.

## Como funciona

\\\mermaid
flowchart TD
    U[Usuário] -->|prompt| PROD[VS Code / JetBrains / CLI]
    PROD -->|conecta| GATE[Kilo Gateway\n/kilo-gateway]
    GATE -->|roteia| CLI[Kilo CLI\npackages/opencode]
    CLI -->|gerencia| AM[Agent Manager\npackages/kilo-vscode]
    AM -->|cria| AG[Agente Especializado]
    AG -->|usa| TOOLS[Tools: read/write/bash/edit]
    AG -->|consulta| IDX[Indexing\npackages/kilo-indexing]
    AG -->|chama| LLM[500+ Models\npackages/llm]
    AG -->|verifica| CHK[Self-check]
    AG -->|responde| PROD
    PROD --> U
\\\

## Fluxo Interno

\\\mermaid
sequenceDiagram
    participant U as Usuário
    participant PROD as Produto
    participant GATE as Kilo Gateway
    participant CLI as Kilo CLI
    participant AM as Agent Manager
    participant AG as Agente
    participant LLM as LLM
    
    U->>PROD: Prompt
    PROD->>GATE: Autentica + roteia
    GATE->>CLI: Encaminha
    CLI->>AM: Cria sessão
    AM->>AG: Instancia agente
    loop Tool-calling loop
        AG->>LLM: Prompt + tools
        LLM-->>AG: Tool call
        AG->>AG: Executa tool
        AG->>LLM: Resultado
    end
    AG-->>U: Resposta
\\\

## Dependências Principais

### Monorepo (Turborepo + Bun workspaces)
| Package | Nome | Propósito |
|---------|------|-----------|
| packages/opencode/ | @kilocode/cli | Core CLI — agentes, tools, sessões, server, TUI |
| packages/sdk/js/ | @kilocode/sdk | SDK TypeScript auto-gerado |
| packages/kilo-vscode/ | kilo-code | Extensão VS Code + Agent Manager |
| packages/kilo-gateway/ | @kilocode/kilo-gateway | Auth, provider routing, API |
| packages/kilo-telemetry/ | @kilocode/kilo-telemetry | PostHog + OpenTelemetry |
| packages/kilo-i18n/ | @kilocode/kilo-i18n | Internacionalização |
| packages/kilo-ui/ | @kilocode/kilo-ui | Componentes SolidJS |
| packages/kilo-indexing/ | — | Indexação RAG (Qdrant) |
| packages/kilo-docs/ | — | Site de documentação |
| packages/kilo-jetbrains/ | — | Plugin JetBrains |
| packages/kilo-sandbox/ | — | Sandbox de execução |
| packages/llm/ | — | Integração 500+ modelos |
| packages/plugin/ | @kilocode/plugin | Interface de plugins |

### Dependências externas
- Bun runtime
- TypeScript 5.x
- Turborepo
- Qdrant (vector store)
ama (embeddings locais)
- PostHog (telemetria)
- SolidJS (UI)

## Agentes Especializados

| Agente | Descrição |
|--------|-----------|
| **Code** | Padrão. Implementa e edita código |
| **Plan** | Projeta arquitetura e escreve planos de implementação |
| **Ask** | Responde perguntas sem tocar arquivos |
| **Debug** | Soluciona problemas e rastreia issues |
| **Review** | Revisa mudanças (performance, segurança, estilo, testes) |

## Funcionalidades Principais

1. **Code generation** — Geração de código a partir de linguagem natural
2. **Inline autocomplete** — Sugestões ghost-text com tab para aceitar
3. **Self-checking** — Agente revisa e corrige seu próprio trabalho
4. **Terminal e browser control** — Executa comandos e automatiza web
5. **MCP marketplace** — Marketplace de servidores MCP
6. **500+ models** — Troca de modelo mid-task
7. **Autonomous Mode** — kilo run --auto para CI/CD
8. **Agent Manager** — Painel multi-sessão com git worktree isolation
9. **Code Reviews** — Revisão automática de PRs

## Pontos Fortes

1. **Multi-agentes**: 5 agentes especializados + custom agents
2. **Multi-plataforma**: VS Code + JetBrains + CLI + Cloud
3. **500+ modelos**: Flexibilidade total de provedor
4. **Agent Manager**: Orquestração multi-sessão com worktrees
5. **MCP marketplace**: Ecossistema extensível
6. **Self-checking**: Auto-revisão de código
7. **Autonomous mode**: CI/CD sem intervenção humana
8. **Open source**: MIT license

## Limitações

1. **Sem sandbox nativo**: Depende de kilo-sandbox separado
2. **Sem per-directory rules**: AGENTS.md apenas no root
3. **Sem error learning**: Erros não são rastreados entre sessões
4. **Sem memory namespace**: Memória não isolada por projeto
5. **Sem decision records**: Sem documentação automática de decisões
6. **Acoplamento VS Code**: Extensão fortemente acoplada ao CLI

## Oportunidades para o XForge

1. **Genius Council**: Nenhum projeto tem debate multi-perspectiva
2. **Per-directory AGENTS.md**: Monorepo support
3. **Error pattern learning**: Rastreamento de erros entre sessões
4. **Memory namespace isolation**: LGPD compliance
5. **Decision records**: Documentação automática
6. **Self-healing**: Auto-correção de erros comuns
# Cline

## O que é

Cline é um agente de código AI open-source que funciona como extensão para VS Code, plugin JetBrains, CLI, e Kanban web. Diferencial: checkpoint/restore, multi-agent teams, scheduled agents, e SDK programático. Apache 2.0.

## Qual objetivo

Automatizar desenvolvimento através de um agente que lê estrutura do projeto, executa comandos, edita código com diffs revisáveis, e coordena multi-agentes.

## Como funciona

\\\mermaid
flowchart TD
    U[Usuário] -->|prompt| PROD[VS Code / JetBrains / CLI / Kanban]
    PROD -->|ativa| CORE[Cline Core]
    CORE -->|loop| LLM[LLM via Provider]
    LLM -->|tool call| TOOLS[Tools: read/write/bash/browser]
    TOOLS -->|resultado| LLM
    LLM -->|response| CORE
    CORE -->|diff| PROD
    PROD -->|aprovação| U
    CORE -->|salK[Checkpoint]
\\\

## Fluxo Interno

\\\mermaid
sequenceDiagram
    participant U as Us PROD as Produto
    participant CORE as Cline Core
    participant LLM as LLM
    participant TL as Tools
    participant CHK as Checkpoint

    U->>PROD: Prompt
    PROD->>CORE: Inicia agente
    loop Tool-calling
        CORE->>LLM: Context + tools
        LLM-->>CORE: Tool call
        CORE->>TL: Executa
        TL-->>CORE: Resultado
        CORE->>CHK: Salva checkpoint
        CORE->>LLM: Resultado
    end
    CORE-->>U: Resposta + diffs
\\\

## Produtos

| Produto               | Localização  | Descrição                              |
| --------------------- | ------------ | -------------------------------------- |
| **SDK**               | sdk/         | API Node.js para agentes programáticos |
| **CLI**               | pps/cli/    | Terminal UI, headless mode             |
| **VS Code Extension** | raiz         | Extensão Marketplace                   |
| **JetBrains Plugin**  | fechado      | Plugin IntelliJ/PyCharm/WebStorm       |
| **Kanban**            | cline/kanban | Multi-agent task board com worktrees   |
| **Docs**              | docs/        | Documentação pública                   |

## Funcionalidades Principais

1. **Plan and Act modes** — Planeja antes de executar
2. **Human-in-the-loop** — Aprovação de cada mudança
3. **Checkpoints** — Save/restore de estado
4. **Multi-agent teams** — Coordenação de agentes especialistas
5. **Scheduled agents** — Cron jobs para automação
6. **Messaging integration** — Telegram, Slack, Discord, WhatsApp, Linear
7. **Headless CLI** — CI/CD com JSON output
8. **Rules e Skills** — .clinerules + skills carregáveis
9. **MCP support** — Servidores MCP externos
10. **SDK programático** — Plugins e custom tools

## Pontos Fortes

1. **Checkpoint/restore**: Estado completo para retomada
2. **Multi-agent teams**: Coordenação com persistência
3. **Scheduled agents**: Automação recorrente
4**: Integração com 5+ plataformas
4. **SDK programático**: Extensibilidade total
5. **Diff review**: Cada mudança revisável
6. **Multi-provedor**: 10+ provedores LLM

## Limitações

1. **Sem compactação**: Contexto limitado
2. **Sem memória entre sessões**: Sem aprendizado
3. **Sem per-directory rules**: Regras globais
4. **Sem error learning**: Sem rastreamento de erros
5. **JetBrains fechado**: Plugin não open-source

## Oportunidades para o XForge

1. com estado completo
2. Multi-agent teams para tarefas complexas
3. Scheduled agents para automação
4. Messaging integration (Slack, Telegram)

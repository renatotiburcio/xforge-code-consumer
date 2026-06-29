# Roo-Code

## O que é

Roo-Code é um agente de código AI como extensão VS Code. Diferencial: sistema de múltiplos modos (Code, Architect, Ask, Debug, Custom) com ferramentas específicas por modo. Foi descontinuado em 15 de maio de 2026. Apache 2.0.

## Qual objetivo

Fornecer diferentes comportamentos de agente dependendo do tipo de tarefa, com ferramentas especializadas por modo e MCP support.

## Como funciona

\\\mermaid
flowchart TD
    U[Usuário] -->|prompt + modo| EXT[VS Code Extension]
    EXT -->|detecta| MD[Mode Detector]
    MD -->|architect| AG_A[Agent Architect]
    MD -->|code| AG_C[Agent Code]
    MD -->|ask| AG_K[Agent Ask]
    MD -->|debug| AG_D[Agent Debug]
    MD -->|custom| AG_U[Agent Custom]
    AG_A -->|usa| TOOLS_A[Tools: plan, search, write]
    AG_C -->|usa| TOOLS_C[Tools: read, write, edit, bash]
    AG_K -->|usa| TOOLS_K[Tools: search, read]
    AG_D -->|usa| TOOLS_D[Tools: read, bash, debug]
    TOOLS_A --> LLM[LLM]
    TOOLS_C --> LLM
    TOOLS_K --> LLM
    TOOLS_D --> LLM
    LLM -->|responde| EXT
    EXT --> U
\\\

## Modos

| Modo | Descrição | Tools |
|------|-----------|-------|
| **Code** | Codificação diária, edição de arquivos | read, write, edit, bash |
| **Architect** | Planejamento de sistemas, specs, migrações | plan, search, write |
| **Ask** | Respostas rápidas, explicações, documentação | search, read |
| **Debug** | Rastreamento de problemas, logs, isolamento | read, bash, debug |
| **Custom** | Modos especializados definidos pelo usuário | customizáveis |

## Funcionalidades Principais

1. **Múltiplos modos**: Comportamento especializado por tipo de tarefa
2. **Tools por modo**: Ferramentas relevantes para cada contexto
3. **Mode detection**: Detecção automática de intenção
4. **MCP support**: Servidores MCP externos
5. **Custom modes**: Modos personalizáveis
6. **Auto-generation**: Geração de código, documentação, testes

## Pontos Fortes

1. **Sistema de modos**: Diferencial único entre projetos
2. **Tools por modo**: Ferramentas relevantes por contexto
3. **Mode detection**: Detecção automática
4. **Custom modes**: Extensibilidade

## Limitações

1. **Descontinuado**: Projeto encerrado em maio 2026
2. **Sem compactação**: Contexto limitado
3. **Sem memória**: Sem persistência
4. **Sem error learning**: Sem rastreamento

## Oportunidades para o XForge

1. Sistema de modos é excelente — integrar com skills
2. Tools por modo = skills especializadas
3. Mode detection pode ser melhorado com LLM
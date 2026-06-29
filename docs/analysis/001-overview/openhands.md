# OpenHands

## O que é

OpenHands é um agente AI open-source como web app com backend de agente. Usa sandbox Docker para execução segura de código. Originalmente da UC Berkeley.

## Qual objetivo

Fornecer um agente que executa tarefas em ambiente sandboxado, com segurança para executar código arbitrário sem risco ao sistema host.

## Como funciona

\\\mermaid
flowchart TD
    U[Usuário] -->|prompt| WEB[Web App]
    WEB -->|envia| API[Backend API]
    API -->|cria| AG[Agente]
    AG -->|executa| SANDBOX[Docker Sandbox]
    SANDBOX -->|retorna| AG
    AG -->|planeja| PLN[Planner]
    PLN -->|envia| AG
    AG -->|responde| API
    API --> U
\\\

## Funcionalidades Principais

1. **Sandbox Docker**: Execução segura de código
2. **Event-driven**: Arquitetura reativa
3. **Web UI**: Acessível de qualquer lugar
4. **Planejamento**: Planner integrado
5. **Multi-agente**: Coordenação de agentes

## Pontos Fortes

1. **Sandbox**: Execução segura
2. **Event-driven**: Escalável
3. **Web UI**: Acessível

## Limitações

1. **Latência**: Docker adiciona overhead
2. **Complexidade**: Infraestrutura complexa
3. **Sem MCP**: Sem ferramentas externas padronizadas

## Oportunidades para o XForge

1. Sandbox é excelente para execução segura
2. Event-driven architecture é escalável
3. Planner pode ser integrado com Genius Council
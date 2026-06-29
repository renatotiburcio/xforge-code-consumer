# OpenHands — Arquitetura

## Visão Geral

OpenHands é um web app Python com backend de agente. Usa sandbox Docker para execução segura.

## Estrutura de Diretórios

```
openhands/
  agent/            # Sistema de agentes
  sandbox/          # Sandbox Docker
  events/           # Event system
  context/          # Context assembly
  memory/           # Sistema de memória
  tools/            # Ferramentas
  providers/        # Provedores LLM
frontend/           # React frontend
openhands-ui/       # UI components
containers/         # Docker containers
skills/             # Skills carregáveis
tests/              # Testes
```

## Componentes Principais

| Componente | Local | Responsabilidade |
|------------|-------|------------------|
| Agent | `agent/` | Sistema de agentes |
| SandboxManager | `sandbox/` | Gerencia containers Docker |
| EventBus | `events/` | Sistema de eventos |
| ContextProvider | `context/` | Monta contexto |

## Dependências Externas

| Dependência | Uso |
|-------------|-----|
| Python | Linguagem |
| Docker | Sandbox |
| FastAPI | Backend API |
| React | Frontend |

## Padrões Arquiteturais

1. **Sandbox Docker** — Execução segura de código
2. **Event-driven** — Arquitetura reativa
3. **Web UI** — Acessível de qualquer lugar

## Pontos Fortes

1. Sandbox seguro
2. Event-driven escalável
3. Web UI acessível

## Limitações

1. Latência do Docker
2. Complexidade de infraestrutura
3. Sem MCP

## Oportunidades para o XForge

1. Sandbox é excelente para execução segura
2. Event-driven é escalável
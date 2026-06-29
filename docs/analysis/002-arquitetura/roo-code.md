# Roo-Code — Arquitetura

## Visão Geral

Roo-Code é um monorepo pnpm com estrutura de apps/packages/src. A arquitetura é centrada em modos de agente com ferramentas especializadas.

## Estrutura de Diretórios

```
apps/               # Aplicações
packages/           # Packages compartilhados
src/
  extension.ts      # Entry point
  modes/
    index.ts        # Mode detector
    architect.ts    # Modo Architect
    code.ts         # Modo Code
    debug.ts        # Modo Debug
    ask.ts          # Modo Ask
  tools/
    index.ts        # Tool registry
  context/          # Context assembly
  memory/           # Sistema de memória
webview-ui/         # UI components
locales/            # Internacionalização (18 idiomas)
schemas/            # JSON schemas
scripts/            # Build scripts
releases/           # Releases
```

## Componentes Principais

| Componente | Local | Responsabilidade |
|------------|-------|------------------|
| ModeDetector | `src/modes/index.ts` | Detecta modo baseado no prompt |
| AgentFactory | `src/modes/` | Cria agente apropriado |
| ToolRegistry | `src/tools/index.ts` | Registra tools por modo |
| ContextAssembler | `src/context/` | Monta contexto |

## Modos

| Modo | System Prompt | Tools |
|------|---------------| | Expert developer | read, write, edit, | System architect | plan, search, write |
| Ask | Code reviewer | search, read |
| Debug | Debugger | read, bash, debug |
| Custom | User-defined | Customizáveis |

## Dependências Externas

| Dependência | Uso |
|-------------|-----|
| TypeScript | Linguagem |
| pnpm | Package manager |
| VS Code API | Extensão |
| MCP SDK | Servidores MCP |

## Padrões Arquiteturais

1. **Mode-based** — Comportamento especializado por tipo de tarefa
2. **Tools por modo** — Ferramentas relevantes por contexto
3. **Mode detection** — Detecção automática de intenção

## Pontos Fortes

1. Sistema de modos único
2. Tools especializadas por modo
3. Custom modes

## Limitações

1. Descontinuado (maio 2026)
2. Sem compactação
3. Sem memória entre sessões

## Oportunidades para o XForge

1. Sistema de modos é excelente
2. Tools por modo = skills especializadas
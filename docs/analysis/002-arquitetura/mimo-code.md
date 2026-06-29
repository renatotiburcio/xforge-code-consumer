# MiMo-Code — Arquitetura

## Visão Geral

MiMo-Code é uma extensão VS Code leve e simples.

## Estrutura de Diretórios

```
src/
  extension.ts      # Entry point
  providers/        # Providers
  context/          # Context assembly
  memory/           # Sistema de memória
  tools/            # Ferramentas
packages/           # Packages compartilhados
sdks/               # SDKs
docs/               # Documentação
infra/              # Infraestrutura
nix/                # Nix configs
patches/            # Patches
script/             # Scripts
assets/             # Assets
```

## Componentes Principais

| Componente | Responsabilidade |
|------------|------------------|
| Entry Point | Ativação da extensão |
| Providers | Providers de UI |
| Context | Montagem de contexto |

## Dependências Externas

| Dependência | Uso |
|-------------|-----|
| TypeScript | Linguagem |
| VS Code API | Extensão |

## Padrões Arquiteturais

1. **Minimalista** — Leve e rápido
2. **Multi-provedor** — Suporte a vários LLMs

## Pontos Fortes

1. Leve
2. Simples
3. Rápido

## Limitações

1. Funcionalidades limitadas
2. Sem MCP

## Oportunidades para o XForge

1. Simplicidade é diferencial para onboarding
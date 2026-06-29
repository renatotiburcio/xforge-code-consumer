# Continue — Arquitetura

## Visão Geral

Continue é um monorepo pnpm workspaces com 15+ packages. A arquitetura é centrada em `packages/core` que alimenta CLI, VS Code e JetBrains.

## Estrutura de Diretórios

```
packages/
  core/             # Sistemas centrais (RAG, model, context)
  extension/        # Extensão VS Code
  gui/              # Interface gráfica
  binary/           # CLI standalone
  context/          # Context providers
  model/            # Model providers
extensions/
  vscode/           # VS Code extension source
  cli/              # CLI source
  intellij/         # JetBrains plugin source
skills/             # Skills carregáveis
sync/               # Sync between products
```

## Componentes Principais

| Componente | Package | Responsabilidade |
|------------|---------|------------------|
| ContextProvider | core | Resolve @file/@folder/@codebase |
| SemanticIndexer | core | Indexação semântica com SQLite |
| RAGRetriever | core | Recuperação semântica |
| AutocompleteProvider | core | Autocomplete inteligente |
| ModelConfig | core | Configuração de modelos |

## Dependências Externas

| Dependência | Uso |
|-------------|-----|
| TypeScript | Linguagem |
| pnpm | Package manager |
| SQLite | Local embeddings |
| VS Code API | Extensão |
| IntelliJ SDK | Plugin |

## Padrões Arquiteturais

1. **Shared Core** — Mesmo core para todos os produtos
2. **@context System** — Referência explícita de arquivos/pastas
3. **Local RAG** — Embeddings locais sem cloud
4. **Skills Carregáveis** — Regras sob demanda

## Pontos Fortes

1. @context system único
2. RAG local sem cloud
3. Multi-IDE
4. Pioneiro

## Limitações

1. Read-only (não mantido)
2. Sem multi-agentes
3. Sem compactação
4. Sem memória entre sessões

## Oportunidades para o XForge

1. @context system é excelente
2. RAG local é modelo para híbrido
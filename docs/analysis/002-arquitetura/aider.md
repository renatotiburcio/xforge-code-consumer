# Aider — Arquitetura

## Visão Geral

Aider é um CLI Python com arquitetura simples e focada. Não é extensão VS Code — roda apenas no terminal.

## Estrutura de Diretórios

```
aider/
  main.py           # Entry point
  repomap.py        # Repo mapping (estrutura do projeto)
  commands.py       # Comandos
  models.py         # Modelos LLM
  io.py             # Terminal UI
  utils.py          # Utilitários
benchmark/          # Benchmarks
docker/             # Docker setup
requirements/       # Requirements
scripts/            # Scripts
tests/              # Testes
```

## Componentes Principais

| Componente | Arquivo | Responsabilidade |
|------------|---------|------------------|
| ChatSession | `main.py` | Sessão de chat principal |
| RepoMap | `repomap.py` | Mapeamento do repositório |
| EditLoop | `main.py` | Loop de edição de arquivos |
| GitIntegration | `utils.py` | Integração com git |
| PromptGenerator | `main.py` | Geração de prompts |

## Dependências Externas

| Dependência | Uso |
|-------------|-----|
| Python 3.10+ | Linguagem |
| Git | Versionamento |
| OpenAI/Anthropic API | LLM |

## Padrões Arquiteturais

1. **CLI-first** — Terminal-only, sem GUI
2. **Git-native** — Entende commits, diffs, branches
3. **Repo mapping** — Indexação automática da estrutura
4. **Edit loop** — Gera patches git

## Pontos Fortes

1. Git-native workflow
2. Repo mapping automático
3. Pair programming
4. Minimal UI

## Limitações

1. Sem UI rica
2. Sem multi-agentes
3. Sem compactação
4. Sem MCP

## Oportunidades para o XForge

1. Git-native é excelente modelo
2. Repo mapping pode integrar com RAG
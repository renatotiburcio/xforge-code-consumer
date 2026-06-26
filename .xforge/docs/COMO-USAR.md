# COMO USAR

Guia rapido de uso do XForge Enterprise Development OS.

## Instalacao

\`\`\`bash
# Clonar o template
git clone <repo-url> meu-projeto
cd meu-projeto

# Inicializar
xforge init
\`\`\`

## Comandos Principais

| Comando | Descricao |
|---------|-----------|
| `/xforge` | Orquestracao geral |
| `/analisar-projeto` | Analisar projeto existente |
| `/criar-projeto` | Criar novo projeto |
| `/desenvolver` | Desenvolver feature |
| `/qualidade` | Quality gates |
| `/seguranca` | Auditoria de seguranca |
| `/conhecimento` | Gerenciar conhecimento |
| `/memoria` | Gerenciar memoria |
| `/documentacao` | Gerar documentacao |
| `/release` | Gestao de releases |

## Configuracao

Edite \`kilo.jsonc\` para configurar:
- **provider**: Provedores de IA (openrouter, anthropic, openai, ollama)
- **agent**: Modelos por agente
- **routing**: Routing por complexidade
- **permissions**: Permissoes de execucao

## Estrutura

\`\`\`
.kilo/
  agents/     # Agentes especializados
  commands/   # Comandos publicos
  skills/     # Skills por dominio
  rules/      # Regras obrigatorias
  workflows/  # Workflows YAML
  routing/    # Routing rules
.xforge/
  decisions/  # Decision Records
  knowledge/  # Base de conhecimento
  memory/     # Memoria persistente
  scripts/    # Automacao
  archive/    # Historico
docs/         # Manual canonico (57 paginas)
\`\`\`

## Proximos Passos

1. Leia o manual completo em \`docs/SUMMARY.md\`
2. Configure seus providers em \`kilo.jsonc\`
3. Execute \`/analisar-projeto\` no seu projeto
4. Use \`/xforge\` para qualquer tarefa

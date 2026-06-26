---
id: como-estender
type: documentacao
tags: [docs, guia, extender, customizar, contribuir]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

# Como Estender o XForge Template

## Adicionar um Novo Agente

1. Criar arquivo em `.kilo/agents/nome-do-agente.md`
2. Adicionar YAML frontmatter:

```yaml
---
name: nome-do-agente
description: O que este agente faz
mode: primary
color: "#10B981"
permission:
  read: allow
  edit:
    "*.cs": "allow"
    "*.md": "allow"
    "*": "deny"
  bash: ask
---
```

3. Registrar em `.kilo/core/registries/expert-registry.json`
4. Rodar `doctor.ps1` para validar

## Adicionar um Novo Comando

1. Criar arquivo em `.kilo/commands/nome-comando.md`
2. Adicionar YAML frontmatter:

```yaml
---
description: O que o comando faz
agent: code
---
```

3. Adicionar secao `## Exemplos` com 2-3 exemplos
4. Criar workflow correspondente em `.kilo/workflows/nome-comando.md`
5. Rodar `doctor.ps1` para validar

## Adicionar uma Nova Skill

1. Criar diretorio em `.kilo/skills/nome-da-skill/`
2. Criar `SKILL.md` dentro com frontmatter:

```yaml
---
name: nome-da-skill
description: Quando usar e o que faz
metadata:
  version: 1.0.0
---
```

3. Rodar `doctor.ps1` para validar

## Adicionar um MCP Server

1. Criar arquivo JSON em `.kilo/mcp/nome-server.json`
2. Seguir o schema:

```json
{
  "name": "meu-server",
  "version": "1.0.0",
  "description": "Descricao do server",
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "meu-mcp-server"],
  "env": {},
  "capabilities": { "tools": [] }
}
```

3. Adicionar variaveis de ambiente necessarias

## Modificar o Doctor

O script `doctor.ps1` verifica:
- Estrutura de diretorios
- kilo.jsonc (chaves permitidas)
- Registros (paths validos)
- Comandos e workflows
- Agentes (frontmatter)
- Skills (SKILL.md)
- Encoding (mojibake)
- Connectivity (config + provider)

Para adicionar uma nova validacao:
1. Adicionar funcao no `doctor.ps1`
2. Adicionar secao de output
3. Atualizar chaves permitidas do `kilo.jsonc` se necessario

## Atualizar Config Global

Arquivo: `~/.xforge/config.json`

Campos disponiveis:
- `provider.active` — provedor ativo (openrouter, openai, etc.)
- `provider.model` — modelo ativo
- `routing.providers` — lista de provedores com URLs
- `preferences.language` — idioma preferido
- `preferences.doctorOnStartup` — rodar doctor ao iniciar
- `preferences.autoReindex` — reindexar RAG automaticamente

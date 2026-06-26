---
id: arquitetura
type: documentacao
tags: [docs, arquitetura, visao, camadas, design]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

# Arquitetura do XForge Template

## Principio Fundamental

```
.kilo   = camada operacional (substituivel, versionavel)
.xforge = camada persistente (NUNCA deletar, conhecimento do projeto)
```

## Camadas

### .kilo/ — Operacional
Contem tudo que o Kilo precisa para operar:
- Agentes, comandos, skills, regras, workflows
- Scripts de automacao (doctor, RAG)
- Registros (expert-registry, command-registry, skill-registry)
- MCP server configs

Esta camada pode ser atualizada sem perda de conhecimento.

### .xforge/ — Persistente
Contem o conhecimento do projeto:
- Base de conhecimento (knowledge/)
- Indice RAG (rag/)
- Backlog, roadmap, sprints
- Decisoes arquiteturais (decisions/)
- Memoria do projeto (memory/)
- DNA do projeto (project-dna/)

Esta camada NUNCA deve ser deletada durante atualizacoes.

## Fluxo de Operacao

```
Usuario -> /comando -> Kilo
  -> AGENTS.md (instrucoes)
  -> .kilo/rules/ (regras)
  -> Seleciona agente primario
  -> Seleciona skills minimas
  -> Valida policies + RBAC
  -> Executa tarefa
  -> Valida resultado
  -> Atualiza .xforge/ (quando aplicavel)
```

## RAG (Retrieval-Augmented Generation)

```
.xforge/knowledge/ -> rag_local.py -> chunks/ -> indexes/
                                                  |
Usuario faz query <--------------------------------+
  -> Busca no indice -> Retorna docs relevantes
```

Configuracao: `.xforge/rag/config.json`
- 786 documentos indexados
- 1,859 chunks
- Chunking: maxLines=40, overlapLines=5

## Agentes

### Classificacao
- **Primary** (20): Diretores, orquestradores, user-facing
- **Subagent** (16): Engenheiros, especialistas, gerenciadores

### Permissoes
- Primary: edit amplo (*.cs, *.md, *.ps1, *.py, *.json) + bash:ask
- Subagent: edit restrito (*.md only) + bash:deny

## Provider Routing

```
kilo.jsonc
  -> routing.providers (5: openrouter, openai, anthropic, google, xai)
  -> agent.model (por agente)
  -> ~/.xforge/config.json (preferencias do usuario)
```

## Doctor

Validacao em 7 secoes:
1. Estrutura requerida
2. kilo.jsonc (shape + chaves permitidas)
3. Registros (paths validos)
4. Comandos + workflows
5. Agentes + Skills
6. Encoding (mojibake)
7. Connectivity (config + provider)

---
name: memory-management
description: Use when creating, updating, querying, or pruning project memory entries.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# memory-management

## Objetivo

Gerenciar a memória persistente do projeto.

## Tipos de Memória

| Tipo | Local | Retenção | Exemplo |
|------|-------|:--------:|---------|
| **Decision** | .xforge/decisions/ | Permanente | "Usar Minimal API" |
| **Session** | .xforge/memory/sessions/ | 7 dias | "Refactor auth module" |
| **Global** | .xforge/memory/global/ | Permanente | "Prefer XForge.MediatR" |
| **Learning** | .xforge/learning/ | Permanente | "EF Core gotcha: Include()"

## Procedimento

### Criar Entrada
1. Identificar tipo de memória
2. Verificar se já existe similar
3. Criar com timestamp e fonte
4. Indexar para busca

### Atualizar
1. Buscar entrada existente
2. Verificar se nova info contradiz
3. Atualizar (não duplicar)
4. Recalcular confiança

### Consultar
1. Buscar por keyword (BM25)
2. Filtrar por tipo e scope
3. Ordenar por relevância
4. Retornar top-N

### Poda
- Entradas > 30 dias sem uso → arquivar
- Entradas contraditórias → marcar deprecated
- Nunca deletar decisões permanentes

## Regras

- NUNCA salvar passwords, keys, tokens
- Sempre registrar fonte
- Dados sensíveis → pseudonimizar
- Atualizar memória após decisões significativas

---
name: dominio
description: Mapear, documentar e gerenciar dominios e conhecimento do projeto
agent: code
category: xforge-public
---

# /dominio

## Objetivo
Mapear, documentar e gerenciar os dominios de negocio e conhecimento do projeto.

## Sub-comandos

| Sub-comando | Acao |
|-------------|------|
| `/dominio mapear` | Mapear dominios de negocio |
| `/dominio documentar` | Documentar conhecimento de dominio |
| `/dominio buscar` | Buscar conhecimento |
| `/dominio curar` | Curadoria de conhecimento |
| `/dominio promover` | Promover conhecimento experimental |

## Procedimento

### Mapear
1. Identificar bounded contexts
2. Mapear entidades e regras de negocio
3. Criar mapa de dominios

### Documentar
1. Criar knowledge files por dominio
2. Adicionar trust score e source
3. Indexar no RAG

### Buscar
1. Buscar por keyword no knowledge
2. Filtrar por aplicabilidade (stack)
3. Retornar resultados com trust score

### Curar
1. Identificar conhecimento duplicado
2. Identificar conhecimento obsoleto
3. Promover ou depreciar

### Promover
1. Validar conhecimento experimental
2. Verificar uso em 2+ projetos
3. Promover para enterprise-standard

## Uso
```
/dominio mapear
/dominio documentar
/dominio buscar <keyword>
/dominio curar
/dominio promover
```


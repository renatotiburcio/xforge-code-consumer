---
name: aprender
description: Aprendizado continuo — estudar fontes, ingerir conhecimento, extrair licoes
agent: code
category: xforge-public
---

# /aprender

## Objetivo
Aprendizado continuo: estudar fontes externas, ingerir conhecimento, extrair licoes e melhorar o sistema.

## Sub-comandos

| Sub-comando | Acao |
|-------------|------|
| `/aprender estudar <url>` | Estudar fonte externa |
| `/aprender ingerir` | Ingerir conhecimento na knowledge base |
| `/aprender licoes` | Extrair licoes de erros/sucessos |
| `/aprender aplicar` | Aplicar conhecimento aprendido |

## Procedimento

### Estudar
1. Acessar URL/documento
2. Extrair informacoes relevantes
3. Estruturar em knowledge entry

### Ingerir
1. Validar trust score
2. Adicionar a knowledge base
3. Indexar no RAG
4. Emitir evento KNOWLEDGE_PROMOTED

### Licoes
1. Ler feedback log
2. Identificar padroes de erro
3. Criar regra preventiva
4. Atualizar knowledge

### Aplicar
1. Buscar conhecimento relevante
2. Aplicar ao contexto atual
3. Validar resultado

## Uso
```
/aprender estudar https://docs.example.com
/aprender ingerir
/aprender licoes
/aprender aplicar
```


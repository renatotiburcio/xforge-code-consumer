---
description: Cria uma feature respeitando arquitetura, memória, impacto, testes e governança.
agent: code
---

# /criar-feature

## Fluxo

1. Recuperar memória.
2. Consultar graph/search.
3. Analisar impacto.
4. Validar policy/RBAC.
5. Planejar.
6. Executar somente faltantes.
7. Testar.
8. Documentar.
9. Atualizar memória.
10. Criar PR.

## Objetivo operacional

Este artefato não deve ser apenas informativo. Ele deve orientar execução real dentro do XForge Enterprise Development OS.

## Quando usar

Use este artefato quando a solicitação, workflow, agente ou rotina envolver `Criar Feature` ou depender desta capacidade para tomar uma decisão técnica, operacional, arquitetural, de memória, governança ou qualidade.

## Procedimento mínimo

1. Recuperar memória relevante.
2. Identificar projeto, módulo, domínio, cliente e risco.
3. Validar policies, RBAC, security rules e semantic boundaries.
4. Consultar knowledge graph, search engine e histórico quando disponível.
5. Executar análise ou ação com saída rastreável.
6. Atualizar audit trail, memória, backlog, roadmap ou playbook quando aplicável.
7. Emitir evento interno quando houver mudança relevante.
8. Reindexar conhecimento quando arquivos de memória, docs, SDD ou legacy forem alterados.

## Saída esperada

- decisão ou diagnóstico objetivo;
- arquivos alterados ou criados;
- riscos identificados;
- próximos passos;
- memória atualizada quando aplicável;
- evidência para revisão humana quando necessário.

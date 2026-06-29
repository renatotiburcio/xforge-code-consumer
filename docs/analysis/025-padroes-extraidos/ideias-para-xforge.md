# Ideias para o XForge

## I-001: Genius Council
- **Origem**: Nenhum projeto tem
- **Descrição**: 38+ especialistas debatem decisões
- **Benefício**: Decisões de maior qualidade
- **Problema**: Latência, custo
- **Melhorar**: Cache, small models para rotina
- **Prioridade**: P0

## I-002: Self-Healing Rules
- **Origem**: Nenhum projeto tem
- **Descrição**: 12 regras de auto-correção
- **Benefício**: Menos erros
- **Problema**: False positives
- **Melhorar**: Confidence scoring
- **Prioridade**: P0

## I-003: Per-Directory AGENTS.md
- **Origem**: Kilo Code suporta parcialmente
- **Descrição**: Diferentes regras por diretório
- **Benefício**: Contexto específico por módulo
- **Problema**: Descoberta, conflitos
- **Melhorar**: findUp com max 3 níveis
- **Prioridade**: P1

## I-004: Living Knowledge Graph
- **Origem**: Nenhum projeto tem
- **Descrição**: Conhecimento com TTL e trust score
- **Benefício**: Conhecimento sempre atualizado
- **Problema**: Curation overhead
- **Melhorar**: Auto-promotion
- **Prioridade**: P1

## I-005: Memory Namespace Isolation
- **Origem**: Nenhum projeto tem
- **Descrição**: Memória isolada por projeto
- **Benefício**: LGPD compliance
- **Problema**: Cross-project learning limitado
- **Melhorar**: DR + human approval
- **Prioridade**: P0

## I-006: Hybrid RAG
- **Origem**: Kilo Code (Qdrant), Continue (SQLite), Aider (repo map)
- **Descrição**: Combinar 4 tipos de busca
- **Benefício**: Melhor recall e precisão
- **Problema**: Complexidade
- **Melhorar**: Lazy indexing
- **Prioridade**: P1

## I-007: Error Pattern Learning
- **Origem**: Nenhum projeto tem
- **Descrição**: Rastreia erros entre sessões
- **Benefício**: Prevenção de erros recorrentes
- **Problema**: Storage, privacy
- **Melhorar**: Sanitize PII, TTL
- **Prioridade**: P1

## I-008: Decision Records
- **Origem**: Nenhum projeto tem
- **Descrição**: Decisões documentadas automaticamente
- **Benefício**: Rastreabilidade
- **Problema**: Overhead
- **Melhorar**: DR apenas para decisões não-trivial
- **Prioridade**: P2

## I-009: Stack-Agnostic
- **Origem**: Nenhum projeto tem
- **Descrição**: Detecta stack e adapta comportamento
- **Benefício**: Funciona para qualquer projeto
- **Problema**: Detection accuracy
- **Melhorar**: Explicit declaration
- **Prioridade**: P1

## I-010: Router + Worker
- **Origem**: Kilo Code
- **Descrição**: Small model routes, large model executes
- **Benefício**: 70% economia
- **Problema**: Latência do router
- **Melhorar**: Cache de decisões
- **Prioridade**: P0
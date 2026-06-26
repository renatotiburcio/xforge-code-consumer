# Self-Learning Genius Rule (v3.39.0)

> Regra institucional: cada Genius aprende continuamente com novo conhecimento que entra no sistema.

## 1. Conceito

Cada Genius (AG001-AG066+) possui memoria dedicada. Quando novo conhecimento entra no sistema via:

- Compliance Intelligence MCP (leis, normas, jurisprudencia)
- Market Intelligence MCP (reviews, features, concorrentes)
- Product Engineering MCP (decisoes arquitetonicas, ADRs)
- Treinamento manual do usuario
- Feedback de code review

O Knowledge Router identifica a area, valida trust score, e alimenta o Genius correspondente.

## 2. Estrutura

`
.xforge/memory/genius/
  AG001-turing/
    knowledge.jsonl
    contradictions.log
  AG002-vonneumann/
    ...
  AG039-marion/
    ...
`

## 3. Knowledge Entry Schema

`json
{
  id: K-AG039-001,
  genius: AG039,
  domain: Contabilidade,
  statement: NBC TG 26 atualizada em 2025,
  source: CFC Resolucao 1.500/2025,
  trustScore: 100,
  createdAt: 2026-06-19,
  expiresAt: 2027-06-19
}
`

## 4. Fluxo de Atualizacao

1. Knowledge input (lei nova, review, ADR, treinamento)
2. Knowledge Router classifica (area, dominio, genius destinatario)
3. Valida trust score > 50 (fontes oficiais = 100, blogs = 60, AI = 40)
4. Detecta contradicao com conhecimento existente
   - Sem contradicao: append a genius memory
   - Com contradicao: abre debate (AG999 Devil Advocate)
5. Atualiza knowledge graph (.xforge/knowledge/genius/)
6. Reindexa RAG (.xforge/rag/index/)
7. Audit trail (.xforge/audit/genius-update.log)
8. Genius esta enriquecido para proxima invocacao

## 5. Trigger

- Automatico: hook pos-MCP (quando MCP gera knowledge novo)
- Manual: comando /genius-learn
- Periodic: revisao trimestral por dominio (TTL: legislacao 3-6 meses)

## 6. Validacao Continua

A cada atualizacao o Genius verifica: consistencia interna, coerencia com fontes oficiais, idade (TTL), trust score.

Se validacao falhar: reverter para versao anterior, notificar humano, abrir DR de revisao.

## 7. Quando NAO Aplicar

- Input com trust score < 50 (descartar)
- Input que contradiz fonte oficial (debate)
- Input com dados pessoais (LGPD - mascarar)
- Input desatualizado (TTL expirado)

## 8. Referencias

- DR-0128 (esta expansao)
- DR-0127 (macro discovery)
- DR-0126 (composable commands)
- .kilo/skills/genius-council/SKILL.md
- .kilo/rules/02-genius-council-framework.md
- .kilo/rules/knowledge-rules.md
- .kilo/rules/ttl-rules.md


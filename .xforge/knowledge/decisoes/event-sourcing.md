---
id: knowledge-decisoes-event-sourcing
type: knowledge
title: ADR-0016: Event Sourcing para Dominios Criticos
category: decisoes
domain: architecture
trustScore: 80
source: human-expert
createdAt: 2026-06-14
lastValidated: 2026-06-14
tags: [adr, event-sourcing, architecture, audit]
---

# ADR-0016: Event Sourcing para Dominios Criticos

## Status

Aceita. Proposta por Renato Tiburcio em 2026-06-14.

## Contexto

Tres dominios do ERP demandam rastreabilidade completa por motivos legais/regulatorios:

1. **Fiscal**: SPED, EFD ICMS/IPI, EFD Contribuicoes, ECD, ECF
2. **Folha**: eSocial S-1000 ate S-3000
3. **Contabil**: ECD, ECF, livros obrigatorios

Modelo tradicional (CRUD) perde o historico de alteracoes apos UPDATE.
Auditoria exige o estado ANTERIOR de cada campo.

## Decisao

Adotar **Event Sourcing** para os dominios fiscal, folha e contabil.

Cada alteracao de estado = um evento imutavel publicado. Estado atual = replay
dos eventos. Eventos sao append-only e versionados.

## Alternativas consideradas

| Alternativa | Pros | Contras | Veredito |
|-------------|------|---------|----------|
| Event Sourcing | Historico completo, replay temporal, audit-ready | Complexidade inicial | **ESCOLHIDA** |
| Temporal tables (SQL Server) | Nativo, simples | Vendor lock-in, nao-portatil | Rejeitada |
| Audit log separado | Baixo impacto | Historico parcial, nao-replayable | Rejeitada |
| Soft delete + campos | Trivial | Limitado, manual | Rejeitada |

## Consequencias

### Positivas

- Audit trail completo sem logica adicional
- Time-travel: consultar estado em qualquer ponto no tempo
- Reproducao de cenarios para debugging
- Integra com Kafka para stream processing futuro

### Negativas

- Curva de aprendizado maior
- Storage cresce indefinidamente (mitigavel com snapshots periodicos)
- Queries simples requerem projection/materialized view
- Versionamento de schema de eventos precisa ser gerenciado

## Implementacao

Stack:

- **Event Store**: PostgreSQL com tabela `events` append-only
- **Projections**: materialized views atualizadas por triggers ou jobs
- **Replay**: utilitario CLI que aplica eventos em ordem
- **Versionamento**: campo `schema_version` em cada evento

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    stream_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    schema_version INT NOT NULL,
    payload JSONB NOT NULL,
    metadata JSONB NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_events_stream ON events(stream_id, occurred_at);
```

## Referencias

- Fowler, M. (2005). Event Sourcing
- Vernon, V. (2013). Implementing Domain-Driven Design
- Greg Young - CQRS and Event Sourcing
- LGPD Art. 37, 46 (rastreabilidade)


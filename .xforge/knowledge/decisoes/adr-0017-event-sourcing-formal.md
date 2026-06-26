---
id: adr-0017-event-sourcing-formal
type: decisao
title: ADR-0017: Event Sourcing para Dominios Fiscais e Folha
domain: arquitetura
trustScore: 85
source: ADR formal + XForge team
tags: [adr, event-sourcing, cqrs]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# ADR-0017: Event Sourcing para Dominios Fiscais e Folha

## Status

Accepted (2026-06-14) - XForge v1.1.2

## Contexto

Os dominios fiscal (NFe, NFCe, SPED) e folha de pagamento (eSocial) tem caracteristicas que combinam perfeitamente com Event Sourcing:

1. Imutabilidade legal
2. Auditoria obrigatoria (LGPD Art. 37)
3. Reconstrucao historica
4. Eventos externos (SEFAZ, eSocial)
5. Snapshots regulatorios

## Decisao

Adotar Event Sourcing + CQRS para:

- fiscal/calculo (NFe, NFCe, NFs-e, SAT, CT-e, MDF-e)
- fiscal/sped (EFD ICMS/IPI, EFD Contribuicoes, ECD, ECF)
- trabalhista/folha (calculo, rescisao, ferias, 13o)
- trabalhista/esocial (S-1000, S-1200, S-3000, S-2200, S-2220)

## Modelo de Dados

```csharp
public abstract record DomainEvent {
    public Guid EventId { get; init; }
    public Guid AggregateId { get; init; }
    public string EventType { get; init; }
    public DateTime OccurredAt { get; init; }
    public string SchemaVersion { get; init; }
    public string CorrelationId { get; init; }
    public string Payload { get; init; }
}
```

## Armazenamento

- Event store: PostgreSQL com tabela domain_events (append-only)
- Projections: Tabelas materializadas
- Snapshots: A cada 1000 eventos por agregado
- Retencao: 5 anos fiscal, 20 anos folha

## Consequencias Positivas

- Auditoria completa
- Time travel (replay em qualquer ponto)
- Integracao facilitada (eventos como contrato)
- Compliance LGPD Art. 37 nativo

## Consequencias Negativas

- Curva de aprendizado
- Eventual consistency
- Crescimento do banco (5-10x)
- Debugging complexo

## Alternativas

| Opcao | Veredito |
|-------|----------|
| CRUD tradicional | Rejeitado |
| Audit log separado | Rejeitado |
| Event Sourcing | Escolhido |
| CDC + Kafka | Rejeitado (overhead) |

## Referencias

- ADR-0016
- Greg Young, Event Sourcing (2014)

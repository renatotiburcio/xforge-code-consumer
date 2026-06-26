---
id: adr-0018-cache-estrategia
type: decisao
title: ADR-0018: Estrategia de Cache Multinivel (L1 Memory + L2 Distributed)
domain: arquitetura
trustScore: 82
source: ADR formal + XForge v1.1.1 learnings
tags: [adr, cache, performance]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# ADR-0018: Estrategia de Cache Multinivel

## Status

Accepted (2026-06-14) - XForge v1.1.2

## Contexto

Em v1.1.1 implementamos cache in-process para INDEX.json (60s TTL) e doctor (5s TTL):

- xforge_doctor: 2529ms -> <100ms (hit) = 25x speedup
- xforge_knowledge_search: 592ms -> <1ms (hit) = 500x speedup
- Beneficios por-processo: cada node server.js cria novo subprocess

Em producao com N pods, cache L1 tem hit rate menor.

## Decisao

Adotar cache multinivel:

- L1 (in-process): Memory cache, TTL 5-60s
- L2 (distributed): Redis, TTL 1-10min, compartilhado entre pods
- L3 (CDN/edge): Para assets estaticos, futuro

## Arquitetura

Request -> L1 check (in-process) -> HIT? return. MISS: L2 check (Redis) -> HIT? return + set L1. MISS: Compute/store -> set L1 + L2.

## TTLs por Tipo de Dados

| Dado | L1 TTL | L2 TTL | Invalidacao |
|------|--------|--------|-------------|
| doctor check | 5s | NAO | Manual/TTL |
| INDEX.json | 60s | 5min | mtime + TTL |
| tenant config | 30s | 10min | File watch |
| workflow list | 60s | 1h | File watch + TTL |
| pack list | 120s | 30min | File watch + TTL |
| policy rules | 60s | 5min | File watch + TTL |
| RBAC matrix | 60s | 5min | File watch + TTL |

## Consequencias Positivas

- Performance: 25-500x speedup
- Reduz carga em disco
- Escalabilidade: L2 compartilhado
- Resiliencia: L2 offline = continua com L1

## Consequencias Negativas

- Consistencia (mitigado por TTL)
- Memoria (L1 usa RAM)
- Complexidade
- Custo Redis: $15-50/mes

## Metricas de Sucesso

| Metrica | Target |
|---------|--------|
| L1 hit rate | > 60% |
| L2 hit rate | > 80% |
| L1 latency p95 | < 5ms |
| L2 latency p95 | < 20ms |
| Cache memory | < 100MB |

## Alternativas

| Opcao | Veredito |
|-------|----------|
| L1 only | Rejeitado |
| L1 + L2 | Escolhido |
| L2 only | Rejeitado |
| Sem cache | Rejeitado |

## Referencias

- ADR-0015
- v1.1.1 doctor/INDEX cache

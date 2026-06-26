---
id: knowledge-projeto-observability-strategy
type: knowledge
title: Estrategia de Observabilidade XForge
category: projeto
domain: architecture
trustScore: 75
source: human-expert
createdAt: 2026-06-14
lastValidated: 2026-06-14
tags: [observability, monitoring, logging, metrics, tracing]
---

# Estrategia de Observabilidade XForge

## Pilares

1. **Logs estruturados** - contexto pesquisavel e agregavel
2. **Metricas** - numericas, agregadas, com retencao
3. **Tracing distribuido** - correlacao cross-service
4. **Alertas** - proativos, com runbook

## Stack escolhida

| Pilar | Ferramenta | Justificativa |
|-------|------------|---------------|
| Logs | Serilog + Elasticsearch | Open source, pesquisa full-text, dashboards Kibana |
| Metricas | Prometheus + Grafana | Padrao de mercado, alertas robustos |
| Tracing | OpenTelemetry + Jaeger | Vendor neutral, futuro-proof |
| APM | Elastic APM (opcional) | Integracao nativa com ELK |
| Alertas | Alertmanager | Padrao, integracao Slack/PagerDuty |

## Logs estruturados (Serilog)

Formato canonico (campos principais):

- @timestamp, @level, service, version
- correlation_id, user_id, tenant_id
- request_path, request_method, request_duration_ms, request_status
- message, business-specific fields (ex: nfe_id, pedido_id)

Correlation ID propagado por toda a cadeia (API, worker, banco, integracao).

## Metricas chave (RED + 4 Golden Signals)

### RED (Request, Error, Duration)

- http_requests_total{path, method, status} (counter)
- http_request_duration_seconds{path, method} (histogram)
- http_errors_total{path, method, status_class} (counter)

### 4 Golden Signals

- **Latency**: p50, p95, p99 por endpoint
- **Traffic**: requests per second
- **Errors**: error rate (5xx) e taxa de falha por tipo
- **Saturation**: CPU, memoria, conexoes DB, fila, threads

### Metricas de negocio (NFe, ERP)

- nfe_emitidas_total{cnpj, uf, status} (counter)
- nfe_emitida_duration_seconds (histogram)
- nfe_rejeitada_total{codigo_rejeicao} (counter)
- pedidos_processados_total{status} (counter)
- folha_funcionarios_processados_total{empresa} (counter)

## Tracing distribuido (OpenTelemetry)

Spans criados em:

- HTTP entrypoint (request_id, user_id, ip)
- DB query (query, row_count, duration)
- HTTP client (URL, status, retries)
- Background job (job_id, payload_size)
- Integration call (provider, method, attempt)

Sampling rate:

- 100% em dev/staging
- 10% em producao (configuravel)
- 100% em requests com error (sempre tracear problemas)

## Alertas (Alertmanager)

Severidades:

| Severidade | Resposta | Canal | Exemplo |
|------------|----------|-------|---------|
| Critical | Imediata (1 min) | PagerDuty | DB indisponivel, integracao fora |
| High | 15 min | Slack #alerts | Taxa de erro > 5% |
| Medium | 1h | Slack #monitoring | Latencia p95 > 2s sustentada |
| Low | Proximo dia util | Email | Disco > 80% |

## Retencao

| Tipo | Retencao | Justificativa |
|------|----------|---------------|
| Logs aplicacao | 30 dias hot + 90 dias warm | LGPD Art. 37 + operacional |
| Metricas | 1 ano (alta resolucao 7d) | Tendencia + auditoria |
| Traces | 7 dias | Sampling, custo |
| Audit trail | 5 anos (WORM) | LGPD + regulatorio |

## Referencias

- OpenTelemetry specification
- Google SRE Book - Chapter 6 (Monitoring Distributed Systems)
- Elastic APM documentation
- Prometheus best practices


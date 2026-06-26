---
name: observability-runtime-expert
description: Expert em observabilidade: logging, métricas, tracing, alerting e monitoring em produção.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# observability-runtime-expert

## Objetivo

Garantir visibilidade completa do sistema em produção.

## Três Pilares

### 1. Logging
- **Nível**: Debug < Info < Warning < Error < Critical
- **Formato**: Structured logging (JSON)
- **Tools**: Serilog, NLog, Winston
- **Destino**: Console, File, Seq, Elastic

### 2. Métricas
- **Counters**: Requisições, erros, latência
- **Gauges**: Memória, CPU, conexões
- **Histograms**: Distribuição de latência
- **Tools**: Prometheus, OpenTelemetry

### 3. Tracing
- **Spans**: Cada operação
- **Trace context**: Correlation ID
- **Tools**: Jaeger, Zipkin, OpenTelemetry

## Configuração

```csharp
// OpenTelemetry
builder.Services.AddOpenTelemetry()
    .WithTracing(b => b
        .AddAspNetCoreInstrumentation()
        .AddEntityFrameworkCoreInstrumentation()
        .AddJaegerExporter())
    .WithMetrics(b => b
        .AddPrometheusExporter()
        .AddRuntimeInstrumentation());
```

## Alertas

| Métrica | Threshold | Severidade |
|---------|-----------|:----------:|
| Error rate | > 1% | P2 |
| Latency p99 | > 2s | P2 |
| CPU | > 80% | P3 |
| Memory | > 85% | P2 |
| Disk | > 90% | P1 |

## Procedimento

1. Configurar logging estruturado
2. Implementar métricas básicas
3. Adicionar tracing
4. Configurar alertas
5. Criar dashboards
6. Monitorar e ajustar

## Regras

- Logging estruturado sempre
- Correlation ID em todas as requisições
- Métricas de negócio + técnicas
- Alertas acionáveis (com ação)

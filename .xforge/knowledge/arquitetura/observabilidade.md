---
id: observabilidade
type: knowledge
tags: [observabilidade, logging, metricas, tracing, serilog, opentelemetry, health-checks, dotnet]
owner: project-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Observabilidade
- **Principais responsabilidades**: Configurar Serilog para logging estruturado; Instrumentar com OpenTelemetry (métricas + traces); Implementar health checks para todos os serviços
- **Seções principais**: Propósito, Responsabilidades, Três Pilares, Serilog — Logging Estruturado
- **Tags**: observabilidade, logging, metricas, tracing, serilog, opentelemetry, health-checks, dotnet
- **Tipo**: knowledge | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `observabilidade` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 11 |


# Observabilidade

## Propósito
Instrumentar o sistema ERP com logging estruturado, métricas, distributed tracing e health checks para monitoramento completo em produção.

## Responsabilidades
- Configurar Serilog para logging estruturado
- Instrumentar com OpenTelemetry (métricas + traces)
- Implementar health checks para todos os serviços
- Definir alertas e dashboards operacionais

## Três Pilares

```
                     ┌──────────────────────────────┐
                     │       OBSERVABILIDADE         │
                     └──────────────┬───────────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
    ┌────────▼────────┐   ┌────────▼────────┐   ┌────────▼────────┐
    │    MÉTRICAS      │   │      LOGS        │   │    TRACES       │
    │ • CPU, Memória   │   │ • Eventos        │   │ • Request flow   │
    │ • Latência p95   │   │ • Erros          │   │ • Span timing    │
    │ • Throughput     │   │ • Auditoria      │   │ • Dependências   │
    │ • Error rate     │   │ • Debug          │   │ • Context prop.  │
    └──────────────────┘   └──────────────────┘   └──────────────────┘
```

## Serilog — Logging Estruturado

```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .MinimumLevel.Override("Microsoft.EntityFrameworkCore", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .Enrich.WithThreadId()
    .Enrich.WithEnvironmentName()
    .Enrich.WithProperty("Application", "ERP.Api")
    .WriteTo.Console(new CompactJsonFormatter())
    .WriteTo.File("logs/erp-.log", rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 30, fileSizeLimitBytes: 100 * 1024 * 1024)
    .WriteTo.Seq("http://localhost:5341")
    .CreateLogger();
```

**Sinks:** Console (dev), File (local), Seq (staging), Elasticsearch (produção/ELK), Application Insights (Azure).

**Enrichers:** MachineName, ThreadId, EnvironmentName, CorrelationId, TenantId (custom).

## OpenTelemetry — Métricas e Traces

```csharp
builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("erp-api"))
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation(o => {
            o.RecordException = true;
            o.Filter = ctx => !ctx.Request.Path.StartsWithSegments("/health");
        })
        .AddHttpClientInstrumentation()
        .AddSqlClientInstrumentation()
        .AddSource("ERP.Application")
        .AddOtlpExporter())
    .WithMetrics(metrics => metrics
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddRuntimeInstrumentation()
        .AddMeter("ERP.Application")
        .AddPrometheusExporter()
        .AddOtlpExporter());
```

**Exporters:** Jaeger/Zipkin (traces), Prometheus (métricas), Azure Monitor, OTLP (universal).

## Métricas Customizadas

```csharp
public class ErpMetrics {
    private static readonly Meter Meter = new("ERP.Business", "1.0.0");
    private static readonly Counter<long> InvoicesIssued = Meter.CreateCounter<long>("erp.invoices.issued");
    private static readonly Counter<long> SalesOrders = Meter.CreateCounter<long>("erp.sales.orders");
    private static readonly Histogram<double> InvoiceTotal = Meter.CreateHistogram<double>("erp.invoice.total", unit: "BRL");
    private static readonly Histogram<double> OrderProcessingTime = Meter.CreateHistogram<double>("erp.order.processing.ms", unit: "ms");

    public void InvoiceIssued(decimal total, string operationType) {
        InvoicesIssued.Add(1, new KeyValuePair<string, object?>("operation.type", operationType));
        InvoiceTotal.Add((double)total, new KeyValuePair<string, object?>("operation.type", operationType));
    }
}
```

## Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddSqlServer(connectionString, name: "database", tags: new[] { "ready" })
    .AddRedis(redisConnection, name: "redis", tags: new[] { "ready" })
    .AddRabbitMQ(rabbitConnection, name: "rabbitmq", tags: new[] { "ready" })
    .AddCheck<CustomBusinessHealthCheck>("business-logic", tags: new[] { "ready" });

app.MapHealthChecks("/health");
app.MapHealthChecks("/health/ready", new HealthCheckOptions { Predicate = c => c.Tags.Contains("ready") });
app.MapHealthChecks("/health/live", new HealthCheckOptions { Predicate = _ => false });
```

## Alertas

| Alerta | Condição | Severidade |
|--------|----------|------------|
| **HighErrorRate** | Taxa de erro > 5% em 5min | Critical |
| **HighLatency** | p95 > 2s em 5min | Warning |
| **HighCPUUsage** | CPU > 85% em 10min | Warning |
| **PodCrashLooping** | Restart rate > 0 em 15min | Critical |

**Canais:** Email, Slack, PagerDuty, Teams, SMS via Azure Action Groups.

## Retenção de Dados

| Tipo | Retenção |
|------|----------|
| Logs Debug | 7 dias |
| Logs Produção | 30 dias |
| Logs Auditoria | 90-365 dias |
| Métricas (alta resolução) | 15 dias |
| Métricas (agregadas) | 90-365 dias |
| Traces detalhados | 7-14 dias |

## Dependências
- [deploy-net.md](deploy-net.md) — Deploy dos componentes de monitoramento
- [multi-tenancy.md](multi-tenancy.md) — Enrichers de tenant nos logs

## Restrições
- Nunca logar dados sensíveis (senhas, tokens, CPFs completos)
- Usar sampling em produção para controlar custos (ex: 10% de requests OK, 100% de erros)
- Correlation ID deve ser propagado em todas as requests e serviços downstream


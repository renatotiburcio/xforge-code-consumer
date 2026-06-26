---
id: playbook-obs-high-error-rate
type: playbook
title: AlertManager: Error Rate Acima do Threshold
severity: critical
status: validated
trustScore: 91
source: prometheus-oficial + sre-handbook
lastValidated: 2026-06-14
tags: ["observability", "alertmanager", "prometheus", "error-rate", "sre", "incident"]
---

## Sintoma
Alerta: `HighErrorRate` firing.
```
ALERT HighErrorRate
  IF (sum(rate(http_requests_total{status=~"5.."}[5m]))
      / sum(rate(http_requests_total[5m]))) > 0.01
  FOR 2m
LABELS { severity="critical" }
ANNOTATIONS { summary="Error rate > 1% for 2min" }
```

## Acoes Imediatas (< 5 min)

### 1. ACK no PagerDuty
- Assumir o alerta (evita duplicatas)
- Definir war room (canal Slack #incident-XXXX)

### 2. Avaliar escopo
```promql
# Quantos servicos afetados?
sum by (service) (rate(http_requests_total{status=~"5.."}[5m])) > 0

# Qual servico tem mais erros?
topk(5, sum by (service) (rate(http_requests_total{status=~"5.."}[5m])) / sum by (service) (rate(http_requests_total[5m])))
```

### 3. Verificar dependencias externas
- Database (CPU, conexoes, locks)
- Cache (Redis ping)
- Servicos externos (SEFAZ, bancos, APIs)
- Network (DNS, conectividade)

## Diagnostico

### 1. Logs do servico afetado
```bash
# Ultimos 100 ERROR
kubectl logs -n prod deploy/xforge-api --tail=100 | grep ERROR

# Ou com kubectl context
stern -n prod xforge-api --since 5m
```

### 2. Distributed traces
- Abrir Jaeger/Tempo
- Filtrar por service + status=error
- Identificar latency p99 + trace ID do pior caso

### 3. Metricas por endpoint
```promql
# Top 10 endpoints com mais 5xx
topk(10,
  sum by (path) (rate(http_requests_total{status=~"5.."}[5m]))
)
```

## Causas Comuns

### 1. Deploy novo com bug
- **Verificar**: hora do alerta coincide com deploy?
- **Acao**: rollback (se deploy recente)
- **SLA**: rollback em < 5min via blue-green (ADR-0021)

### 2. Dependencia externa fora
- **Verificar**: status de SEFAZ, gateways de pagamento, etc
- **Acao**: ativar modo degradado (retry, fallback)
- **Status page**: comunicar usuarios se > 15min

### 3. Banco de dados sobrecarregado
- **Verificar**: CPU, IOPS, locks, slow queries
- **Acao**: kill long queries, escalar read replicas
- **Mitigacao**: rate limiting por usuario

### 4. Memory leak (process reiniciando)
- **Verificar**: `process_resident_memory_bytes` subindo?
- **Acao**: restart servico, investigar dump
- **Mitigacao**: circuit breaker para evitar overload

### 5. Bot / ataque (DDoS, scraper)
- **Verificar**: padroes anomalos de IPs, user-agents
- **Acao**: ativar WAF (Cloudflare), rate limiting agressivo
- **Evidencia**: access logs + geo distribution

## Mitigacao Imediata

### 1. Rollback (se deploy < 30min)
```bash
# Blue-green
kubectl -n prod set image deploy/xforge-api xforge-api=registry/xforge:previous
# Ou
kubectl -n prod rollout undo deploy/xforge-api
```

### 2. Scale out (se load increase)
```bash
kubectl -n prod scale deploy/xforge-api --replicas=10
```

### 3. Ativar circuit breaker
```csharp
services.AddHttpClient("sefaz")
    .AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(TimeSpan.FromSeconds(5)))
    .AddPolicyHandler(Policy.BulkheadAsync<HttpResponseMessage>(100));
```

### 4. Rate limiting
```csharp
services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(httpContext =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: httpContext.User.Identity?.Name ?? httpContext.Request.Headers.Host.ToString(),
            factory: _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 100,
                Window = TimeSpan.FromMinutes(1)
            }));
});
```

## Resolucao

### 1. Identificar root cause
- Stack trace do log
- Trace distribuido do caso representativo
- Metricas correlacionadas (latency subiu ANTES do error rate?)

### 2. Aplicar fix
- Bug fix em codigo: branch + commit
- Configuracao: mudar param (rate limit, timeout)
- Infraestrutura: restart, scale

### 3. Validar
- Error rate caiu < 0.1%?
- Latency normalizou?
- Todos os endpoints OK?
- Smoke tests passaram?

### 4. Comunicar
- Status page (se > 15min)
- Canal #customers
- Email para top accounts (se impacto)

## Post-Mortem (ate 7 dias)

### 1. Blameless
- Foco no sistema, nao na pessoa
- "O que deixou isso ser possivel?" > "Quem fez?"
- Cultura de aprendizado

### 2. Template
```markdown
## Incident: HighErrorRate 2026-06-14
**Duration**: 14:32 - 15:18 (46min)
**Impact**: 0.8% requests failed (3,200 errors / 400K)
**Root cause**: Memory leak em servico de calculo fiscal
**Detection**: AlertManager (2min delay)
**Resolution**: Restart servico + scale up

## Timeline
- 14:32 - Alerta firing
- 14:35 - ACK Renato
- 14:42 - Root cause identificado
- 14:55 - Fix aplicado (restart)
- 15:18 - Alert resolved

## Action Items
- [ ] Investigar memory leak (owner: @dev, due: 2026-06-21)
- [ ] Adicionar test de memory em CI (owner: @qa, due: 2026-06-28)
- [ ] Melhorar runbook de restart (owner: @sre, due: 2026-07-05)
```

### 3. Licoes
- Adicionar a runbook
- Criar alerta preventivo (se aplicavel)
- Atualizar training da equipe
- Melhorar monitoring

## Prevencao

### 1. SLOs + Error Budgets
- Definir SLO: 99.9% success rate
- Error budget: 0.1% requests podem falhar
- Atingir budget = parar deploys nao-essenciais
- Confia no budget para tomar decisoes

### 2. Testes de Carga
- k6, Locust, NBomber
- Semana antes de deploy grande
- Simular picos de Black Friday

### 3. Chaos Engineering
- Chaos Monkey: matar instancias randomicamente
- LitmusChaos: testar failover de banco
- Game days: simular cenarios reais

### 4. Canários Longos
- 5% por 1h antes de 100% (nao 30min)
- Metricas comparadas com baseline

## Referencias
- Google SRE Book - Chapter 5: Eliminating Toil
- Google SRE Book - Chapter 6: Monitoring Distributed Systems
- Google SRE Book - Chapter 8: Release Engineering
- Prometheus AlertManager docs
- ADR-0022 XForge: Observability Stack

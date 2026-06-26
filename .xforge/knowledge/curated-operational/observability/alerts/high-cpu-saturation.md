---
id: playbook-obs-saturation-cpu
type: playbook
title: CPU Saturation - Investigar e Resolver
severity: high
status: validated
trustScore: 88
source: sre-handbook + operacao-real
lastValidated: 2026-06-14
tags: ["observability", "cpu", "saturation", "performance", "sre"]
---

## Sintoma
Alerta firing: `HighCpuSaturation`
```
ALERT HighCpuSaturation
  IF (rate(node_cpu_seconds_total{mode!="idle"}[5m]) > 0.85) > 0.9
  FOR 10m
LABELS { severity="warning" }
ANNOTATIONS { summary="CPU > 85% for 10min" }
```

## Causas Comuns

### 1. Load Increase (trafego real subiu)
- Black Friday, lancamento, campanha marketing
- Endpoint viral / compartilhamento em redes sociais
- **Sintoma**: throughput subiu, latencia estavel inicialmente
- **Fix**: scale out (horizontal scaling)

### 2. CPU-intensive code path
- Loop infinito ou mal escrito
- Recalculo excessivo (sem cache)
- Regex catastrófico (ReDoS)
- JSON parsing de payload gigante
- Criptografia/criptografia intensa
- **Sintoma**: throughput igual, latencia alta
- **Fix**: profiling, fix code, cache

### 3. Memory pressure (GC)
- Muitas alocacoes
- LOH (Large Object Heap) fragmentation
- **Sintoma**: gen2 GC frequente, pausas GC > 100ms
- **Fix**: pool arrays, Struct vs Class, evitar boxing

### 4. Thread starvation
- Thread pool exhausted
- Sync over async (`.Result` ou `.Wait()`)
- **Sintoma**: requests na fila, latency crescendo
- **Fix**: `await` em vez de `.Result`, `Task.Run` para CPU-bound

### 5. I/O wait (NAO CPU real)
- Disco lento (muitas queries)
- Network lento (chamadas externas)
- **Sintoma**: CPU alta mas tambem iowait alto
- **Fix**: query optimization, connection pooling, cache

## Diagnostico

### 1. Confirmar causa real
```bash
# top
top -bn1 | head -20

# Ver processos
ps aux --sort=-%cpu | head -10

# Load average
uptime  # load 1.0 = 100% em single-core, 2.0 em 2-core, etc
```

### 2. .NET specific
```bash
# dotnet-counters (built-in)
dotnet-counters collect -p <PID> --refresh-interval 1

# CPU usage por thread
dotnet-counters monitor -p <PID> System.Runtime

# Thread pool starvation
dotnet-counters monitor -p <PID> System.Threading
```

### 3. .NET profiler (sampling)
```bash
# dotnet-trace (built-in)
dotnet-trace collect -p <PID> --duration 00:00:30

# PerfView (GUI, mais completo)
# https://github.com/microsoft/perfview
```

### 4. Continuous profiler (producao)
- Datadog APM, New Relic, Elastic APM
- Visualiza flame graph em tempo real
- Identifica hot paths automaticamente

### 5. Database CPU
```sql
-- Postgres: top queries por CPU
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Locks (CPU alto pode ser waits)
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid
FROM pg_locks blocked_locks
JOIN pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
WHERE NOT blocked_locks.granted;
```

## Mitigacao Imediata

### 1. Scale Out (load real)
```bash
# Kubernetes
kubectl -n prod scale deploy/xforge-api --replicas=10

# Verificar se ajuda
watch kubectl -n prod top pod
```

### 2. Restart servico (rapido, mas temporario)
```bash
kubectl -n prod rollout restart deploy/xforge-api
# Perde requests em andamento, mas libera recursos
```

### 3. Drain problematic instance
```bash
# Tira 1 instancia do pool para investigacao
kubectl -n prod drain xforge-api-xyz --ignore-daemonsets
```

### 4. Kill runaway thread (last resort)
```bash
# Listar threads por CPU
ps -eLf | sort -k 4 -nr | head -10

# Kill process (CUIDADO: perde estado)
kill -9 <PID>
```

## Prevencao

### 1. Auto-scaling agressivo
```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: xforge-api
spec:
  scaleTargetRef:
    apiVersion: src/v1
    kind: Deployment
    name: xforge-api
  minReplicas: 3
  maxReplicas: 30
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # scale up antes de saturar
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
    scaleDown:
      stabilizationWindowSeconds: 300
```

### 2. Cache de CPU-intensive operations
```csharp
services.AddMemoryCache();

// Cache de calculo pesado
public async Task<RelatorioFiscal> GerarRelatorio(int mes, int ano)
{
    var key = $"relatorio:{mes}:{ano}";
    return await _cache.GetOrCreateAsync(key, async entry =>
    {
        entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1);
        return await GerarRelatorioInterno(mes, ano);
    });
}
```

### 3. Async/await correto (evitar thread starvation)
```csharp
// RUIM
public ActionResult Get(int id)
{
    var data = _service.GetAsync(id).Result;  // deadlock risk!
    return Ok(data);
}

// BOM
public async Task<ActionResult> Get(int id)
{
    var data = await _service.GetAsync(id);
    return Ok(data);
}
```

### 4. Code review checklist
- [ ] Sem `.Result` ou `.Wait()` em codigo async
- [ ] Sem loops infinitos
- [ ] Sem recursao sem caso base
- [ ] Operacoes CPU-bound em `Task.Run` se bloqueantes
- [ ] Profiling em pre-release (codepath > 100ms)

### 5. Performance testing
- NBomber / k6 / Locust
- CI: rodar smoke test de perf
- Carga: 2x pico normal, ver degradação
- Soak: 1h sustentado, ver memory/CPU growth

## Caso Real (2025-03)
Black Friday, 5x trafego normal. CPU 95% sustentado, latency p95 = 8s.
**Root cause**: 
1. Auto-scaling nao configurado (sempre 3 replicas)
2. Recalculo de precos sem cache (cada request recalculava 50ms)
**Fix**:
1. HPA com min 3, max 30
2. Cache de 1h para tabela de precos
**Resultado**: latency p95 voltou a 200ms, CPU 60% com 8 replicas.

## Metricas por Camada

| Camada | CPU Normal | CPU Alerta | CPU Critico |
|--------|:----------:|:----------:|:-----------:|
| App server | 40-60% | 70% | 85%+ |
| Database | 30-50% | 70% | 85%+ |
| Cache (Redis) | 10-30% | 50% | 70%+ |
| Load balancer | 5-15% | 30% | 50%+ |

## Referencias
- Google SRE Book - Chapter 5: Eliminating Toil
- Brendan Gregg - CPU Performance
- ADR-0022 XForge: Observability
- Polly resilience patterns
- .NET: dotnet-counters, dotnet-trace
- Kubernetes: HPA, Cluster Autoscaler

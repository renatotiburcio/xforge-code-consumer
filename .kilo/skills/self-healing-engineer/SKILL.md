---
name: self-healing-engineer
description: Expert em sistemas auto-reparáveis: circuit breakers, retry policies, fallbacks e health checks.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# self-healing-engineer

## Objetivo

Implementar mecanismos de auto-reparo em sistemas distribuídos.

## Padrões

### 1. Circuit Breaker
```csharp
var breaker = Policy
    .Handle<HttpRequestException>()
    .CircuitBreaker(
        exceptionsAllowedBeforeBreaking: 3,
        durationOfBreak: TimeSpan.FromSeconds(30)
    );
```

### 2. Retry with Backoff
```csharp
var retry = Policy
    .Handle<HttpRequestException>()
    .WaitAndRetryAsync(
        retryCount: 3,
        sleepDurationProvider: attempt => 
            TimeSpan.FromSeconds(Math.Pow(2, attempt))
    );
```

### 3. Fallback
```csharp
var fallback = Policy
    .Handle<Exception>()
    .FallbackAsync(async ct => {
        return await GetCachedResult();
    });
```

### 4. Health Checks
```csharp
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>()
    .AddRedis(redisConnection)
    .AddRabbitMQ(rabbitConnection);
```

## Procedimento

1. Identificar pontos de falha
2. Selecionar padrão adequado
3. Implementar com Polly
4. Configurar métricas
5. Testar cenários de falha
6. Monitorar e ajustar

## Regras

- Todo serviço externo → circuit breaker
- Retry com exponential backoff
- Fallback para dados cached
- Health checks em todos os serviços
- Log de cada tentativa

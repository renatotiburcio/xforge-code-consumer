---
id: playbook-dotnet-circuit-breaker
type: playbook
title: .NET Circuit Breaker + Retry + Fallback com Polly
severity: medium
status: validated
trustScore: 91
source: polly-docs + operacao-real
lastValidated: 2026-06-14
tags: ["dotnet", "resilience", "polly", "circuit-breaker", "retry", "fallback"]
---

## Quando Usar
- Chamadas para servicos externos (SEFAZ, gateways pagamento, APIs terceiros)
- Operacoes que podem falhar transitoriamente (network blip, timeout)
- Evitar cascading failures (1 servico lento derruba todos)

## Os 3 Padroes Essenciais

### 1. Retry (tentar de novo)
Para falhas transitorias (timeout, 5xx).

```csharp
services.AddHttpClient<ISefazClient>()
    .AddPolicyHandler(HttpPolicyExtensions
        .HandleTransientHttpError()  // 5xx, 408, network errors
        .Or<TimeoutException>()
        .WaitAndRetryAsync(3, attempt => 
            TimeSpan.FromSeconds(Math.Pow(2, attempt)),  // 2s, 4s, 8s
            onRetry: (outcome, delay, attempt, ctx) =>
            {
                _logger.LogWarning(
                    "Retry {Attempt} after {Delay}s due to {Error}",
                    attempt, delay.TotalSeconds, outcome.Exception?.Message);
            }));
```

### 2. Circuit Breaker (abrir o circuito)
Para evitar hammering em servico que esta down.

```csharp
var circuitBreaker = HttpPolicyExtensions
    .HandleTransientHttpError()
    .CircuitBreakerAsync(
        handledEventsAllowedBeforeBreaking: 5,  // 5 falhas seguidas
        durationOfBreak: TimeSpan.FromSeconds(30),  // aberto por 30s
        onBreak: (outcome, breakDelay) =>
        {
            _logger.LogError("Circuit OPENED for {Delay}s", breakDelay.TotalSeconds);
            _metrics.IncrementCounter("circuit_breaker.open");
        },
        onReset: () =>
        {
            _logger.LogInformation("Circuit RESET");
            _metrics.IncrementCounter("circuit_breaker.reset");
        },
        onHalfOpen: () => _logger.LogInformation("Circuit HALF-OPEN"));

services.AddHttpClient<ISefazClient>()
    .AddPolicyHandler(circuitBreaker);
```

### 3. Fallback (resposta alternativa)
Quando o servico primario falha, usar plano B.

```csharp
var fallback = Policy<HttpResponseMessage>
    .Handle<BrokenCircuitException>()
    .OrTransientHttpError()
    .FallbackAsync(
        fallbackValue: new HttpResponseMessage(System.Net.HttpStatusCode.OK)
        {
            Content = new StringContent(
                "{"status":"degraded","cached":true}")
        },
        onFallbackAsync: (outcome, ctx) =>
        {
            _logger.LogWarning("Using fallback for {Uri}", ctx.OperationKey);
            return Task.CompletedTask;
        });

services.AddHttpClient<ISefazClient>()
    .AddPolicyHandler(fallback);
```

## Combinando os 3

```csharp
services.AddHttpClient<ISefazClient>(c =>
{
    c.BaseAddress = new Uri("https://sefaz.example.com");
    c.Timeout = TimeSpan.FromSeconds(10);
})
.AddPolicyHandler(retryPolicy)          // 1. Retry primeiro (3x)
.AddPolicyHandler(circuitBreakerPolicy)  // 2. Circuit breaker
.AddPolicyHandler(timeoutPolicy)         // 3. Timeout
.AddPolicyHandler(fallbackPolicy);       // 4. Fallback ultimo
```

Ordem importa: outermost (retry) wraps innermost (fallback). Fluxo:
1. Request
2. Timeout (10s) corta se demorar
3. Circuit breaker verifica se pode chamar
4. Retry tenta 3x se falhar transitoria
5. Fallback retorna cache se tudo falhar

## Politica por Tipo de Servico

### SEFAZ (fiscal)
- Timeout: 10s
- Retry: 3x com backoff 2s/4s/8s
- Circuit breaker: 5 falhas em 30s
- Fallback: contingencia SVC-AN

```csharp
.AddPolicyHandler(retrySefaz)
.AddPolicyHandler(circuitBreakerSefaz)
.AddPolicyHandler(fallbackSefaz);  // contingencia
```

### Gateway Pagamento
- Timeout: 30s
- Retry: 2x com backoff 1s/2s (NAO 3x - cliente esperando)
- Circuit breaker: 3 falhas em 60s
- Fallback: enqueue + retry async

```csharp
.AddPolicyHandler(retryPayment)
.AddPolicyHandler(circuitBreakerPayment);
```

### Database (EF Core)
- **NAO usar retry implicito** (transaction state)
- Usar Polly com cuidado em transacoes
- Timeout: 5s

```csharp
.AddPolicyHandler(retryDb);
// CUIDADO: nao usar em transacoes longas!
```

## Bulkhead (isolamento de recursos)
Evita que 1 servico lento consuma todos os recursos.

```csharp
var bulkhead = Policy.BulkheadAsync<HttpResponseMessage>(
    maxParallelization: 50,    // max 50 chamadas simultaneas
    maxQueuingActions: 100);   // max 100 enfileiradas

services.AddHttpClient<ISefazClient>()
    .AddPolicyHandler(bulkhead);
```

## Timeout vs CancellationToken
- **HttpClient.Timeout**: timeout TOTAL da request
- **CancellationToken**: propaga cancelamento

```csharp
public async Task<Nfe> EmitirNfeAsync(Nfe nfe, CancellationToken ct)
{
    var response = await _httpClient.PostAsJsonAsync("nfe", nfe, ct);
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadFromJsonAsync<Nfe>(cancellationToken: ct);
}
```

## Health Check + Circuit Breaker

Combinar com health check para tirar servicos down do pool.

```csharp
services.AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("db")
    .AddUrlGroup(new Uri("https://sefaz.example.com/health"), "sefaz");
```

## Caso Real (2024-07)
Marketplace integrado a 5 gateways de pagamento. 1 gateway com problema.
50% das tentativas de pagamento falhavam. Carga no sistema subiu 5x (retries sem circuit breaker).
**Custo**: 30min de degradacao, R$ 50K em vendas perdidas.
**Fix**: implementar circuit breaker (5 falhas = abrir 30s).
**Resultado**: 99.5% success rate, latency p95 caiu de 8s para 2s.

## Monitoramento

```csharp
public class CircuitBreakerMetrics
{
    public void IncrementOpened() => Counter("circuit_breaker.opened").Increment();
    public void IncrementReset() => Counter("circuit_breaker.reset").Increment();
    public void IncrementRejected() => Counter("circuit_breaker.rejected").Increment();
    public TimeSpan CurrentBreakDuration() => _currentBreakDuration;
}
```

Alertas:
- Circuit breaker open > 5min: P2
- 3+ servicos com circuit aberto simultaneo: P1
- Fallback ativado > 10% das chamadas: P3

## Testes

### Unit Test com Polly
```csharp
[Fact]
public async Task Retry_3x_ThenSuccess()
{
    var policy = HttpPolicyExtensions.HandleTransientHttpError()
        .WaitAndRetryAsync(3, _ => TimeSpan.FromMilliseconds(10));
    
    var calls = 0;
    var handler = new Mock<HttpMessageHandler>();
    handler.SetupAnyRequest()
        .Returns<HttpRequestMessage, CancellationToken>((req, ct) =>
        {
            calls++;
            if (calls < 3) return Task.FromResult(new HttpResponseMessage(503));
            return Task.FromResult(new HttpResponseMessage(200));
        });
    
    var client = new HttpClient(handler.Object);
    var response = await client.GetAsync("http://test");
    Assert.Equal(3, calls);
    Assert.Equal(200, response.StatusCode);
}
```

### Chaos Testing
```csharp
[Fact]
public async Task CircuitBreaker_OpensAfter5Failures()
{
    var failures = 0;
    var handler = new Mock<HttpMessageHandler>();
    handler.SetupAnyRequest()
        .Returns(() => Task.FromResult(new HttpResponseMessage(503)));
    
    var client = new HttpClient(handler.Object);
    var policy = HttpPolicyExtensions.HandleTransientHttpError()
        .CircuitBreakerAsync(5, TimeSpan.FromSeconds(1));
    
    for (int i = 0; i < 5; i++)
        await client.GetAsync("http://test");  // 5 falhas
    
    await Assert.ThrowsAsync<BrokenCircuitException>(
        () => client.GetAsync("http://test"));  // 6a falha eh rejeitada
}
```

## Referencias
- Polly: https://www.pollydocs.org/
- Microsoft.Extensions.Resilience (.NET 8+)
- ADR-0025 XForge: API Gateway
- ADR-0022 XForge: Observability
- Release It! (Michael Nygard) - Stability Patterns

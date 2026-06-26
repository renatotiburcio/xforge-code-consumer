---
name: wiremock-contract-testing-expert
description: Expert em testes de contrato com WireMock: simulação de APIs, stubs, verificação de contratos.
metadata:
  version: "7.0.0"
  xforge-category: "testing"
---

# wiremock-contract-testing-expert

## Objetivo

Testar integrações com APIs externas usando simulação.

## Quando Usar

- API externa indisponível em dev/test
- Testar cenários de erro (500, timeout)
- Testar contratos entre equipes
- Isolar dependências externas

## Configuração

```csharp
var wireMock = WireMockServer.Start(new WireMockServerSettings
{
    Port = 8080,
    StartAdminInterface = true
});

wireMock
    .Given(Request.Create()
        .WithPath("/api/users")
        .UsingGet())
    .RespondWith(Response.Create()
        .WithStatusCode(200)
        .WithHeader("Content-Type", "application/json")
        .WithBodyAsJson(new[] { new { id = 1, name = "Test" } }));
```

## Cenários

| Cenário | Status Code | Uso |
|---------|:-----------:|-----|
| Sucesso | 200/201 | Fluxo principal |
| Não encontrado | 404 | Resource missing |
| Validação | 400 | Input inválido |
| Não autorizado | 401/403 | Auth failure |
| Erro servidor | 500 | Retry/circuit breaker |
| Timeout | — | Timeouts, degraded |

## Procedimento

1. Identificar API externa
2. Criar stubs para cada cenário
3. Configurar testes de contrato
4. Rodar testes
5. Verificar contratos
6. Documentar divergências

## Regras

- Stubs devem espelhar API real
- Testar happy path E error paths
- Atualizar stubs quando API muda
- Versionar contratos

---
name: testcontainers-integration-testing-expert
description: Expert em testes de integração com TestContainers: bancos, filas, cache em containers Docker.
metadata:
  version: "7.0.0"
  xforge-category: "testing"
---

# testcontainers-integration-testing-expert

## Objetivo

Testar integrações com infraestrutura real usando containers Docker.

## Containers Suportados

| Container | Pacote NuGet | Uso |
|-----------|-------------|-----|
| PostgreSQL | Testcontainers.PostgreSql | Banco relacional |
| Redis | Testcontainers.Redis | Cache |
| RabbitMQ | Testcontainers.RabbitMQ | Filas |
| MongoDB | Testcontainers.MongoDb | NoSQL |
| Elasticsearch | Testcontainers.Elasticsearch | Busca |

## Configuração

```csharp
var postgres = new PostgreSqlBuilder()
    .WithImage("postgres:16")
    .WithDatabase("testdb")
    .WithUsername("test")
    .WithPassword("test")
    .Build();

await postgres.StartAsync();

var connectionString = postgres.GetConnectionString();
```

## Procedimento

1. Identificar dependência de infra
2. Criar container correspondente
3. Configurar connection string
4. Rodar migration
5. Executar testes
6. Cleanup automático

## Regras

- Containers devem ser efêmeros
- Cleanup automático após teste
- NUNCA usar dados de produção
- Versionar imagens Docker

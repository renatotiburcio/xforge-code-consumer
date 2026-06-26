---
id: logging
type: pattern
tags: [logging, serilog, structured-logging, seq, enrichers, sinks]
owner: project-team
version: "1.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Logging Estruturado com Serilog
- **Seções principais**: Propósito, Descrição do Padrão, Quando Usar, Exemplo de Uso
- **Tags**: logging, serilog, structured-logging, seq, enrichers, sinks
- **Tipo**: pattern | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `logging` |
| Tipo | pattern |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Logging Estruturado com Serilog

## Propósito

Padronizar o logging estruturado em sistemas ERP usando Serilog, cobrindo enrichers, sinks (console, arquivo, Seq), correlation IDs, níveis de log e mascaramento de dados sensíveis.

## Descrição do Padrão

### Configuração via appsettings.json

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "Microsoft.EntityFrameworkCore": "Warning"
      }
    },
    "WriteTo": [
      { "Name": "Console" },
      { "Name": "File", "Args": { "path": "logs/meuerp-.log", "rollingInterval": "Day", "retainedFileCountLimit": 30 } },
      { "Name": "Seq", "Args": { "serverUrl": "http://localhost:5341" } }
    ],
    "Enrich": ["FromLogContext", "WithMachineName", "WithThreadId"],
    "Properties": { "Application": "MeuERP", "Environment": "Production" }
  }
}
```

### Uso nos Serviços

```csharp
public class NfeService : INfeService
{
    private readonly ILogger<NfeService> _logger;

    public async Task<NfeResponse> EmitirNfe(NfeRequest request)
    {
        _logger.LogInformation("Emitindo NF-e para cliente {ClienteId} com {Itens} itens",
            request.ClienteId, request.Itens.Count);

        try
        {
            var nfe = await ProcessarNfe(request);
            _logger.LogInformation("NF-e {NfeNumero} emitida. Chave: {Chave}",
                nfe.Numero, nfe.ChaveAcesso);
            return nfe;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Erro ao emitir NF-e para cliente {ClienteId}", request.ClienteId);
            throw;
        }
    }
}
```

### Enrichers

```csharp
.Enrich.FromLogContext()        // Propriedades do contexto (CorrelationId)
.Enrich.WithMachineName()       // Nome da máquina
.Enrich.WithThreadId()          // ID da thread
.Enrich.WithEnvironmentName()   // Ambiente (Development/Production)

// Enricher customizado para multi-tenancy
public class TenantEnricher : ILogEventEnricher
{
    public void Enrich(LogEvent logEvent, ILogEventPropertyFactory factory)
    {
        var tenantId = TenantContext.Current?.TenantId ?? "system";
        logEvent.AddPropertyIfAbsent(factory.CreateProperty("TenantId", tenantId));
    }
}
```

### Correlation ID

```csharp
// Middleware para adicionar CorrelationId
app.Use(async (context, next) =>
{
    var correlationId = context.Request.Headers["X-Correlation-Id"].FirstOrDefault()
        ?? Guid.NewGuid().ToString();
    using (LogContext.PushProperty("CorrelationId", correlationId))
    {
        context.Response.Headers["X-Correlation-Id"] = correlationId;
        await next();
    }
});
```

### Auditoria

```csharp
public class AuditLogger
{
    public void LogCriacao(string entidade, int id, string usuario, object dados)
    {
        _logger.LogInformation("AUDIT | CREATE | {Entidade} | Id: {Id} | Usuario: {Usuario} | Dados: {@Dados}",
            entidade, id, usuario, dados);
    }

    public void LogAlteracao(string entidade, int id, string usuario, object antes, object depois)
    {
        _logger.LogInformation("AUDIT | UPDATE | {Entidade} | Id: {Id} | Antes: {@Antes} | Depois: {@Depois}",
            entidade, id, usuario, antes, depois);
    }
}
```

### Mascaramento de Dados Sensíveis

```csharp
public static class LogMasker
{
    public static string MaskEmail(string email)
    {
        if (string.IsNullOrEmpty(email) || !email.Contains('@')) return "***";
        var parts = email.Split('@');
        var name = parts[0];
        var masked = name.Length <= 2 ? new string('*', name.Length)
            : name[..2] + new string('*', name.Length - 2);
        return $"{masked}@{parts[1]}";
    }

    public static string MaskCpf(string cpf) =>
        string.IsNullOrEmpty(cpf) || cpf.Length < 4 ? "***"
        : $"***.***.***-{cpf[^2..]}";
}
```

### Níveis de Log

| Nível | Uso |
|-------|-----|
| `Debug` | Desenvolvimento, diagnóstico detalhado |
| `Information` | Operações normais (criação, atualização) |
| `Warning` | Situações inesperadas mas recuperáveis |
| `Error` | Falhas em operações (catch de exceção) |
| `Fatal` | Falha crítica da aplicação |

## Quando Usar

- Toda operação de negócio deve ter log estruturado.
- Auditoria de operações críticas (criação, alteração, exclusão).
- Diagnóstico de erros em produção via Seq/ELK.
- Rastreamento de requisições com CorrelationId.

## Exemplo de Uso

```csharp
_logger.LogInformation("Pedido {PedidoId} criado por {Usuario} com {Itens} itens. Total: {Total}",
    pedido.Id, usuario.Nome, pedido.Itens.Count, pedido.ValorTotal);
```

## Padrões Relacionados

- [[seguranca-api.md]] — log de autenticação e autorização negada
- [[autenticacao-autorizacao.md]] — auditoria de login
- [[ef-core-patterns.md]] — diagnóstico de queries lentas


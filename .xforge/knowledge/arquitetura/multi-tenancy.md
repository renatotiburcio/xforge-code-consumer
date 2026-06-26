---
id: multi-tenancy
type: knowledge
tags: [multi-tenancy, erp, saas, isolamento, tenant, dotnet, ef-core]
owner: project-team
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Multi-Tenancy
- **Principais responsabilidades**: Garantir isolamento lógico de dados entre tenants; Resolver o tenant atual por subdomínio, header, JWT ou path; Aplicar global query filters no EF ...
- **Seções principais**: Propósito, Responsabilidades, Estratégias de Isolamento, Modelo Hibrido Recomendado
- **Tags**: multi-tenancy, erp, saas, isolamento, tenant, dotnet, ef-core
- **Tipo**: knowledge | **Versão**: 1.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `multi-tenancy` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 12 |


# Multi-Tenancy

## Propósito
Definir a estratégia de multi-tenancy para o ERP SaaS, garantindo isolamento de dados entre tenants (empresas/clientes) que compartilham a mesma instância da aplicação.

## Responsabilidades
- Garantir isolamento lógico de dados entre tenants
- Resolver o tenant atual por subdomínio, header, JWT ou path
- Aplicar global query filters no EF Core
- Gerenciar connection strings para tenants dedicados

## Estratégias de Isolamento

| Critério | DB por Tenant | Schema por Tenant | Shared + TenantId |
|----------|:---:|:---:|:---:|
| Isolamento de dados | ★★★★★ | ★★★★ | ★★★ |
| Custo de infra | ★ | ★★★ | ★★★★★ |
| Facilidade de migração | ★★ | ★★ | ★★★★★ |
| Performance previsível | ★★★★★ | ★★★★ | ★★★ |
| Cross-tenant queries | ★ | ★★★★ | ★★★★★ |
| Escalabilidade | ★★ | ★★★ | ★★★★★ |

## Modelo Hibrido Recomendado

```
+-------------------------------------------------------------+
|  SHARED DATABASE (maioria dos tenants)                       |
|  - Pequenas e médias empresas                                |
|  - Isolamento via TenantId + Global Query Filters            |
+-------------------------------------------------------------+
|  DEDICATED DATABASE (tenants enterprise)                     |
|  - Grandes empresas com alto volume                          |
|  - Requisitos de compliance específicos                      |
+-------------------------------------------------------------+
```

```csharp
public enum TenantIsolationLevel { Shared, Dedicated, Premium }

public class Tenant {
    public Guid Id { get; set; }
    public string Subdomain { get; set; } = string.Empty;
    public TenantIsolationLevel IsolationLevel { get; set; }
    public string? ConnectionString { get; set; } // null = shared DB
    public Guid PlanoId { get; set; }
    public bool Ativo { get; set; }
}
```

## Entidade Base e Global Query Filters

```csharp
public abstract class TenantEntity {
    public Guid TenantId { get; set; }
    public Tenant Tenant { get; set; } = null!;
}

// No DbContext
protected override void OnModelCreating(ModelBuilder modelBuilder) {
    foreach (var entityType in modelBuilder.Model.GetEntityTypes()) {
        if (typeof(TenantEntity).IsAssignableFrom(entityType.ClrType)) {
            var method = typeof(ErpDbContext)
                .GetMethod(nameof(SetTenantFilter), BindingFlags.NonPublic | BindingFlags.Static)!
                .MakeGenericMethod(entityType.ClrType);
            method.Invoke(null, new object[] { modelBuilder, _tenantContext });
        }
    }
}

private static void SetTenantFilter<TEntity>(ModelBuilder builder, ITenantContext ctx)
    where TEntity : TenantEntity {
    builder.Entity<TEntity>().HasQueryFilter(e => e.TenantId == ctx.CurrentTenantId);
}
```

## Resolução de Tenant

```csharp
public class CompositeTenantResolver : ITenantResolver {
    private readonly List<ITenantResolver> _resolvers = new() {
        new SubdomainTenantResolver(),  // empresa1.erp.com.br
        new HeaderTenantResolver(),     // X-Tenant-ID: uuid
        new JwtTenantResolver(),        // claim tenant_id no JWT
        new PathTenantResolver(),       // /api/{tenant}/...
        new QueryStringTenantResolver() // ?tenant=xxx
    };

    public async Task<Tenant?> ResolveAsync(HttpContext ctx) {
        foreach (var r in _resolvers) {
            var t = await r.ResolveAsync(ctx);
            if (t is not null) return t;
        }
        return null;
    }
}
```

## Validação de Segurança

```csharp
// Interceptor que valida tenant em cada SaveChanges
public class TenantValidationInterceptor : SaveChangesInterceptor {
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData, InterceptionResult<int> result, CancellationToken ct = default) {
        var entries = eventData.Context!.ChangeTracker.Entries<TenantEntity>();
        foreach (var entry in entries) {
            if (entry.Entity.TenantId != _tenantContext.CurrentTenantId)
                throw new TenantAccessException(
                    $"Entidade do tenant {entry.Entity.TenantId} acessada por {_tenantContext.CurrentTenantId}");
        }
        return base.SavingChangesAsync(eventData, result, ct);
    }
}
```

## Row-Level Security (SQL Server)

```sql
CREATE FUNCTION dbo.fn_TenantAccessPredicate(@TenantId UNIQUEIDENTIFIER)
RETURNS TABLE WITH SCHEMABINDING
AS RETURN SELECT 1 AS AccessResult
WHERE @TenantId = CAST(SESSION_CONTEXT(N'TenantId') AS UNIQUEIDENTIFIER);

CREATE SECURITY POLICY dbo.TenantFilterPolicy
ADD FILTER PREDICATE dbo.fn_TenantAccessPredicate(TenantId) ON dbo.Empresas,
ADD FILTER PREDICATE dbo.fn_TenantAccessPredicate(TenantId) ON dbo.NotasFiscais
WITH (STATE = ON);
```

## Cache Isolado por Tenant

```csharp
public class TenantCacheService {
    private readonly IDistributedCache _cache;
    private string TenantKey(string key, Guid tenantId) => $"t:{tenantId:N}:{key}";

    public async Task<T?> GetAsync<T>(string key, Guid tenantId, CancellationToken ct = default) {
        var data = await _cache.GetAsync(TenantKey(key, tenantId), ct);
        return data is null ? default : JsonSerializer.Deserialize<T>(data);
    }
}
```

## Hierarquia de Tenants

```
TENANT (Conta/Organização)
|-- Empresa (CNPJ: 11.222.333/0001-44)
|   |-- Filial 1 (CNPJ: 11.222.333/0002-25)
|   |-- Filial 2 (CNPJ: 11.222.333/0003-06)
|-- Empresa 2 (CNPJ: 44.555.666/0001-77) [Holding]
|-- Autônomo (CPF: 123.456.789-00)
`-- Escritório Contábil (gerencia múltiplos tenants)
```

## Dependências
- [clean-architecture.md](clean-architecture.md) — Camada Domain com TenantEntity
- [deploy-net.md](deploy-net.md) — Deploy de migrations multi-tenant
- [observabilidade.md](observabilidade.md) — Logs com enricher de TenantId

## Restrições
- Dados NUNCA devem vazar entre tenants — regra mais crítica
- Todas as queries devem filtrar por TenantId (global query filter + validação explícita)
- Cache deve ser escopado por tenant
- Connection strings de tenants dedicados ficam no TenantStore com cache


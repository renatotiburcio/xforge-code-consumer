---
id: multi-tenant-architecture
type: conhecimento
tags: [multi-tenant, arquitetura, shared-database, rls, saas]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Padrões de Multi-Tenancy para aplicações SaaS com .NET
- **Seções principais**: Modelos, Shared Database + RLS, Discriminator, Isolamento
- **Tags**: multi-tenant, arquitetura, shared-database, rls, saas

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| Modelo padrão | Shared Database + Discriminator |
| Isolamento dados | TenantId em todas as tabelas |
| RLS | PostgreSQL Row-Level Security |
| EF Core | Filtro global HasQueryFilter |

# Multi-Tenant Architecture Patterns

## Modelos de Multi-Tenancy

### 1. Shared Database, Shared Schema (Recomendado para XForge)
- Todos os tenants na mesma tabela
- Coluna `TenantId` em todas as tabelas
- Filtro automático via EF Core
- Mais simples, menor custo, mais fácil de manter

### 2. Shared Database, Separate Schema
- Um schema por tenant
- Mais isolamento, mas mais complexo
- Adequado para compliance rígido

### 3. Separate Database
- Um banco por tenant
- Máximo isolamento
- Alto custo operacional

## Implementação com EF Core

### Entity Base

```csharp
public abstract class TenantEntity
{
    public Guid TenantId { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public bool IsDeleted { get; set; }
}
```

### DbContext com Filtro Global

```csharp
public class XForgeDbContext : DbContext
{
    private readonly ITenantService _tenantService;

    public XForgeDbContext(DbContextOptions options, ITenantService tenantService)
        : base(options)
    {
        _tenantService = tenantService;
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Filtro global: só retorna dados do tenant atual
        foreach (var entityType in modelBuilder.Model.GetEntityTypes())
        {
            if (typeof(TenantEntity).IsAssignableFrom(entityType.ClrType))
            {
                modelBuilder.Entity(entityType.ClrType)
                    .HasQueryFilter(CreateTenantFilter(entityType.ClrType));
            }
        }
    }

    private LambdaExpression CreateTenantFilter(Type entityType)
    {
        var parameter = Expression.Parameter(entityType, "e");
        var property = Expression.Property(parameter, "TenantId");
        var tenantId = Expression.Constant(_tenantService.GetCurrentTenantId());
        var comparison = Expression.Equal(property, tenantId);
        return Expression.Lambda(comparison, parameter);
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        foreach (var entry in ChangeTracker.Entries<TenantEntity>())
        {
            if (entry.State == EntityState.Added)
            {
                entry.Entity.TenantId = _tenantService.GetCurrentTenantId();
            }
        }
        return await base.SaveChangesAsync(cancellationToken);
    }
}
```

### Tenant Service

```csharp
public interface ITenantService
{
    Guid GetCurrentTenantId();
    void SetCurrentTenantId(Guid tenantId);
}

public class TenantService : ITenantService
{
    private readonly IHttpContextAccessor _httpContextAccessor;
    private Guid _currentTenantId;

    public TenantService(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public Guid GetCurrentTenantId()
    {
        // Extrair do JWT, header, ou subdomain
        var tenantClaim = _httpContextAccessor.HttpContext?.User?.FindFirst("tenant_id");
        if (tenantClaim != null && Guid.TryParse(tenantClaim.Value, out var tenantId))
        {
            return tenantId;
        }
        return _currentTenantId;
    }

    public void SetCurrentTenantId(Guid tenantId)
    {
        _currentTenantId = tenantId;
    }
}
```

## PostgreSQL Row-Level Security (RLS)

```sql
-- Habilitar RLS na tabela
ALTER TABLE Produtos ENABLE ROW LEVEL SECURITY;

-- Criar política
CREATE POLICY tenant_isolation ON Produtos
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- No EF Core, definir a variável de sessão
-- ctx.Database.ExecuteSqlRaw("SET app.current_tenant_id = '{tenantId}'");
```

## Migração de Dados

```sql
-- Adicionar coluna TenantId em todas as tabelas existentes
ALTER TABLE Produtos ADD COLUMN tenant_id UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001';
ALTER TABLE Clientes ADD COLUMN tenant_id UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001';
ALTER TABLE Pedidos ADD COLUMN tenant_id UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001';

-- Criar índices
CREATE INDEX idx_produtos_tenant ON Produtos(tenant_id);
CREATE INDEX idx_clientes_tenant ON Clientes(tenant_id);
CREATE INDEX idx_pedidos_tenant ON Pedidos(tenant_id);
```

## Validação por Tenant

```csharp
// Service que valida acesso ao tenant
public class TenantValidator
{
    public void ValidateAccess(TenantEntity entity, Guid currentTenantId)
    {
        if (entity.TenantId != currentTenantId)
        {
            throw new UnauthorizedAccessException("Acesso negado: tenant não autorizado");
        }
    }
}
```

## Considerações

1. **Backup por tenant**: Ferramentas de backup devem suportar backup/restauração individual por tenant
2. **Migrações**: Scripts de migração devem ser executados para todos os tenants
3. **Performance**: Índices em `tenant_id` são obrigatórios
4. **Cache**: Cache deve ser partitionado por tenant
5. **Rate limiting**: Limites devem ser por tenant, não por IP

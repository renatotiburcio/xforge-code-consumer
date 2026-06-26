---
name: postgresql-efcore-expert
description: Expert em PostgreSQL com EF Core: migrations, queries, performance, partitioning e extensions.
metadata:
  version: "7.0.0"
  xforge-category: "technical-expert"
---

# postgresql-efcore-expert

## Objetivo

Otimizar e configurar PostgreSQL com EF Core.

## Configuração

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString, npgsql =>
    {
        npgsql.MigrationsAssembly("Infrastructure");
        npgsql.EnableRetryOnFailure(3);
        npgsql.CommandTimeout(30);
    }));
```

## Best Practices

### Migrations
- Uma migration por feature
- Nome descritivo: `Add_Auth_Table`
- Down migration sempre implementada
- Testar em banco limpo

### Queries
- Use `.AsNoTracking()` para reads
- Use `.Select()` para projetar apenas campos necessários
- Evite `.Include()` em loops
- Use `.SplitQuery()` para múltiplos includes

### Performance
```csharp
// ✅ OK
var users = await context.Users
    .AsNoTracking()
    .Where(u => u.Active)
    .Select(u => new { u.Id, u.Name })
    .ToListAsync();

// ❌ RUIM
var users = await context.Users
    .Include(u => u.Orders)
    .Include(u => u.Addresses)
    .ToListAsync();
```

### Indexes
```csharp
entity.HasIndex(e => e.Email).IsUnique();
entity.HasIndex(e => new { e.Status, e.CreatedAt });
```

## Procedimento

1. Configurar connection string
2. Criar migrations
3. Otimizar queries
4. Adicionar indexes
5. Testar performance
6. Monitorar em produção

## Regras

- NUNCA use raw SQL sem parameterização
- Sempre AsNoTracking para reads
- Migration testada em banco limpo
- Index para foreign keys

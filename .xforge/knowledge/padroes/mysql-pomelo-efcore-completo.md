---
id: mysql-pomelo-efcore-completo
type: conhecimento
tags: [mysql, pomelo, ef-core, migrations, performance, charset, utf8mb4]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre MySQL com Pomelo EF Core - Completo
- **Seções principais**: Conceito, Setup, Conexão, Entity Configuration
- **Tags**: mysql, pomelo, ef-core, migrations, performance, charset, utf8mb4
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `mysql-pomelo-efcore-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 15 |


# MySQL com Pomelo EF Core - Completo

## Conceito

Pomelo.EntityFrameworkCore.MySql é o provider MySQL para EF Core, suportando todas as funcionalidades do EF Core com MySQL.

## Setup

```csharp
// Program.cs
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseMySql(
        builder.Configuration.GetConnectionString("DefaultConnection"),
        ServerVersion.AutoDetect(builder.Configuration.GetConnectionString("DefaultConnection")),
        mySqlOptions =>
        {
            mySqlOptions.MigrationsAssembly("Infrastructure");
            mySqlOptions.EnableRetryOnFailure(3, TimeSpan.FromSeconds(5), null);
            mySqlOptions.CommandTimeout(30);
            mySqlOptions.CharSetBehavior(CharSetBehavior.NeverAppend);
        }));
```

## Conexão

```json
// appsettings.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Port=3306;Database=mydb;User=root;Password=password;SslMode=Preferred;"
  }
}
```

### Parâmetros Importantes

| Parâmetro | Descrição |
|-----------|-----------|
| `Server` | Host do MySQL |
| `Port` | Porta (padrão 3306) |
| `Database` | Nome do banco |
| `User` | Usuário |
| `Password` | Senha |
| `SslMode` | None, Preferred, Required, VerifyCA, VerifyFull |
| `AllowPublicKeyRetrieval` | true para Some SSL |
| `ConnectionTimeout` | Timeout de conexão |

## Entity Configuration

```csharp
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.ToTable("products");
        
        builder.HasKey(e => e.Id);
        
        builder.Property(e => e.Name)
            .HasMaxLength(200)
            .IsRequired()
            .HasColumnType("varchar(200) CHARACTER SET utf8mb4");
        
        builder.Property(e => e.Price)
            .HasColumnType("decimal(18,2)");
        
        builder.Property(e => e.Description)
            .HasColumnType("text");
        
        builder.HasIndex(e => e.Name)
            .IsUnique();
        
        builder.HasOne(e => e.Category)
            .WithMany(c => c.Products)
            .HasForeignKey(e => e.CategoryId)
            .OnDelete(DeleteBehavior.Restrict);
    }
}
```

## UTF-8

```csharp
// Configuração global
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseMySql(connectionString, serverVersion, mySql =>
    {
        mySql.CharSetBehavior(CharSetBehavior.NeverAppend);
    }));

// Por tabela
builder.ToTable("products", "utf8mb4");

// Por coluna
builder.Property(e => e.Name)
    .HasColumnType("varchar(200) CHARACTER SET utf8mb4_unicode_ci");
```

## Migrations

```bash
# Criar migration
dotnet ef migrations add AddProductTable

# Listar migrations
dotnet ef migrations list

# Remover última migration
dotnet ef migrations remove

# Aplicar migration
dotnet ef database update

# Gerar script SQL
dotnet ef migrations script -o migrations.sql
```

## Query Optimization

```csharp
// No-tracking para leituras
var products = await _context.Products
    .AsNoTracking()
    .Where(p => p.IsActive)
    .ToListAsync();

// Select projetado
var dtos = await _context.Products
    .Select(p => new ProductDto
    {
        Id = p.Id,
        Name = p.Name,
        Price = p.Price
    })
    .ToListAsync();

// Split queries para joins complexos
var orders = await _context.Orders
    .Include(o => o.Items)
    .Include(o => o.Customer)
    .AsSplitQuery()
    .ToListAsync();

// Raw SQL
var products = await _context.Products
    .FromSqlRaw("SELECT * FROM products WHERE price > {0}", 100)
    .ToListAsync();

// Compiled queries
private static readonly Func<AppDbContext, int, Task<Product?>> GetProductById =
    EF.CompileAsyncQuery((AppDbContext ctx, int id) =>
        ctx.Products.FirstOrDefault(p => p.Id == id));
```

## Transactions

```csharp
using var transaction = await _context.Database.BeginTransactionAsync();
try
{
    _context.Products.Add(new Product { Name = "Test" });
    await _context.SaveChangesAsync();
    
    _context.Orders.Add(new Order { ProductId = 1 });
    await _context.SaveChangesAsync();
    
    await transaction.CommitAsync();
}
catch
{
    await transaction.RollbackAsync();
    throw;
}
```

## Batch Operations

```csharp
// Bulk update
await _context.Products
    .Where(p => p.CategoryId == 1)
    .ExecuteUpdateAsync(s => s
        .SetProperty(p => p.Discount, 0.1m)
        .SetProperty(p => p.UpdatedAt, DateTime.UtcNow));

// Bulk delete
await _context.Products
    .Where(p => p.IsDiscontinued)
    .ExecuteDeleteAsync();
```

## Performance

```csharp
// Connection pooling
"Server=localhost;Port=3306;Database=mydb;User=root;Password=pass;MinimumPoolSize=5;MaximumPoolSize=100;ConnectionLifeTime=300;"

// Prepared statements
options.UseMySql(connectionString, serverVersion, mySql =>
{
    mySql.CommandTimeout(30);
    mySql.EnableRetryOnFailure(3);
});
```

## Indexes

```csharp
// Índice simples
builder.HasIndex(e => e.Name);

// Índice composto
builder.HasIndex(e => new { e.CategoryId, e.Price });

// Índice único
builder.HasIndex(e => e.Email).IsUnique();

// Índice filtered (MySQL 8.0+)
builder.HasIndex(e => e.Name)
    .HasFilter("is_active = 1");

// Índice com collation
builder.HasIndex(e => e.Name)
    .HasDatabaseName("IX_name_utf8mb4")
    .HasAnnotation("MySql:IndexCollation", "utf8mb4_unicode_ci");
```

## JSON Columns (MySQL 5.7+)

```csharp
builder.Property(e => e.Metadata)
    .HasColumnType("json");

// Uso
var product = new Product
{
    Name = "Test",
    Metadata = JsonDocument.Parse("{\"color\":\"red\"}")
};
```

## Stored Procedures

```csharp
// Chamar stored procedure
var result = await _context.Database
    .ExecuteSqlRawAsync("CALL sp_update_stock({0}, {1})", productId, quantity);

// Com retorno
var products = await _context.Products
    .FromSqlRaw("CALL sp_get_products_by_category({0})", categoryId)
    .ToListAsync();
```

## Diferenças MySQL vs SQL Server

| Aspecto | MySQL | SQL Server |
|---------|-------|-----------|
| Identity | AUTO_INCREMENT | IDENTITY(1,1) |
| TOP | LIMIT | TOP |
| OFFSET | LIMIT/OFFSET | OFFSET/FETCH |
| NVARCHAR | VARCHAR + utf8mb4 | NVARCHAR |
| GETDATE() | NOW() | GETDATE() |
| Boolean | TINYINT(1) | BIT |
| GUID | CHAR(36) | UNIQUEIDENTIFIER |

## Fontes Oficiais
- pomelo.github.io/Pomelo.EntityFrameworkCore.MySql
- docs.microsoft.com/ef/core/providers/pomelo
- dev.mysql.com/doc/connector-net/en/

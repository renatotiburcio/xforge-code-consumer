---
id: sql-server-postgresql-patterns
type: conhecimento
tags: [sql, sqlserver, postgresql, performance, index, query, migration]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre SQL Server e PostgreSQL — Padrões de Performance
- **Seções principais**: SQL Server vs PostgreSQL, Índices, Queries Otimizadas, Stored Procedures vs Functions
- **Tags**: sql, sqlserver, postgresql, performance, index, query, migration
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `sql-server-postgresql-patterns` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 7 |


# SQL Server e PostgreSQL — Padrões de Performance

## SQL Server vs PostgreSQL

| Aspecto | SQL Server | PostgreSQL |
|---------|-----------|------------|
| Licença | Pago (Express gratuito) | Open source |
| JSON | JSON nativo | JSONB (melhor) |
| Full-text | FTS nativo | pg_trgm + tsvector |
| Partitioning | Nativo | Herança/Partitions |
| Extensions | DDL | pg_*, contrib |
| Window Functions | Sim | Sim |
| CTEs | Sim | Sim + Recursive |

## Índices

### SQL Server
```sql
-- Índice clustered (único por tabela)
CREATE CLUSTERED INDEX IX_Pedidos_Data 
ON Pedidos (DataPedido);

-- Índice non-clustered
CREATE NONCLUSTERED INDEX IX_Pedidos_Cliente 
ON Pedidos (ClienteId) 
INCLUDE (Status, Total);

-- Índice filtered
CREATE NONCLUSTERED INDEX IX_Pedidos_Pendentes 
ON Pedidos (DataPedido) 
WHERE Status = 'Pendente';

-- Índice columnstore (analytics)
CREATE NONCLUSTERED COLUMNSTORE INDEX IX_Vendas_Analytics 
ON Vendas (ProdutoId, DataVenda, Valor);
```

### PostgreSQL
```sql
-- B-tree (padrão)
CREATE INDEX idx_pedidos_data ON pedidos (data_pedido);

-- GIN (JSONB, full-text)
CREATE INDEX idx_produtos_tags ON produtos USING GIN (tags);

-- GiST (geoespacial, range)
CREATE INDEX idx_localizacao ON empresas USING GiST (localizacao);

-- Partial index
CREATE INDEX idx_pedidos_pendentes ON pedidos (data_pedido) 
WHERE status = 'Pendente';

-- Covering index
CREATE INDEX idx_pedidos_cliente ON pedidos (cliente_id) 
INCLUDE (status, total);

-- BRIN (tabelas grandes ordenadas)
CREATE INDEX idx_logs_data ON logs USING BRIN (data);
```

## Queries Otimizadas

### N+1 Problem
```sql
-- ❌ RUIM: N+1
SELECT * FROM Pedidos WHERE ClienteId = 1;
-- Para cada pedido:
SELECT * FROM ItensPedido WHERE PedidoId = @id;

-- ✅ BOM: JOIN
SELECT p.*, i.* 
FROM Pedidos p
INNER JOIN ItensPedido i ON p.Id = i.PedidoId
WHERE p.ClienteId = 1;
```

### Cursor vs Set-based
```sql
-- ❌ RUIM: Cursor
DECLARE cursor CURSOR FOR SELECT Id FROM Pedidos;
OPEN cursor;
FETCH NEXT FROM cursor INTO @id;
-- loop...

-- ✅ BOM: Set-based
UPDATE Pedidos SET Status = 'Fechado' 
WHERE DataPedido < DATEADD(MONTH, -6, GETDATE())
AND Status = 'Aberto';
```

### Pagination
```sql
-- ❌ RUIM: OFFSET
SELECT * FROM Produtos ORDER BY Id OFFSET 1000 ROWS FETCH NEXT 20 ROWS ONLY;

-- ✅ BOM: Keyset pagination
SELECT * FROM Produtos 
WHERE Id > @lastId 
ORDER BY Id 
FETCH NEXT 20 ROWS ONLY;
```

### Window Functions
```sql
-- Ranking
SELECT 
    ProdutoId,
    Quantidade,
    RANK() OVER (PARTITION BY CategoriaId ORDER BY Quantidade DESC) AS Rank
FROM Vendas;

-- Running total
SELECT 
    DataVenda,
    Valor,
    SUM(Valor) OVER (ORDER BY DataVenda) AS TotalAcumulado
FROM Vendas;

-- Lag/Lead
SELECT 
    DataVenda,
    Valor,
    LAG(Valor, 1) OVER (ORDER BY DataVenda) AS ValorAnterior
FROM Vendas;
```

## Stored Procedures vs Functions

### SQL Server
```sql
-- Stored Procedure
CREATE PROCEDURE sp_BaixarEstoque
    @ProdutoId INT,
    @Quantidade INT
AS
BEGIN
    UPDATE Estoque SET Quantidade = Quantidade - @Quantidade
    WHERE ProdutoId = @ProdutoId AND Quantidade >= @Quantidade;
    
    IF @@ROWCOUNT = 0
        THROW 50001, 'Estoque insuficiente', 1;
END;

-- Function (inline - melhor performance)
CREATE FUNCTION fn_CalcularDesconto(@PedidoId INT)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @Total DECIMAL(10,2);
    SELECT @Total = SUM(Quantidade * PrecoUnitario) 
    FROM ItensPedido WHERE PedidoId = @PedidoId;
    RETURN @Total * 0.1; -- 10% desconto
END;
```

### PostgreSQL
```sql
-- Function (único jeito de stored procedures)
CREATE OR REPLACE FUNCTION baixar_estoque(
    p_produto_id INT, 
    p_quantidade INT
) RETURNS VOID AS $$
BEGIN
    UPDATE estoque SET quantidade = quantidade - p_quantidade
    WHERE produto_id = p_produto_id AND quantidade >= p_quantidade;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Estoque insuficiente';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

## Concorrência

### SQL Server - Optimistic Concurrency
```sql
-- Usar rowversion
ALTER TABLE Produtos ADD Versao ROWVERSION;

-- UPDATE com verificação
UPDATE Produtos 
SET Nome = @Nome, Preco = @Preco
WHERE Id = @Id AND Versao = @Versao;

IF @@ROWCOUNT = 0
    -- Conflito de concorrência
```

### PostgreSQL - Advisory Locks
```sql
-- Lock pessimista
SELECT pg_advisory_lock(12345); -- Lock por chave
-- ... operação ...
SELECT pg_advisory_unlock(12345);

-- Lock por transação
SELECT * FROM Pedidos WHERE id = 1 FOR UPDATE SKIP LOCKED;
```

## Backup e Recovery

### SQL Server
```sql
-- Full backup
BACKUP DATABASE MeuBanco TO DISK = 'C:\backup\MeuBanco.bak';

-- Differential
BACKUP DATABASE MeuBanco TO DISK = 'C:\backup\MeuBanco_diff.bak' WITH DIFFERENTIAL;

-- Transaction log
BACKUP LOG MeuBanco TO DISK = 'C:\backup\MeuBanco_log.trn';
```

### PostgreSQL
```bash
# Backup
pg_dump -U postgres -d meubanco -F c -f backup.dump

# Restore
pg_restore -U postgres -d meubanco backup.dump

# Continuous archiving
archive_mode = on
archive_command = 'cp %p /archive/%f'
```

## Fontes Oficiais
- docs.microsoft.com/sql
- postgresql.org/docs
- use-the-index-luke.com

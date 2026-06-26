---
id: playbook-db-migration-zero-downtime
type: playbook
title: Database Migration Sem Downtime (Expand-Contract)
severity: high
status: validated
trustScore: 93
source: prisma-db + stripe-migrations
lastValidated: 2026-06-14
tags: ["database", "migration", "zero-downtime", "expand-contract", "blue-green"]
---

## Principio
Nunca faca migration destrutiva em deploy. Use Expand-Contract (multi-deploy).

## Erros Comuns

### 1. Adicionar coluna NOT NULL sem default
```sql
ALTER TABLE clientes ADD COLUMN email VARCHAR(255) NOT NULL;
```
**Quebra**: app faz INSERT sem email -> erro.

### 2. Renomear coluna
```sql
ALTER TABLE clientes RENAME COLUMN nome TO razao_social;
```
**Quebra**: app faz SELECT nome -> coluna nao existe.

### 3. Mudar tipo de coluna
```sql
ALTER TABLE pedidos ALTER COLUMN total TYPE VARCHAR(20);
```
**Quebra**: conversao falha.

## Padrao Expand-Contract (3 Deploys)

### Exemplo: Adicionar coluna `email` NOT NULL

### Deploy 1: EXPAND (adicionar coluna nullable)
```sql
ALTER TABLE clientes ADD COLUMN email VARCHAR(255);
CREATE INDEX idx_clientes_email ON clientes(email) WHERE email IS NOT NULL;
```
**Seguro**: coluna existe nullable, app nao usa.

### Deploy 2: BACKFILL + APP COMECA A USAR
```sql
UPDATE clientes SET email = LOWER(TRIM(nome)) || '@placeholder.local'
WHERE email IS NULL;
```
**App**: comeca a popular coluna. Coluna ainda nullable.

### Deploy 3: CONTRACT (NOT NULL)
```sql
ALTER TABLE clientes ALTER COLUMN email SET NOT NULL;
```
**Seguro**: app ja popula email em todo INSERT.

## Caso: Renomear Coluna (5 Deploys)

### Deploy 1: ADD nova coluna + backfill
```sql
ALTER TABLE clientes ADD COLUMN razao_social VARCHAR(255);
UPDATE clientes SET razao_social = nome WHERE razao_social IS NULL;
```

### Deploy 2: APP LE/AJUSTA AMBAS
```csharp
public string? Nome { get; set; }
public string? RazaoSocial { get; set; }
public string NomeExibicao => RazaoSocial ?? Nome ?? "";
```

### Deploy 3: BACKFILL FINAL (job batch)
```sql
UPDATE clientes SET razao_social = nome 
WHERE razao_social IS NULL OR razao_social = '';
```

### Deploy 4: SWITCH READ
```csharp
public string NomeExibicao => RazaoSocial ?? "";
```

### Deploy 5: SWITCH WRITE
```csharp
void Salvar() { INSERT (razao_social) VALUES (...); }
```

### Deploy 6 (futuro): DROP coluna antiga
```sql
ALTER TABLE clientes DROP COLUMN nome;
```

## Ferramentas

### EF Core (.NET)
```csharp
public partial class AddEmailToClientes : Migration
{
    protected override void Up(MigrationBuilder mb)
    {
        mb.AddColumn<string>(
            name: "email",
            table: "clientes",
            type: "varchar(255)",
            nullable: true);  // NAO false!
        mb.Sql("UPDATE clientes SET email = LOWER(TRIM(nome)) || '@x.com' WHERE email IS NULL");
    }
}
```

### Postgres: Adicionar FK sem lock
```sql
-- 1. Adicionar coluna nullable + backfill
ALTER TABLE pedidos ADD COLUMN cliente_id_new BIGINT;
UPDATE pedidos SET cliente_id_new = cliente_id;

-- 2. Adicionar FK NOT VALID (sem validar existentes)
ALTER TABLE pedidos ADD CONSTRAINT fk_cliente_new
    FOREIGN KEY (cliente_id_new) REFERENCES clientes(id) NOT VALID;

-- 3. Em manutencao: VALIDATE (sem lock exclusivo)
ALTER TABLE pedidos VALIDATE CONSTRAINT fk_cliente_new;
```

### Postgres: Unique Index sem lock
```sql
CREATE UNIQUE INDEX CONCURRENTLY uk_clientes_email
ON clientes(email) WHERE email IS NOT NULL;
```

## Backfill em Tabela Grande
```sql
DO $$
DECLARE
    batch_size INT := 10000;
    rows_updated INT;
BEGIN
    LOOP
        UPDATE clientes SET email = LOWER(TRIM(nome)) || '@x.com'
        WHERE id IN (
            SELECT id FROM clientes WHERE email IS NULL LIMIT batch_size
        );
        GET DIAGNOSTICS rows_updated = ROW_COUNT;
        EXIT WHEN rows_updated = 0;
        RAISE NOTICE 'Updated % rows', rows_updated;
        PERFORM pg_sleep(0.1);
    END LOOP;
END $$;
```

## Checklist
- [ ] Migration eh additive (ADD COLUMN/INDEX/TABLE)?
- [ ] NAO dropa coluna/tabela?
- [ ] NAO renomeia sem coluna intermediaria?
- [ ] NAO muda tipo sem coluna intermediaria?
- [ ] Backfill idempotente?
- [ ] Default permite INSERT sem erro?
- [ ] Indexes CONCURRENTLY?
- [ ] Constraints NOT VALID + VALIDATE separado?
- [ ] Rollback testado em staging?

## Monitorar
```sql
-- Locks ativos
SELECT * FROM pg_locks WHERE NOT granted;
-- Queries longas
SELECT pid, query, now() - query_start AS duration
FROM pg_stat_activity
WHERE state != 'idle' AND now() - query_start > interval '1 second';
```

## Caso Real (2024-06)
Deploy de madrugada: ALTER COLUMN valor TYPE NUMERIC(15,4) em tabela 50M rows.
Lock de 8min. R$ 80K em vendas perdidas.
**Fix**: 4 deploys em 5 dias (expand, backfill, app switch, drop).

## Referencias
- Martin Fowler - Evolutionary Database Design
- Stripe: Migrating millions of rows
- ADR-0021 XForge: Deploy Blue-Green
- ADR-0024 XForge: Disaster Recovery

---
id: playbook-erp-venda-simultanea-race
type: playbook
title: ERP Venda Simultanea Mesma Unidade (race condition)
severity: high
status: validated
trustScore: 89
source: operacao-real + best-practices
lastValidated: 2026-06-14
tags: ["erp", "venda", "concorrencia", "race-condition", "estoque", "lock"]
---

## Sintoma
Dois vendedores confirmam venda do mesmo produto ao mesmo tempo. Ambos veem "1 unidade disponivel" e vendem. Resultado: 2 vendas para 1 unidade (overselling).

## Causa
Race condition: SELECT + UPDATE nao eh atomico.
```sql
-- Vendedor A: SELECT saldo WHERE produto_id=1  -- 1
-- Vendedor B: SELECT saldo WHERE produto_id=1  -- 1
-- A: UPDATE estoque SET saldo=0 WHERE produto_id=1
-- B: UPDATE estoque SET saldo=0 WHERE produto_id=1  -- oversell!
```

## Solucoes (em ordem de complexidade)

### 1. Lock Pessimista
```python
with transaction():
    row = db.execute("SELECT saldo FROM estoque WITH (ROWLOCK, XLOCK) WHERE produto_id=:id").fetchone()
    if row.saldo < quantidade: raise SaldoInsuficiente()
    db.execute("UPDATE estoque SET saldo = saldo - :q WHERE produto_id = :id", ...)
```

### 2. Lock Otimista (Recomendado para Alta Concorrencia)
```sql
ALTER TABLE estoque ADD COLUMN versao BIGINT NOT NULL DEFAULT 0;
```
```python
result = db.execute("""
    UPDATE estoque SET saldo = saldo - :q, versao = versao + 1
    WHERE produto_id = :id AND versao = :v AND saldo >= :q
""", q=quantidade, v=versao_atual)
if result.rowcount == 0: raise ConcurrencyError("Estoque mudou, recarregar")
```

### 3. Reserva Explicita
```sql
CREATE TABLE reserva_estoque (
    id BIGINT PRIMARY KEY, produto_id BIGINT, quantidade INT,
    cliente_id BIGINT, expira_em TIMESTAMP, status VARCHAR(20)
);
```
- Vendedor A reserva: saldo_disponivel=0, reserva=1
- Vendedor B ve saldo_disponivel=0 -> bloqueia
- Vendedor A confirma: reserva -> saida
- Reserva expira em 30min se nao confirmada

## Caso Real (2024-12)
E-commerce Black Friday, 200 req/s. Lock pessimista causava deadlock (timeout 5s) -> erro 503.
**Fix**: lock otimista com retry exponencial (max 3 tentativas, 100ms inicial).
Resultado: 0 oversell, latencia p95 = 80ms (vs 1200ms).

## Padroes por Volume

| Volume | Padrao Recomendado |
|--------|-------------------|
| < 10 vendas/min | Lock pessimista |
| 10-100 vendas/min | Lock otimista + retry |
| 100-1000 vendas/min | Reserva + fila |
| > 1000 vendas/min | Fila + multi-worker com sharding por produto |

## Prevencao
- Teste de concorrencia: simular 100 vendas simultaneas
- Monitor: alertar se oversell > 0 em 24h
- Reconciliacao: comparar vendas confirmadas vs estoque
- Padrao saga: separar confirmacao de venda da baixa de estoque

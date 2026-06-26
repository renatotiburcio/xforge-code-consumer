---
id: playbook-erp-estoque-negativo
type: playbook
title: ERP Estoque Negativo (venda > saldo)
severity: high
status: validated
trustScore: 87
source: operacao-real + best-practices
lastValidated: 2026-06-14
tags: ["erp", "estoque", "edge-case", "saldo-negativo", "venda"]
---

## Sintoma
Venda confirmada mas estoque do produto fica **negativo** (ex: -3 unidades). Bloqueia relatorios, gera inventario divergente, problemas no SPED.

## Causas
1. **Venda antes da compra ser baixada**: cliente vendeu, fornecedor entregou mas XML nao foi processado ainda
2. **Perda/avaria nao registrada**: produto quebrou, mas sistema nao sabe
3. **Erro de contagem**: inventario nao foi atualizado
4. **Reserva sem baixa**: vendedor segurou produto mas nao baixou do estoque
5. **Transferencia entre lojas nao processada**: saida registrada mas entrada nao
6. **Devolucao nao processada**: cliente devolveu mas NF de entrada nao foi feita
7. **Multi-deposito com sincronizacao atrasada**

## Diagnostico
```sql
SELECT p.id, p.nome, e.deposito_id, e.saldo, p.unidade
FROM produtos p
JOIN estoque e ON e.produto_id = p.id
WHERE e.saldo < 0
ORDER BY e.saldo ASC
LIMIT 20;
```

## Decisoes de Design

| Cenario | Bloquear? | Justificativa |
|---------|:---------:|---------------|
| Venda ecommerce | SIM | cliente recebe confirmacao mas nao tem estoque |
| Venda B2B com pedido | SIM | mesma coisa |
| Venda balcao (PDV) | NAO | cliente ja levou o produto |
| Venda com reserva previa | NAO | estoque ja foi reservado |
| Ordem de producao | DEPENDE | industria nao pode produzir sem MP |
| Servico (nao tem estoque) | irrelevante | |

## Solucao

### 1. Prevenir (Recomendado)
```python
def confirmar_venda(itens, deposito_id):
    for item in itens:
        saldo = estoque_service.get_saldo(item.produto_id, deposito_id)
        if saldo < item.quantidade:
            return Result.fail(f"Saldo insuficiente para {item.produto.nome}")
    return Result.ok()
```

### 2. Detectar (Auditoria)
```python
def auditoria_estoque():
    negativos = estoque_repo.get_negativos()
    if negativos:
        enviar_alerta(to=estoque@empresa.com, details=formatar_relatorio(negativos))
```

### 3. Corrigir (Casos)
- **Avaria/perda**: registrar movimentacao de perda (tipo=BX) com custo
- **Erro de contagem**: fazer inventario de ajuste com auditoria
- **Venda sem baixa**: emitir NF de saida retroativa (cuidado com SEFAZ)
- **Multi-deposito**: sincronizar e bloquear venda se reserva > saldo

## Caso Real (2024-09)
Mercado com 5 lojas + CD. Sistema permitia venda em loja A mesmo com estoque na loja B.
**Fix**: trava de estoque centralizado + reserva explicita.

## Prevencao
- Bloqueio configuravel por tipo de venda
- Reserva explicita (em transito vs reservado vs disponivel)
- Alerta diario de estoque negativo
- Multi-deposito: lock pessimista ou estoque virtual centralizado

## Referencias
- WMS Best Practices
- SPED Contribuicoes: estoque negativo impacta credito PIS/COFINS

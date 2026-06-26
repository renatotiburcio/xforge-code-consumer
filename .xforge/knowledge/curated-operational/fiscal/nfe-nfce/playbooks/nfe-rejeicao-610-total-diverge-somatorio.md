---
id: playbook-nfe-rejeicao-610-total-diverge-somatorio
type: playbook
title: NFe Rejeicao 610 Total Diverge do Somatorio
severity: high
status: validated
trustScore: 91
source: sefaz-oficial + suporte-producao
lastValidated: 2026-06-14
tags: ["nfe", "sefaz", "rejeicao", "610", "total", "fiscal"]
---

## Sintoma
SEFAZ rejeita com codigo 610: "Rejeicao: Total da NF-e difere do somatorio dos Valores dos Itens".

## Causas Comuns
1. **Arredondamento/truncamento**: itens com 4+ casas decimais somam diferente do total
2. **Desconto/Acrescimo**: desconto no cabecalho nao foi aplicado aos itens
3. **Frete/Seguro/Outras Despesas**: incluidos em tag errada (devem ir em `vFrete`, `vSeg`, `vOutro`)
4. **ICMS-ST**: valor de ICMS-ST nao incluido no total do item mas incluido no total da NF
5. **Diferenca por tipo de calculo**: ICMS proprio, IPI, PIS, COFINS cada um tem seu proprio campo

## Diagnostico
```python
def validar_total_nfe(nfe: dict) -> Tuple[bool, str]:
    soma_itens = sum(item["vProd"] for item in nfe["itens"])
    soma_itens_com_imp = sum(
        item["vProd"]
        + item.get("vFrete", 0)
        + item.get("vSeg", 0)
        + item.get("vOutro", 0)
        + item.get("vII", 0)
        + item.get("vIPI", 0)
        - item.get("vDesc", 0)
        for item in nfe["itens"]
    )
    total_nfe = nfe["total"]["vNF"]
    diff = abs(soma_itens_com_imp - total_nfe)
    if diff > 0.01:  # tolerancia 1 centavo
        return False, f"diferenca R$ {diff:.2f} (itens={soma_itens_com_imp}, nf={total_nfe})"
    return True, ""
```

## Solucao
1. **Calcular total a partir dos itens** (nunca aceitar total digitado manualmente)
2. Arredondar para 2 casas decimais em CADA item E no total (mesma regra)
3. Validar antes de transmitir:
   ```python
   assert abs(soma_itens - nfe["vNF"]) < 0.01, "Total NF diverge"
   ```
4. Para ICMS-ST: somar valor no campo `vST` separado (nao soma no vNF)

## Caso Real (2024-12)
Cliente emitia NFe com 200 itens. 5 itens tinham desconto de 0.3% aplicado.
Sistema calculava desconto por item mas o total estava fixo (digitado).
Diferenca media: R$ 0.07 por NFe (200 itens * 0.0003%) — rejeitada 100%.

**Fix**: total calculado = soma(quantidade * valor_unitario) - soma(descontos)

## Prevencao
- Total SEMPRE calculado a partir dos itens (regra de ouro)
- Bloquear usuario de editar total manualmente
- Job pre-emissao: recalcular e comparar (se diferenca > 0.01, alerta)
- Teste unitario: gerar NFe com 100 itens aleatorios, validar totais

## Referencias
- Manual de Orientacao NFe 7.0 - Item 5.6 (totalizacao)
- NT 2018.005 - Regras de arredondamento
- Rejeicao 610 - Schema XML

---
id: playbook-nfe-rejeicao-120-cfop-invalido
type: playbook
title: NFe Rejeicao 120 CFOP Invalido
severity: medium
status: validated
trustScore: 90
source: sefaz-oficial + operacao-real
lastValidated: 2026-06-14
tags: ["nfe", "sefaz", "rejeicao", "120", "cfop", "fiscal"]
---

## Sintoma
SEFAZ rejeita com codigo 120: "CFOP invalido".

## Causas Comuns
1. **CFOP nao preenchido** ou com tamanho != 4
2. **CFOP incompativel com operacao**:
   - CFOP 5xxx/6xxx/7xxx (interestadual/exterior) usado em operacao interna
   - CFOP 1xxx/2xxx usado em operacao interestadual
3. **CFOP vs tipo de emitente**: Simples Nacional tem CFOPs especificos (1xxx/2xxx nao usam 1.409; usar 5.405)
4. **CFOP vs destinatario**: CFOP para consumidor final difere de revenda
5. **CFOP descontinuado** em 2026: revisar tabela atualizada

## Tabela de Decisao Rapida

| Operacao | Dentro UF | Fora UF | Exterior |
|----------|-----------|---------|----------|
| Venda | 5.102, 5.405, 5.408 | 6.102, 6.108, 6.408 | 7.102 |
| Devolucao | 5.202, 5.410 | 6.202, 6.410 | 7.202 |
| Transferencia | 5.152, 5.153 | 6.152, 6.153 | - |
| Remessa | 5.916, 5.949 | 6.916, 6.949 | 7.949 |

## Diagnostico
```sql
-- Verificar CFOPs usados no mes
SELECT cfop, COUNT(*)
FROM nfe_itens i JOIN nfe_cabecalho c ON c.id = i.nfe_id
WHERE c.data_emissao >= DATE_TRUNC('month', CURRENT_DATE)
GROUP BY cfop
ORDER BY 2 DESC;
```

```python
# Validar CFOP vs origem/destino/operacao
def validar_cfop(cfop: str, uf_origem: str, uf_destino: str, tipo_operacao: str) -> bool:
    if len(cfop) != 4: return False
    primeiro = cfop[0]
    if uf_origem == uf_destino:
        return primeiro in ("5",)  # interno
    elif uf_destino == "EX":
        return primeiro == "7"
    else:
        return primeiro == "6"  # interestadual
```

## Solucao
1. Validar CFOP na emissao (antes de transmitir)
2. Manter tabela de CFOPs atualizada (ajustar a cada mudanca)
3. Configurar alertas: CFOP terminado em 933/949/999 (genericos) pedem revisao

## Prevencao
- Tabela de CFOPs por natureza de operacao + UF
- Validacao no backend antes de gerar XML
- Dropdown com filtro por contexto (origem, destino, operacao)
- Revisao trimestral com contador

## Referencias
- Ajuste SINIEF 22/2019 - CFOPs
- Tabela CFOP atualizada 2026 (publicada CONFAZ)
- Manual de Orientacao NFe - Item 5.1

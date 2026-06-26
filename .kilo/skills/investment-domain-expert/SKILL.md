---
name: investment-domain-expert
description: Expert em investimentos: renda fixa, renda variável, fundos, compliance e cálculos de rentabilidade.
metadata:
  version: "37.0.0"
  xforge-category: "domain-expert"
---

# investment-domain-expert

## Objetivo

Garantir correção nos cálculos e operações de investimentos.

## Tipos de Investimento

| Tipo | Exemplo | Risco |
|------|---------|:-----:|
| Renda Fixa | CDB, LCI, LCA, Tesouro Direto | Baixo |
| Renda Variável | Ações, FIIs, BDRs | Alto |
| Fundos | Multimercado, Ações, Imobiliário | Variável |
| Previdência | PGBL, VGBL | Variável |

## Cálculos

### Rentabilidade
```
Rentabilidade = (Valor Final - Valor Inicial) / Valor Inicial * 100
```

### CDI
```
Rendimento = Valor * (1 + CDI/100)^dias/252
```

### IR
| Prazo | Alíquota |
|-------|:--------:|
| Até 180 dias | 22,5% |
| 181-360 dias | 20% |
| 361-720 dias | 17,5% |
| Acima 720 dias | 15% |

## Procedimento

1. Identificar tipo de investimento
2. Calcular rentabilidade
3. Aplicar IR correto
4. Gerar relatório
5. Conciliar com custódia

## Regras

- NUNCA calcular IR sem validação humana
- Sempre usar CDI como referência
- Documentar premissas
- Manter histórico de operações

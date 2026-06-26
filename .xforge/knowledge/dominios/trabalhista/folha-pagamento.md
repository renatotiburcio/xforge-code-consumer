---
id: folha-pagamento
type: knowledge
tags: [folha, pagamento, proventos, descontos, inss, irrf, fgts, encargos, contabil]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Folha de Pagamento — Cálculos e Encargos
- **Principais responsabilidades**: Calcular mensalmente proventos (salário, horas extras, adicionais) e descontos (INSS, IRRF, faltas, benefícios).; Aplicar tabelas progressivas de I...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Constraints
- **Tags**: folha, pagamento, proventos, descontos, inss, irrf, fgts, encargos, contabil
- **Restrições/Regras**: **Pagamento**: até o 5º dia útil do mês seguinte (CLT Art. 459).; **FGTS**: depósito até dia 7 do mês seguinte.

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `folha-pagamento` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 7 |


# Folha de Pagamento — Cálculos e Encargos

## Propósito
Documentar os eventos de folha de pagamento (proventos e descontos), cálculos de INSS, IRRF, FGTS, encargos patronais e integração contábil.

## Responsabilidades
- Calcular mensalmente proventos (salário, horas extras, adicionais) e descontos (INSS, IRRF, faltas, benefícios).
- Aplicar tabelas progressivas de INSS e IRRF vigentes.
- Calcular FGTS (8%) e encargos patronais (INSS 20%, RAT, terceiros).
- Gerar provisão contábil de 13º (1/12 mensal) e férias (1/12 + 1/3).
- Integrar com eSocial (eventos S-1200, S-1210, S-1299).

## Dependências
- Tabelas INSS e IRRF atualizadas anualmente.
- Cadastro de funcionários com dados contratuais, dependentes e jornada.
- Controle de ponto para apuração de horas extras, faltas e atrasos.
- Tabela de rubricas S-1010 cadastrada no eSocial.

## Constraints
- **Pagamento**: até o 5º dia útil do mês seguinte (CLT Art. 459).
- **FGTS**: depósito até dia 7 do mês seguinte.
- **13º**: 1ª parcela até 30/11, 2ª parcela até 20/12.
- **Teto INSS 2026**: R$ 8.380,75 (atualizar anualmente).
- **Desconto VT**: limitado a 6% do salário base.

## Conteúdo

### Estrutura da Folha
```
(+) Salário base
(+) Horas extras (50%, 75%, 100%)
(+) Adicional noturno (20%)
(+) Insalubridade (10%, 20%, 40%)
(+) Periculosidade (30%)
(+) DSR sobre variáveis
(+) Comissões / Gratificações
(+) Outros proventos
────────────────────────────── (=) Total proventos
(-) INSS (tabela progressiva)
(-) IRRF (tabela progressiva)
(-) Vale-transporte (6%)
(-) Faltas e atrasos
(-) Pensão alimentícia
(-) Outros descontos
────────────────────────────── (=) Salário líquido
```

### Tabela INSS 2026 (Empregado)
| Faixa Salarial | Alíquota |
|----------------|----------|
| Até R$ 1.518,00 | 7,50% |
| R$ 1.518,01 a R$ 2.777,65 | 9,00% |
| R$ 2.777,66 a R$ 4.190,38 | 12,00% |
| R$ 4.190,39 a R$ 8.380,75 | 14,00% |

**Teto INSS 2026**: R$ 8.380,75

### Tabela IRRF 2026 (Mensal)
| Base de Cálculo | Alíquota | Parcela a Deduzir |
|-----------------|----------|-------------------|
| Até R$ 2.427,65 | Isento | R$ 0,00 |
| R$ 2.427,66 a R$ 2.826,65 | 7,50% | R$ 182,07 |
| R$ 2.826,66 a R$ 3.751,05 | 15,00% | R$ 393,23 |
| R$ 3.751,06 a R$ 4.664,68 | 22,50% | R$ 627,32 |
| Acima de R$ 4.664,68 | 27,50% | R$ 861,36 |

**Dedução por dependente**: R$ 189,59 (2026)


> **Nota:** Com deduções legais (INSS + dependentes), salários brutos de até ~R$ 5.000 podem ter base de cálculo abaixo do limite de isenção do IRRF (R$ 2.427,65), resultando em IRRF = R$ 0,00. Veja detalhes em [inss-irrf](inss-irrf.md).


### FGTS
- **Alíquota**: 8% sobre remuneração bruta
- **Aprendiz**: 2%
- **Depósito**: até dia 7 do mês seguinte
- **Base de cálculo**: salário + horas extras + adicionais + DSR + 13º (1/12)

### Encargos Patronais
| Encargo | Alíquota |
|---------|----------|
| INSS Patronal | 20% |
| RAT (risco médio) | 2% (ajustado por FAP: 0,5 a 2,0) |
| Terceiros (SESI, SENAI, SEBRAE, etc.) | 5,8% |
| Salário-educação | 2,5% |
| FGTS | 8% |
| **Total estimado** | **~38,3%** |

### Provisão Contábil
**13º Salário:**
```
Provisão mensal = Salário / 12
Lançamento: D — Despesa de 13º (Provisão) / C — Provisão para 13º
```

**Férias:**
```
Provisão mensal = (Salário + 1/3) / 12
Lançamento: D — Despesa de Férias (Provisão) / C — Provisão para Férias
```

### Cálculo de Hora Extra
```
Valor da hora = Salário / 220h
Hora extra 50% = Hora normal × 1,5
Hora extra 100% = Hora normal × 2,0
```

### Cálculo de DSR
```
DSR = (Total de variáveis no mês / Dias úteis) × Domingos e feriados
```

### Cálculo de INSS (exemplo: salário R$ 5.000)
```
Faixa 1: R$ 1.518,00 × 7,50% = R$ 113,85
Faixa 2: (R$ 2.777,65 − R$ 1.518,00) × 9% = R$ 113,37
Faixa 3: (R$ 4.190,38 − R$ 2.777,65) × 12% = R$ 169,53
Faixa 4: (R$ 5.000 − R$ 4.190,38) × 14% = R$ 113,35
Total INSS = R$ 510,10
```

### Cálculo de IRRF (exemplo: salário R$ 5.000, 1 dependente)
```
Base = R$ 5.000 − R$ 510,10 − R$ 189,59 = R$ 4.300,31
IRRF = R$ 4.300,31 × 22,50% − R$ 627,32 = R$ 340,25
```

### Integração Contábil
| Conta | Débito | Crédito |
|-------|--------|---------|
| Despesa de salários | X | |
| Salários a pagar | | X |
| INSS a recolher | | X |
| IRRF a recolher | | X |
| FGTS a recolher | | X |
| Banco (pagamento) | | X |

## Related Documents
- [clt](clt.md) — Consolidação das Leis do Trabalho
- [inss-irrf](inss-irrf.md) — Detalhamento INSS e IRRF
- [fgts](fgts.md) — Detalhamento do FGTS
- [esocial-folha](esocial-folha.md) — Eventos de folha no eSocial


## Documentos Relacionados
- \luxos/folha-pagamento.md\ — Fluxo completo do processo de folha de pagamento

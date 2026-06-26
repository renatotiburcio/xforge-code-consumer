---
id: tributos-regimes-tributarios
type: knowledge
tags: [tributos, regimes, simples-nacional, lucro-presumido, lucro-real, mei]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar os regimes tributários brasileiros, suas características, alíquotas e critérios de escolha para empresas.
- **Principais responsabilidades**: Explicar os quatro regimes: MEI, Simples Nacional, Lucro Presumido e Lucro Real; Detalhar anexos, alíquotas e faixas de faturamento; Fornecer compa...
- **Seções principais**: Purpose, Responsibilities, Dependencies, Conteúdo
- **Tags**: tributos, regimes, simples-nacional, lucro-presumido, lucro-real, mei
- **Restrições/Regras**: Valores e alíquotas sujeitos a atualização legislativa; Reforma Tributária (EC 132/2023) impactará os regimes a parti...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tributos-regimes-tributarios` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 6 |


# Regimes Tributários Brasileiros

## Purpose
Documentar os regimes tributários brasileiros, suas características, alíquotas e critérios de escolha para empresas.

## Responsibilities
- Explicar os quatro regimes: MEI, Simples Nacional, Lucro Presumido e Lucro Real
- Detalhar anexos, alíquotas e faixas de faturamento
- Fornecer comparativo e critérios de escolha

## Dependencies
- `icms.md` — detalhes do ICMS por regime
- `pis-cofins.md` — detalhes de PIS/COFINS por regime
- `irpj-csll.md` — detalhes de IRPJ/CSLL por regime
- `reforma-tributaria.md` — impacto da reforma nos regimes

## Conteúdo

### MEI — Microempreendedor Individual
- **Limite**: R$ 81.000/ano
- **DAS mensal**: R$ 71,60 (comércio) a R$ 76,60 (comércio + serviços)
- **Isenção**: IRPJ, CSLL, PIS, COFINS, IPI incluídos no DAS
- **Obrigações**: DAS mensal, DASN-SIMEI anual
- **Restrições**: 1 empregado, CNAEs limitados, sem sócios

### Simples Nacional (LC 123/2006)
- **Limite**: R$ 4.800.000/ano (sublimites por UF: R$ 1,8M ou R$ 3,6M)
- **Pagamento**: DAS mensal (guia única)
- **Anexos**: I (Comércio), II (Indústria), III (Serviços), IV (Serviços Profissionais), V (Serviços com fator r < 28%), VI (Saúde)
- **Alíquotas**: Progressivas por faixa (6% a 33%)
- **Fator "r"**: Se folha ≥ 28% da receita, tributa pelo Anexo III em vez do V
- **Obrigações**: DAS, DEFIS, DIRF, ECD/ECF

### Lucro Presumido
- **Limite**: Até R$ 78.000.000/ano
- **Apuração**: Trimestral
- **Presunção IRPJ**: 8% (comércio/indústria), 32% (serviços)
- **Presunção CSLL**: 12% (comércio/indústria), 32% (serviços)
- **Alíquotas**: IRPJ 15% + 10% adicional (>R$ 20K/mês), CSLL 9%, PIS 0,65%, COFINS 3%
- **Regime cumulativo**: Sem créditos de PIS/COFINS
- **Carga típica (serviços)**: ~12-15% + ISS

### Lucro Real
- **Obrigatoriedade**: Receita > R$ 78.000.000/ano
- **Apuração**: Trimestral ou anual
- **Alíquotas**: IRPJ 15% + 10%, CSLL 9%, PIS 1,65%, COFINS 7,6%
- **Regime não-cumulativo**: Com créditos sobre insumos
- **Compensação de prejuízos**: Até 30% do lucro tributável
- **Obrigações**: ECF, ECD, LALUR, EFD-Contribuições

### Comparativo Rápido
| Critério | MEI | Simples | Lucro Presumido | Lucro Real |
|---|---|---|---|---|
| Limite | R$ 81K | R$ 4,8M | R$ 78M | Sem limite |
| PIS/COFINS | No DAS | No DAS | 0,65%/3% | 1,65%/7,6% |
| Créditos | Não | Parcial | Não | Sim |
| Prejuízo | Não | Não | Não | Até 30% |

### Critério de Escolha
1. **MEI**: Microempreendedores com faturamento baixo e atividade permitida
2. **Simples Nacional**: Pequenas empresas que se enquadram nos anexos
3. **Lucro Presumido**: Empresas com margem alta e baixa folha de custos
4. **Lucro Real**: Grandes empresas ou com muitos créditos de insumos

## Constraints
- Valores e alíquotas sujeitos a atualização legislativa
- Reforma Tributária (EC 132/2023) impactará os regimes a partir de 2026

## Related Documents
- `icms.md` — ICMS por regime
- `pis-cofins.md` — PIS/COFINS cumulativo vs não-cumulativo
- `irpj-csll.md` — Cálculo de IRPJ/CSLL
- `reforma-tributaria.md` — Transição dos regimes


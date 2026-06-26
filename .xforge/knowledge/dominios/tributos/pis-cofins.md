---
id: tributos-pis-cofins
type: knowledge
tags: [tributos, pis, cofins, federal, cumulativo, nao-cumulativo]
owner: project-team
version: "1.0.0"
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Documentar PIS e COFINS, contribuições federais sobre receita bruta, seus regimes de tributação e regras de crédito.
- **Principais responsabilidades**: Explicar os regimes cumulativo e não-cumulativo; Detalhar alíquotas, créditos permitidos e obrigações acessórias; Cobrir retenções na fonte
- **Seções principais**: Purpose, Responsibilities, Dependencies, Conteúdo
- **Tags**: tributos, pis, cofins, federal, cumulativo, nao-cumulativo
- **Restrições/Regras**: Alíquotas e regras sujeitas a alteração por legislação federal; Transição para CBS requer adaptação de sistemas

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tributos-pis-cofins` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 6 |


# PIS/COFINS — Programas de Integração Social e Financiamento da Seguridade Social

## Purpose
Documentar PIS e COFINS, contribuições federais sobre receita bruta, seus regimes de tributação e regras de crédito.

## Responsibilities
- Explicar os regimes cumulativo e não-cumulativo
- Detalhar alíquotas, créditos permitidos e obrigações acessórias
- Cobrir retenções na fonte

## Dependencies
- `regimes-tributarios.md` — enquadramento por regime
- `irpj-csll.md` — tributos federais correlatos
- `reforma-tributaria.md` — substituição por CBS

## Conteúdo

### Conceito
PIS e COFINS são contribuições sociais federais que financiam seguro-desemprego, abono salarial e seguridade social. Incidem sobre a receita bruta das empresas (CF, art. 195).

### Regimes de Tributação
| Regime | PIS | COFINS | Cumulativo? |
|---|---|---|---|
| **Não Cumulativo** | 1,65% | 7,6% | Não |
| **Cumulativo** | 0,65% | 3% | Sim |
| **Simples Nacional** | No DAS | No DAS | — |

### Regime Não Cumulativo (Lucro Real)
- **Alíquotas**: PIS 1,65%, COFINS 7,6%
- **Créditos permitidos**: Mercadorias para revenda, insumos, energia elétrica, aluguéis, depreciação, arrendamento mercantil, armazenagem, frete, vale-transporte, máquinas e equipamentos
- **Não geram crédito**: Despesas com pessoal, despesas financeiras, multas, doações, patrocínios

### Regime Cumulativo (Lucro Presumido)
- **Alíquotas**: PIS 0,65%, COFINS 3%
- **Sem direito a créditos** sobre custos/despesas

### Exclusões da Base
- ICMS e ISS destacados na nota fiscal
- Devoluções de vendas, abatimentos, descontos incondicionais
- Receitas financeiras (regime não cumulativo)
- Venda de ativo imobilizado, dividendos, reversão de provisões

### Retenções na Fonte
| Serviço | PIS | COFINS | CSLL |
|---|---|---|---|
| Natureza profissional | 0,65% | 3% | 1,5% |
| Propriedade intelectual | 0,65% | 3% | 1,5% |

### Obrigações Acessórias
- **EFD Contribuições** — Blocos 0, A, C, D, F, I, M, P, 1, 9
- **DCTF** — Declaração de Débitos e Créditos Tributários Federais
- Apuração mensal, recolhimento até dia 25 do mês seguinte

### Regras
- Apuração: mensal
- Compensação permitida no mesmo período
- Reforma Tributária: PIS/COFINS substituídos pela CBS a partir de 2027

## Constraints
- Alíquotas e regras sujeitas a alteração por legislação federal
- Transição para CBS requer adaptação de sistemas

## Related Documents
- `regimes-tributarios.md` — Regimes e enquadramento
- `irpj-csll.md` — Tributos federais
- `reforma-tributaria.md` — CBS como substituto


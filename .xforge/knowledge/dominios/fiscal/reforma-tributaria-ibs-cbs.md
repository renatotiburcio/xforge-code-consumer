---
id: reforma-tributaria-ibs-cbs
type: conhecimento
tags: [fiscal, reforma, ibs, cbs, isento, split-payment]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Reforma Tributária - IBS, CBS e Imposto Seletivo
- **Seções principais**: Visão Geral, Alíquotas, Split Payment, Período de Transição
- **Tags**: fiscal, reforma, ibs, cbs, isento, split-payment
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `reforma-tributaria-ibs-cbs` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 7 |


# Reforma Tributária - IBS, CBS e Imposto Seletivo

## Visão Geral

A Emenda Constitucional 132/2023 unifica mais de 20 tributos em 3 impostos novos:

| Novo Imposto | Tributos Substituídos |
|-------------|----------------------|
| **IBS** (Imposto sobre Bens e Serviços) | ICMS, ISS, IPI, PIS, COFINS, FUNRURAL, SN |
| **CBS** (Contribuição sobre Bens e Serviços) | IRPJ, CSLL, PIS, COFINS |
| **Imposto Seletivo** | IPI (部分), impostos seletivos atuais |

## Alíquotas

### IBS
- Alíquota uniforme entre estados
- Prevista: ~17,74% (estimativa inicial)
- Compensação com estados (diferencial)

### CBS
- Alíquota única federal
- Prevista: ~8,87% (estimativa inicial)

### Imposto Seletivo
- Incidência sobre: combustíveis, bebidas, tabaco, minerais
- Alíquota variável por produto
- Adicional ao IBS/CBS

## Split Payment

### Conceito
- Pagamento do imposto é feito no momento da transação
- Banco retém e repassa ao fisco automaticamente
- Reduz sonegação e inadimplência

### Fluxo
```
Comprador → Pagamento → Banco → Split
                                ↓
                    IBS/CBS retido → Fisco
                    Valor líquido → Vendedor
```

### Impacto no ERP
- Cálculo de imposto no momento do pagamento
- Integração com gateway de pagamento
- Split automático no checkout
- Conciliação: valor líquido vs imposto retido

## Período de Transição

| Ano | Fase |
|-----|------|
| 2026 | Convivência (antigos + novos) |
| 2027 | CBS e IBS (fase 1) |
| 2028-2032 | Eliminação gradual dos antigos |
| 2033 | Sistema plenamente operacional |

### Regras de Transição
- Empresas de pequeno porte: regime especial
- Setores sensíveis: alíquotas reduzidas
- Créditos acumulados: compensação gradual

## Crédito Financeiro

### Conceito
- Crédito tributário acumulado
- Compensação com débitos futuros
- Prazo: 10 anos (regime atual)

### No Novo Sistema
- Crédito de IBS/CBS
- Compensação entre períodos
- Regras de transferência entre filiais

## Impactos no ERP

### Mudanças Necessárias
1. **Motor de cálculo**: nova engine para IBS/CBS
2. **Tabelas fiscais**: alíquotas por estado e tipo
3. **Split payment**: integração com gateway
4. **Créditos**: controle de créditos acumulados
5. **Relatórios**: DRE e apuração atualizados
6. **NF-e**: novos campos e layouts

### Adequações Contábeis
- Contas de tributos: nova estrutura
- DRE: classificação de tributos
- Balanço: passivos de tributos
- Notas explicativas: transição tributária

## Comitê Gestor

- Comitê Gestor do IBS/CBS
- Responsável por regulamentação
- Resoluções e orientações
- Sistemas de arrecadação

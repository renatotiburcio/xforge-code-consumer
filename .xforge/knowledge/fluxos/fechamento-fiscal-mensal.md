---
id: fechamento-fiscal-mensal
type: fluxo
title: Fechamento Fiscal Mensal: Checklist Completo ate o SPED
domain: fiscal
trustScore: 90
source: XForge ERP + legislacao tributaria BR
tags: [fechamento, fiscal, sped]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# Fechamento Fiscal Mensal

## Cronograma

| Dia | Atividade |
|-----|-----------|
| 1-5 | Conferencia NFe |
| 5-10 | CFOP, NCM, CST |
| 10-15 | Apuracao ICMS, IPI, ICMS-ST |
| 15-17 | Apuracao PIS, COFINS |
| 17-18 | Retencoes (ISS, IRRF, PIS/COFINS/CSLL) |
| 18-19 | Validacao EFD ICMS/IPI (PVA) |
| 19-20 | Validacao EFD Contribuicoes (PVA) |
| 20 | Transmissao SPED |
| 25 | GIA / GISS |

## Checklist Entrada

- NFe de entrada importadas
- CFOP confere (1xxx=DF, 2xxx=FE)
- NCM conferido (8 digitos)
- CST ICMS correto (00, 10, 20, 40, 41, 50, 51, 60, 70, 90)
- Aliquota ICMS confere
- ICMS-ST calculado
- IPI destacado (industria)
- PIS/COFINS aliquotas (1.65/7.6 ou 2/9.25)
- Importacoes: DI, II, AFRMM

## Checklist Saida

- NFe/NFCe/NFs-e/CT-e/MDF-e emitidos
- Devolucoes e cancelamentos
- DIFAL vendas para FE
- Remessas (industria, conserto, amostra)
- Transferencias entre filiais
- Bonificacoes e brindes
- Exportacoes com RE e DI

## Apuracao

- ICMS: debitos - creditos = saldo
- ICMS-ST: apuracao em separado
- IPI: apuracao propria (industria)
- PIS: cumulativo (0.65%) ou nao-cumulativo (1.65%)
- COFINS: cumulativo (3%) ou nao-cumulativo (7.6%)
- ISS: servicos tomados e prestados
- IRRF: 1.5% sobre servicos
- PIS/COFINS/CSLL retido: 4.65% (Lei 10.833)

## EFD ICMS/IPI - Blocos

0: Abertura | C: Documentos | E: Apuracao | H: Inventario | 1: Outros | 9: Encerramento

## Erros Comuns

| Codigo | Causa | Solucao |
|--------|-------|---------|
| 204 | Duplicidade NFe | Cancelar duplicada |
| 539 | Chave diferente | Conferir manifestacao |
| 972 | Resp tecnico | Atualizar certidao |
| E0312 | Cod trib nacional | Conferir cod servico |
| D750 PVA 603 | Erro schema | Verificar layout |

## Referencias

- EFD ICMS/IPI - Guia Pratico
- EFD Contribuicoes - Manual
- PVA - Programa Validador

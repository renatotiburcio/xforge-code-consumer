---
id: knowledge-glossario-cfop
type: knowledge
title: CFOP - Codigo Fiscal de Operacoes e Prestacoes
category: glossario
domain: fiscal
trustScore: 90
source: human-expert
createdAt: 2026-06-14
lastValidated: 2026-06-14
tags: [cfop, fiscal, icms, nfe, sped]
---

# CFOP - Codigo Fiscal de Operacoes e Prestacoes

## Definicao

O **CFOP** e o codigo de 4 digitos que identifica a **natureza da operacao**
( circulacao de mercadorias ou prestacao de servicos ) para fins de
apuracao de ICMS, IPI, PIS/COFINS e geracao de livros fiscais.

Definido pelo **Convenio SINIEF** e usado em:

- NFe / NFCe
- NFSe
- SPED Fiscal (EFD ICMS/IPI)
- Livros de entradas e saidas

## Estrutura

```
XX.YY
  YY = Operacao especifica (00-99)
XX  = Grupo
```

### Grupos principais

| Primeiro digito | Significado | Exemplo |
|-----------------|-------------|---------|
| 1.x.x.x | Entrada | 1.102 = Compra para comercializacao |
| 2.x.x.x | Saida | 2.102 = Venda de mercadoria |
| 3.x.x.x | Prestacao de servicos de transporte | 3.102 = Transporte interestadual |
| 5.x.x.x | Vendas de energia eletrica / comunicacao | 5.102 = Venda de energia |
| 6.x.x.x | Outras saidas (transferencia, devolucao) | 6.102 = Devolucao de compra |
| 7.x.x.x | Operacoes de aquisicao de servicos | 7.102 = Compra de servico de transporte |

## CFOPs mais comuns

| CFOP | Descricao | Tipo |
|------|-----------|------|
| 1.102 | Compra para comercializacao | Entrada |
| 1.401 | Compra para industrializacao | Entrada |
| 1.556 | Compra de material para uso/consumo | Entrada |
| 1.949 | Outra entrada de mercadoria | Entrada |
| 2.102 | Venda de mercadoria | Saida |
| 2.401 | Venda de producao do estabelecimento | Saida |
| 2.405 | Venda de mercadoria recebida de terceiros | Saida |
| 2.556 | Venda de material de uso/consumo | Saida |
| 2.949 | Outra saida de mercadoria | Saida |
| 5.102 | Venda de energia eletrica | Saida |
| 6.102 | Devolucao de compra | Entrada (ajuste) |
| 7.949 | Outra prestacao de servico | Entrada |

## Validacoes

- CFOP x CST (Codigo de Situacao Tributaria) devem ser compativeis
- CFOP x finalidade NFe (1=normal, 2=complementar, 3=ajuste, 4=devolucao)
- CFOP x tipo de operacao (entrada/saida) deve estar consistente com direcao do documento

## Referencias

- Convenio SINIEF 06/1989 (CFOP)
- Ajuste SINIEF 13/2010
- Manual de Orientacao do Contribuinte (NFe)
- Tabela CFOP atualizada: https://www.confaz.fazenda.gov.br/


---
id: icms-st-substituicao-tributaria
type: dominio
title: ICMS-ST: Substituicao Tributaria Detalhada com Exemplos
domain: fiscal
trustScore: 88
source: XForge + CONFAZ + legislacao estadual
tags: [icms, st, confa]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# ICMS-ST: Substituicao Tributaria

## Conceito

A Substituicao Tributaria (ICMS-ST) transfere a responsabilidade do recolhimento do ICMS para um contribuinte da cadeia (geralmente fabricante/importador ou distribuidor).

## Tipos

| Tipo | Descricao | Exemplo |
|------|-----------|---------|
| Para frente | Industrial paga + repassa | Fabricante cerveja |
| Para tras | Recolhe retroativo | Combustivel |
| Concomitante | Mesmo momento | Atacadista |

## Quando Aplica

- Operacoes interestaduais com MVA
- Produtos com acordo CONFAZ
- Produtos regulados (medicamentos, combustiveis, bebidas, cigarros, autopecas)
- Operacoes com destinatario nao contribuinte

## Calculo

### Base de Calculo (MVA)

```
Base ST = (Valor operacao + IPI + Frete + Seguro + Outras) x (1 + MVA)
```

Ou:

```
Base ST = (Valor operacao - ICMS proprio) x (1 + MVA)
```

### Valor ICMS-ST

```
ICMS-ST = (Base ST x Aliquota destino) - ICMS proprio
```

## Exemplo Pratico

```
Produto: Notebook
Valor operacao: R$ 5.000
ICMS proprio (12% interestadual): R$ 600
MVA: 40%
Aliquota destino (SP): 18%

Base ST = 5.000 x 1.40 = R$ 7.000
ICMS destino = 7.000 x 18% = R$ 1.260
ICMS-ST a recolher = 1.260 - 600 = R$ 660
```

## MVA - Margem de Valor Agregado

| Categoria | MVA Media |
|-----------|-----------|
| Eletronicos | 30-50% |
| Cosmeticos | 40-60% |
| Eletrodomesticos | 35-50% |
| Autopecas | 50-80% |
| Medicamentos | 30-50% |
| Combustiveis | Definido CONFAZ |

## CEST (Codigo Especificador ST)

| CEST | Descricao |
|------|-----------|
| 01.001.00 | Bebidas alcoolicas |
| 10.001.00 | Autopecas |
| 12.001.00 | Cosmeticos |
| 13.001.00 | Material construcao |
| 17.001.00 | Medicamentos |
| 21.001.00 | Eletronicos |

## DIFAL (ICMS Interestadual)

```
DIFAL = (Base x Aliquota destino) - (Base x Aliquota origem)
```

## Erros Comuns

| Erro | Solucao |
|------|---------|
| MVA desatualizada | Atualizar tabela CONFAZ |
| CEST incorreto | Conferir tabela CEST (NFe rejeicao 977) |
| Esquecer ICMS-ST entrada | Parametrizar gatilho |
| Aliquota destino errada | Validar UF destinatario |
| NCM incorreto | Conferir NCM receita federal |

## Convenios CONFAZ Principais

| Convenio | Assunto |
|----------|---------|
| CONFAZ 13/92 | Combustiveis |
| CONFAZ 52/91 | ST generica |
| CONFAZ 81/93 | Autopecas |
| CONFAZ 110/07 | Medicamento |
| CONFAZ 142/18 | Cigarros |

## SPED EFD ICMS/IPI - Registros ST

| Registro | Conteudo |
|----------|----------|
| 0205 | Alteracoes item com MVA |
| C100 | Documento com ST |
| C101 | Papel imune/isencao |
| C105 | ICMS-ST calculado |
| E200 | Apuracao ICMS-ST UF |
| E210 | Detalhes apuracao |
| E220 | Ajustes ICMS-ST |
| E250 | Obrigacoes ST a recolher |

## Referencias

- CONFAZ - Conselho Nacional Politica Fazendaria
- SINIEF - Sistema Nacional Informacoes Economico-Fiscais
- Regulamento ICMS de cada estado

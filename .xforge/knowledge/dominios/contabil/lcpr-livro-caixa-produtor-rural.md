---
id: lcpr-livro-caixa-produtor-rural
type: conhecimento
tags: [lcpr, produtor-rural, contabilidade-rural, itr, car, ccir, safra]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre LCPR - Livro Caixa do Produtor Rural
- **Seções principais**: Base Legal, Conceito, Quem é Obrigatório, Estrutura do LCPR
- **Tags**: lcpr, produtor-rural, contabilidade-rural, itr, car, ccir, safra
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `lcpr-livro-caixa-produtor-rural` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 10 |


# LCPR - Livro Caixa do Produtor Rural

## Base Legal
- Lei 8.212/1991, art. 25, §1º, III
- Lei 8.213/1991
- IN RFB 1.700/2017
- Lei 13.169/2015 (atualização valores)

## Conceito

O LCPR é um livro de escrituração contábil obrigatório para o produtor rural pessoa física que optou pela tributação com base no lucro presumido, destinado à comprovação da atividade rural e da apuração da receita bruta.

## Quem é Obrigatório

### Produtores Rurais PF
- Com CCIR (Cadastro de Certificação de Imóvel Rural)
- Com CAR (Cadastro Ambiental Rural)
- Com inscrição no CNPJ (se aplicável)
- Optantes pelo Lucro Presumido rural

### Quem NÃO é obrigatório
- PJ em geral (usa ECD/ECF)
- MEI rural (LCPR simplificado)
- Segurados especiais (comprovação simplificada)

## Estrutura do LCPR

### Receitas

#### Receitas da Atividade Rural
| Código | Receita | Descrição |
|--------|---------|-----------|
| 01 | Venda de Produtos | Soja, milho, café, etc. |
| 02 | Venda de Animais | Bovinos, suínos, aves |
| 03 | Serviços Rurais | Aluguel máquinas, prestação serviço |
| 04 | Subvenção | PRONAF, pronafi, subsídios |
| 05 | Outras Receitas | Arrendamento, parceria |

#### Receitas Não-Rurais
| Código | Receita | Descrição |
|--------|---------|-----------|
| 06 | Aluguel | Imóveis urbanos |
| 07 | Outras | Qualquer receita não-rural |

### Despesas

#### Despesas Dedutíveis
| Código | Despesa | Exemplos |
|--------|---------|----------|
| 01 | Sementes | Soja, milho, algodão |
| 02 | Fertilizantes | Adubos, calcário, gesso |
| 03 | Defensivos | Herbicidas, fungicidas, inseticidas |
| 04 | Mão de obra | Trabalhadores, empreitada |
| 05 | Máquinas | Combino, manutenção, depreciação |
| 06 | Terra | Arrendamento, ITR, seguros |
| 07 | Energia | Elétrica, diesel, gasolina |
| 08 | Transporte | Frete, logistics |
| 09 | Outros | Materiais, utensílios, escritório |

#### Despesas Não-Dedutíveis
| Código | Despesa |
|--------|---------|
| 10 | Multas e juros moratórios |
| 11 | Despesas pessoais |
| 12 | Despesas com bens de uso pessoal |
| 13 | Despesas sem documentação |

## Apuração

### Receita Bruta Rural
```
Receita Bruta = Σ Receitas da Atividade Rural (códigos 01 a 05)
```

### Despesas Dedutíveis
```
Despesas = Σ Despesas dedutíveis (códigos 01 a 09)
```

### Lucro/Prejuízo
```
Lucro = Receita Bruta - Despesas Dedutíveis
```

### Base de Cálculo para Tributação

#### Lucro Presumido Rural
```
Base IRPJ = Receita Bruta × 32% (presunção)
Base CSLL = Receita Bruta × 32% (presunção)
Base PIS = Receita Bruta × 1,65%
Base COFINS = Receita Bruta × 7,60%
```

#### Lucro Real Rural
```
Base = Lucro apurado no LCPR
IRPJ = Lucro × 15% (+ adicional 10% se > R$ 20.000/mês)
CSLL = Lucro × 9%
```

## Exemplo Prático

### Dados da Safra 2025

#### Receitas
| Mês | Produto | Quantidade | Preço | Total |
|-----|---------|:----------:|------:|------:|
| Mar | Soja | 500 sc | R$ 120 | R$ 60.000 |
| Abr | Soja | 300 sc | R$ 125 | R$ 37.500 |
| Jul | Milho | 400 sc | R$ 80 | R$ 32.000 |
| Set | Café | 100 sc | R$ 900 | R$ 90.000 |
| **Total** | | | | **R$ 219.500** |

#### Despesas
| Mês | Despesa | Valor |
|-----|---------|------:|
| Jan | Sementes | R$ 15.000 |
| Fev | Fertilizantes | R$ 25.000 |
| Mar | Defensivos | R$ 12.000 |
| Abr | Mão de obra | R$ 18.000 |
| Mai | Máquinas/combustível | R$ 10.000 |
| Jun | ITR | R$ 3.000 |
| Jul | Seguros | R$ 2.000 |
| **Total** | | **R$ 85.000** |

#### Apuração
```
Receita Bruta: R$ 219.500
(-) Despesas: R$ 85.000
= Lucro: R$ 134.500

IRPJ (32%): R$ 134.500 × 32% = R$ 43.040
IRPJ (15%): R$ 43.040 × 15% = R$ 6.456
CSLL (9%): R$ 43.040 × 9% = R$ 3.874
PIS (1,65%): R$ 219.500 × 1,65% = R$ 3.622
COFINS (7,60%): R$ 219.500 × 7,60% = R$ 16.682

Total Impostos: R$ 30.634
```

## Documentos Obrigatórios

| Documento | Descrição | Validade |
|-----------|-----------|----------|
| CCIR | Certificação de imóvel rural | Anual |
| CAR | Cadastro ambiental rural | Anual |
| ITR | Imposto territorial rural | Anual |
| Notas fiscais | Entradas e saídas | Contínuo |
| NF-e de venda | Produtos rurais | Contínuo |
| Contratos | Arrendamento, parceria | Contínuo |
| Folha de pagamento | Mão de obra rural | Mensal |

## Obrigações Acessórias

### Para Lucro Presumido Rural
| Obrigação | Prazo |
|-----------|-------|
| LCPR | Anual |
| DIRF | Anual |
| SPED Contribuições | Mensal |
| eSocial (se tiver empregados) | Mensal |

### Para Lucro Real Rural
| Obrigação | Prazo |
|-----------|-------|
| ECD | Dia 31/07 |
| ECF | Dia 31/07 |
| LCPR (complementar) | Dia 31/07 |
| DCTFWeb | Dia 15 mês seguinte |

## Diferença para Atividade Urbana

| Aspecto | Rural | Urbano |
|---------|-------|--------|
| Presunção IRPJ | 32% | 32% (serviços) |
| Presunção CSLL | 32% | 32% |
| PIS | 1,65% | 0,65% (LP) ou 1,65% (LR) |
| COFINS | 7,60% | 3,00% (LP) ou 7,60% (LR) |
| Livro Caixa | LCPR | Não tem |
| Escrituração | Simplificada | Completa |

## Fontes Oficiais
- Lei 8.212/1991, art. 25
- IN RFB 1.700/2017
- Lei 13.169/2015
- Portal da Receita Federal

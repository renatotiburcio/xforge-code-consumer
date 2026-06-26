---
id: financeiro-completo
type: conhecimento
tags: [financeiro, centros-custo, rateios, orcamentos, forecast, dre, kpis]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Financeiro - Guia Completo
- **Seções principais**: Centros de Custo, Orçamentos, Forecast Financeiro, DRE Gerencial
- **Tags**: financeiro, centros-custo, rateios, orcamentos, forecast, dre, kpis
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `financeiro-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 8 |


# Financeiro - Guia Completo

## Centros de Custo

### Conceito
Unidade de negócios ou atividade para controle de receitas e despesas.

### Estrutura Hierárquica
```
1.0 - Matriz
  1.1 - Administrativo
    1.1.1 - RH
    1.1.2 - TI
    1.1.3 - Financeiro
  1.2 - Comercial
    1.2.1 - Vendas SP
    1.2.2 - Vendas RJ
    1.2.3 - E-commerce
  1.3 - Industrial
    1.3.1 - Produção A
    1.3.2 - Produção B
  2.0 - Filial SP
  3.0 - Filial RJ
```

### Rateio de Custos
#### Fixos (Proporcional)
```
Aluguel rateado = Aluguel Total × (Funcionários do CC / Total de Funcionários)
```

#### Variáveis (Base de Alocação)
```
TI rateado = Custo TI × (Usuários do CC / Total de Usuários)
```

#### Múltiplas Bases
```
Rateio = Σ (Custo × Base de Alocação) / Total da Base
```

### Exemplo de Rateio
| Centro de Custo | Funcionários | Funcionários % | Custo Rateado |
|-----------------|:------------:|:--------------:|--------------:|
| RH | 5 | 10% | R$ 2.000 |
| TI | 15 | 30% | R$ 6.000 |
| Vendas SP | 20 | 40% | R$ 8.000 |
| Produção | 10 | 20% | R$ 4.000 |
| **Total** | **50** | **100%** | **R$ 20.000** |

## Orçamentos

### Tipos
| Tipo | Prazo | Uso |
|------|-------|-----|
| Operacional | Mensal/Anual | Controle de despesas |
| Estratégico | 3-5 anos | Planejamento |
| Projetos | Por projeto | Controle de investimento |

### Processo Orçamentário
```
1. Diretrizes estratégicas
2. Propostas dos centros de custo
3. Consolidação e negociação
4. Aprovação (assembleia/diretoria)
5. Controle mensal (realizado vs orçado)
6. Review e ajustes
```

### Fórmulas de Controle
```
Desvio = Realizado - Orçado
Desvio % = (Desvio / Orçado) × 100
Execução % = (Realizado / Orçado) × 100
```

### Indicadores Orçamentários
| Indicador | Fórmula | Meta |
|-----------|---------|------|
| Execução orçamentária | Realizado / Orçado | 90-110% |
| Desvio acumulado | Σ Desvios mensais | < 5% |
| Acuracidade do forecast | 1 - |Previsto-Real|/Real | > 90% |

## Forecast Financeiro

### Métodos
| Método | Descrição | Precisão |
|--------|-----------|:--------:|
| Histórico | Média dos últimos 12 meses | Baixa |
| Sazonal | Média com ajuste sazonal | Média |
| Bottom-up | Soma de previsões individuais | Alta |
| Rolling | Atualização contínua (12 meses) | Alta |

### Forecast de Receitas
```
Forecast = Pedidos em Aberto + Previsão Vendas + Sazonalidade
```

### Forecast de Despesas
```
Forecast = Despesas Fixas + (Variáveis × Volume Esperado) + Investimentos
```

## DRE Gerencial

### Estrutura
```
Receita Bruta de Vendas
(-) Deduções (devoluções, abatimentos, impostos sobre vendas)
= Receita Líquida
(-) Custo dos Produtos/Serviços Vendidos
= Lucro Bruto
(-) Despesas Operacionais
  (-) Despesas Administrativas
  (-) Despesas Comerciais
  (-) Despesas de P&D
  (-) Despesas Financeiras (líquidas)
= EBITDA
(-) Depreciação e Amortização
= EBIT (Lucro Operacional)
(-) Resultado Não Operacional
(-) Imposto de Renda e CSLL
= Lucro Líquido
```

### Margens
| Margem | Fórmula | Target |
|--------|---------|--------|
| Margem Bruta | Lucro Bruto / Receita Líquida | > 40% |
| Margem Operacional | EBIT / Receita Líquida | > 15% |
| Margem Líquida | Lucro Líquido / Receita Líquida | > 10% |
| EBITDA | EBITDA / Receita Líquida | > 20% |

## KPIs Financeiros

### Liquidez
| KPI | Fórmula | Meta |
|-----|---------|------|
| Liquidez Geral | AC / PC | > 1,5 |
| Liquidez Corrente | AC / PC (curto prazo) | > 1,2 |
| Liquidez Seca | (AC - Estoques) / PC | > 1,0 |
| Liquidez Imediata | Disponível / PC | > 0,5 |

### Solvência
| KPI | Fórmula | Meta |
|-----|---------|------|
| Endividamento | PL / Ativo | < 0,6 |
| Cobertura de Juros | EBIT / Juros | > 3 |
| Dívida Líquida / EBITDA | (Financiamentos - Caixa) / EBITDA | < 3 |

### Rentabilidade
| KPI | Fórmula | Meta |
|-----|---------|------|
| ROA | Lucro Líquido / Ativo Total | > 5% |
| ROE | Lucro Líquido / PL | > 15% |
| ROI | Lucro / Investimento | > 20% |
| Margem EBITDA | EBITDA / Receita | > 15% |

### Eficiência
| KPI | Fórmula | Meta |
|-----|---------|------|
| Giro de Estoque | CVMS / Estoque Médio | > 4x |
| Giro de Recebíveis | Receita / Contas a Receber | > 12x |
| Giro de Pagáveis | CMV / Contas a Pagar | ~12x |
| Ciclo de Caixa | Giro Estoque + Giro CR - Giro CP | < 60 dias |

## Conciliação Financeira

### Diária
1. Saldo bancário vs extrato
2. Cheques emitidos vs compensados
3. Transferências entre contas

### Mensal
1. Fechamento de caixa
2. Conciliação bancária completa
3. Apuração de resultados

### Anual
1. Fechamento contábil
2. Demonstrações contábeis
3. Declaração de IR

## Fluxo de Caixa Detalhado

### Componentes
```
Saldo Inicial
+ Recebimentos Operacionais
+ Recebimentos de Investimentos
+ Recebimentos Financeiros
(-) Pagamentos a Fornecedores
(-) Pagamentos de Pessoal
(-) Pagamentos de Impostos
(-) Pagamentos Financeiros
(-) Investimentos em Imobilizado
= Saldo Final
```

### Projeção
| Mês | Saldo Inicial | Receitas | Despesas | Saldo Final |
|-----|-------------:|---------:|---------:|------------:|
| Jan | 100.000 | 250.000 | 220.000 | 130.000 |
| Fev | 130.000 | 280.000 | 230.000 | 180.000 |
| Mar | 180.000 | 300.000 | 240.000 | 240.000 |

## Fontes Oficiais
- Lei 6.404/76
- NBC TG 26 (CPC 26)
- NBC TG 28 (CPC 27)
- CPC 38 (Instrumentos Financeiros)

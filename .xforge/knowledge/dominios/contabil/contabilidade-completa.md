---
id: contabilidade-completa
type: conhecimento
tags: [contabil, partidas-dobradas, encerramento, conciliacao, balancete, diario, razao]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Contabilidade - Guia Completo
- **Seções principais**: Partidas Dobradas, Livros Contábeis, Demonstrações Contábeis, Encerramento Contábil
- **Tags**: contabil, partidas-dobradas, encerramento, conciliacao, balancete, diario, razao
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `contabilidade-completa` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 7 |


# Contabilidade - Guia Completo

## Partidas Dobradas

### Conceito
Toda transação contábil afeta pelo menos duas contas: uma de débito e uma de crédito, com valores iguais.

### Regra
```
Σ Débitos = Σ Créditos
```

### Exemplos

#### Venda à Vista
```
Débito:  Caixa (1.01.01.001)           R$ 10.000
Crédito: Receita de Vendas (3.01.01)   R$ 10.000
```

#### Venda a Prazo
```
Débito:  Contas a Receber (1.01.02)    R$ 10.000
Crédito: Receita de Vendas (3.01.01)   R$ 10.000
```

#### Compra de Material
```
Débito:  Estoques (1.01.03)            R$ 5.000
Crédito: Fornecedores (2.01.01)        R$ 5.000
```

#### Pagamento de Fornecedor
```
Débito:  Fornecedores (2.01.01)        R$ 5.000
Crédito: Caixa/Banco (1.01.01)         R$ 5.000
```

#### Folha de Pagamento
```
Débito:  Despesa com Pessoal (4.01.01)  R$ 30.000
Crédito: Salários a Pagar (2.01.02)    R$ 22.000
Crédito: INSS a Recolher (2.01.03)     R$ 5.000
Crédito: FGTS a Recolher (2.01.04)     R$ 2.400
Crédito: IRRF a Recolher (2.01.05)     R$ 600
```

## Livros Contábeis

### Diário
- Registra todas as transações cronologicamente
- Cada lançamento tem: data, histórico, débito, crédito, valor

| Data | Histórico | Conta Débito | Conta Crédito | Valor |
|------|-----------|-------------|---------------|------:|
| 01/02 | Venda cliente X | 1.01.02 | 3.01.01 | 10.000 |
| 01/02 | Custo venda | 4.02.01 | 1.01.03 | 6.000 |

### Razão
- Extrato de cada conta contábil
- Mostra todas as movimentações de uma conta

| Data | Histórico | Débito | Crédito | Saldo |
|------|-----------|-------:|--------:|------:|
| 01/02 | Venda | 10.000 | - | 10.000 |
| 05/02 | Recebimento | - | 10.000 | 0 |

### Balancete
- Resumo de todas as contas em um período
- Mostra saldos devedores e credores

| Conta | Descrição | Débito | Crédito | Saldo |
|-------|-----------|-------:|--------:|------:|
| 1.01.01 | Caixa | 50.000 | 30.000 | 20.000 D |
| 2.01.01 | Fornecedores | 10.000 | 25.000 | 15.000 C |
| 3.01.01 | Receitas | - | 100.000 | 100.000 C |

## Demonstrações Contábeis

### Balanço Patrimonial
```
ATIVO                              PASSIVO + PL
┌─────────────────────┐           ┌─────────────────────┐
│ Circulante          │           │ Circulante          │
│  Caixa         20.000│           │  Fornecedores  25.000│
│  Receber       45.000│           │  Salários       8.000│
│  Estoques      35.000│           │  Impostos       7.000│
│                     │           │                     │
│ Não Circulante      │           │ Não Circulante      │
│  Imobilizado  80.000│           │  Empréstimos   40.000│
│  Intangível   20.000│           │                     │
│                     │           │ PL                  │
│                     │           │  Capital        50.000│
│                     │           │  Lucro Acum.    75.000│
│ TOTAL        200.000│           │ TOTAL          200.000│
└─────────────────────┘           └─────────────────────┘
```

### Demonstração do Resultado (DRE)
```
Receita Bruta                      500.000
(-) Deduções                       (50.000)
= Receita Líquida                  450.000
(-) CMV                           (270.000)
= Lucro Bruto                      180.000
(-) Despesas Operacionais         (100.000)
  (-) Administrativas              (40.000)
  (-) Comerciais                   (35.000)
  (-) Financeiras (líquidas)       (25.000)
= EBITDA                            80.000
(-) D&A                            (20.000)
= EBIT                              60.000
(-) IR/CSLL                        (15.000)
= Lucro Líquido                     45.000
```

### Demonstração do Fluxo de Caixa (DFC)
```
FLUXO OPERACIONAIS
  Lucro Líquido                     45.000
  (+) D&A                           20.000
  (-) Aumento CR                    (5.000)
  (+) Aumento CP                     8.000
= Caixa Operacional                  68.000

FLUXO DE INVESTIMENTOS
  (-) Aquisição imobilizado         (30.000)
= Caixa Investimentos               (30.000)

FLUXO FINANCEIRO
  (+) Empréstimo tomado              40.000
  (-) Amortização                   (20.000)
= Caixa Financeiro                   20.000

VARIAÇÃO LÍQUIDA                     58.000
Saldo Inicial                        10.000
SALDO FINAL                          68.000
```

## Encerramento Contábil

### Passos do Encerramento

#### 1. Conciliação
- Conciliar todas as contas de balancete
- Verificar inventário de estoques
- Conciliar contas bancárias

#### 2. Ajustes
- Depreciação de imobilizado
- Amortização de intangível
- Provisão para devedores duvidosos
- Provisão para impostos
- Reclassificação de contas

#### 3. Apuração do Resultado
```
Receitas - Despesas = Resultado do Exercício
```

#### 4. Encerramento das Contas de Resultado
```
Débito:  Contas de Receita       R$ 500.000
Crédito: Resultado do Exercício  R$ 500.000

Débito:  Resultado do Exercício  R$ 455.000
Crédito: Contas de Despesa      R$ 455.000
```

#### 5. Apropriação do Resultado
```
Débito:  Resultado do Exercício  R$ 45.000
Crédito: Lucro Acumulado        R$ 45.000
```

## Conciliação Contábil

### Tipos
| Tipo | Frequência | Escopo |
|------|:----------:|--------|
| Bancária | Diária/Mensal | Extrato vs lançamentos |
| Clientes | Mensal | Fichas vs NFS emitidas |
| Fornecedores | Mensal | Fichas vs NFS recebidas |
| Estoques | Mensal | Sistema vs físico |
| Fiscal | Mensal | EFD vs demonstrações |
| Interna | Mensal | Balancete de verificação |

### Procedimento
1. Extrair saldos do sistema
2. Extrair saldos da fonte (banco, cliente, etc.)
3. Identificar divergências
4. Investigar causas
5. Ajustar lançamentos
6. Validar conciliação

## Normas Contábeis

### CPCs Mais Utilizados
| CPC | Assunto |
|-----|---------|
| CPC 00 | Apresentação das Demonstrações Contábeis |
| CPC 16 | Estoques |
| CPC 24 | Provisões |
| CPC 25 | Contingências |
| CPC 26 | Demonstrações Contábeis |
| CPC 27 | Ativo Imobilizado |
| CPC 29 | Arrendamentos |
| CPC 38 | Instrumentos Financeiros |
| CPC 47 | Receita de Contrato com Cliente |

### Hierarquia
```
CF/88 → Lei 6.404/76 → Lei 11.638/07 → NBC TG (CPCs) → Interpretações
```

## Fontes Oficiais
- Lei 6.404/76
- Lei 11.638/2007
- CPC (cfc.org.br)
- IFRS Foundation
- RFB (SPED Contábil)

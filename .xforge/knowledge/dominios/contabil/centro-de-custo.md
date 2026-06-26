---
id: contabil-centro-de-custo
type: domain
tags: [contabil, centro-de-custo, rateio, custos, dres-por-cc, rh, fiscal]
owner: contabil
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Centro de Custo
- **Seções principais**: Propósito, Responsabilidades, Dependências, Restrições
- **Tags**: contabil, centro-de-custo, rateio, custos, dres-por-cc, rh, fiscal
- **Tipo**: domain | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `contabil-centro-de-custo` |
| Tipo | domain |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | contabil |
| Total de seções | 5 |


# Centro de Custo

## Propósito

Agrupar despesas e receitas por unidade organizacional para controle, análise de resultados e tomada de decisão gerencial. Permite apurar resultado por departamento, filial, projeto ou linha de negócio.

## Responsabilidades

**Conceito:** Centro de custo é uma unidade de agrupamento de gastos que permite rastrear despesas às áreas responsáveis, viabilizando DRE por centro de custo e rateio de custos indiretos.

**Estrutura Hierárquica:**

`
EMPRESA
├── MATRIZ
│   ├── ADMINISTRATIVO
│   │   ├── FINANCEIRO
│   │   ├── CONTABILIDADE
│   │   └── TI
│   ├── COMERCIAL
│   │   ├── VENDAS INTERNA
│   │   ├── VENDAS EXTERNA
│   │   └── MARKETING
│   └── OPERACIONAL
│       ├── PRODUÇÃO
│       └── LOGÍSTICA
├── FILIAL 01
│   ├── LOJA
│   └── ESTOQUE
└── FILIAL 02
    ├── LOJA
    └── ESTOQUE
`

**Rateio de Custos Indiretos:**

| Custo Indireto | Base de Rateio | Destino |
|----------------|----------------|---------|
| Aluguel | Área m² | Todos os CC |
| Energia | Potência instalada | Produção, Loja |
| TI | Nº de usuários | Todos os CC |
| RH | Nº de funcionários | Todos os CC |
| Contabilidade | Receita | Todos os CC |
| Depreciação | Ativo alocado | CC responsável |

O rateio deve ser consistente entre períodos. Base de rateio definida por diretoria.

**DRE por Centro de Custo:**

`
                     TOTAL      ADM    COMERCIAL    OPERACIONAL
Receita Líquida     830.000      -     830.000            -
CMV                (400.000)     -    (400.000)           -
Lucro Bruto         430.000      -     430.000            -
Desp. Vendas        (50.000)     -     (50.000)           -
Desp. Admin        (120.000) (120.000)    -              -
Desp. Operacional  (80.000)      -        -          (80.000)
Resultado           180.000  (120.000) 380.000       (80.000)
`

**Integração com RH:** Cada funcionário é vinculado a um centro de custo. Os lançamentos de folha distribuem automaticamente salários e encargos ao CC correspondente.

**Integração com Fiscal:** O registro I100 da ECD exige a identificação do centro de custo nos lançamentos contábeis.

## Dependências

- **escrituracao-contabil.md** — vinculação do CC nos lançamentos
- **ecd.md** — registro I100 (centro de custos na ECD)
- **contabilidade-custos.md** — métodos de rateio e custeio

## Restrições

- Funcionário deve estar vinculado a um CC para geração dos lançamentos de folha
- Rateio deve ser documentado e consistente
- Alterações na estrutura de CC exigem planejamento retroativo para comparações
- CC inativo não pode receber novos lançamentos

## Documentos Relacionados

- ECD — Registro I100 (Centro de Custos)
- ERP — Módulo Folha de Pagamento (vinculação funcionário → CC)
- NBC — Contabilidade de Custos

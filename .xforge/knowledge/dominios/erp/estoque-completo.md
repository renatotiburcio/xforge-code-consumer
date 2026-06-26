---
id: estoque-completo
type: conhecimento
tags: [estoque, curva-abc, mrp, wms, custo-medio, fifo, lote, validade, kardex]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Estoque - Guia Completo
- **Seções principais**: Conceitos Fundamentais, Métodos de Avaliação, Curva ABC, MRP (Material Requirements Planning)
- **Tags**: estoque, curva-abc, mrp, wms, custo-medio, fifo, lote, validade, kardex
- **Restrições/Regras**: **Proibido** em sistema ERP; Validar sempre: Quantidade Disponível ≥ 0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `estoque-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 12 |


# Estoque - Guia Completo

## Conceitos Fundamentais

### Tipos de Estoque
| Tipo | Descrição |
|------|-----------|
| **Físico** | Quantidade real disponível no almoxarifado |
| **Disponível** | Físico - Reservado - Bloqueado |
| **Reservado** | Comprometido com pedidos em aberto |
| **Bloqueado** | Avariado, em análise, ou retenção fiscal |
| **Projecionado** | Disponível + Pedidos de Compra - Pedidos de Venda |

### Fluxo de Estoque
```
Entrada → Armazenagem → Reserva → Expedição → Baixa
   ↓          ↓           ↓          ↓         ↓
 Kardex    Estoque     Reservado   Saída     Custo
```

## Métodos de Avaliação

### Custo Médio Ponderado
```
Custo Médio = (Saldo Anterior + Entradas) / (Qtd Anterior + Qtd Entradas)
```

| Mês | Entrada | Qtd | Custo Unit. | Saldo Qtd | Saldo Valor | Custo Médio |
|-----|--------:|----:|------------:|----------:|------------:|------------:|
| Jan | - | - | - | 100 | R$ 5.000 | R$ 50,00 |
| Fev | Compra | 50 | R$ 55,00 | 150 | R$ 7.750 | R$ 51,67 |
| Mar | Compra | 30 | R$ 48,00 | 180 | R$ 9.190 | R$ 51,06 |

### FIFO (First In, First Os primeiros a entrar são os primeiros a sair
```
Saída unitário = Custo da 1ª entrada disponível
```

### FIFO Legal (Art. 166, Lei 6.404/76)
- Para tributação (IRPJ, CSLL)
- Pode diferir do custo contábil
- Cálculo separado para efeito fiscal

### UEPS (Proibido no Brasil)
- Não é aceito pela legislação brasileira
- Gera estoque "phantom" com custos antigos

## Curva ABC

### Classificação por Valor
| Classe | % do Valor | % dos Itens | Ação |
|--------|:----------:|:-----------:|------|
| **A** | 80% | 20% | Controle rígido, revisão semanal |
| **B** | 15% | 30% | Controle moderado, revisão mensal |
| **C** | 5% | 50% | Controle simples, revisão trimestral |

### Cálculo
1. Listar itens por valor total (Qtd × Custo)
2. Ordenar do maior para o menor
3. Calcular % acumulado do valor
4. Classificar: A (até 80%), B (80-95%), C (95-100%)

### Exemplo
| Item | Qtd | Custo Unit. | Total | % Acum. | Classe |
|------|----:|------------:|------:|--------:|:------:|
| 1 | 100 | R$ 500 | R$ 50.000 | 50% | A |
| 2 | 200 | R$ 150 | R$ 30.000 | 80% | A |
| 3 | 500 | R$ 20 | R$ 10.000 | 90% | B |
| 4 | 1000 | R$ 5 | R$ 5.000 | 95% | B |
| 5 | 2000 | R$ 2,50 | R$ 5.000 | 100% | C |

## MRP (Material Requirements Planning)

### Entradas
- Estoque disponível
- Pedidos de compra em aberto
- Lead time de fornecedores
- Lote mínimo e múltiplo

### Processamento
```
Demanda → Necessidade Líquida → Planejamento → Pedido de Compra
  ↓              ↓                  ↓              ↓
Previsão     Estoque atual    Lote econômico   Fornecedor
```

### Fórmulas
```
Necessidade Líquida = Demanda - Estoque Disponível - Reservas
Ponto de Pedido = Consumo Diário × Lead Time + Estoque Segurança
Estoque Segurança = Desvio Padrão × Z × √Lead Time
```

## Lote e Rastreabilidade

### Gestão por Lote
- Cada entrada gera novo lote
- Lote vinculado a NF-e de entrada
- Rastreabilidade:ornecedor → Lote → Produto → Pedido de Venda

### Validade
- FEFO (First Expired, First Out)
- Alertas de vencimento (30, 15, 7 dias)
- Bloqueio automático de lotes vencidos

### Rastreabilidade Completa
```
Fornecedor → NF-e → Lote → Entrada Estoque → Reserva → Expedição → Pedido de Venda → Cliente
```

## Kardex

### Estrutura
| Data | Doc | Histórico | Entrada Qtd | Entrada $ | Saída Qtd | Saldo Qtd | Saldo $ |
|------|-----|-----------|------------:|----------:|----------:|----------:|--------:|
| 01/02 | NF-123 | Compra | 100 | 5.000 | - | 100 | 5.000 |
| 05/02 | PD-456 | Venda | - | - | 50 | 50 | 2.500 |
| 10/02 | NF-456 | Compra | 80 | 4.200 | - | 130 | 6.700 |

## Inventário

### Inventário Físico
- Contagem física de todos os itens
- Comparação com estoque do sistema
- Ajuste via lançamento contábil
- Frequência: anual (obrigatório) + rotativo

### Procedimento
1. Paralisação de movimentações
2. Contagem física (1ª contagem)
3. Conferência (2ª contagem divergência)
4. Recontagem (3ª contagem se necessário)
5. Ajuste no sistema
6. Lançamento contábil

## Custos de Estoque

### Componentes do Custo
| Componente | Descrição |
|------------|-----------|
| Custo de aquisição | Preço de compra + frete + seguros |
| Custo de importação | II + ICMS-importação + desembaraço |
| Custo de produção | Mão de obra + overhead + materiais |
| Custo de oportunidade | Capital parado no estoque |

### Indicadores
| Indicador | Fórmula | Target |
|-----------|---------|--------|
| Giro de Estoque | Custo Vendas / Estoque Médio | > 4x/ano |
| Dias de Estoque | 365 / Giro | < 90 dias |
| Cobertura | Estoque / Consumo Diário | 30-60 dias |
| Fill Rate | Pedidos atendidos / Pedidos totais | > 95% |

## Transferências

### Entre Filiais
1. Criar transferência de origem (saída)
2. Criar transferência de destino (entrada)
3. CFOP de transferência (6.151/1.151)
4. ICMS: crédito na origem, débito no destino
5. Rastreabilidade por lote mantida

### Processo
```
Filial A (Origem) → Transferência → Filial B (Destino)
     ↓                                   ↓
  Saída (-)                         Entrada (+)
  CFOP 6.151                        CFOP 1.151
```

## Regras de Negócio

### Estoque Negativo
- **Proibido** em sistema ERP
- Validar sempre: Quantidade Disponível ≥ 0
- Se Tentar Saída > Disponível → bloquear

### Reserva
- Reserva automática ao criar pedido de venda
- Liberação automática ao cancelar pedido
- Conflito: 2 pedidos para mesma unidade → fila

### Revisão Periódica
- A (20%): revisão semanal
- B (30%): revisão mensal
- C (50%): revisão trimestral

## Integrações

| Módulo | Integração |
|--------|------------|
| Compras | Pedido de compra gera entrada |
| Vendas | Pedido de venda gera reserva |
| Fiscal | Entrada gera NF-e, CFOP, CST |
| Contábil | Custo médio gera lançamento |
| Produção | BOM gera requisição de material |
| WMS | Endereçamento e expedição |

## Fontes Oficiais
- Lei 6.404/76 (Art. 166, 183)
- NBC TG 16 (R2) - Estoques
- NBC TG 26 (CPC 16) - Estoques
- RIR/2018 (Art. 345-346)

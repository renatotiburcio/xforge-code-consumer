---
id: reforma-tributaria-completa
type: conhecimento
tags: [fiscal, reforma, ibs, cbs, split-payment, transicao, 2026-2033]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Reforma Tributária - Guia Completo
- **Seções principais**: Base Legal, Visão Geral, Alíquotas, Split Payment
- **Tags**: fiscal, reforma, ibs, cbs, split-payment, transicao, 2026-2033
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `reforma-tributaria-completa` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 10 |


# Reforma Tributária - Guia Completo

## Base Legal
- Emenda Constitucional 132/2023
- Lei Complementar 214/2025 (IBS/CBS)
- Lei Complementar 215/2025 (IS)
- Lei Complementar 216/2025 (Regulamentação)

## Visão Geral

### 3 Novos Tributos

| Tributo | Substitui | Alíquota Estimada | Competência |
|---------|-----------|:-----------------:|-------------|
| **IBS** (Imposto sobre Bens e Serviços) | ICMS, ISS, IPI, PIS, COFINS, FUNRURAL, SN | ~17,74% | Estados/Municípios |
| **CBS** (Contribuição sobre Bens e Serviços) | IRPJ, CSLL, PIS, COFINS | ~8,87% | União |
| **Imposto Seletivo** | IPI (部分), impostos seletivos | Variável | União |

### Tributos Substituídos

#### IBS substitui:
- ICMS (estadual)
- ISS (municipal)
- IPI (federal)
- PIS (federal)
- COFINS (federal)
- FUNRURAL
- SN (Simples Nacional - parcela I)
- FECP/FCP

#### CBS substitui:
- IRPJ
- CSLL
- PIS (parcela II)
- COFINS (parcela II)

#### Imposto Seletivo incide sobre:
- Combustíveis
- Bebidas alcoólicas
- Tabaco
- Minerais
- Jogos e apostas
- Veículos automotores

## Alíquotas

### IBS
- Alíquota uniforme entre estados (conforme EC 132)
- Prevista: ~17,74% (estimativa inicial do Comitê Gestor)
- Compensação com estados (diferencial de alíquota)
- Setores sensíveis podem ter alíquota zero ou reduzida

### CBS
- Alíquota única federal
- Prevista: ~8,87% (estimativa inicial)
- Pode variar conforme regulamentação

### Imposto Seletivo
- Alíquota variável por produto
- Incide ADICIONAL ao IBS/CBS
- Produtos nocivos: alíquota mais alta
- Exemplos iniciais:
  - Combustíveis: ~25%
  - Bebidas: ~15-30%
  - Tabaco: ~60%
  - Jogos: ~30%

### Carga Tributária Total (estimativa)

| Produto | IBS | CBS | IS | Total |
|---------|:---:|:---:|:--:|:-----:|
| Produto geral | 17,74% | 8,87% | - | 26,61% |
| Combustível | 17,74% | 8,87% | 25% | 51,61% |
| Bebida alcoólica | 17,74% | 8,87% | 20% | 46,61% |
| Tabaco | 17,74% | 8,87% | 60% | 86,61% |
| Serviço geral | 17,74% | 8,87% | - | 26,61% |

## Split Payment

### Conceito
- Pagamento do imposto é feito no momento da transação
- Banco retém automaticamente e repassa ao fisco
- Reduz sonegação e inadimplência

### Fluxo
```
Comprador → Pagamento → Banco → Split Automático
                                ↓
                    IBS retido → Tesouro Estadual
                    CBS retido → Tesouro Federal
                    Valor líquido → Vendedor
```

### Modalidades

#### Split Padrão
- Todos os pagamentos são splitados
- Banco retém IBS + CBS automaticamente
- Vendedor recebe valor líquido

#### Split Voluntário
- Opção do contribuinte
- Pode escolher não usar split
- Mais flexível mas mais risco

### Impacto no ERP/Software

#### Motor de Cálculo
```csharp
public class SplitPaymentCalculator
{
    public SplitResult Calculate(decimal total, string productCategory)
    {
        var ibs = total * GetIbsRate(productCategory);
        var cbs = total * GetCbsRate(productCategory);
        var is = total * GetIsRate(productCategory);
        
        return new SplitResult
        {
            Total = total,
            Ibs = ibs,
            Cbs = cbs,
            ImpostoSeletivo = is,
            TotalImpostos = ibs + cbs + is,
            ValorLiquido = total - ibs - cbs - is
        };
    }
}
```

#### Integração com Gateway
1. Checkout calcula impostos
2. Gateway faz split automático
3. Confirmação via webhook
4. Conciliação: valor líquido vs impostos retidos

## Crédito Financeiro

### Conceito
- Crédito tributário acumulado
- Compensação com débitos futuros
- Prazo: 10 anos

### No Novo Sistema
- Crédito de IBS pode ser compensado com IBS
- Crédito de CBS pode ser compensado com CBS
- NÃO pode compensar IBS com CBS
- Transferência entre filiais: permitida

### Regras de Crédito
| Origem | Compensação | Prazo |
|--------|-------------|-------|
| IBS pago a mais | IBS futuro | 10 anos |
| CBS pago a mais | CBS futuro | 10 anos |
| IS pago a mais | IS futuro | 10 anos |
| Crédito acumulado antigo | Novo IBS/CBS | Regra de transição |

## Período de Transição (2026-2033)

### Fases

| Ano | Fase | O que acontece |
|-----|------|----------------|
| **2026** | **Piloto + NFS-e Nacional** | **CBS: piloto voluntário (Receita Federal). NFS-e padrão nacional obrigatória para Simples Nacional (01/09/2026, Res. CGSN 189/2026). Alíquotas zero em regra geral.** |
| 2027 | CBS e IBS (fase 1) | CBS e IBS começam a valer com alíquotas progressivas |
| 2028 | CBS e IBS (fase 2) | Ampliação da base |
| 2029 | CBS e IBS (fase 3) | Mais setores incluídos |
| 2030 | Eliminação I | Primeiros tributos antigos saem |
| 2031 | Eliminação II | Mais tributos antigos saem |
| 2032 | Eliminação III | Quase todos antigos saem |
| 2033 | Pleno | Sistema 100% operacional (CBS 26,5% + IBS 17,5%) |

### Alíquotas Progressivas (2026-2032)

| Tributo | Alíquota inicial (2026) | Alíquota plena (2033) |
|---------|:-----------------------:|:---------------------:|
| CBS | 0,1% | 26,5% |
| IBS | 0,1% | 17,5% |

### Regras de Transição

#### Para Empresas
- Regime especial para empresas de pequeno porte
- Créditos acumulados: compensação gradual
- Regime especial para setores sensíveis

#### Para Setores Sensíveis
- Saúde: alíquota zero
- Educação: alíquota zero
- Transporte público: alíquota reduzida
- Alimentação básica: alíquota zero
- Moradia: alíquota reduzida

#### Para Estados e Municípios
- Cota-parte do IBS
- Compensação pela União
- Regime fiscal transitório

## Impactos no ERP

### Mudanças Necessárias

#### 1. Motor de Cálculo
- Nova engine para IBS/CBS/IS
- Tabelas por estado (alíquotas)
- Regras por setor/produto
- Créditos acumulados

#### 2. Tabelas Fiscais
- Alíquotas IBS por estado
- Alíquotas CBS (federal)
- Alíquotas IS por produto
- Setores com alíquota zero

#### 3. Split Payment
- Integração com gateway
- Cálculo no momento do pagamento
- Webhook de confirmação
- Conciliação automática

#### 4. Créditos
- Controle de créditos IBS
- Controle de créditos CBS
- Compensação automática
- Transferência entre filiais

#### 5. Relatórios
- DRE: classificação de tributos
- Balanço: passivos de tributos
- ECF: nova estrutura
- SPED: novos layouts

#### 6. NF-e
- Novos campos e layouts
- Identificação do split
- Dados do crédito
- Eventos de compensação

## Adequações Contábeis

### Plano de Contas
```
1.1.1.1 - IBS a Recolher
1.1.1.2 - CBS a Recolher
1.1.1.3 - IS a Recolher
1.1.2.1 - Crédito de IBS
1.1.2.2 - Crédito de CBS
2.1.1.1 - IBS a Pagar
2.1.1.2 - CBS a Pagar
```

### DRE
```
Receita Bruta
(-) Deduções da Receita Bruta
= Receita Líquida
(-) Custo dos Serviços/Produtos
= Lucro Bruto
(-) Despesas Operacionais
(-) IBS e CBS sobre vendas
= Lucro Operacional
(-) Imposto de Renda
= Lucro Líquido
```

### Notas Explicativas
- Transição tributária
- Créditos acumulados
- Impactos nos próximos exercícios
- Riscos e contingências

## Comitê Gestor do IBS/CBS

### Composição
- União (Receita Federal)
- Estados (SEFAZ)
- Municípios (FENAPLEM)

### Atribuições
- Definir alíquotas
- Regulamentar sistemas
- Arbitrar divergências
- fiscalizar arrecadação

### Sistemas
- Cadastro Nacional de Contribuintes
- Sistema de Arrecadação
- Sistema de Fiscalização
- Sistema de Conciliação

## Fontes Oficiais
- EC 132/2023
- Lei Complementar 214/2025
- Lei Complementar 215/2025
- Lei Complementar 216/2025
- Portal da Reforma Tributária (gov.br)
- Comitê Gestor do IBS/CBS

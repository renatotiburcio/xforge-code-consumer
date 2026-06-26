---
id: dctfweb-completo
type: conhecimento
tags: [dctfweb, declaracao, credito, pis, cofins, contribuicao, esocial]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre DCTFWeb - Declaração do Crédito Tributário do PIS/PASEP e da COFINS
- **Seções principais**: Base Legal, Conceito, Obrigação, Eventos
- **Tags**: dctfweb, declaracao, credito, pis, cofins, contribuicao, esocial
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `dctfweb-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 14 |


# DCTFWeb - Declaração do Crédito Tributário do PIS/PASEP e da COFINS

## Base Legal
- Lei 10.637/2002 (PIS não-cumulativo)
- Lei 10.833/2003 (COFINS não-cumulativa)
- Lei 12.890/2013 (DCTFWeb)

## Conceito

A DCTFWeb é a declaração que consolida as contribuições ao PIS/PASEP e à COFINS, substituindo a DIRF e a GFIP para empresas obrigadas ao eSocial.

## Obrigação

### Quem Deve Entregar
- Empresas obrigadas ao eSocial
- Órgãos públicos
- OSCIPs e entidades sem fins lucrativos

### Prazo
- Até o dia 15 do mês seguinte ao de referência
- Fechamento dos eventos do eSocial (S-1299) é pré-requisito

## Eventos

### Evento de Fechamento

| Evento | Descrição | Prazo |
|--------|-----------|-------|
| S-1299 | Fechamento dos Eventos Periódicos | Dia 15 do mês seguinte |

### Eventos de Contribuição

| Evento | Descrição |
|--------|-----------|
| S-1200 | Remuneração dos trabalhadores |
| S-1210 | Pagamentos de rendimentos do trabalho |
| S-1260 | Comercialização da produção rural |
| S-1299 | Fechamento dos eventos periódicos |

## Cálculo da Contribuição

### PIS (Não-Cumulativo)
```
PIS = Receita Bruta × 1,65%
(-) Créditos de PIS
= PIS a Recolher
```

### COFINS (Não-Cumulativo)
```
COFINS = Receita Bruta × 7,60%
(-) Créditos de COFINS
= COFINS a Recolher
```

### PIS (Cumulativo)
```
PIS = Receita Bruta × 0,65%
```

### COFINS (Cumulativo)
```
COFINS = Receita Bruta × 3,00%
```

## Créditos

### Créditos de PIS
| Item | Alíquota |
|------|:--------:|
| Mercadorias para revenda | 1,65% |
| Matéria-prima | 1,65% |
| Energia elétrica | 1,65% |
| Aluguel de imóveis | 1,65% |
| Depreciação de imobilizado | 1,65% |

### Créditos de COFINS
| Item | Alíquota |
|------|:--------:|
| Mercadorias para revenda | 7,60% |
| Matéria-prima | 7,60% |
| Energia elétrica | 7,60% |
| Aluguel de imóveis | 7,60% |
| Depreciação de imobilizado | 7,60% |

## Apuração Mensal

### Passo-a-Passo

1. **Fechamento do eSocial** (S-1299)
2. **Apuração do PIS/COFINS**
   - Receita bruta do período
   - Créditos do período
   - Cálculo da contribuição
3. **Geração da DCTFWeb**
   - Consolidação dos eventos
   - Cálculo do valor a recolher
4. **Transmissão**
   - Assinatura digital
   - Envio via web service
5. **Recolhimento**
   - DARF (Documento de Arrecadação)
   - Prazo: até o dia 20 do mês seguinte

### Exemplo de Apuração

#### Empresa de Comércio (Não-Cumulativo)
| Mês | Receita Bruta | PIS (1,65%) | COFINS (7,60%) |
|-----|-------------:|------------:|---------------:|
| Jan | R$ 200.000 | R$ 3.300 | R$ 15.200 |
| Fev | R$ 250.000 | R$ 4.125 | R$ 19.000 |
| Mar | R$ 300.000 | R$ 4.950 | R$ 22.800 |

#### Com Créditos
| Item | PIS | COFINS |
|------|----:|-------:|
| Receita bruta | R$ 3.300 | R$ 15.200 |
| (-) Crédito mercadorias | R$ 500 | R$ 2.000 |
| (-) Crédito energia | R$ 100 | R$ 400 |
| (-) Crédito aluguel | R$ 50 | R$ 200 |
| **A recolher** | **R$ 2.650** | **R$ 12.600** |

## DARF

### Estrutura do DARF
| Campo | Descrição |
|-------|-----------|
| Código | 8099 (PIS), 5856 (COFINS) |
| Período | Mês/Ano de referência |
| Valor | Valor a recolher |
| Vencimento | Dia 20 do mês seguinte |

### Geração
```csharp
// Exemplo de geração de DARF
var darf = new DARF
{
    Codigo = "8099", // PIS
    Periodo = "01/2025",
    ValorPrincipal = 2650.00m,
    ValorMulta = 0,
    ValorJuros = 0,
    DataVencimento = new DateTime(2025, 2, 20)
};
```

## Retenções

### PIS/COFINS na Fonte
| Tipo | PIS | COFINS |
|------|:---:|:------:|
| Juros de capital próprio | 1,65% | 7,60% |
| Comissões e corretagens | 1,65% | 7,60% |
| Royalties | 1,65% | 7,60% |
| Aluguéis | 1,65% | 7,60% |

### Processo
1. Retenção no pagamento
2. Recolhimento via DARF
3. Declaração na DCTFWeb
4. Crédito para o beneficiário

## Substituição Tributária

### PIS/COFINS-ST
- Aplicada sobre vendas de determinados produtos
- Alíquota varia por produto
- Crédito presumido para o adquirente

## Diferença para DIRF/GFIP

| Aspecto | DIRF/GFIP (antigo) | DCTFWeb (atual) |
|---------|-------------------|-----------------|
| Obrigação | GFIP + DIRF | DCTFWeb |
| Prazo | GFIP: dia 15/DIRF: julho | Dia 15 |
| Eventos | GFIP: movimentações | S-1200 a S-1299 |
| Validação | Manual | Automática (eSocial) |

## Obrigações Acessórias Relacionadas

| Obrigação | Prazo | Finalidade |
|-----------|-------|------------|
| DCTFWeb | Dia 15 | Declaração PIS/COFINS |
| DARF PIS | Dia 20 | Recolhimento PIS |
| DARF COFINS | Dia 20 | Recolhimento COFINS |
| EFD Contribuições | Dia 15 | Escrituração detalhada |
| ECD | Dia 31/07 | Escrituração contábil |

## Penalidades

| Infração | Multa |
|----------|-------|
| Atraso na entrega | R$ 20,00 por dia |
| Informações incorretas | 2% sobre o valor |
| Não entrega | Multa mínima |
| DARF atrasado | Multa de 0,33% por dia + juros SELIC |

## Fontes Oficiais
- Lei 10.637/2002
- Lei 10.833/2003
- Lei 12.890/2013
- Portal eSocial (esocial.gov.br)
- RFB (receita.fazenda.gov.br)

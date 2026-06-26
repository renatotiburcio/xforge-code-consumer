---
id: escrituracao-fiscal-completa
type: conhecimento
tags: [escrituracao, sped, efd, ecd, ecf, apuracao, icms, pis, cofins, irpj, csll]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Escrituração Fiscal - Guia Completo
- **Seções principais**: Visão Geral, EFD ICMS/IPI (Escrituração Fiscal Digital), EFD Contribuições, ECD (Escrituração Contábil Digital)
- **Tags**: escrituracao, sped, efd, ecd, ecf, apuracao, icms, pis, cofins, irpj, csll
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `escrituracao-fiscal-completa` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 9 |


# Escrituração Fiscal - Guia Completo

## Visão Geral

```
Documentos Fiscais → Escrituração → Apuração → Obrigação Acessória → Transmissão
     ↓                    ↓              ↓              ↓                  ↓
NF-e/NFC-e           EFD ICMS/IPI    Cálculo ICMS    SPED Fiscal      SEFAZ
CT-e/MDF-e           EFD Contrib.    Cálculo PIS     SPED Contrib.     eSocial
BPM                  ECD/ECF         Cálculo IPI     ECF              REINF
```

## EFD ICMS/IPI (Escrituração Fiscal Digital)

### Blocos
| Bloco | Registros | Descrição |
|-------|-----------|-----------|
| **0** | 0000-0990 | Abertura e Identificação |
| **C** | C100-C190 | Documentos Fiscais I (Mercadorias) |
| **D** | D100-D190 | Documentos Fiscais II (Serviços) |
| **E** | E100-E530 | Apuração ICMS e IPI |
| **G** | G110-G140 | Crédito ICMS Ativo Permanente |
| **H** | H005-H020 | Inventário Físico |
| **K** | K001-K235 | Controle Produção e Estoque |
| **1** | 1001-1990 | Complemento Escrituração |
| **9** | 9001-9999 | Controle e Encerramento |

### Registros Principais

#### C100 - Documento (NF-e)
| Campo | Descrição |
|-------|-----------|
| COD_MOD | Modelo documento (55=NF-e, 65=NFC-e) |
| COD_SIT | Situação (00=Regular, 02=Cancelado) |
| VL_DOC | Valor do documento |
| VL_BC_ICMS | Base de cálculo ICMS |
| VL_ICMS | Valor do ICMS |
| VL_IPI | Valor do IPI |

#### C170 - Itens do Documento
| Campo | Descrição |
|-------|-----------|
| COD_ITEM | Código do item |
| CFOP | Código de operação |
| CST_ICMS | Situação tributária ICMS |
| CST_IPI | Situação tributária IPI |
| CST_PIS | Situação tributária PIS |
| CST_COFINS | Situação tributária COFINS |
| VL_ITEM | Valor do item |
| VL_BC_ICMS | Base cálculo ICMS |
| VL_ICMS | Valor ICMS |

#### C190 - Registro Analítico
| Campo | Descrição |
|-------|-----------|
| CST_ICMS | Situação tributária |
| CFOP | Código de operação |
| ALIQ_ICMS | Alíquota ICMS |
| VL_OPR | Valor da operação |
| VL_BC_ICMS | Base cálculo |
| VL_ICMS | Valor ICMS |

### Apuração ICMS (E100-E110)

#### E110 - Apuração ICMS Próprias
| Campo | Descrição |
|-------|-----------|
| VL_TOT_DEBITOS | Total débitos |
| VL_AJ_DEBITOS | Ajustes débitos |
| VL_TOT_CREDITOS | Total créditos |
| VL_AJ_CREDITOS | Ajustes créditos |
| VL_SLD_CREDOR | Saldo credor |
| VL_SLD_DEVEDOR | Saldo devedor |
| VL_DED_ANTER | Deduções anteriores |
| VL_ICMS_RECOLHER | ICMS a recolher |
| VL_ICMS_ANTER | ICMS anterior |

### Apuração IPI (E500-E530)

#### E500 - Período Apuração IPI
| Campo | Descrição |
|-------|-----------|
| IND_APUR | 0=Mensal, 1=Trimestral |
| VL_BC_IPI | Base cálculo IPI |
| VL_IPI | Valor IPI |

## EFD Contribuições

### Blocos
| Bloco | Conteúdo |
|-------|----------|
| **0** | Abertura e Identificação |
| **A** | Apuração da Contribuição (1.100-1.800) |
| **C** | Documentos Fiscais (C100-C180) |
| **D** | Documentos de Serviços (D100-D500) |
| **F** | Demais Documentos (F100-F600) |
| **I** | Investimentos (I100-I200) |
| **M** | Apuração (M100-M630) |
| **P** | Contribuição (P100-P230) |

### Registros Principais

#### C100 - Documento (complementar ao EFD ICMS)
| Campo | Contribuição |
|-------|-------------|
| VL_BC_PIS | Base cálculo PIS |
| VL_PIS | Valor PIS |
| VL_BC_COFINS | Base cálculo COFINS |
| VL_COFINS | Valor COFINS |

#### M100 - Crédito PIS
| Campo | Descrição |
|-------|-----------|
| VL_BC_PIS | Base cálculo |
| ALIQ_PIS | Alíquota (0,65% ou 1,65%) |
| VL_CRED | Valor crédito |
| VL_CRED_ORI | Crédito original |
| VL_CRED_EXT | Crédito extemporâneo |

#### M200 - Consolidação PIS
| Campo | Descrição |
|-------|-----------|
| VL_TOT_CONT_NC_PER | Total contribuição não-cumulativa |
| VL_TOT_CRED_DESC | Créditos descontados |
| VL_TOT_CONT_NC_DEV | Contribuição a devolver |
| VL_RET_NC | Retenções não-cumulativas |
| VL_OUT_DED_NC | Outras deduções |
| VL_CONT_NC_REC | Contribuição a recolher |

### Regimes de PIS/COFINS

| Regime | Alíquota PIS | Alíquota COFINS | Dedutível? |
|--------|:------------:|:---------------:|:----------:|
| Cumulativo (LP) | 0,65% | 3,00% | Não |
| Não-cumulativo (LR) | 1,65% | 7,60% | Sim |
| Monofásico | Varia | Varia | Não |
| Substituição | Varia | Varia | Não |

## ECD (Escrituração Contábil Digital)

### Blocos
| Bloco | Conteúdo |
|-------|----------|
| **0** | Abertura |
| **I** | Escrituração Contábil (I001-I990) |
| **J** | Balancetes (J001-J990) |
| **K** | Demonstrações Contábeis (K001-K990) |
| **1** | Complemento |
| **9** | Encerramento |

### Registros Principais
| Registro | Descrição |
|----------|-----------|
| I001 | Abertura do Bloco I |
| I050 | Plano de Contas |
| I051 | Plano de Contas Referencial |
| I100 | Balancetes/Transcrições |
| I150 | Balancetes de Verificação |
| J050 | Plano de Contas (KPCE) |
| J100 | Balanço Patrimonial |
| J150 | Demonstração do Resultado |
| K030 | Demonstrações Contábeis |

## ECF (Escrituração Contábil Fiscal)

### Obrigação
- Empresas obrigadas ao Lucro Real
- Substitui LALUR e LACS
- Prazo: até 31 de julho

### Blocos
| Bloco | Conteúdo |
|-------|----------|
| **0** | Abertura |
| **A** | Escrituração Contábil |
| **B** | Livro Caixa |
| **C** | Apuração Lucro Real |
| **D** | LALUR |
| **E** | Lucro Presumido |
| **G** | Inspetor/Prova Fiscal |
| **H** | Inventário Físico |
| **I** | SPCD |
| **K** | Operações com Exterior |
| **M** | Apuração da Contribuição |
| **P** | Apuração da Contribuição |
| **X** | Outras Informações |
| **9** | Encerramento |

## Apuração Detalhada

### ICMS

#### Alíquotas Internas (exemplos)
| Estado | Alíquota |
|--------|:--------:|
| SP | 18% |
| RJ | 20% |
| MG | 18% |
| RS | 17% |
| PR | 19,5% |
| SC | 17% |
| BA | 20,5% |

#### Operações
| Operação | CFOP | ICMS |
|----------|------|------|
| Venda interna | 5.102 | Alíquota interna |
| Venda interestadual | 6.102 | Alíquota interestadual |
| Remessa para depósito | 5.152 | Alíquota interna |
| Devolução de venda | 1.202 | Estorno crédito |

### PIS/COFINS

#### Não-Cumulativo (Lucro Real)
| Entrada/Saída | PIS | COFINS |
|---------------|:---:|:------:|
| Receita bruta | 1,65% | 7,60% |
| Compras (crédito) | 1,65% | 7,60% |
| Energia (crédito) | 1,65% | 7,60% |
| Aluguel (crédito) | 1,65% | 7,60% |

#### Cumulativo (Lucro Presumido)
| Entrada/Saída | PIS | COFINS |
|---------------|:---:|:------:|
| Receita bruta | 0,65% | 3,00% |
| Sem créditos | - | - |

### IRPJ/CSLL

#### Lucro Real
```
IRPJ = Lucro Real × 15%
IRPJ Adicional = (Lucro Real - R$ 20.000/mês) × 10%
CSLL = Lucro Real × 9%
```

#### Lucro Presumido
```
IRPJ = Receita × Presunção × 15%
IRPJ Adicional = (Base - R$ 60.000/trimestre) × 10%
CSLL = Receita × Presunção × 9%
```

## Obrigações Acessórias

| Obrigação | Entidade | Prazo |
|-----------|----------|-------|
| EFD ICMS/IPI | SEFAZ | Dia 15 mês seguinte |
| EFD Contribuições | RFB | Dia 15 mês seguinte |
| ECD | RFB/eCAC | Dia 31/07 |
| ECF | RFB | Dia 31/07 |
| SPED Fiscal | SEFAZ | Dia 15 mês seguinte |
| REINF | eSocial | Dia 15 mês seguinte |
| DCTFWeb | eSocial | Dia 15 mês seguinte |

## Procedimento Mensal

1. **Dia 1-5**: Fechamento de período no ERP
2. **Dia 5-10**: Apuração de ICMS, IPI, PIS, COFINS
3. **Dia 10-12**: Geração de arquivos EFD
4. **Dia 12-14**: Validação com validador SEFAZ
5. **Dia 14**: Correção de erros
6. **Dia 15**: Transmissão dos arquivos

## Fontes Oficiais
- Convênio S/N (EFD ICMS/IPI)
- IN RFB 1.252/2012 (EFD Contribuições)
- IN RFB 2.004/2021 (ECD)
- IN RFB 2.005/2021 (ECF)
- Portal SPED (sped.fazenda.gov.br)

---
id: fgts
type: knowledge
tags: [trabalhista, fgts, dirf, dctfweb, efd-reinf, obrigacoes, tributos]
owner: equipe-juridico-trabalhista
version: "1.0.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar de forma abrangente as quatro principais obrigações acessórias federais vinculadas à folha de pagamento: F...
- **Seções principais**: Purpose, Responsibilities, Dependencies, 1. FGTS — Fundo de Garantia do Tempo de Serviço
- **Tags**: trabalhista, fgts, dirf, dctfweb, efd-reinf, obrigacoes, tributos
- **Restrições/Regras**: Este documento é referência genérica e não substitui consulta à legislação vigente; Valores, alíquotas e prazos devem...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `fgts` |
| Tipo | knowledge |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | equipe-juridico-trabalhista |
| Total de seções | 11 |


# FGTS, DIRF, DCTFWeb e EFD-Reinf

Referência completa das obrigações acessórias federais relacionadas a tributos sobre a folha de pagamento e rendimentos.

## Purpose

Documentar de forma abrangente as quatro principais obrigações acessórias federais vinculadas à folha de pagamento: FGTS (Fundo de Garantia do Tempo de Serviço), DIRF (Declaração do Imposto de Renda Retido na Fonte), DCTFWeb (Declaração de Débitos e Créditos Tributários Federais Web) e EFD-Reinf (Escrituração Fiscal Digital de Retenções).

## Responsibilities

Este documento cobre: normas, alíquotas, prazos, sistemas, penalidades, cruzamento de dados e tabelas comparativas para cada obrigação. Serve como base para configuração de sistemas de folha de pagamento e obrigações acessórias.

## Dependencies

- `clt.md` — referência geral da CLT, verbas rescisórias e remuneração
- `beneficios.md` — incidência tributária de benefícios

---

## 1. FGTS — Fundo de Garantia do Tempo de Serviço

### 1.1 Base Legal

| Norma | Descrição |
|---|---|
| Lei nº 8.036/1990 | Dispõe sobre o FGTS |
| Decreto nº 99.684/1990 | Regulamenta a Lei 8.036/1990 |
| Lei nº 14.438/2022 | Institui o FGTS Digital |
| Lei Complementar nº 110/2001 | Multa adicional de 10% sobre depósitos |

### 1.2 Depósitos Mensais

#### Alíquotas por Categoria

| Categoria do Trabalhador | Alíquota | Observação |
|---|---|---|
| Trabalhador CLT (geral) | 8% | Sobre remuneração bruta |
| Aprendiz (Lei 10.097/2000) | 2% | Sobre remuneração bruta |
| Trabalhador doméstico | 8% | Depósito mensal |
| Trabalhador doméstico (multa antecipada) | +3,2% | Depósito mensal a título de multa antecipada (total 11,2%) |
| Trabalhador temporário | 8% | Sobre remuneração bruta |
| Atleta profissional | 2% | Sobre remuneração bruta |

#### Base de Cálculo

**Incluem:** salário base, adicionais (noturno, insalubridade, periculosidade, função), horas extras, sobreaviso, comissões, gorjetas, 13º salário (1/12 mensal), DSR sobre variáveis, aviso prévio, férias + 1/3.

**Não incluem:** diárias de viagem (até 50%), ajuda de custo, auxílio-alimentação (se não pago em dinheiro), vale-transporte, PLR.

#### Prazo de Recolhimento

| Situação | Prazo |
|---|---|
| Depósito mensal | Dia 7 do mês seguinte ao mês de referência |
| Depósito rescisório | Dia útil anterior ao efetivo pagamento das verbas rescisórias |

Se o dia 7 cair em dia não útil, o vencimento é antecipado para o último dia útil anterior.

#### Sistemas de Recolhimento

| Sistema | Descrição | Status |
|---|---|---|
| FGTS Digital | Plataforma obrigatória (Lei 14.438/2022) | Obrigatório |
| Conectividade Social | Canal de transmissão empresa-Caixa | Em transição |
| SEFIP | Sistema Empresa de Recolhimento do FGTS | Em descontinuação |

### 1.3 Saques Permitidos

| Modalidade | Condição | Observações |
|---|---|---|
| Demissão sem justa causa | Desligamento pelo empregador sem justa causa | Saque total + multa 40% |
| Término de contrato por prazo determinado | Fim de contrato temporário | Saque total |
| Aposentadoria | Concessão de aposentadoria pelo INSS | Saque total |
| Compra da casa própria | Sistema Financeiro de Habitação | Até 80% do saldo |
| Doença grave | Câncer, HIV/AIDS, estágio terminal | Saque total |
| Conta inativa | Sem depósito por 3+ anos | Saque total |
| Saque-Aniversário | Optante pela modalidade | Alíquota progressiva; perde multa rescisória |
| Morte do titular | Falecimento do trabalhador | Dependentes/herdeiros sacam |
| Calamidade pública | Reconhecimento federal/estadual | Até valor definido anualmente |
| Idade igual ou superior a 70 anos | Trabalhador com 70+ anos | Saque total |

#### Tabela Saque-Aniversário (Alíquotas Progressivas)

| Faixa de Saldo | Alíquota | Parcela a Deduzir |
|---|---|---|
| Até R$ 500,00 | 50% | R$ 0,00 |
| De R$ 500,01 a R$ 1.000,00 | 40% | R$ 50,00 |
| De R$ 1.000,01 a R$ 5.000,00 | 30% | R$ 150,00 |
| De R$ 5.000,01 a R$ 10.000,00 | 20% | R$ 650,00 |
| De R$ 10.000,01 a R$ 15.000,00 | 15% | R$ 1.150,00 |
| De R$ 15.000,01 a R$ 20.000,00 | 10% | R$ 1.900,00 |
| Acima de R$ 20.000,00 | 5% | R$ 2.900,00 |

```
Exemplo: Saldo R$ 8.000,00
Saque = (R$ 8.000,00 × 20%) - R$ 650,00 = R$ 950,00
```

### 1.4 Multa Rescisória

#### Multa de 40%

| Item | Detalhe |
|---|---|
| Base de cálculo | Todos os depósitos realizados durante o contrato de trabalho |
| Alíquota | 40% |
| Aplicabilidade | Demissão sem justa causa, rescisão indireta |
| Prazo de pagamento | Dia do efetivo pagamento das verbas rescisórias |
| Guia | GRRF / GRRF Digital |

```
Exemplo: Total de depósitos no contrato: R$ 25.000,00
Multa 40%: R$ 25.000,00 × 40% = R$ 10.000,00
```

### 1.5 FGTS Digital (Lei 14.438/2022)

| Característica | Detalhe |
|---|---|
| Obrigatoriedade | Empregadores a partir de 01/03/2024 |
| Substitui | SEFIP, GRRF, GRF |
| Pagamento | Via PIX (ePIX) |
| Acesso | fgtsdigital.sistema.gov.br |
| Certificado digital | Obrigatório (e-CNPJ A1 ou A3) |
| Funcionalidades | Emissão de guias, consulta de extratos, recolhimento rescisório, parcelamento |

### 1.6 Penalidades por Atraso

| Tipo de Penalidade | Detalhe |
|---|---|
| Multa moratória | 5% a 50% sobre o valor do depósito |
| Juros de mora | 0,5% ao mês (pro rata die) |
| Correção monetária | Pelo índice TR (Taxa Referencial) |
| Multa por infração | Aplicada pela fiscalização do trabalho |

### 1.7 SEFIP e Guias

| Guia | Descrição |
|---|---|
| GFIP | Guia de Recolhimento do FGTS e de Informações à Previdência Social |
| GRRF | Guia de Recolhimento Rescisório do FGTS |
| GRF | Guia de Recolhimento do FGTS (mensal) |

### 1.8 Códigos de Recolhimento FGTS

| Código | Descrição |
|---|---|
| 0139 | Recolhimento mensal — empregados |
| 0189 | Recolhimento — empregado doméstico |
| 0308 | Recolhimento — aprendiz |
| 0332 | Recolhimento — trabalhador avulso |
| 115 | Recolhimento rescisório — GRRF |
| 325 | Recolhimento complementar |
| 640 | Depósito recursal |
| 650 | Depósito administrativo |

---

## 2. DIRF — Declaração do Imposto de Renda Retido na Fonte

### 2.1 O que é

A DIRF é a declaração anual que informa à Receita Federal os rendimentos pagos, creditados, entregues, empregados ou remetidos a pessoas físicas e jurídicas, bem como os correspondentes valores de imposto de renda retido na fonte.

**Base legal:** IN RFB nº 2.178/2024 (e atualizações anuais).

### 2.2 Obrigatoriedade

São obrigados a entregar a DIRF:

- Pessoas jurídicas que efetuaram retenção de IR na fonte
- Pessoas físicas que efetuaram retenção de IR na fonte
- Empresas que pagaram rendimentos sujeitos à retenção, mesmo que por substituição tributária
- Órgãos da administração pública federal, estadual e municipal
- Organizações internacionais com sede no Brasil

### 2.3 Prazo de Entrega

| Exercício | Prazo |
|---|---|
| DIRF anual | Último dia útil de fevereiro do ano seguinte ao ano-calendário |

O prazo exato é definido anualmente por Instrução Normativa da RFB.

### 2.4 Rendimentos Declarados

| Tipo | Observação |
|---|---|
| Rendimentos do trabalho assalariado | Salários, férias, 13º, PLR |
| Participação nos Lucros e Resultados (PLR) | Valor pago a empregados |
| Rendimentos do trabalho sem vínculo empregatício | Autônomos (Carnê Leão) |
| Honorários profissionais | Advogados, médicos, contadores |
| Rendimentos de aplicações financeiras | Poupança, CDB, fundos |
| Dividendos | A partir de 1996 (isentos) |
| Resgate PGBL | Tributável integralmente |
| Resgate VGBL | Tributável sobre rendimentos |
| Benefícios previdenciários | Acima da faixa isenta |

### 2.5 Informações Obrigatórias por Beneficiário

1. Rendimento bruto total anual
2. Imposto de renda retido na fonte total anual
3. Parcela isenta (contribuintes com 65+ anos)
4. Deduções (pensão alimentícia judicial, dependentes, contribuição previdenciária)
5. Rendimentos isentos e não tributáveis (13º, PLR, indenizações)
6. Rendimentos sujeitos à tributação exclusiva (ganho de capital, JCP)
7. Rendimentos tributáveis recebidos acumuladamente (RRA)

### 2.6 Cruzamento de Dados

A Receita Federal realiza cruzamento automático entre:

| Declaração | Dados Cruzados |
|---|---|
| DIRF × DIRPF | Rendimentos declarados pela empresa vs. informados pelo contribuinte |
| DIRF × ECD | Contábil vs. fiscal |
| DIRF × EFD-Contribuições | PIS/COFINS vs. rendimentos |
| DIRF × EFD-Reinf | Eventos trabalhistas vs. DIRF |

**Consequências de divergência:** malha fina, multa por omissão (20% do imposto devido), notificação fiscal.

### 2.7 Retificação da DIRF

| Item | Detalhe |
|---|---|
| Prazo | 5 anos (art. 173, CTN) |
| Como | Entregar nova DIRF com indicador de retificação |
| Efeito | Substitui integralmente a declaração anterior |
| Multa | Não há multa para retificação espontânea |

---

## 3. DCTFWeb — Declaração de Débitos e Créditos Tributários Federais Web

### 3.1 O que é

A DCTFWeb é a declaração que apura e informa os débitos e créditos tributários federais, substituindo a DCTF tradicional. Transmitida pelo portal e-CAC da Receita Federal.

**Base legal:** IN RFB nº 2.055/2021 (e atualizações).

### 3.2 Créditos Declarados

| Tributo | Código de Receita | Observação |
|---|---|---|
| IRPJ | 2089 | Estimativa mensal, balanço trimestral, lucro real/presumido |
| CSLL | 2372 | Estimativa, lucro real/presumido |
| PIS/Pasep | 8109 | Sobre faturamento ou folha |
| COFINS | 2172 | Sobre faturamento |
| IPI | 0401 | Operações com produtos industrializados |
| IOF | 5600 | Operações de crédito, câmbio, seguro |
| Salário-Educação | 1180 | Contribuição social sobre folha |
| INSS (Patronal) | 2100 | Contribuição previdenciária sobre folha |
| RAT | 2100 | Alíquota de 1%, 2% ou 3% |
| Terceiros | 2100 | Contribuições destinadas a terceiros |

### 3.3 Periodicidade e Prazo

| Item | Detalhe |
|---|---|
| Periodicidade | Mensal |
| Prazo de entrega | 15º dia útil do 2º mês seguinte ao mês de referência |

**Exemplo:** DCTFWeb de janeiro/2026 → vencimento em 15º dia útil de março/2026.

### 3.4 Integração com EFD-Reinf

A DCTFWeb importa automaticamente os dados da EFD-Reinf:

| Evento EFD-Reinf | Informação para DCTFWeb |
|---|---|
| R-2010 | Retenção de INSS sobre serviços tomados |
| R-2020 | Retenção de INSS sobre serviços prestados |
| R-2060 | Retenção de contribuições previdenciárias (PIS, COFINS, CSLL) |
| R-2070 | Retenções de IR, PIS, COFINS, CSLL |
| R-4010 | Retenção de IR sobre rendimentos de PF |
| R-4020 | Retenção de IR sobre rendimentos de PJ |
| R-9000 | Fechamento |

### 3.5 Multas

| Tipo | Detalhe |
|---|---|
| Multa de ofício | 2% ao mês-calendário (máximo 20%) sobre o valor do tributo |
| Multa por atraso na entrega | R$ 500,00 por mês-calendário (reduzida para R$ 150,00 se entregue antes de procedimento fiscal) |
| Multa por omissão | 20% do imposto devido (se espontânea: 10%) |
| Juros de mora | Taxa Selic acumulada + 1% no mês do pagamento |

**Exemplo de cálculo de multa por atraso:**
```
Tributo devido: R$ 50.000,00
Atraso: 3 meses
Multa de ofício: R$ 50.000,00 × 2% × 3 = R$ 3.000,00
Multa por atraso na entrega: R$ 500,00 × 3 = R$ 1.500,00
Juros Selic (ex: 14,75% a.a.): R$ 50.000,00 × (14,75%/12) × 3 = R$ 1.843,75
Total: R$ 56.343,75
```

### 3.6 Retificação da DCTFWeb

| Item | Detalhe |
|---|---|
| Prazo | 5 anos (art. 173, CTN) |
| Como | Entregar nova DCTFWeb com indicador de retificação |
| Efeito | Substitui integralmente a declaração anterior |

### 3.7 Situações Especiais

| Situação | Efeito na DCTFWeb |
|---|---|
| Suspensão de exigibilidade | Débito declarado mas não exigível |
| Imunidade | Isenção constitucional |
| Isenção | Isenção concedida por lei específica |
| Parcelamento | Débito parcelado — declarar com código específico |
| Compensação | Crédito de tributo compensado com outro débito |

---

## 4. EFD-Reinf — Escrituração Fiscal Digital de Retenções

### 4.1 O que é

A EFD-Reinf é a escrituração fiscal digital que registra as retenções de INSS, IR, PIS, COFINS e CSLL sobre pagamentos a pessoas físicas e jurídicas. Integra-se com a DCTFWeb e o eSocial.

### 4.2 Eventos Principais

| Evento | Descrição |
|---|---|
| R-1000 | Informações do contribuinte |
| R-1070 | Processos administrativos/judiciais |
| R-2010 | Retenção de INSS sobre serviços tomados |
| R-2020 | Retenção de INSS sobre serviços prestados |
| R-2060 | Retenção de contribuições previdenciárias (PIS, COFINS, CSLL) |
| R-2070 | Retenções de IR, PIS, COFINS, CSLL |
| R-2098 | Reabertura dos eventos periódicos |
| R-2099 | Fechamento dos eventos periódicos |
| R-3010 | Espetáculos desportivos |
| R-4010 | Retenção de IR sobre rendimentos de PF |
| R-4020 | Retenção de IR sobre rendimentos de PJ |
| R-4040 | Retenção de IR sobre rendimentos de residentes no exterior |
| R-4080 | Retenção de IR sobre pagamentos a PJ |
| R-4099 | Fechamento dos eventos não periódicos |
| R-9000 | Exclusão de eventos |

### 4.3 Prazo de Entrega

Os eventos devem ser transmitidos até o dia 15 do mês seguinte ao da ocorrência (ou último dia útil anterior). Eventos de fechamento (R-2099, R-4099) seguem cronograma específico.

### 4.4 Retenções Abrangidas

- INSS sobre serviços tomados e prestados
- IRRF sobre rendimentos do trabalho e de capital
- PIS, COFINS e CSLL sobre pagamentos a terceiros
- Contribuições previdenciárias sobre receita bruta

---

## 5. Tabela Comparativa

| Característica | FGTS | DIRF | DCTFWeb | EFD-Reinf |
|---|---|---|---|---|
| Natureza | Depósito fundiário | Declaração informativa | Declaração de débitos | Escrituração fiscal |
| Base legal | Lei 8.036/1990 | IN RFB 2.178/2024 | IN RFB 2.055/2021 | IN RFB 2.005/2021 |
| Periodicidade | Mensal | Anual | Mensal | Mensal |
| Prazo | Dia 7 do mês seg. | Último dia útil de fev. | 15º dia útil do 2º mês seg. | Dia 15 do mês seguinte |
| Sistema | FGTS Digital | PGD DIRF | DECFWEB | Sistema EFD-Reinf |
| Destinatário | Caixa Econômica Federal | Receita Federal | Receita Federal | Receita Federal |
| Multa por atraso | 5-50% + juros + TR | R$ 500/mês (máx R$ 5.000) | 2% a.m. (máx 20%) + R$ 500/mês | Conforme DCTFWeb |
| Retificação | GRRF complementar | DIRF retificadora | DCTFWeb retificadora | Evento de retificação |
| Integração | eSocial | GFIP, ECD, EFD-Reinf | EFD-Reinf, ECD | DCTFWeb, eSocial |
| Certificado digital | Obrigatório | Recomendado | Obrigatório | Obrigatório |

---

## 6. Referências Oficiais

### 6.1 Legislação

| Norma | Assunto |
|---|---|
| Lei nº 8.036/1990 | FGTS |
| Decreto nº 99.684/1990 | Regulamentação do FGTS |
| Lei nº 14.438/2022 | FGTS Digital |
| Lei Complementar nº 110/2001 | Multa adicional FGTS |
| IN RFB nº 2.178/2024 | DIRF |
| IN RFB nº 2.055/2021 | DCTFWeb |
| CTN (Lei nº 5.172/1966) | Código Tributário Nacional |

### 6.2 Portais e Sistemas

| Sistema | URL |
|---|---|
| FGTS Digital | fgtsdigital.sistema.gov.br |
| Conectividade Social | conectividade.caixa.gov.br |
| e-CAC (RFB) | cav.receita.fazenda.gov.br |
| DIRF (RFB) | gov.br/receitafederal |
| DCTFWeb (RFB) | gov.br/receitafederal |

---

## Constraints

- Este documento é referência genérica e não substitui consulta à legislação vigente
- Valores, alíquotas e prazos devem ser verificados periodicamente
- A RFB e a Caixa Econômica Federal podem alterar sistemas e layouts sem aviso prévio
- Certificado digital é obrigatório para FGTS Digital e DCTFWeb

## Related Documents

- [`clt.md`](./clt.md) — CLT, verbas rescisórias e remuneração
- [`beneficios.md`](./beneficios.md) — Benefícios trabalhistas e incidência tributária

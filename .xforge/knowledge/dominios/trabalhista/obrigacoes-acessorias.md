---
id: obrigacoes-acessorias-v2
type: knowledge
tags: [obrigacoes-acessorias, dirf, dctfweb, efd-reinf, esocial, ecf, ecd, dirpf, rais, caged, gfip, dirpj, dasn-simei, carne-leao, sped, rfb]
owner: trabalhista
version: "1.0"
updated: "2026-06-09"
---

## Resumo Executivo

- **Propósito**: Documentar as principais obrigacoes acessorias federais brasileiras: o que sao, tabela completa com descricao/prazo/s...
- **Principais responsabilidades**: Cumprir os prazos de entrega de todas as obrigacoes acessorias aplicaveis a empresa.; Manter certificado digital (A1 ou A3) valido para transmissao...
- **Seções principais**: Proposito, Responsabilidades, Dependencias, Constraints
- **Tags**: obrigacoes-acessorias, dirf, dctfweb, efd-reinf, esocial, ecf, ecd, dirpf, rais, caged, gfip, dirpj, dasn-simei, carne-leao, sped, rfb
- **Restrições/Regras**: **Transmissao eletronica**: obrigatoria para todas as obrigacoes -- nao ha mais entrega em papel.; **Certificado digi...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `obrigacoes-acessorias-v2` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 7 |


# Obrigações Acessórias Federais

## Proposito

Documentar as principais obrigacoes acessorias federais brasileiras: o que sao, tabela completa com descricao/prazo/sistema, calendario de prazos mes a mes, penalidades por infracao, cruzamento de dados pela RFB e a integracao entre eSocial, EFD-Reinf e DCTFWeb, como base para compliance fiscal-trabalhista.

## Responsabilidades

- Cumprir os prazos de entrega de todas as obrigacoes acessorias aplicaveis a empresa.
- Manter certificado digital (A1 ou A3) valido para transmissao eletronica.
- Validar dados antes da transmissao para evitar rejeicoes e penalidades.
- Retificar declaracoes dentro do prazo para evitar multas.
- Guardar documentacao por no minimo 5 anos (prazo decadencial).
- Acompanhar atualizacoes legislativas e normativas das obrigacoes.
- Coordenar a integracao entre eSocial, EFD-Reinf e DCTFWeb.

## Dependencias

- Certificado digital e-CNPJ (padrao ICP-Brasil, tipo A1 ou A3).
- Sistema de escrituracao contabil e fiscal (ERP).
- Sistema de folha de pagamento (para eSocial).
- Contabilidade (para ECD, ECF, DIRF, DCTFWeb).
- Cadastro atualizado na Receita Federal (CPF/CNPJ).
- Tabelas e leiautes vigentes de cada obrigacao.
- [eSocial Geral](./esocial-geral.md) -- visao geral do eSocial.
- [Departamento Pessoal](./departamento-pessoal.md) -- eventos cadastrais e nao-periodicos.
- [Holerite / Contracheque](./holerite.md) -- remuneracao refletida em S-1200 e S-1210.

## Constraints

- **Transmissao eletronica**: obrigatoria para todas as obrigacoes -- nao ha mais entrega em papel.
- **Certificado digital**: obrigatorio para assinatura e transmissao.
- **Prazos**: rigorosos -- multas sao aplicadas por mes de atraso.
- **Guarda**: manter documentacao por minimo 5 anos (decadencia de creditos tributarios).
- **Retificacao**: permitida dentro do prazo, sem multa se espontanea.
- **Cruzamento de dados**: RFB cruza informacoes entre todas as declaracoes -- inconsistencias geram autuacoes.
- **eSocial + EFD-Reinf + DCTFWeb**: integracao obrigatoria -- dados devem ser coerentes entre os tres sistemas.

## Conteudo

### 1. Visao Geral

Obrigacoes acessorias sao deveres administrativos que complementam o pagamento de tributos. Incluem declaracoes, escrituracoes, guias e demonstrativos que informam ao fisco sobre operacoes, rendimentos, retencoes e pagamentos realizados pelo contribuinte.

**Importancia**: comprovam a regularidade fiscal; permitem o cruzamento de dados pelo fisco; fundamentam creditos tributarios e restituicoes; substituem documentos fisicos por registros digitais (SPED).

**Principio da Integracao**: Todas as obrigacoes acessorias federais estao interconectadas pelo **SPED** (Sistema Publico de Escrituracao Digital). Os dados informados em uma obrigacao sao cruzados com os dados de outras, permitindo a Receita Federal identificar inconsistencias, omissoes e fraudes.

### 2. Tabela Completa de Obrigações Acessorias

| Obrigacao | Descricao | Prazo | Sistema |
| DIRF | Declaracao do IR Retido na Fonte -- rendimentos com retencao de IR, CSLL, PIS, COFINS | Fevereiro (ano anterior) | DIRF Web / RFB |
| DCTFWeb | Declaracao de Debitos e Creditos Tributarios Federais Web | dia 15 do mes seguinte | DCTFWeb / RFB |
| EFD-Reinf | Escrituracao Fiscal Digital de Retencoes -- retencoes de IR, CSLL, PIS, COFINS, ISS | dia 15 do mes seguinte | EFD-Reinf / SPED |
| DIRPJ | Informacoes Economico-Fiscais da PJ (substituida pela ECF desde 2014) | -- | Substituida |
| DASN-SIMEI | Declaracao Anual do Simples Nacional -- MEI (faturamento, empregado, compras, vendas) | 31 de maio | Portal do Empreendedor |
| RAIS | Relacao Anual de Informacoes Sociais (substituida pelo eSocial) | Marco | eSocial (novo) |
| CAGED | Cadastro Geral de Empregados e Desempregados (substituido pelo eSocial) | Janeiro | eSocial (novo) |
| GFIP | Guia de Recolhimento do FGTS (substituida) | dia 7 | FGTS Digital (novo) |
| ECF | Escrituracao Contabil Fiscal -- apuracao do IRPJ e CSLL | ultimo dia util de julho | SPED |
| ECD | Escrituracao Contabil Digital -- livros contabeis (Diario, Razao, auxiliares) | ultimo dia util de maio | SPED |
| EFD ICMS/IPI | Escrituracao Fiscal Digital -- operacoes de ICMS e IPI | dia 20 do mes seguinte | SPED |
| EFD Contribuicoes | EFD PIS/COFINS -- apuracao de PIS e COFINS | dia 15 do mes seguinte | SPED |
| eSocial | Escrituracao Digital das Obrigações Fiscais, Previdenciarias e Trabalhistas | variavel por evento | eSocial |
| DCTF | Declaracao de Debitos e Creditos Tributarios Federal (substituida pela DCTFWeb) | -- | Substituida |
| DIRPF | Declaracao do IR Pessoa Fisica -- rendimentos, deducoes, bens | abril | IRPF / RFB |
| Carnê-Leao | Recolhimento mensal de IR sobre rendimentos recebidos de PF | ultimo dia util do mes seguinte | Carnê-Leao Web / RFB |

### 3. Calendario de Prazos -- Mes a Mes

**Janeiro**: DCTFWeb (dia 15), EFD-Reinf (dia 15), EFD Contribuicoes (dia 15), EFD ICMS/IPI (dia 20), eSocial S-1299 (dia 15), Carnê-Leao (ultimo dia util).

**Fevereiro**: DIRF (ate 28/02 util), DCTFWeb (dia 15), EFD-Reinf (dia 15), EFD Contribuicoes (dia 15), EFD ICMS/IPI (dia 20), Carnê-Leao (ultimo dia util).

**Marco**: RAIS (ate marco), DCTFWeb (dia 19), EFD-Reinf (dia 15), EFD Contribuicoes (dia 17), EFD ICMS/IPI (dia 20), Carnê-Leao (ultimo dia util).

**Abril**: DIRPF (ate 30/04), DCTFWeb (dia 15), EFD-Reinf (dia 15), EFD Contribuicoes (dia 15), EFD ICMS/IPI (dia 22), Carnê-Leao (ultimo dia util).

**Maio**: ECD (ultimo dia util), DASN-SIMEI (31/05), DCTFWeb (dia 15), EFD-Reinf (dia 15), EFD Contribuicoes (dia 15), EFD ICMS/IPI (dia 20), Carnê-Leao (ultimo dia util).

**Junho**: DCTFWeb (dia 16), EFD-Reinf (dia 15), EFD Contribuicoes (dia 15), EFD ICMS/IPI (dia 21), Carnê-Leao (ultimo dia util).

**Julho**: ECF (ultimo dia util), DCTFWeb (dia 15), EFD-Reinf (dia 15), EFD Contribuicoes (dia 15), EFD ICMS/IPI (dia 20), Carnê-Leao (ultimo dia util).

**Agosto a Dezembro**: DCTFWeb (dia 17), EFD-Reinf (dia 15), EFD Contribuicoes (dia 15), EFD ICMS/IPI (dia 20), eSocial S-1299 (dia 15), Carnê-Leao (ultimo dia util).

> Prazos exatos podem variar conforme o calendario oficial da Receita Federal. Sempre verificar o calendario atualizado no site da RFB.

### 4. Penalidades

| Infracao | Multa | Base Legal |
| Atraso na entrega | R$ 500,00 por mes-calendario (minimo) | Art. 57 Decreto 9.580/2018 |
| Nao entrega | R$ 1.500,00 por mes-calendario (minimo) | Art. 57 Decreto 9.580/2018 |
| Omissao de informacoes | 2% do valor da operacao (minimo R$ 500,00) | Legislacao especifica |
| Informacoes incorretas | 2% do valor da operacao | Legislacao especifica |
| DIRF -- omissao | R$ 500,00 por mes (minimo) | Art. 57 II, "a" |
| eSocial -- atraso | R$ 1.800,00 por evento (multa diaria) | IN RFB especifica |
| EFD-Reinf -- atraso | R$ 500,00 por mes | IN RFB 2.219/2024 |

**Reducao de multas**: entrega antes de qualquer intimacao = 50%; entrega apos intimacao, no prazo = 25%; entrega espontanea com pagamento = 50-75%.

**Observacoes**: multas sao por mes-calendario de atraso, nao por dia. O valor minimo de R$ 500,00 se aplica mesmo que o tributo devido seja inferior. Empresas do Simples Nacional tem valores diferenciados em alguns casos.

### 5. Cruzamento de Dados

A Receita Federal mantem um sistema integrado de cruzamento de informacoes entre todas as obrigacoes acessorias:

| Cruzamento | O que e verificado |
| DIRF x DIRPF | Rendimentos informados pela empresa x rendimentos declarados pelo contribuinte |
| eSocial x DIRF | Remuneracao de empregados x retencoes de IRRF informadas na DIRF |
| ECD x ECF | Escrituracao contabil x apuracao de IRPJ/CSLL |
| EFD-Reinf x DCTFWeb | Retencoes informadas x debitos declarados |
| eSocial x EFD-Reinf | Trabalhadores ativos x rendimentos informados |
| DIRF x Carnê-Leao | Rendimentos pagos x rendimentos declarados |
| EFD Contribuicoes x ECD | PIS/COFINS x escrituracao contabil |
| FGTS Digital x eSocial | Depositos de FGTS x remuneracoes informadas |

**Consequencias de inconsistencias**: malha fiscal (retencao da DIRPF), intimacao, auto de infracao, multas de 75% a 150% do tributo, impedimento de emissao de CND.

**Boas praticas**: validar dados antes de cada transmissao; manter consistencia entre eSocial, EFD-Reinf e DCTFWeb; retificar imediatamente inconsistencias; guardar documentacao suporte por 5+ anos; realizar conciliacao mensal entre folha, contabilidade e obrigacoes.

### 6. eSocial + EFD-Reinf + DCTFWeb -- Integracao

**eSocial**: informacoes trabalhistas, previdenciarias e fiscais (S-1200, S-1210, S-2200, S-2299).
**EFD-Reinf**: retencoes de IR, CSLL, PIS, COFINS, ISS, IRRF (eventos R-1000 a R-9015).
**DCTFWeb**: consolidacao de debitos e creditos de tributos federais.

**Fluxo integrado para folha**:
1. DP calcula folha (proventos, descontos, bases).
2. Sistema gera eventos eSocial (S-1200, S-1210).
3. Sistema gera eventos EFD-Reinf (retencoes de IR, INSS, etc.).
4. DCTFWeb consolida os debitos de tributos federais.
5. GPS/Gerenciador: debitos de INSS.
6. FGTS Digital: depositos de FGTS.
7. RFB cruza dados entre os tres sistemas.

**Mapeamento de eventos**:
| Informacao | eSocial | EFD-Reinf | DCTFWeb |
| Remuneracao mensal | S-1200 | -- | -- |
| Pagamentos | S-1210 | -- | -- |
| Retencao IRRF | -- | R-2010/R-2060 | Consolida |
| Retencao INSS | -- | R-2010 | Consolida |
| Retencao PIS/COFINS/CSLL | -- | R-2060 | Consolida |
| Retencao ISS | -- | R-2010 | Consolida |
| Fechamento folha | S-1299 | -- | -- |

**Substituicoes pelo eSocial**: GFIP -> eSocial+DCTFWeb; CAGED/RAIS -> eSocial; CAT -> S-2210; PPP -> S-2240.

**Consistencia obrigatoria**: valores de retencao no eSocial devem bater com EFD-Reinf; debitos na DCTFWeb devem refletir as retencoes da EFD-Reinf; remuneracoes no eSocial devem refletir nos pagamentos (S-1210) e retencoes (EFD-Reinf). Inconsistencias geram rejeicao ou autuacao.

## Documentos Relacionados

- [Departamento Pessoal](./departamento-pessoal.md) -- eventos de eSocial cadastrais e nao-periodicos.
- [Holerite / Contracheque](./holerite.md) -- remuneracao refletida em S-1200 e S-1210.
- [Saude e Seguranca do Trabalho](./saude-trabalho.md) -- eventos de SST no eSocial.
- [eSocial Geral](./esocial-geral.md) -- visao geral do eSocial.
- [eSocial Folha](./esocial-folha.md) -- eventos periodicos de folha.
- [eSocial Trabalhadores](./esocial-trabalhadores.md) -- eventos cadastrais.
- [eSocial Empregadores](./esocial-empregadores.md) -- eventos do empregador.
- [Folha de Pagamento](./folha-pagamento.md) -- calculos que alimentam as obrigacoes.
- [INSS e IRRF](./inss-irrf.md) -- retencoes que alimentam DIRF e eSocial.
- [FGTS](./fgts.md) -- recolhimento e GFIP/DCTFWeb.

## Referencias

| Fonte | URL |
| Receita Federal -- Obrigacoes | www.gov.br/receitafederal/pt-br/declaracoes-e-demonstrativos |
| SPED | www.gov.br/sped/pt-br |
| eSocial | www.gov.br/esocial/pt-br |
| DCTFWeb | www.gov.br/receitafederal/pt-br/dctfweb |
| EFD-Reinf | www.gov.br/receitafederal/pt-br/efd-reinf |

| Norma | Assunto |
| IN RFB 2.219/2024 | EFD-Reinf |
| IN RFB 2.099/2023 | DCTFWeb |
| Decreto 9.580/2018 | Regulamento do IR (RIR/2018) |
| Lei 9.532/1997 | Obrigacoes tributarias acessorias |
| CTN, Art. 143-174 | Obrigacoes tributarias |

> Prazos e valores sao atualizados anualmente. Consultar sempre as instrucoes normativas vigentes no site da Receita Federal do Brasil para informacoes atualizadas.

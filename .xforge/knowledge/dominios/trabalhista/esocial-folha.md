---
id: esocial-folha
type: knowledge
tags: [esocial, folha, pagamento, s1200, s1299, remuneracao, fechamento]
owner: trabalhista
version: 1.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Eventos de Folha de Pagamento no eSocial (S-1200 a S-1299)
- **Principais responsabilidades**: Enviar eventos de remuneração (S-1200, S-1202) e pagamentos (S-1210) mensalmente.; Gerenciar o fluxo de fechamento: reabertura (S-1298) → reenvio d...
- **Seções principais**: Propósito, Responsabilidades, Dependências, Constraints
- **Tags**: esocial, folha, pagamento, s1200, s1299, remuneracao, fechamento
- **Restrições/Regras**: **Prazo**: Eventos periódicos até o **dia 15 do mês seguinte** ao período de apuração.; **Fechamento (S-1299)**: Após...

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `esocial-folha` |
| Tipo | knowledge |
| Versão | 1.0 |
| Atualizado | 2026-06-09 |
| Owner | trabalhista |
| Total de seções | 6 |


# Eventos de Folha de Pagamento no eSocial (S-1200 a S-1299)

## Propósito
Documentar os eventos periódicos de folha de pagamento no eSocial, que informam remunerações, pagamentos e o ciclo de fechamento mensal.

## Responsabilidades
- Enviar eventos de remuneração (S-1200, S-1202) e pagamentos (S-1210) mensalmente.
- Gerenciar o fluxo de fechamento: reabertura (S-1298) → reenvio de eventos → fechamento (S-1299).
- Cadastrar rubricas na tabela S-1010 antes de utilizá-las nos eventos de folha.
- Informar adiantamento, 13º salário, férias e rescisões nos eventos correspondentes.

## Dependências
- Tabelas S-1000 (empregador), S-1010 (rubricas) e S-1020 (lotações) cadastradas.
- Eventos cadastrais do trabalhador (S-2200) enviados e aceitos.
- Certificado digital e-CNPJ para transmissão.

## Constraints
- **Prazo**: Eventos periódicos até o **dia 15 do mês seguinte** ao período de apuração.
- **Fechamento (S-1299)**: Após envio, nenhum evento pode ser enviado sem antes reabrir (S-1298).
- **Reabertura (S-1298)**: Só pode ser enviada se já houve S-1299 para o período.
- Rubricas referenciadas devem estar cadastradas na S-1010.
- Lotações referenciadas devem estar cadastradas na S-1020.

## Conteúdo

### Eventos de Remuneração

| Evento | Descrição | Público |
|--------|-----------|---------|
| S-1200 | Remuneração do Trabalhador (RGPS/CLT) | Empregados CLT |
| S-1202 | Remuneração de RPPS | Servidores públicos |
| S-1207 | Benefícios Previdenciários — RPPS | Aposentados/Pensionistas |

### Eventos de Pagamento

| Evento | Descrição |
|--------|-----------|
| S-1210 | Pagamentos de Rendimentos do Trabalho |
| S-1250 | Aquisição de Produção Rural (PF) |
| S-1260 | Comercialização da Produção Rural (PF) |
| S-1270 | Contratação de Trabalhadores Avulsos Não Portuários |
| S-1280 | Informações Complementares (periódicos) |

### Eventos de Controle

| Evento | Descrição |
|--------|-----------|
| S-1295 | Solicitação de Totalização para Pagamento (opcional) |
| S-1298 | Reabertura dos Eventos Periódicos |
| S-1299 | Fechamento dos Eventos Periódicos |

### Fluxo de Fechamento da Folha
```
1. S-1298 (Reabertura) — se já houve S-1299 no período
2. S-1200 (Remuneração CLT) — por trabalhador
   S-1202 (Remuneração RPPS) — por servidor
   S-1210 (Pagamentos) — referenciando S-1200
3. S-1295 (Totalização) — opcional
4. S-1299 (Fechamento) — confirma fim do período
```

### S-1200 — Remuneração do Trabalhador (CLT)
- **Campos principais**: `perApur` (AAAA-MM), `indApuracao` (1=Mensal, 2=Anual/13º), `cpfTrab`, `codCateg`.
- **Estrutura**: `dmDev` (demonstrativo mensal) → `itensRemun` (rubricas) → `infoPerApur` (por lotação).
- **Rubricas**: Cada item deve referenciar `codRubr` + `ideTabRubr` cadastrados na S-1010.
- **Retificação**: `indRetif=2` + `nrRecibo` do evento original.

### S-1210 — Pagamentos
- Referencia o `ideDmDev` do S-1200 correspondente.
- **Campos**: `dtPgto`, `tpPgto` (1=Remuneração, 2=Rescisória, 4=Adiantamento, 5=13º, 6=Férias), `vrLiq` (valor líquido).
- **Tipos de pagamento**: remuneração mensal, verbas rescisórias, adiantamento, 13º, férias.

### Adiantamento no eSocial
- Informado no S-1210 com `tpPgto=4`.
- Descontado automaticamente no S-1210 de remuneração (`tpPgto=1`).

### 13º Salário no eSocial
- **S-1200**: `indApuracao=2` (Anual) — remuneração do 13º.
- **S-1210**: `tpPgto=5` — pagamento do 13º.
- 1ª parcela: 50% sem descontos. 2ª parcela: com desconto de INSS e IRRF.

### Férias no eSocial
- **S-2230**: Afastamento temporário por férias (início e retorno).
- **S-1200**: Remuneração de férias com rubricas específicas (férias + 1/3 constitucional).
- **S-1210**: `tpPgto=6` — pagamento de férias.

### Rescisão no eSocial
- **S-2299**: Desligamento do trabalhador (prazo: 10 dias).
- **S-1200**: Remuneração das verbas rescisórias.
- **S-1210**: `tpPgto=2` — pagamento de verbas rescisórias.

### S-1299 — Fechamento
- Confirma que todos os eventos do período foram enviados.
- **Campos `infoFech`**: `evtRemun` (S/N), `evtPgtos` (S/N), `evtAqProd` (S/N), `evtComProd` (S/N), `evtContratAvNP` (S/N), `evtInfoComplPer` (S/N).
- Após o fechamento, o período fica bloqueado para novos eventos.

## Related Documents
- [esocial-empregador](esocial-empregadores.md) — Tabelas de rubricas (S-1010) e lotações (S-1020)
- [esocial-trabalhador](esocial-trabalhadores.md) — Eventos cadastrais do trabalhador
- [esocial-geral](esocial-geral.md) — Visão geral do eSocial
- [folha-pagamento](folha-pagamento.md) — Cálculos de folha de pagamento

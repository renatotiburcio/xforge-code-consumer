---
id: rescisao-funcionario
type: fluxo
tags: [rescisao, desligamento, esocial, s-2299, aviso-previo, fgts, homologacao]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Rescisão de Funcionário
- **Seções principais**: Propósito, Etapas, Pontos de Decisão, Integrações
- **Tags**: rescisao, desligamento, esocial, s-2299, aviso-previo, fgts, homologacao
- **Tipo**: fluxo | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `rescisao-funcionario` |
| Tipo | fluxo |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Rescisão de Funcionário

## Propósito
Documentar o fluxo completo de desligamento: aviso prévio, exames, cálculo rescisório, evento eSocial, pagamento e homologação, cobrindo todos os tipos de rescisão.

## Etapas

1. **Aviso Prévio**: 30 dias base + 3 dias por ano completo de serviço (máximo 90 dias). Pode ser trabalhado (jornada reduzida em 2h/dia ou 7 dias corridos) ou indenizado. Pedido de demissão: aviso de 30 dias (se não cumprido, desconto no saldo).
2. **Exames Demissionais**: ASO emitido pelo médico do trabalho em até 10 dias antes do desligamento. Avalia se o trabalhador sai em condições de saúde compatíveis com a função exercida. Obrigatório para todos os vínculos com mais de 90 dias.
3. **Cálculo Rescisório**:
   - **Saldo de salário**: dias trabalhados no mês / 30 × salário
   - **Férias vencidas**: salário + 1/3 constitucional (se não gozadas)
   - **Férias proporcionais**: meses trabalhados no período aquisitivo / 12 × salário + 1/3
   - **13º proporcional**: meses trabalhados no ano / 12 × salário
   - **Multa FGTS**: 40% sobre depósitos (sem justa causa) ou 20% (acordo)
   - **Aviso prévio indenizado**: salário + 1/3 de férias + 13º proporcional
4. **Tipos de Rescisão**:
   - **Sem justa causa**: todos os direitos + multa FGTS 40% + saque FGTS + seguro-desemprego
   - **Por justa causa**: apenas saldo salário + férias vencidas (sem 1/3). Sem multa FGTS, sem saque, sem seguro
   - **Pedido de demissão**: saldo salário + férias vencidas + 13º proporcional. Sem multa FGTS, sem seguro. Aviso prévio obrigatório
   - **Acordo (Lei 13.467/2017)**: metade do aviso prévio, metade da multa FGTS (20%), saque de 80% do FGTS. Sem seguro-desemprego
   - **Término de contrato experiência**: saldo salário + férias proporcionais + 13º proporcional. Sem multa se término normal
5. **Evento eSocial S-2299** (Desligamento): enviado até o último dia útil seguinte ao desligamento. Contém: data desligamento, motivo (codMotDeslig), pensão alimentícia, aviso prévio, FGTS, seguro-desemprego. Referencia o S-2200 original.
6. **Pagamento**: Prazo de 10 dias corridos após o término do contrato (se aviso prévio trabalhado) ou 1º dia útil após o fim do aviso (se indenizado). Depósito via TED/PIX.
7. **Homologação**: Obrigatória para contratos com mais de 1 ano. Realizada no sindicato da categoria ou na DRT (atual Ministério do Trabalho). Entrega de documentos: TRCT, extrato FGTS, guia SD/CD, comprovante de aviso prévio.

## Pontos de Decisão

| Decisão | Condição | Caminho |
|---------|----------|---------|
| Contrato > 1 ano? | Sim | Homologação obrigatória |
| Sem justa causa? | Sim | Multa FGTS 40% + saque + seguro |
| Justa causa? | Sim | Direitos mínimos, sem multa |
| Acordo? | Sim | 20% multa + 80% saque FGTS |
| Aviso cumprido? | Não | Desconto no saldo (pedido demissão) |

## Integrações

- **eSocial**: S-2299 (desligamento), S-2250 (aviso prévio), S-1210 tpPgto=2 (pagamento rescisório)
- **Folha de Pagamento**: cálculo automático das verbas rescisórias, geração de guias FGTS (GFIP/SEFIP)
- **Fiscal**: DIRF (informe de rendimentos com valores rescisórios), EFD-Reinf
- **Contábil**: baixa de provisões, rateio de encargos rescisórios
- **Financeiro**: pagamento bancário, controle de verbas

## Documentos Relacionados

- [Admissão de Funcionário](admissao-funcionario.md)
- [Folha de Pagamento](folha-pagamento.md)
- [Fluxo de Vendas](venda-completa.md)


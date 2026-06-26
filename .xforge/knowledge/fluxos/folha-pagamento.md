---
id: folha-pagamento
type: fluxo
tags: [folha, esocial, inss, irrf, fgts, remuneração, 13o, ferias, rescisao]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Folha de Pagamento
- **Seções principais**: Propósito, Etapas, Pontos de Decisão, Integrações
- **Tags**: folha, esocial, inss, irrf, fgts, remuneração, 13o, ferias, rescisao
- **Tipo**: fluxo | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `folha-pagamento` |
| Tipo | fluxo |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# Folha de Pagamento

## Propósito
Documentar o fluxo completo de folha de pagamento: apontamento, cálculo de proventos/descontos, encargos, pagamento, eventos eSocial e contabilização, incluindo 13º, férias e rescisão.

## Etapas

1. **Apontamento**: Ponto eletrônico, controle de horas extras, faltas, atrasos, banco de horas. Dados alimentam o cálculo da rubrica de cada colaborador.
2. **Cálculo de Proventos**: Salário base, horas extras (adicional 50-100%), adicional noturno (20%), adicional de insalubridade/periculosidade, DSR, comissões, participação nos lucros.
3. **Cálculo de Descontos**: INSS (alíquotas progressivas até teto), IRRF (tabela progressiva com dependentes), vale-transporte (6% do salário), conveniência médica, faltas e atrasos, pensão alimentícia (ordem judicial).
4. **FGTS**: Recolhimento de 8% sobre a remuneração (empregado CLTSaque em conta vinculada Caixa). Depósito independente, não representa desconto do trabalhador (exceto multa rescisória).
5. **Pagamento**: Transferência bancária (TED/PIX) para conta do colaborador. Fechamento até o 5º dia útil do mês subsequente à folha (CLT Art. 459).
6. **Eventos eSocial**:
   - **S-1200** (Remuneração CLT): mensal, com rubricas detalhadas, periodApur referência infoPerApur/infoPerAnt, ideDmDev único por trabalhador.
   - **S-1210** (Pagamentos): referência ao ideDmDev do S-1200, com dtPgto, tpPgto (1-remuneração, 5-13º, 6-férias, 2-rescisão), valores líquidos por rubrica.
   - **S-1299** (Fechamento): confirma encerramento do período. Após este, nenhum evento enviado sem S-1298 (reabertura). Prazo: dia 15 do mês seguinte.
   - S-1280 (informações complementares), S-1202 (RPPS), S-1207 (benefícios RPPS).
7. **Contabilização**: Provisões de encargos, rateio por centro de custo, fechamento contábil (devengado). Integração com SPED Contribuições e EFD-Reinantes.

### Especiais

- **13º Salário**: Indicionado (15 faltas/mês sem justa causa). Primeira parcela até 30/11, segunda até 20/12. Base = remuneração + média de variáveis. eSocial: S-1200 com indApuracao=2 + S-1210 tpPgto=5.
- **Férias**: Período aquisitivo de 12 meses. 30 dias de descanso + 1/3 constitucional. Abono de férias (1/3) em até 2x. eSocial: S-1210 tpPgto=6.
- **Rescisão**: Aviso prévio (30 dias + 3 anos de casa/ano). Saldo salário, férias vencidas + proporcionais + 1/3, 13º proporcional. Multa FGTS 40% (sem justa causa). eSocial: S-2299 (desligamento) + S-1210 tpPgto=2.

## Pontos de Decisão

| Decisão | Condição | Camento |
|---------|----------|---------|
| Empregado CLTPS? | Sim | S-1200 + controle INSS/FGTS |
| Servidor RPPS? | Sim | S-1202 + S-1207 |
| Período já fechado? | S-1298 enviado | Enviar evento |
| Período já fechado? | Sem S-1298 | Bloqueado — precisa reabertura |

## Integrações

- **RH/Departamento Pessoal**: admissão (S-2190/S-2200), afastamento (S-2230), alteração cadastral (S-2205)
- **Fiscal**: DIRF (informe de rendimentos), EFD-Reinf (retenções)
- **Contábil**: provisões, rateio de centros de custo, fechamento mensal
- **Financeiro**: pagamento bancário, controle de verbas

## Documentos Relacionados

- [Admissão de Funcionário](admissao-funcionario.md)
- [Rescisão de Funcionário](rescisao-funcionario.md)
- [PDV/Frente de Caixa](pdv-venda.md)


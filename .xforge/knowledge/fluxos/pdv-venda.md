---
id: pdv-venda
type: fluxo
tags: [pdv, frente-caixa, nfc-e, sat, pagamento, varejo]
owner: project-team
version: 1.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Tema**: Documentação completa sobre PDV — Fluxo de Venda no Frente de Caixa
- **Seções principais**: Propósito, Etapas, Pontos de Decisão, Integrações
- **Tags**: pdv, frente-caixa, nfc-e, sat, pagamento, varejo
- **Tipo**: fluxo | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `pdv-venda` |
| Tipo | fluxo |
| Versão | 1.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 5 |


# PDV — Fluxo de Venda no Frente de Caixa

## Propósito
Documentar o fluxo completo de venda no ponto de varejo: abertura de caixa até fechamento, incluindo emissão de NFC-e/SAT, formas de pagamento, contingência e cancelamento.

## Etapas

1. **Login do Operador**: Autenticação por senha ou biometria. Operador deve estar ativo, com turno aberto. Bloqueio após 3 tentativas falhas.
2. **Abertura de Caixa**: Caixa deve estar fechado do dia anterior. Fundo de caixa (troco) obrigatório — registrar cédulas/moedas por espécie. Impressão de comprovante Z1.
3. **Registro de Itens**: Produto identificado por código de barras, código interno ou busca. Quantidade padrão 1 (alterável). Preço obtido da tabela vigente (filial + tipo). Verificação de estoque configurável.
4. **Cálculo de Impostos**: ICMS (alíquota interna/interestadual), ISS para serviços. Substituição tributária quando aplicável. DIFAL para consumidor final não contribuinte.
5. **Pagamento**: Formas aceitas — dinheiro (com cálculo automático de troco), cartão crédito/débito via TEF (PIN Pad + operadora), PIX (QR Code estático/dinâmico, conciliação automática), vale-refeição/alimentação (Aleo, Ticket, Sodexo), cheque, fiado/crediário. Múltiplas formas por venda permitidas.
6. **Emissão NFC-e/SAT**: NFC-e: PDV gera XML → assina com certificado A1/A3 → transmite à SEFAZ → autorização → DANFE NFC-e. SAT (SP): PDV envia dados ao dispositivo SAT → assina e transmite → CF-e-SAT.
7. **Fechamento de Caixa (Redução Z)**: Conferência de espécies (contagem física vs. sistema). Sangrias e reforços registrados. Total por forma de pagamento consolidado. Fudo de caixa + vendas em dinheiro = total em espécie.

## Pontos de Decisão

| Decisão | Condição | Caminho |
|---------|----------|---------|
| Estoque insuficiente? | Sim | Bloquear, vender ou permitir negativo (supervisor) |
| SEFAZ indisponível? | Sim | Contingência (offline até 24h SAT / 7d NFC-e) |
| Troco insuficiente? | Sim | Alerta + oferecer PIX troco (Lei 14.620/2022) |
| Cancelar NFC-e? | Dentro do prazo | Evento de cancelamento com justificativa (15+ chars) |

## Integrações

- **ERP/Estoque**: baixa automática de estoque no momento da venda ou configuração por parâmetro; inventário rotativo
- **Fiscal**: emissão NFC-e/SAT/MFE; contingência FS-DA/EPEC; envio de XML ao cliente; SPED Fiscal
- **Financeiro**: conciliação de recebimentos (TED, PIX, TEF), contabilização por forma de pagamento
- **eSocial**: controle de jornada dos operadores via S-2200/S-2190
- **ALM/MDBE**: SAT em São Paulo; NFC-e na maioria dos estados; MFE no Ceará

## Documentos Relacionados

- [Fluxo de Vendas](venda-completa.md)
- [Fluxo de Compras](compra-completa.md)
- [Folha de Pagamento](folha-pagamento.md)


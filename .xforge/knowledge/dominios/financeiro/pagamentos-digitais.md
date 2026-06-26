---
id: fin-pagamentos-digitais
type: dominio
tags: [financeiro, pix, open-finance, boleto, cnab, pagamento]
owner: project-team
version: 2.0.0
updated: 2026-06-09
---

## Resumo Executivo

- **Propósito**: Gerenciar meios de pagamento eletrônico: PIX, Open Finance, boletos bancários e cartões.
- **Principais responsabilidades**: Integração com APIs de pagamento; Geração de cobranças (PIX, boleto, cartão); Conciliação automática de recebimentos
- **Seções principais**: Purpose, Responsibilities, PIX, Open Finance
- **Tags**: financeiro, pix, open-finance, boleto, cnab, pagamento
- **Tipo**: dominio | **Versão**: 2.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `fin-pagamentos-digitais` |
| Tipo | dominio |
| Versão | 2.0.0 |
| Atualizado | 2026-06-09 |
| Owner | project-team |
| Total de seções | 9 |


# Pagamentos Digitais

## Purpose
Gerenciar meios de pagamento eletrônico: PIX, Open Finance, boletos bancários e cartões.

## Responsibilities
- Integração com APIs de pagamento
- Geração de cobranças (PIX, boleto, cartão)
- Conciliação automática de recebimentos
- Gestão de chaves PIX e consentimentos Open Finance

## PIX
- **Chaves:** e-mail, telefone, CPF/CNPJ, chave aleatória, EVP
- **QR Code:** estático (valor variável) e dinâmico (valor fixo)
- **API:** Banco Central (SPI), endpoints de cobrança (cob, cobv)
- **Limites:** definidos pelo BC, noturno reduzido (R$ 1.000 padrão)
- **Juros/mora:** cobrança de juros de 1% ao mês sobre PIX com vencimento
- **Devolução:** endpoint de devolução obrigatório

## Open Finance
- **Fases:** 1) dados institucionais, 2) dados cadastrais, 3) serviços de iniciação de pagamento, 4) dados de operações de crédito
- **Consentimento:** obrigatório, prazo máximo 12 meses, revogável
- **Iniciação de pagamento:** PIX via Open Finance (sem redirecionamento)
- **Padrão:** API Open Finance Brasil (FAPI security profile)

## Boletos Bancários
- **Padrão:** CNAB 240 (FEBRABAN) ou CNAB 400
- **Registro:** obrigatório para boletos acima de determinado valor
- **Layout:** campo livre, nosso número, código de barras, linha digitável
- **Baixa:** automática via arquivo de retorno (CNAB)
- **Conciliação:** por nosso número, valor e data

## Cartões
- **Bandeiras:** Visa, Mastercard, Elo, Amex
- **Modalidades:** crédito, débito, voucher
- **Taxas:** definidas por adquirente (Cielo, Rede, Stone, PagSeguro)
- **Antecipação:** recebimento antecipado com desconto
- **Chargeback:** contestação de cobrança pelo portador

## Contabilização
```
PIX/Boleto recebido:
  DÉBITO: Banco
  CRÉDITO: Contas a Receber

Boleto pago:
  DÉBITO: Fornecedores
  CRÉDITO: Banco
```

## Dependencies
- `dominios/financeiro/contas-a-pagar.md`
- `dominios/financeiro/contas-a-receber.md`
- `dominios/financeiro/conciliacao-bancaria.md`

## Related Documents
- `dominios/fiscal/nfe.md` (DANFE, pagamento na nota)
- `compliance/lgpd.md` (consentimento Open Finance)


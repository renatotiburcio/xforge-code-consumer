# Playbook — Timeout SEFAZ seguido de reenvio incorreto

## Resumo Executivo

- **Tema**: Playbook — Timeout SEFAZ seguido de reenvio incorreto
- **Itens principais**: `moc-nfe-7-visao-geral-confaz`; `bling-rejeicao-204`; ERP não recebe retorno do lote
- **Seções**: Código, Domínio, Status, Trust Score
- **Categoria**: fiscal | **Tipo**: curated-operational

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| Título | Playbook — Timeout SEFAZ seguido de reenvio incorreto |
| Categoria | fiscal |
| Tipo | curated-operational |
| Seções | 12 |


## Código

`TIMEOUT`

## Domínio

`fiscal.nfe`

## Status

`derived-operational`

## Trust Score

`55`

## Fontes

- `moc-nfe-7-visao-geral-confaz`
- `bling-rejeicao-204`

## Sintomas

- ERP não recebe retorno do lote
- Usuário tenta emitir novamente
- Depois aparece duplicidade

## Diagnóstico

- Distinguir falha de comunicação de falha de autorização
- Consultar recibo/chave antes de gerar novo número

## Ações recomendadas

- Implementar consulta de recibo/status
- Persistir nRec
- Bloquear reemissão cega
- Exibir mensagem clara ao usuário

## Prevenção

- State machine de emissão
- Retry idempotente
- Consulta antes de nova emissão

## Edge cases

- Lote processado após timeout
- Usuário fecha tela e tenta novamente
- Fila duplicada

## Comportamento por UF/Município

- Pode variar conforme disponibilidade dos autorizadores

## Revisão humana obrigatória

False

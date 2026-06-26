# Playbook — Código de tributação nacional não administrado

## Resumo Executivo

- **Tema**: Playbook — Código de tributação nacional não administrado
- **Itens principais**: `tecnospeed-nfse-rejeicoes`; `nfse-documentacao-atual`; NFS-e rejeitada por código de tributação inválido/não vigente
- **Seções**: Código, Domínio, Status, Trust Score
- **Categoria**: fiscal | **Tipo**: curated-operational

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| Título | Playbook — Código de tributação nacional não administrado |
| Categoria | fiscal |
| Tipo | curated-operational |
| Seções | 12 |


## Código

`E0312`

## Domínio

`fiscal.nfse`

## Status

`community-hint`

## Trust Score

`60`

## Fontes

- `tecnospeed-nfse-rejeicoes`
- `nfse-documentacao-atual`

## Sintomas

- NFS-e rejeitada por código de tributação inválido/não vigente

## Diagnóstico

- Conferir código nacional de tributação e vigência
- Verificar competência

## Ações recomendadas

- Validar código no portal/documentação vigente
- Atualizar tabela local
- Criar validação pré-envio

## Prevenção

- Sincronizar tabelas NFS-e
- Versionar códigos por competência

## Edge cases

- Código válido em uma competência e inválido em outra

## Comportamento por UF/Município

- NFS-e pode ter variação municipal quando fora do padrão nacional

## Revisão humana obrigatória

True

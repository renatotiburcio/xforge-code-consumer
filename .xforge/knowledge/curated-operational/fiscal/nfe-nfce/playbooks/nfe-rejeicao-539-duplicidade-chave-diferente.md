# Playbook — Duplicidade de NF-e com diferença na Chave de Acesso

## Resumo Executivo

- **Tema**: Playbook — Duplicidade de NF-e com diferença na Chave de Acesso
- **Itens principais**: `webmania-rejeicao-539`; `totalerp-rejeicao-204`; `nfe-nt-2011-004`
- **Seções**: Código, Domínio, Status, Trust Score
- **Categoria**: fiscal | **Tipo**: curated-operational

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| Título | Playbook — Duplicidade de NF-e com diferença na Chave de Acesso |
| Categoria | fiscal |
| Tipo | curated-operational |
| Seções | 12 |


## Código

`539`

## Domínio

`fiscal.nfe`

## Status

`community-hint`

## Trust Score

`65`

## Fontes

- `webmania-rejeicao-539`
- `totalerp-rejeicao-204`
- `nfe-nt-2011-004`
- `moc-nfe-anexo-i`

## Sintomas

- SEFAZ informa duplicidade com diferença na chave
- Mesmo CNPJ emitente, modelo, série e número podem conflitar com nota anterior

## Diagnóstico

- Conferir se já existe documento autorizado/denegado com mesma numeração
- Verificar diferenças em data de emissão, tipo de emissão, cNF ou posições da chave
- Conferir migração entre sistemas emissores

## Ações recomendadas

- Consultar documentos existentes na SEFAZ
- Gerar nova numeração quando aplicável
- Não simplesmente reenviar sem consultar status
- Registrar causa no playbook de suporte

## Prevenção

- Controle único de série/número
- Rotina de importação de última numeração antes de iniciar novo emissor
- Consulta antes de reemissão após falha

## Edge cases

- Primeira nota no ERP novo mas não primeira nota do CNPJ
- Mudança de emissão normal para contingência
- Retorno atrasado após timeout

## Comportamento por UF/Município

- Relatos comunitários de comportamento diferente por UF devem ser tratados como baixo trust até validação

## Revisão humana obrigatória

True

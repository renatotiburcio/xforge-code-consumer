# Playbook — Duplicidade de NF-e

## Resumo Executivo

- **Tema**: Playbook — Duplicidade de NF-e
- **Itens principais**: `oobj-rejeicao-204`; `totalerp-rejeicao-204`; `bling-rejeicao-204`
- **Seções**: Código, Domínio, Status, Trust Score
- **Categoria**: fiscal | **Tipo**: curated-operational

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| Título | Playbook — Duplicidade de NF-e |
| Categoria | fiscal |
| Tipo | curated-operational |
| Seções | 12 |


## Código

`204`

## Domínio

`fiscal.nfe`

## Status

`community-hint`

## Trust Score

`65`

## Fontes

- `oobj-rejeicao-204`
- `totalerp-rejeicao-204`
- `bling-rejeicao-204`
- `moc-nfe-anexo-i`

## Sintomas

- SEFAZ retorna rejeição 204 ao autorizar NF-e/NFC-e
- Pode indicar chave/número já usado ou cenário de instabilidade conforme suporte de emissores

## Diagnóstico

- Verificar se já existe NF-e autorizada com mesma chave ou mesma sequência/série/modelo/CNPJ
- Conferir emissões feitas por outro sistema ou portal da SEFAZ
- Confirmar se não houve reenvio após timeout

## Ações recomendadas

- Consultar a chave/número na SEFAZ
- Ajustar número sequencial e série se houver duplicidade real
- Se houver instabilidade, consultar status SEFAZ antes de inutilizar ou alterar sequência
- Registrar incidente e fonte da decisão

## Prevenção

- Controlar numeração por CNPJ, modelo, série e ambiente
- Criar lock transacional para emissão
- Persistir estado de envio/retorno
- Tratar timeout com consulta antes de reemitir

## Edge cases

- Timeout no envio seguido de reenvio
- Migração de emissor antigo para novo sistema
- Notas emitidas no portal do governo fora do ERP
- Ambiente homologação vs produção

## Comportamento por UF/Município

- Há relatos comunitários de comportamento divergente em SC/MG; tratar como hipótese e validar contra documentação/SEFAZ

## Revisão humana obrigatória

True

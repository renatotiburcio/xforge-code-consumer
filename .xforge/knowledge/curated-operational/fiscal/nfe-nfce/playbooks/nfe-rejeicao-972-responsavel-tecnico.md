# Playbook — Obrigatória as informações do responsável técnico

## Resumo Executivo

- **Tema**: Playbook — Obrigatória as informações do responsável técnico
- **Itens principais**: `sefaz-pe-rejeicoes-comuns`; SEFAZ rejeita pela ausência do grupo de responsável técnico; Verificar se o layout/regra da UF exige o grupo responsáv...
- **Seções**: Código, Domínio, Status, Trust Score
- **Categoria**: fiscal | **Tipo**: curated-operational

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| Título | Playbook — Obrigatória as informações do responsável técnico |
| Categoria | fiscal |
| Tipo | curated-operational |
| Seções | 12 |


## Código

`972`

## Domínio

`fiscal.nfe`

## Status

`official-uf`

## Trust Score

`80`

## Fontes

- `sefaz-pe-rejeicoes-comuns`

## Sintomas

- SEFAZ rejeita pela ausência do grupo de responsável técnico

## Diagnóstico

- Verificar se o layout/regra da UF exige o grupo responsável técnico
- Verificar se dados do software house/responsável técnico foram configurados

## Ações recomendadas

- Preencher grupo responsável técnico conforme leiaute aplicável
- Revisar CNPJ/contato/email/telefone/idCSRT/hashCSRT quando exigidos
- Validar por UF e ambiente

## Prevenção

- Configurar cadastro do responsável técnico por emitente/UF
- Criar validação antes do envio

## Edge cases

- Regra opcional em algumas UFs e obrigatória em outras
- Divergência entre homologação e produção

## Comportamento por UF/Município

- Exemplo público citado pela SEFAZ PE; verificar demais UFs

## Revisão humana obrigatória

True

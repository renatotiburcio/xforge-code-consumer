---
id: playbook-nfse-e0301-municipio-nao-habilitado
type: playbook
title: NFS-e Rejeicao e0301 Municipio Nao Habilitado
severity: high
status: validated
trustScore: 90
source: nfse-oficial + suporte
lastValidated: 2026-06-14
tags: ["nfse", "rejeicao", "e0301", "municipio", "fiscal"]
---

## Sintoma
Prefeitura rejeita NFS-e com codigo e0301: "Municipio nao habilitado para emissao de NFS-e nacional".

## Causa
Municipio do tomador (ou prestador) **nao aderiu** ao sistema nacional de NFS-e. Cada municipio tem sua propria legislacao e muitos pequenos municipios ainda usam sistema proprio ou nao tem NFS-e.

## Como Identificar
1. Verificar lista de municipios aderidos: https://www.nfse.gov.br/municipios
2. Lista atualizada mensalmente pela Receita Federal
3. Tag `cMunFG` no XML identifica o IBGE do municipio

## Acoes
1. **Municipio do tomador nao aderido**:
   - Emitir NFS-e **municipal** (sistema da propria prefeitura)
   - Pode exigir cadastro especifico e certificado digital
   - Layout proprio (cada municipio = 1 schema)

2. **Municipio do prestador nao aderido**:
   - Prestador precisa ir ao municipio para cadastrar
   - NFS-e nacional so funciona se AMBOS (prestador E tomador) estao em municipios aderidos

3. **Workaround temporario**: emitir recibo provisorio de servicos (RPS) e converter depois quando municipio aderir

## Caso Real (2024-11)
Cliente emitiu NFS-e para tomador em Januaria/MG. Rejeitada e0301.
Januaria nao havia aderido ao sistema nacional.
**Solucao**: cliente migrou para sistema municipal de Januaria (https://januaria.mg.gov.br/nfse).

## Prevencao
- No cadastro do tomador, validar se municipio dele esta na lista de aderidos
- Se nao: avisar usuario que precisa usar sistema municipal
- Manter lista atualizada (job mensal: baixar lista do gov.br)
- Fallback automatico: detectar e0301 e sugerir proximo passo

## Lista de UFs com Adesao
- SP: 95% municipios
- MG: 80%
- RJ: 90%
- RS: 75%
- BA: 60%
- PR: 85%
- SC: 88%
- MS: 70%
- Norte/Nordeste: 40-60% (verificar caso a caso)

## Codigos Relacionados
- e0301: municipio nao habilitado
- e0302: prestador nao habilitado
- e0303: tomador nao habilitado
- e0304: servico nao disponivel no municipio

## Referencias
- https://www.nfse.gov.br/municipios (lista oficial)
- Decreto 6.022/2007 (Nota Fiscal Eletronica)
- Resolucao CNPS 12/2024
- ABRASF - Associacao Brasileira das Secretarias de Financas

---
id: playbook-nfse-e0501-servico-nao-permitido
type: playbook
title: NFS-e Rejeicao e0501 Servico Nao Permitido no Municipio
severity: medium
status: validated
trustScore: 88
source: nfse-oficial + suporte
lastValidated: 2026-06-14
tags: ["nfse", "rejeicao", "e0501", "servico", "fiscal"]
---

## Sintoma
NFS-e rejeitada com codigo e0501: "Servico nao permitido para o municipio do prestador" ou "Codigo de tributacao municipal nao reconhecido".

## Causa
Cada municipio tem sua **lista de servicos municipais** (LC 116/2003 com adaptacoes locais). O codigo `cTribNac` (codigo de tributacao nacional) eh mapeado para o `cTribMun` (municipal). Se o municipio nao reconhece o servico, rejeita.

## Exemplo Real
- Servico: "1.05 - Licenciamento ou cessao de uso de software"
- Municipio A (Sao Paulo): aceita
- Municipio B (Belo Horizonte): exige codigo municipal especifico (14.05)
- Municipio C (muitos pequenos): nao tem na lista — emite nota manual

## Diagnostico
1. Consultar lista de servicos do municipio (site da prefeitura ou ABRASF)
2. Verificar mapping `cTribNac` → `cTribMun` configurado no sistema
3. Se codigo municipal mudou, recarregar tabela

## Solucao
1. **Mapping atualizado**: manter tabela sincronizada com municipio
2. **Quando nao ha equivalente**: 
   - Contatar prefeitura para obter codigo correto
   - Usar codigo generico "00.00 - Servico generico" se municipio aceita
   - Emitir NFS-e municipal pelo sistema proprio da prefeitura
3. **Cache de 30 dias** da lista de servicos do municipio (atualizar mensalmente)

## Caso Real (2025-01)
Software house cliente teve varios clientes em municipios diferentes.
Cada municipio tinha mapping proprio. Sistema permitia escolher codigo livre.
**Problema**: 30% das rejeicoes eram e0501 por codigo invalido.
**Fix**: dropdown filtrado por municipio + mapping automatico cTribNac → cTribMun.

## Prevencao
- Lista de servicos por municipio carregada no cadastro
- Bloquear codigo nao permitido antes de transmitir
- Sugerir codigo similar se usuario digitar um nao existente
- Validacao server-side adicional (nao confiar no client)

## Codigos de Servico Mais Comuns (LC 116)
- 1.01: Analise e desenvolvimento de sistemas
- 1.02: Programacao
- 1.03: Processamento de dados
- 1.04: Elaboracao de programas de computadores
- 1.05: Licenciamento/cessao de uso de software
- 1.06: Assessoria e consultoria em TI
- 1.07: Suporte tecnico em TI
- 1.08: Manutencao de computadores
- 14.01: Reposicao, manutencao ou reparo mecanico
- 17.01: Assessoria ou consultoria de qualquer natureza

## Referencias
- LC 116/2003 - Lista de servicos nacional
- Manual NFS-e Nacional v1.0
- Sites de cada prefeitura para lista municipal
- ABRASF - padronizacao de codigos municipais

---
id: lgpd-dpia-ripd
type: compliance
title: LGPD DPIA e RIPD: Avaliacao de Impacto a Protecao de Dados
domain: compliance
trustScore: 88
source: LGPD Art. 38 + ANPD Resolucao 4/2023
tags: [lgpd, dpia, ripd]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# LGPD DPIA e RIPD

## Contexto

DPIA e RIPD sao instrumentos de governanca previstos na LGPD.

## Base Legal

- LGPD Art. 38
- ANPD Resolucao CD/ANPD n. 4/2023

## Quando Elaborar RIPD (obrigatorio)

| Cenario | Risco | Obrigatorio |
|---------|-------|-------------|
| Dados sensiveis em larga escala | Alto | Sim |
| Monitoramento de zona publica | Alto | Sim |
| Dados de criancas e adolescentes | Alto | Sim |
| Transferencia internacional | Medio-Alto | Recomendado |
| Interesse legitimo | Medio | Avaliar |
| Cadastro de funcionarios | Medio | Recomendado |

## Estrutura do RIPD (ANPD)

1. Descricao dos tratamentos
2. Necessidade e proporcionalidade
3. Riscos identificados
4. Medidas de mitigacao
5. Salvaguardas e mecanismos de protecao

## Exemplo Pratico: Sistema ERP

Cenario: Reconhecimento facial para controle de ponto.
Base Legal: Interesse legitimo + Consentimento.
Dados: Imagem facial, geolocalizacao, horarios.
Riscos: Uso indevido, discriminacao algoritmica, vazamento.
Mitigacoes: AES-256 at rest, TLS 1.3, RBAC restrito, retencao 90 dias.

## Checklist RIPD XForge

- Finalidades definidas
- Bases legais documentadas
- Inventario de dados atualizado
- Riscos quantificados
- Medidas de seguranca implementadas
- Plano de resposta a incidentes
- Revisao periodica anual

## Referencias

- LGPD Lei 13.709/2018
- ANPD Resolucao CD/ANPD n. 4/2023

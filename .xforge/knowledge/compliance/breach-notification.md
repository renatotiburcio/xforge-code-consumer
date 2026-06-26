---
id: knowledge-compliance-breach-notification
type: knowledge
title: Notificacao de Incidentes LGPD
category: compliance
domain: compliance
trustScore: 90
source: human-expert
createdAt: 2026-06-14
lastValidated: 2026-06-14
tags: [lgpd, breach, incident, anpd, notification]
---

# Notificacao de Incidentes LGPD

## Quando notificar

Vazamento de dados pessoais que possa causar **risco relevante** aos titulares
deve ser comunicado a ANPD (Autoridade Nacional) **em prazo razoavel** (Art. 48).

Boa pratica: **ate 2 dias uteis** apos constatacao.

## O que reportar

1. Descricao do que ocorreu
2. Categorias de dados afetados
3. Numero aproximado de titulares afetados
4. Medidas tomadas para reverter/mitigar
5. Riscos envolvidos
6. Plano de comunicacao aos titulares

## Formato

ANPD recebe via sistema proprio. Titulares recebem via canal direto
(email, SMS, app push) dependendo do caso.

## Categorias de risco

| Categoria | Notificar ANPD | Notificar titular | Prazo |
|-----------|:--------------:|:-----------------:|:-----:|
| Vazamento de dados sensiveis (saude, biometria) | SIM | SIM | 2 dias uteis |
| Vazamento de dados de crianca/adolescente | SIM | SIM | 2 dias uteis |
| Vazamento de CPF + dados financeiros | SIM | SIM | 5 dias uteis |
| Vazamento de nome + email | AVALIAR | SIM | 10 dias uteis |
| Dados anonimos (sem possibilidade de reversao) | NAO | NAO | N/A |

## Prevencao

- DPIA (Data Protection Impact Assessment) obrigatoria para novos produtos
- Pen testing anual
- DLP (Data Loss Prevention) em endpoints
- Treinamento trimestral dos funcionarios
- Plano de resposta a incidentes documentado e testado

## Referencias

- LGPD Art. 48
- Resolucao CD/ANPD 15/2024 (comunicacao de incidentes)
- ISO 27035 (Incident management)


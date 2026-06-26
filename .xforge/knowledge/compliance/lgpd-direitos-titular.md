---
id: lgpd-direitos-titular
type: compliance
title: LGPD Direitos do Titular: Atendimento aos Arts. 17-22
domain: compliance
trustScore: 90
source: LGPD Arts. 17-22 + ANPD Regulamento
tags: [lgpd, direitos-titular, atendimento]
createdAt: 2026-06-14
lastValidated: 2026-06-14
status: active
---

# LGPD Direitos do Titular

## Os 10 Direitos (Arts. 17-22)

| Direito | Prazo | Implementacao XForge |
|---------|-------|---------------------|
| Confirmacao de tratamento | 15 dias | GET /api/lgpd/me/data |
| Acesso aos dados | 15 dias | Relatorio PDF/JSON |
| Correcao | 15 dias | Endpoint self-service |
| Anonimizacao, bloqueio, eliminacao | 15 dias | Job assincrono |
| Portabilidade | 15 dias | Export JSON/XML |
| Eliminacao com consentimento | 15 dias | Hard delete + purge 90 dias |
| Compartilhamento info | 15 dias | Audit log |
| Consequencias de nao consentir | Antes | Tela consentimento |
| Revogacao consentimento | Imediato | /api/lgpd/revoke |
| Revisao decisoes automatizadas | 15 dias | Recurso + analise humana |

## Fluxo de Atendimento (XForge)

1. Titular abre chamado
2. Sistema cria ticket SLA 15 dias
3. DPO recebe alerta
4. Query em todas as tabelas
5. Resposta via canal original
6. Log de auditoria (Art. 37)

## Metricas Recomendadas

| Metrica | Meta |
|---------|------|
| Tempo medio de resposta | < 10 dias |
| % atendimentos no prazo | > 95% |
| Taxa de revogacao | < 5% |
| Reclamacoes ANPD | 0 |

## Penalidades

- Multa ate 2% faturamento (max R$ 50M por infracao)
- Bloqueio de dados
- Publicizacao
- Eliminacao

## Referencias

- LGPD Lei 13.709/2018 Arts. 17-22
- ANPD Resolucao CD/ANPD n. 15/2024

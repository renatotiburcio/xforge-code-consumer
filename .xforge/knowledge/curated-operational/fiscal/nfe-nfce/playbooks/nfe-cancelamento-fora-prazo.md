---
id: playbook-nfe-cancelamento-fora-prazo
type: playbook
title: NFe Cancelamento Fora do Prazo (24h)
severity: medium
status: validated
trustScore: 89
source: sefaz-oficial + suporte
lastValidated: 2026-06-14
tags: ["nfe", "sefaz", "cancelamento", "prazo", "fiscal"]
---

## Sintoma
Tentativa de cancelar NFe retorna erro: "Rejeicao: Prazo de cancelamento expirado".

## Regra Oficial
NFe pode ser cancelada em ate **24 horas** apos a **autorizacao de uso** (nao a emissao).
- 24h = 1440 minutos corridos
- Apos 24h: cancelamento NEGADO, alternativa eh **devolucao/retorno** (NFe de entrada)

## Causas Comuns
1. Usuario esqueceu de cancelar no mesmo dia
2. Sistema operacional caiu e a equipe tentou cancelar no dia seguinte
3. NFe transmitida tarde da noite, autorizacao so chegou 23h depois
4. Bug: timestamp de autorizacao foi perdido (cache expirado)

## Diagnostico
```sql
-- Verificar NFe com mais de 24h de autorizacao ainda ativas
SELECT chave_acesso, data_autorizacao, status
FROM nfe_cabecalho
WHERE status = 'AUTORIZADA'
  AND data_autorizacao < NOW() - INTERVAL 24 HOUR;
```

## Solucao (cascata)
1. **Dentro de 24h**: cancelar normalmente (evento 110111)
2. **Apos 24h**:
   a. Em **devolucao total**: emitir NFe de entrada com CFOP 1.202/2.202/5.202/6.202
   b. Em **devolucao parcial**: emitir NFe de entrada com itens + quantidade devolvida
   c. Documentar motivo em campo proprio
3. **Impossivel recuperar valor total**: se cliente pagou e nao aceita devolucao, registrar como perda operacional

## Caso Real (2024-08)
NFe emitida sexta 18h. Autorizada sexta 19h.
Tentaram cancelar segunda 10h = 63h depois.
**Solucao**: emitiram NFe de devolucao total (mesma chave referenciada, CFOP 1.202).

## Automacao Recomendada
```python
# Job diario: alertar NFe proximas de expirar (12h, 18h, 23h)
def alerta_cancelamento():
    nfes = db.query("""
        SELECT chave_acesso, numero, data_autorizacao
        FROM nfe_cabecalho
        WHERE status = 'AUTORIZADA'
          AND data_autorizacao BETWEEN NOW() - INTERVAL 23 HOUR AND NOW() - INTERVAL 12 HOUR
    """)
    for nfe in nfes:
        horas = (now() - nfe.data_autorizacao).total_seconds() / 3600
        enviar_email(
            to=responsavel_nfe,
            subject=f"NFe {nfe.numero} cancelavel por mais {24 - horas:.1f}h"
        )
```

## Prevencao
- Alerta em 12h e 23h apos autorizacao
- Auto-cancelamento de NFe com erro detectado em 1h
- Bloqueio de NFe 24h+ no dashboard com aviso visual
- Treinamento de equipe sobre prazo de 24h (apenas autorizacao, nao emissao)

## Referencias
- MOC 7.0 - Evento de Cancelamento (110111)
- NT 2019.005 - Regras de cancelamento
- Ajuste SINIEF 03/2019

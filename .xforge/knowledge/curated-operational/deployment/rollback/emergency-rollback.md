---
id: playbook-deploy-emergency-rollback
type: playbook
title: Deploy Falhou - Rollback de Emergencia
severity: critical
status: validated
trustScore: 94
source: devops-best-practices + operacao-real
lastValidated: 2026-06-14
tags: ["deployment", "rollback", "blue-green", "kubernetes", "incident"]
---

## Quando Acionar
- Health check falha em > 50% replicas (5min)
- Error rate subiu > 5% (vs baseline)
- Latencia p95 subiu > 50% (vs baseline)
- Funcionalidade core quebrada (login, NFe, folha)
- Migration destrutiva nao pode ser revertida

## Acao Imediata (< 2 min)

### Blue-Green (Recomendado - ja preparado)
```bash
# 1. Identificar versao anterior
kubectl -n prod get deploy xforge-api -o jsonpath='{.spec.template.spec.containers[0].image}'
# Ex: registry/xforge:1.1.2

# 2. Reverter service selector para blue
kubectl -n prod patch service xforge-api -p '{"spec":{"selector":{"version":"blue"}}}'

# 3. Validar
kubectl -n prod get endpoints xforge-api
# Deve mostrar pods da versao blue
```

### Kubernetes Rollout Undo
```bash
# 1. Ver historico
kubectl -n prod rollout history deploy/xforge-api

# 2. Rollback para revisao anterior
kubectl -n prod rollout undo deploy/xforge-api

# 3. Acompanhar
kubectl -n prod rollout status deploy/xforge-api
```

### Docker Swarm
```bash
docker service rollback xforge_api
```

### Plain VMs (sem orquestrador)
```bash
# 1. Parar versao nova
systemctl stop xforge-app-new

# 2. Iniciar versao antiga
systemctl start xforge-app-old

# 3. Validar
curl -s http://localhost:5000/health
```

## Validar Rollback

### 1. Smoke Tests (< 2min)
```bash
# Health check
curl -s http://api/health | jq .status  # deve ser "healthy"

# Login basico
curl -X POST http://api/auth/login -d '{"user":"smoke","pass":"test"}'

# Endpoint critico
curl -s http://api/nfe/recentes?limit=5

# DB connectivity
psql -c "SELECT COUNT(*) FROM clientes"
```

### 2. Metricas (< 5min)
- Error rate caiu para baseline?
- Latencia voltou ao normal?
- Todas as replicas sao da versao antiga?

```promql
# Validar versao em producao
count by (version) (kube_deployment_status_replicas_available{deployment="xforge-api"})
```

## Apos Rollback

### 1. Comunicar
- Status page (se > 5min outage)
- Canal #incident-XXXX
- Stakeholders chave

### 2. Investigar
- Logs do deploy que falhou
- Diff entre versoes
- Migration que pode ter causado problema

### 3. Fix Forward (opcional)
Se problema eh simples e bem compreendido:
- Hotfix em branch
- Code review rapido (1-2 reviewers)
- CI passa
- Deploy com canary 5% por 30min

### 4. Post-Mortem
- Marcar incident
- Agendar post-mortem (ate 7 dias)
- Action items com owner + prazo

## Caso Real (2024-12)
Deploy de NFe service com bug: valida CNPJ mas gera hash errado para digitos verificadores.
Health check OK (servico sobe), mas 30% das NFe rejeitadas por SEFAZ.
**Erro detectado**: 18min apos deploy (monitor de taxa de rejeicao SEFAZ)
**Acao**: blue-green rollback em 90s.
**Total downtime efetivo**: 0 (blue-green instantaneo).

## Prevencao

### 1. Smoke Tests Pos-Deploy
```yaml
# GitHub Actions
- name: Post-deploy smoke tests
  run: |
    sleep 60  # aguarda warm-up
    ./scripts/smoke-tests.sh https://api.prod.xforge.com.br
    if [ $? -ne 0 ]; then
      echo "SMOKE FAILED - initiating rollback"
      ./scripts/rollback.sh
      exit 1
    fi
```

### 2. Metricas de Deploy (SLI)
- Deploy success rate > 95%
- Mean time to rollback < 10min
- Deploy frequency (DORA)

### 3. Feature Flags
- Decouple deploy from release
- Rollback = turn off flag (sem deploy)
- Usar: LaunchDarkly, Unleash, Optimizely

### 4. Database Migrations
- **Sempre backward-compatible**
- Pattern: expand-contract (adiciona coluna nova, codigo usa, depois remove antiga)
- Migration destrutiva exige janela de manutencao (e roll forward planejado)

## Runbook de Migracao
Se rollback precisa reverter migration:
```bash
# 1. Ver migration aplicada
dotnet ef migrations list --no-build

# 2. Reverter
dotnet ef database update PreviousMigrationName

# 3. Re-deploy versao antiga
kubectl -n prod rollout undo deploy/xforge-api
```

## Referencias
- ADR-0021 XForge: Deploy Strategy Blue-Green
- Kubernetes: Managing Resources - Deployment rollback
- Google SRE Book: Release Engineering
- DORA Metrics: https://www.devops-research.com/research.html
- Feature Flags: https://martinfowler.com/articles/feature-toggles.html

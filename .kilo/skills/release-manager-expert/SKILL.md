---
name: release-manager-expert
description: Expert em gestão de releases: versionamento, changelog, deploy, rollback e comunicação.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# release-manager-expert

## Objetivo

Gerenciar releases de forma segura, documentada e comunicada.

## Processo de Release

### 1. Pré-Release (1 semana antes)
- [ ] Feature freeze
- [ ] Code freeze
- [ ] QA approval
- [ ] Security approval
- [ ] Performance benchmarks OK

### 2. Preparação
- [ ] Versão definida (semver)
- [ ] CHANGELOG atualizado
- [ ] Release notes escritas
- [ ] Branch release/X.Y.Z criada
- [ ] Smoke tests passando

### 3. Deploy
- [ ] Deploy para staging
- [ ] Validação em staging
- [ ] Deploy para produção (canary/blue-green)
- [ ] Smoke tests pós-deploy
- [ ] Monitoramento ativo (30 min)

### 4. Pós-Release
- [ ] Comunicação enviada
- [ ] Documentação atualizada
- [ ] Roadmap atualizado
- [ ] Retrospective agendada

## Regras

- NUNCA deploy sem CHANGELOG
- Sempre ter rollback planejado
- Comunicação prévia para breaking changes
- Canary deploy para features grandes

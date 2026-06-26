---
id: playbook-security-secret-leaked-github
type: playbook
title: Secret (API Key, Password) Vazado no GitHub
severity: critical
status: validated
trustScore: 95
source: incidente-real + best-practices
lastValidated: 2026-06-14
tags: ["security", "secret", "github", "leak", "lgpd", "incident"]
---

## Sintoma
GitHub Secret Scanning ou pre-commit hook detecta secret (API key, password, token) em codigo commitado. Pode ser:
- `aws_access_key_id`
- `api_key = "sk-..."`
- `password = "..."`
- `connection_string` com credenciais
- `private_key.pem`

## Acao Imediata (< 5 min)
1. **REVOGAR O SECRET IMEDIATAMENTE** (nao esperar)
   - AWS: IAM console -> deactivate access key
   - Stripe: dashboard -> roll API key
   - Database: trocar senha
   - GitHub PAT: settings -> revoke
2. **Verificar uso do secret** (logs, billing) para detectar abuso
3. **Gerar novo secret** com permissoes minimas

## Acoes Subsequentes (< 1h)
1. **Remover do historico Git** (BFG Repo-Cleaner ou git filter-repo)
   ```bash
   # git filter-repo
   git filter-repo --invert-paths --path secrets.yaml
   git push origin --force --all
   ```
2. **Avisar equipe** no canal #security-incident
3. **Abrir incident** com severidade P0/P1
4. **Notificar DPO** se dados pessoais foram expostos (LGPD Art. 48)

## Investigacao
1. **Quando vazou?** (git log -p)
2. **Quem commitou?** (git blame)
3. **Quem teve acesso?** (GitHub access logs)
4. **Alguem usou?** (cloud provider logs)
5. **Escopo**: so o secret ou outros dados tambem?

## Caso Real (2025-02)
Desenvolvedor commita `appsettings.json` com connection string de producao.
Bot de mineracao de crypto detectou em 7 minutos. Iniciou mineracao na AWS.
**Impacto**: $12K em custos de EC2 (8 horas de mineracao).
**Causa raiz**: secret em arquivo commitado (devia estar em .env).
**Fix**: pre-commit hook com secret scanning, vaults para secrets, educacao.

## Ferramentas de Prevencao

### 1. Pre-commit Hook (local)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### 2. CI/CD (server-side)
```yaml
# GitHub Actions
- name: Secret scan
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: ${{ github.event.pull_request.base.sha }}
    head: ${{ github.event.pull_request.head.sha }}
```

### 3. Runtime (no app)
```csharp
// .NET: nunca ler secret de appsettings.json
var apiKey = builder.Configuration["ExternalServices:ApiKey"]
    ?? throw new InvalidOperationException("ApiKey not configured");

// Validar no startup que nao eh o default/placeholder
if (apiKey.StartsWith("PLACEHOLDER") || apiKey.Length < 32)
    throw new InvalidOperationException("Invalid API key");
```

## Prevencao
- Secrets SEMPRE em vault (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault)
- `.env` em .gitignore (com `.env.example` sem secrets)
- Pre-commit hook com secret scanning
- CI com detect-secrets + trufflehog
- Educacao: nunca copiar config de prod para dev sem sanitizar
- Rotate secrets a cada 90 dias (politica)
- Principio de menor privilegio: secret com scope minimo

## Apos Resolucao
1. **Post-mortem** (no later than 7 days)
2. **Action items** com owner + prazo
3. **Atualizar runbook** com licoes aprendidas
4. **Comunicar stakeholders** se impacto externo (clientes, usuarios)
5. **LGPD**: notificar ANPD em 72h se dados pessoais expostos (Art. 48)

## Referencias
- OWASP Top 10 A02:2021 - Cryptographic Failures
- LGPD Art. 48 - Comunicacao de incidente
- GitHub Secret Scanning docs
- BFG Repo-Cleaner: https://rtyley.github.io/bfg-repo-cleaner/
- trufflehog: https://github.com/trufflesecurity/trufflehog

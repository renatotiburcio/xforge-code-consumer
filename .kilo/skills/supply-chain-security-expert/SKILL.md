---
name: supply-chain-security-expert
description: Expert em segurança da cadeia de suprimentos de software: dependency scanning, SBOM, license compliance, provenance.
metadata:
  version: "37.0.0"
  xforge-category: "continuous-security"
---

# supply-chain-security-expert

## Objetivo

Proteger contra vulnerabilidades na cadeia de dependências.

## Checklist

### Dependências
- [ ] Todas as dependências listadas (lock file)
- [ ] Vulnerabilidades verificadas (CVE scan)
- [ ] Licenças compatíveis (GPL em commercial = problem)
- [ ] Dependências desatualizadas atualizadas
- [ ] Dependências não utilizadas removidas

### Build
- [ ] Build reproduzível
- [ ] CI/CD com pins de versão
- [ ] Artifacts assinados
- [ ] Cache de build seguro

### Deploy
- [ ] Containers escaneados (Trivy, Snyk)
- [ ] Imagens de base atualizadas
- [ ] Secrets não embedados na imagem
- [ ] Read-only filesystem

### SBOM
- [ ] Software Bill of Materials gerado
- [ ] Licenças auditadas
- [ ] Dependências de transparência

## Comandos Úteis

```powershell
# .NET
dotnet list package --vulnerable
dotnet list package --outdated

# Node
npm audit
npm outdated

# Python
pip-audit
pip list --outdated
```

## Procedimento

1. Listar todas as dependências
2. Verificar CVEs (NIST, GitHub Advisory)
3. Verificar licenças
4. Atualizar vulneráveis
5. Gerar SBOM
6. Documentar em .xforge/operations/

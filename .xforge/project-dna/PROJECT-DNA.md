# PROJECT-DNA

**Gerado em**: 2026-06-22 08:09
**Gerado por**: purify.ps1 (DR-0180 Fase 1)
**Stack detectado**: dotnet
**Confidence**: 0.16
**Signals**: *.csproj, package.json, pyproject.toml, go.mod, Cargo.toml, pom.xml, index.html
**Projeto**: XForge-Development-New

## Visao Geral

Projeto analisado automaticamente por purify.ps1 (DR-0180).

- **Nome**: XForge-Development-New
- **Tipo**: dotnet
- **Stack**: dotnet (confidence 0.16)

## Stack Detectado

- ***.csproj**
- **package.json**
- **pyproject.toml**
- **go.mod**
- **Cargo.toml**
- **pom.xml**
- **index.html**

## Convencoes Detectadas

- **Naming**: PascalCase para classes, camelCase para metodos/variaveis`n- **ORM**: provavel Entity Framework Core (verificar .csproj)
- [OK] Has Tests
- [OK] Has CI/CD
- [ ] Has Docker
- [OK] Has README
- [OK] Has .gitignore

## Lacunas (Gaps)

- [ ] Has Docker

## Proximos Passos Recomendados

1. **Validar PROJECT-DNA**: revisar e ajustar com o time
2. **Rodar Doctor**: xforge doctor para validar setup
3. **Adotar Skills gradualmente**: instalar 1 skill por semana
4. **Aplicar GCF**: usar Conselho dos Genios para decisoes
5. **Documentar Decisoes**: cada DR em .xforge/decisions/ 

## Referencias

- GCF (Regra de Ouro Suprema): .kilo/rules/02-genius-council-framework.md 
- Stack detection: .kilo/skills/stack-aware-context/SKILL.md 
- DR-0180 (este template): .xforge/decisions/DR-0180-stack-aware-context-and-memory-namespace.md 

## Comandos Uteis

``n# Re-rodar deteccao
.xforge/scripts/purify.ps1 -ProjectRoot .

# Ver o que mudaria (sem alterar)
.xforge/scripts/purify.ps1 -WhatIf

# Limpar template-only paths
.xforge/scripts/reset-memory.ps1

# Diff contra manifest
.xforge/scripts/diff-consumer.ps1
``n
---
name: quality-gates
description: Use before finishing development to validate build, warnings, tests, coverage, documentation, memory, security, and release readiness.
metadata:
  version: "7.0.0"
  xforge-category: "enterprise-engineer"
---

# quality-gates

## Objetivo

Validar que o código está pronto para release antes de finalizar qualquer tarefa de desenvolvimento.

## Quando Usar

- Antes de commitar mudanças significativas
- Antes de criar PR
- Antes de release
- Quando o usuário pede "validar" ou "checar qualidade"

## Gates Obrigatórios

### 1. Build
```powershell
dotnet build --no-restore 2>&1 | Select-String "error|warning"
```
- Zero errors aceitável
- Warnings devem ser documentados ou corrigidos

### 2. Testes
```powershell
dotnet test --no-build --verbosity normal
```
- Todos os testes devem passar
- Cobertura mínima: 85%

### 3. Análise de Código
- Sem `TODO` sem issue associada
- Sem `Console.WriteLine` em produção
- Sem commented-out code
- Complexidade ciclomática < 10

### 4. Segurança
- Sem secrets no código
- Sem hardcoded credentials
- Validação de input em endpoints públicos
- Parameterized queries para DB

### 5. Documentação
- README atualizado se aplicável
- CHANGELOG entry se feature nova
- XML docs em APIs públicas

### 6. Memória
- .xforge/memory atualizada se houve decisão de arquitetura
- Knowledge graph atualizado se aplicável

## Saída Esperada

```json
{
  "build": "pass|fail",
  "tests": "pass|fail",
  "coverage": 85,
  "security": "clean|issues",
  "warnings": [],
  "ready": true,
  "blockers": []
}
```

## Bloqueio

Se qualquer gate crítico falhar, NÃO finalizar a tarefa. Reportar o bloqueio e aguardar correção.

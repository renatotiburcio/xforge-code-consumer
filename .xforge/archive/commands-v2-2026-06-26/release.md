---
name: release
description: Gestao de releases e deploys
category: xforge-core
---

# /release

Gerencie releases e deploys.

## Sintaxe

```
/release prepare
/release validate
/release ship
/release rollback
```

## Sub-comandos

| Sub-comando | Descricao | Substitui |
|-------------|-----------|-----------|
| prepare | Preparar release | release-readiness-analysis |
| validate | Validar release | release-readiness-analysis |
| ship | Publicar | ship |
| rollback | Reverter | release-readiness-analysis |

# Git Hooks

## Hooks

| Hook | Action | Blocks on failure |
|------|--------|-------------------|
| `pre-commit` | Runs `doctor.ps1` | Yes |
| `pre-push` | Runs RAG health check | No (warning only) |

## Installation

```powershell
powershell -File .githooks/install.ps1
```

Or manually:
```powershell
git config core.hooksPath .githooks
```

## Bypass (emergency)

```powershell
git commit --no-verify
git push --no-verify
```

# Proactive Quality Gates - XForge Engineer (Stack-Aware)

## Visao Geral

Quality gates automaticos stack-aware que rodam silenciosamente a cada mudanca de codigo, sem intervencao manual. Antes de qualquer gate, o sistema DETECTA o stack do projeto e roda os comandos apropriados.

## Stack Detection (Obrigatorio Antes de Qualquer Gate)

Sinais lidos (ordem de prioridade):
- `angular.json` -> Angular
- `next.config.*` -> Next.js
- `vite.config.*` -> Vite (React, Vue, Svelte, Solid)
- `package.json` -> Node/JS/TS
- `*.csproj` / `*.sln` -> .NET
- `requirements.txt` / `pyproject.toml` -> Python
- `go.mod` -> Go
- `Cargo.toml` -> Rust
- `index.html` standalone -> HTML+Tailwind estatico
- Multi-stack: rodar gates de TODOS os stacks

## Gate 1: Pre-Commit (instantaneo, <2s)

Rodam automaticamente antes de cada commit.

### Checks Stack-Agnostic (todos os stacks)
| Check | Comando | Criterio | Auto-fix |
|-------|---------|----------|----------|
| **Linguagem format** | stack-specific (ver abaixo) | Sem formatacao incorreta | auto-formatter |
| **Secrets** | `gitleaks detect --no-banner` ou `trufflehog` | Zero secrets no codigo | Mover para .env |
| **Self-healing** | SH rules (SH-001 a SH-012) | Zero erros detectaveis | Correcao automatica |

### .NET
| Check | Comando |
|-------|---------|
| **Lint C#** | `dotnet format --verify-no-changes` |
| **Usings** | Verificacao de using nao utilizados |

### Node/TypeScript/React/Next/Angular/Vue/Svelte
| Check | Comando |
|-------|---------|
| **Lint** | `npx eslint . --max-warnings=0` |
| **Format** | `npx prettier --check .` |
| **Types** | `npx tsc --noEmit` |

### Python
| Check | Comando |
|-------|---------|
| **Lint** | `ruff check .` |
| **Format** | `ruff format --check .` |
| **Types** | `mypy .` |

### Go
| Check | Comando |
|-------|---------|
| **Format** | `gofmt -l .` |
| **Lint** | `golangci-lint run --max-issues-per-linter=0` |
| **Vet** | `go vet ./...` |

### Rust
| Check | Comando |
|-------|---------|
| **Format** | `cargo fmt --check` |
| **Lint** | `cargo clippy -- -D warnings` |

### HTML+Tailwind standalone
| Check | Comando |
|-------|---------|
| **HTML lint** | `htmlhint "**/*.html"` |
| **Classes** | `tailwindcss-classnames --check "**/*.html"` |

## Gate 2: Pre-Build (<30s)

### .NET
```powershell
dotnet restore
dotnet build --no-restore
dotnet build -warnaserror
```

### Node/TypeScript
```powershell
npm ci || pnpm install || yarn install
npm run build
npx tsc --noEmit
```

### Python
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m compileall src/
```

### Go
```powershell
go build ./...
go vet ./...
```

### Rust
```powershell
cargo build --workspace
```

### HTML+Tailwind (com build)
```powershell
npm run build:css  # se usa Tailwind CLI
```

## Gate 3: Pre-Push (<60s)

### .NET
```powershell
dotnet test --no-build --verbosity normal
dotnet test --collect:"XPlat Code Coverage" --results ./coverage
dotnet list package --vulnerable
dotnet nuget audit
dotnet build -warnaserror
```

### Node/TypeScript
```powershell
npm test -- --coverage --coverageThreshold='{"global":{"lines":85}}'
npm audit --audit-level=high
```

### Python
```powershell
pytest --cov=. --cov-report=xml --cov-fail-under=85
pip-audit
ruff check .
mypy .
```

### Go
```powershell
go test ./... -race -cover
go test ./... -coverprofile=coverage.out
govulncheck ./...
```

### Rust
```powershell
cargo test --workspace
cargo clippy -- -D warnings
cargo audit
```

## Gate 4: Post-Merge (<5min)

### .NET
```powershell
dotnet build
dotnet test
dotnet test --collect:"XPlat Code Coverage"
dotnet list package --vulnerable
docker build
```

### Node/TypeScript
```powershell
npm run build
npm test
npm test -- --coverage
npm audit
docker build
```

### Python
```powershell
pytest --cov=.
pip-audit
docker build
```

### Go
```powershell
go build ./...
go test ./... -cover
govulncheck ./...
docker build
```

### Rust
```powershell
cargo build --workspace --release
cargo test --workspace
cargo audit
```

## Configuracao (kilo.jsonc)

```json
{
  "qualityGates": {
    "enabled": true,
    "stack": "auto-detect",
    "preCommit": {
      "enabled": true,
      "failOn": "error",
      "autoFix": true,
      "checks": ["format", "secrets", "self-healing"]
    },
    "preBuild": {
      "enabled": true,
      "failOn": "error",
      "warnAs": "warning"
    },
    "prePush": {
      "enabled": true,
      "coverage": { "minimum": 85 },
      "security": { "failOnCritical": true, "failOnHigh": false }
    },
    "postMerge": {
      "enabled": true,
      "branch": "main",
      "autoCreateIssue": true
    }
  }
}
```

## Dashboard de Quality Gates

O `/qualidade` command mostra o status de todos os gates por stack:

```
+--------------------------------------------------+
|           QUALITY GATES STATUS                  |
+--------------------------------------------------+
| Stack: .NET + Node (multi)                      |
|                                                  |
| Pre-Commit  OK 12/12 checks pass               |
| Pre-Build   OK  5/5 checks pass                |
| Pre-Push    WARN 4/5 (coverage 83% < 85%)      |
| Post-Merge  OK  6/6 checks pass                |
+--------------------------------------------------+
| Coverage: 83% (meta: 85%)                       |
| Security: 0 CVEs                                |
| Warnings: 0                                     |
| Self-Heals: 3 auto-fixed                        |
+--------------------------------------------------+
```

## Multi-stack

Quando o projeto tem mais de um stack (ex: Next.js frontend + Node backend, ou .NET API + React frontend):
- Rodar gates de TODOS os stacks detectados em sequencia
- Reportar resultado consolidado
- Bloquear se qualquer stack falhar

## Migracao de .NET-only

Projetos legados que usavam apenas `dotnet` commands:
- Atualizar `kilo.jsonc` para `"stack": "auto-detect"`
- Manter compatibilidade: se so ha `*.csproj`, ainda roda gates .NET
- Adicionar progressivamente outros stacks conforme o projeto cresce

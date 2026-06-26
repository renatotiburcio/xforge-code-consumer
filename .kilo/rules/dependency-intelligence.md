# Dependency Intelligence - XForge Engineer (Stack-Aware)

## Visao Geral

Monitoramento proativo de TODAS as dependencias do projeto, independente de stack. Detecta CVEs, atualizacoes, breaking changes, e incompatibilidades para .NET, Node, Python, Go, Rust, Java, e outros.

## Fontes de Dados (Stack-Aware)

### 1. .NET (NuGet)
```powershell
dotnet list package --vulnerable
dotnet list package --outdated
dotnet list package --include-transitive
```

### 2. Node / npm
```powershell
npm audit
npm audit --json
npm outdated
npm ls --depth=0
```

### 3. pnpm / Yarn (alternativas ao npm)
```powershell
pnpm audit
pnpm outdated
yarn audit
yarn outdated
```

### 4. Python (PyPI)
```powershell
pip-audit
pip list --outdated
safety check
```

### 5. Go (modules)
```powershell
govulncheck ./...
go list -u -m all
go mod tidy -v
```

### 6. Rust (Cargo)
```powershell
cargo audit
cargo outdated
```

### 7. Java / Kotlin (Maven / Gradle)
```powershell
mvn dependency-check:check
mvn versions:display-dependency-updates
./gradlew dependencyUpdates
```

### 8. Docker Images
```bash
docker scout cves <image>
trivy image <image>
grype <image>
```

### 9. GitHub Advisories
API do GitHub para CVEs em dependencias publicas (todos os stacks).

## Stack Detection (Antes de Monitorar)

```python
def detect_stack(project_root):
    signals = {
        "dotnet": ["*.csproj", "*.sln"],
        "node": ["package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"],
        "python": ["requirements.txt", "pyproject.toml", "Pipfile", "setup.py"],
        "go": ["go.mod", "go.sum"],
        "rust": ["Cargo.toml", "Cargo.lock"],
        "java-maven": ["pom.xml"],
        "java-gradle": ["build.gradle", "build.gradle.kts"],
        "ruby": ["Gemfile", "Gemfile.lock"],
        "php": ["composer.json", "composer.lock"],
        "elixir": ["mix.exs", "mix.lock"],
    }
    # Read all manifests and return list of detected stacks
```

## Monitoramento Automatico

### Frequencia de Verificacao (Stack-Aware)

| Tipo | Frequencia | Metodo (per stack) |
|------|-----------|--------------------|
| **CVEs criticos** | A cada build | stack-specific (abaixo) |
| **CVEs altos** | Diariamente | stack-specific + GitHub Advisory |
| **Atualizacoes** | Semanalmente | stack-specific outdated check |
| **Breaking changes** | Antes de atualizar | Analise de release notes |
| **Licencas** | A cada novo pacote | npm ls / pip-licenses / cargo tree |

### Comandos por Stack

#### .NET
```powershell
dotnet list package --vulnerable --include-transitive
dotnet list package --outdated
dotnet nuget locals all --list
```

#### Node
```powershell
npm audit --omit=dev --audit-level=critical
npm audit --audit-level=high
npm outdated
```

#### Python
```powershell
pip-audit --strict
pip list --outdated --format=json
```

#### Go
```powershell
govulncheck ./...
go list -u -m -mod=mod all
```

#### Rust
```powershell
cargo audit
cargo outdated --root-deps-only
```

## Regras de Alerta (todos os stacks)

### CVE Detection

| Severidade | Acao | Auto-fix |
|-----------|------|----------|
| **Critico** | Bloquear build + criar issue + notificar | Atualizar pacote |
| **Alto** | Warn + sugerir atualizacao | Sugerir atualizacao |
| **Medio** | Informar no relatorio | N/A |
| **Baixo** | Log silencioso | N/A |

### Update Detection

| Tipo de Atualizacao | Acao | Risco |
|---------------------|------|-------|
| **Patch** (1.0.x -> 1.0.y) | Sugerir atualizacao | Baixo |
| **Minor** (1.x -> 1.y) | Sugerir com cautela | Medio |
| **Major** (x -> y) | Alertar + analisar breaking changes | Alto |
| **Preview/RC** | NUNCA auto-atualizar | Critico |

## Pacotes Estaveis por Stack (lista de exemplos)

### .NET
- EF Core, Pomelo.EntityFrameworkCore.MySql, Swashbuckle, QuestPDF, OpenTelemetry, Serilog, XForge.MediatR, AutoMapper

### Node
- React, Next, Angular, Vue, Svelte, Express, Fastify, NestJS, Prisma, Drizzle, Zod, TypeScript, TanStack Query

### Python
- FastAPI, Django, Flask, SQLAlchemy, Pydantic, pytest, ruff, mypy, uvicorn, gunicorn

### Go
- gin, echo, fiber, chi, sqlc, pgx, testify, golangci-lint, viper

### Rust
- actix-web, axum, rocket, sqlx, diesel, tokio, serde

## Configuracao (Stack-Aware)

```json
{
  "dependencyIntelligence": {
    "enabled": true,
    "stack": "auto-detect",
    "nuget": {
      "checkVulnerabilities": true,
      "checkUpdates": true,
      "autoFixPatch": true,
      "autoFixMinor": false,
      "autoFixMajor": false,
      "neverUpdate": ["preview", "rc", "alpha", "beta"]
    },
    "npm": {
      "checkAudit": true,
      "checkUpdates": true,
      "autoFixPatch": true,
      "autoFixMinor": false
    },
    "pypi": {
      "checkAudit": true,
      "checkUpdates": true
    },
    "go": {
      "checkVuln": true,
      "checkUpdates": true
    },
    "cargo": {
      "checkAudit": true,
      "checkUpdates": true
    },
    "docker": {
      "checkCves": true,
      "baseImage": "auto-detect"
    },
    "alerting": {
      "criticalCve": ["create-issue", "block-build", "notify"],
      "highCve": ["warn", "suggest-update"],
      "outdated": ["weekly-report"]
    }
  }
}
```

## Relatorio Semanal (Multi-Stack)

```
+==================================================+
|        DEPENDENCY INTELLIGENCE REPORT            |
|             Semana de 09-15 Jun 2026             |
+==================================================+
|                                                  |
| SEGURANCA                                       |
|   CVEs criticos: 0  OK                        |
|   CVEs altos: 1  ATENCAO (.NET: System.Net.Http)|
|                                                  |
| ATUALIZACOES (por stack)                        |
|   .NET: 12 disponiveis                          |
|     Patch (seguro): 5  auto-atualizar          |
|     Minor: 4  revisar                          |
|     Major: 3  analisar breaking changes        |
|   Node: 8 disponiveis                           |
|     Patch: 3  auto-atualizar                   |
|     Minor: 5  revisar                          |
|   Python: 4 disponiveis                         |
|     Patch: 2  auto-atualizar                   |
|     Minor: 2  revisar                          |
|   Go: 6 disponiveis                              |
|   Rust: 3 disponiveis                            |
|                                                  |
| BREAKING CHANGES                                |
|   -> EF Core 10.0.1 -> 10.1.0 (API changes)    |
|   -> React 19 -> 20 (React Server Components)   |
|   -> FastAPI 0.110 -> 0.111 (Pydantic v2 strict) |
|                                                  |
| RESUMO                                          |
|   Total pacotes: 187                            |
|   Atualizados: 142 (76%)                        |
|   Desatualizados: 32 (17%)                      |
|   Vulneraveis: 1 (0.5%)                         |
+==================================================+
```

## Comandos

```
/dependencias verificar vulnerabilidades em todas as dependencias
/dependencias mostrar atualizacoes disponiveis
/dependencias atualizar pacotes patch (seguro)
/dependencias analisar breaking changes em [pacote]
/dependencias gerar relatorio de dependencias
```

## Integracao com Error Pattern Learning

Quando uma atualizacao causa erro, o sistema:

1. Registra o erro no `errors-solutions-graph.json` (stack-specific)
2. Conecta: `erro <-- dependencia <-- atualizacao <-- stack`
3. Na proxima vez que detectar a mesma atualizacao, alerta automaticamente
4. Cria regra de prevencao: "NUNCA atualizar [pacote] para [versao] em [stack] sem testes"

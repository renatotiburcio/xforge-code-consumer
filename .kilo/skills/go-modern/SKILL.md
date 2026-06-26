---
name: go-modern
description: Especialista em Go backend moderno (net/http + Gin/Echo/Fiber + sqlc/SQL + pgx + testify). Cobre API REST, gRPC, microservices, CLI, e deploy (Docker, single binary, Kubernetes). Use para qualquer projeto Go.
whenToUse: Use quando o usuario pedir "API Go", "backend Go", "microservico Go", "Gin API", "Echo API", "Fiber API", "gRPC Go", "CLI em Go", "worker Go". NAO use para .NET (use dotnet-standards), Node (use node-modern) ou Python (use python-modern).
---

# go-modern

## Filosofia

**Go = simplicidade radical, performance nativa, deploy trivial.** Compilado, estaticamente tipado, garbage-collected, excelente para sistemas distribuidos, CLI tools, e infraestrutura. Use para APIs de alta concorrencia, microservices, CLIs, infraestrutura.

## Stack Padrao (2026)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Versao | **Go 1.22+** | Generics, melhor performance, structured logging |
| HTTP | **net/http padrao** OU **Gin** OU **Echo** OU **Fiber** | Stdlib eh poderoso; frameworks para DX |
| Router | **chi** (lightweight) / **Gin** (popular) | Escolha conforme caso |
| DB | **pgx** (PostgreSQL) / **database/sql** (generico) | pgx eh o melhor driver para PostgreSQL |
| Query | **sqlc** (type-safe) / **sqlx** (flexivel) / **GORM** (ORM completo) | sqlc gera codigo type-safe |
| Validation | **go-playground/validator** (struct tags) | Padrao de mercado |
| Auth | **golang-jwt/jwt** / **oauth2** | JWT + OAuth |
| Logging | **log/slog** (stdlib Go 1.21+) / **zerolog** / **zap** | Estruturado, rapido |
| Config | **viper** / **envconfig** / **koanf** | Env vars + files |
| Testing | **testify** / **gomock** / **dockertest** | Padrao de mercado |
| Migrations | **golang-migrate** / **goose** / **atlas** | Versionamento de schema |
| Task Queue | **asynq** / **machinery** | Background jobs |
| gRPC | **google.golang.org/grpc** | Padrao |
| Lint | **golangci-lint** | All-in-one linter |
| Deploy | **Docker** (single binary), **Kubernetes**, **Fly.io**, **Railway** | Multi-target |

## Decisoes de Arquitetura

### 1. HTTP: stdlib vs Gin vs Echo vs Fiber
- **net/http padrao** (Go 1.22+ com ServeMux pattern matching): suficiente para 80% dos casos
- **Gin**: popular, middleware ecosystem, validator
- **Echo**: similar ao Gin, mais rapido em alguns benchmarks
- **Fiber**: API similar ao Express, baseado em fasthttp (nao net/http)
- **chi**: lightweight, stdlib-compatible
- **Recomendacao**: stdlib + chi para APIs; Gin se quiser middleware ecosystem

### 2. DB: sqlc vs sqlx vs GORM vs Ent
- **sqlc** (recomendado): gera codigo type-safe a partir de SQL
- **sqlx**: extensao leve do database/sql
- **GORM**: ORM completo, mas lento e magic
- **Ent**: graph-based, type-safe, complexo
- **Recomendacao**: sqlc para type-safety maxima; sqlx se preferir escrever SQL

### 3. Project Layout
- **Standard Go project layout** (`cmd/`, `internal/`, `pkg/`)
- **Flat** (todos arquivos no root, ok para apps < 20 arquivos)
- **Feature-based** (`internal/<feature>/`)

### 4. Error Handling
- **Sentinel errors** + `errors.Is`
- **Custom error types** + `errors.As`
- **Wrapped errors** com `fmt.Errorf("...: %w", err)`
- **Evite**: panic em libs, error strings sem contexto

### 5. Concurrency
- **Goroutines** para I/O paralelo
- **Channels** para comunicacao
- **errgroup** para coordenar goroutines
- **context.Context** para cancelamento e deadlines
- **sync.WaitGroup** para sincronizacao

### 6. Configuration
- **Env vars** (12-factor app)
- **Viper** se precisar de files + env vars + flags
- **envconfig** para tag-based env binding
- **Valide no startup** - falhe rapido se config invalida


## Estrutura de Pastas (Standard Go Layout + sqlc)

```
/
├── cmd/
│   └── api/
│       └── main.go              # Entry point
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── server/
│   │   ├── server.go            # HTTP server setup
│   │   ├── router.go            # Routes
│   │   └── middleware/
│   ├── handler/                 # HTTP handlers
│   │   ├── user.go
│   │   └── auth.go
│   ├── service/                 # Business logic
│   │   ├── user.go
│   │   └── auth.go
│   ├── repository/              # Data access
│   │   ├── user.go
│   │   └── auth.go
│   ├── model/                   # Domain models
│   │   ├── user.go
│   │   └── errors.go
│   ├── db/
│   │   ├── db.go                # pgx pool
│   │   └── queries/             # sqlc generated
│   └── auth/
│       └── jwt.go
├── pkg/                         # Public libraries (opcional)
├── migrations/                  # SQL migrations
│   └── 000001_init.up.sql
├── api/
│   └── openapi.yaml             # OpenAPI spec
├── scripts/
│   ├── dev.sh
│   └── migrate.sh
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── go.mod
├── go.sum
├── sqlc.yaml
├── .golangci.yml
└── README.md
```

## Setup Inicial

```bash
mkdir my-api && cd my-api
go mod init github.com/user/my-api
go get github.com/jackc/pgx/v5
go get github.com/jackc/pgx/v5/pgxpool
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest
go install github.com/golang-migrate/migrate/v4/cmd/migrate@latest
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

## Padroes Obrigatorios

- **Go 1.22+** (use generics quando fazem sentido)
- **gofmt** + **goimports** (obrigatorio)
- **golangci-lint** (lint all-in-one)
- **Errores wrapped** com `%w` para contexto
- **context.Context** como primeiro parametro em funcoes I/O
- **Structured logging** com `log/slog` ou zerolog
- **Repository pattern** ou **sqlc generated**
- **Graceful shutdown** (SIGTERM handler)
- **Health check** endpoint
- **Config validada no startup**
- **Tests**: table-driven, testify, cobertura > 80%
- **Race detector** em CI (`go test -race`)

## Anti-patterns

- `panic` em libs ou handlers (retorne error)
- Ignorar errors (`_, _ = someFunc()`)
- `init()` com logica complexa
- Variaveis globais mutaveis
- `interface{}` (use `any` em Go 1.18+)
- Mutex desnecessario (prefira channels ou sync.Map)
- `time.Sleep` em testes (use polling ou channels)
- SQL injection (use parametrized queries ou sqlc)
- Hardcoded secrets (use env vars)

## Exemplo: HTTP Handler + Service + sqlc

```go
// internal/handler/user.go
package handler

import (
    "encoding/json"
    "net/http"
    "github.com/go-chi/chi/v5"
    "github.com/user/my-api/internal/service"
)

type UserHandler struct {
    service *service.UserService
}

func NewUserHandler(s *service.UserService) *UserHandler {
    return &UserHandler{service: s}
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    user, err := h.service.GetByID(r.Context(), id)
    if err != nil {
        http.Error(w, err.Error(), http.StatusNotFound)
        return
    }
    json.NewEncoder(w).Encode(user)
}
```

## Validacao

```bash
go build ./...                    # Build
go test ./... -race -cover        # Tests com race detector + coverage
golangci-lint run                 # Lint
gofmt -l .                        # Format check
go vet ./...                      # Static analysis
govulncheck ./...                 # Vulnerabilidades
sqlc generate                     # Regenerate sqlc code
migrate up                        # Apply migrations
```

## Comandos

```
/criar-api API de gestao de usuarios com Go + Chi + sqlc + PostgreSQL
/criar-api microservico gRPC com Go
/criar-projeto CLI em Go com Cobra
/criar-projeto worker com Go + Asynq
```

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `go.mod` + `go.sum` com deps corretas
2. `cmd/api/main.go` (entry point com graceful shutdown)
3. `internal/config/config.go` (env-based config)
4. `internal/server/` (HTTP server + router + middleware)
5. `internal/handler/` (HTTP handlers)
6. `internal/service/` (business logic)
7. `internal/repository/` (data access)
8. `internal/db/` (pgx pool + sqlc generated)
9. `migrations/` (SQL files)
10. `Dockerfile` (multi-stage build)
11. `docker-compose.yml`
12. `Makefile` (build, test, run, migrate)
13. `.golangci.yml`
14. `sqlc.yaml`
15. `.env.example`
16. README com setup, env vars, scripts

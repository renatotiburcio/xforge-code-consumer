---
name: rust-modern
description: Especialista em Rust backend moderno (Axum/Actix-web + Tokio + sqlx/diesel + thiserror + tracing). Cobre API REST, gRPC, microservices, WebAssembly, CLI, sistemas embarcados, e deploy (Docker, single binary, serverless).
whenToUse: Use quando o usuario pedir "API Rust", "backend Rust", "Axum", "Actix-web", "microservico Rust", "CLI em Rust", "Rust com Tokio", "WebAssembly em Rust", "sistema embarcado Rust". NAO use para .NET, Node, Python, Go, ou Java.
---

# rust-modern

## Filosofia

**Rust = memory safety sem garbage collector, performance maxima, zero-cost abstractions.** Compilado, sem runtime, ideal para sistemas criticos, high-performance services, WebAssembly, e ferramentas de linha de comando. Use quando precisa de performance extrema ou memory safety garantida em tempo de compilacao.

## Stack Padrao (Rust 1.78+ / 2026)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Versao | **Rust 1.78+ (edition 2024)** | Performance, async melhorado |
| Async runtime | **Tokio** | Padrao de mercado |
| HTTP server | **Axum** (recomendado) / **Actix-web** / **Rocket** | Axum = ergonomia + Tokio |
| HTTP client | **reqwest** / **hyper** | reqwest = alto nivel, hyper = baixo nivel |
| Serializacao | **serde** + **serde_json** / **toml** / **bincode** | Essencial |
| DB | **sqlx** (async, compile-time checked) / **diesel** (sync) | sqlx eh o mais popular |
| Validation | **validator** (derive macros) / **garde** | Padrao |
| Auth | **jsonwebtoken** / **oauth2-rs** | JWT + OAuth |
| Logging | **tracing** + **tracing-subscriber** | Estruturado, async-aware |
| Config | **config** / **figment** / **dotenvy** | Env vars + files |
| Testing | **built-in** + **tokio-test** + **mockall** + **wiremock-rs** | Rust tem testing built-in |
| Lint/Format | **rustfmt** + **clippy** | Obrigatorio |
| Error handling | **thiserror** (libs) / **anyhow** (apps) | Padrao |
| Build | **Cargo** (built-in) | Workspaces para monorepo |
| Deploy | **Docker** (multi-stage), **single binary**, **Fly.io**, **AWS Lambda** | Multi-target |

## Decisoes de Arquitetura

### 1. Web Framework: Axum vs Actix-web vs Rocket
- **Axum** (recomendado 2026): feito pela equipe do Tokio, ergonomia excelente, modular
- **Actix-web**: mais rapido em benchmarks, actor model, menos idiomatic
- **Rocket**: muito ergonomico, mas tem seu proprio runtime (conflita com Tokio)
- **Warp**: minimalista, baseado em filtros
- **Salvo**: similar ao Axum, com mais baterias

### 2. Async vs Sync
- **Async (Tokio + Axum + sqlx)**: alta concorrencia, I/O-bound
- **Sync (Actix + diesel)**: quando precisa de latencia baixa e controle fino
- **Tokio** eh o runtime padrao (90% do ecossistema usa)

### 3. Error Handling
- **thiserror** (libs): derive Error, errors tipados
- **anyhow** (apps/bins): wrapping de errors, contexto
- **Evite**: `unwrap()` em libs, `panic!` em runtime
- **Result<T, E>**: sempre retorne Result, nao panic

### 4. State Management
- **Compartilhado imutavel**: `Arc<T>`
- **Compartilhado mutavel**: `Arc<Mutex<T>>` ou `Arc<RwLock<T>>` (Tokio versions para async)
- **Channels (mpsc, oneshot)**: para comunicacao entre tasks
- **Database pools (sqlx::Pool)**: para acesso concorrente a DB

### 5. API Style
- **REST + OpenAPI** (default): usar `utoipa` ou `aide` para OpenAPI
- **GraphQL**: `async-graphql`
- **gRPC**: `tonic`
- **tRPC-like**: nao ha equivalente direto; use REST + types


## Estrutura de Pastas (Axum + sqlx)

```
/
├── src/
│   ├── main.rs                  # Entry point (bin)
│   ├── lib.rs                   # Library root (opcional, para tests)
│   ├── config/
│   │   └── mod.rs               # Config loading
│   ├── routes/                  # HTTP handlers
│   │   ├── mod.rs
│   │   ├── users.rs
│   │   └── auth.rs
│   ├── handlers/                # Business logic handlers
│   │   ├── mod.rs
│   │   ├── user.rs
│   │   └── auth.rs
│   ├── models/                  # Domain types
│   │   ├── mod.rs
│   │   ├── user.rs
│   │   └── error.rs
│   ├── db/                      # Database access
│   │   ├── mod.rs
│   │   ├── pool.rs
│   │   └── queries.rs           # sqlx queries
│   ├── middleware/              # Axum middleware
│   │   ├── mod.rs
│   │   ├── auth.rs
│   │   └── logging.rs
│   ├── services/                # Business logic
│   │   ├── mod.rs
│   │   ├── user_service.rs
│   │   └── auth_service.rs
│   └── error.rs                 # Global error type
├── migrations/                  # sqlx migrations
│   └── 20260101000001_init.sql
├── tests/                       # Integration tests
│   ├── common/
│   ├── users.rs
│   └── auth.rs
├── .env.example
├── Cargo.toml
├── Cargo.lock
├── Dockerfile
├── docker-compose.yml
├── .rustfmt.toml
├── clippy.toml
├── sqlx.toml                    # sqlx offline mode
└── README.md
```

## Setup Inicial (Axum + sqlx)

```bash
cargo new my-api --bin
cd my-api
cargo add axum tokio --features full
cargo add tower-http --features cors,trace
cargo add sqlx --features runtime-tokio-rustls,postgres,uuid,chrono
cargo add serde --features derive
cargo add serde_json
cargo add thiserror
cargo add tracing tracing-subscriber
cargo add jsonwebtoken
cargo add argon2
cargo add validator --features derive
cargo install sqlx-cli --no-default-features --features rustls,postgres
sqlx database create
sqlx migrate add init
```

## Padroes Obrigatorios

- **Edition 2024** (ou 2021 minimo)
- **rustfmt** + **clippy** (obrigatorio)
- **`#![deny(unsafe_code)]`** em apps (libs podem ter unsafe documentado)
- **Errors tipados** com `thiserror` (lib) ou `anyhow` (bin)
- **Result<T, E>** sempre que pode falhar
- **Avoid `unwrap()` e `expect()`** em production code
- **Async com Tokio** (nao use actix-rt com Axum)
- **Tracing** para logging estruturado
- **Config validada no startup** (`config-rs` ou manual)
- **Graceful shutdown** (SIGTERM handler via tokio::signal)
- **Health check** endpoint
- **Connection pooling** (sqlx pool)
- **Tests**: unit + integration + doc tests
- **Property-based testing**: `proptest` ou `quickcheck`

## Anti-patterns

- `unwrap()` / `expect()` em codigo de producao
- `panic!` em runtime
- `unsafe` sem documentacao e `// SAFETY:` comment
- `Arc<Mutex<T>>` excessivo (use channels ou `Arc<T>` quando imutavel)
- `String` quando `&str` funciona
- `.clone()` excessivo (prefira borrowing)
- `Rc<T>` em async code (use `Arc<T>`)
- `lazy_static` (use `OnceCell` ou `std::sync::LazyLock`)
- Tokio current_thread runtime (use `#[tokio::main]` com `flavor = "multi_thread"`)
- Mixing de sync I/O em async tasks (block_in_place ou spawn_blocking)

## Exemplo: Axum Handler + Service + sqlx

```rust
// src/main.rs
use axum::{routing::get, Router};
use std::net::SocketAddr;
use tokio::net::TcpListener;
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

mod config;
mod db;
mod error;
mod handlers;
mod middleware;
mod models;
mod routes;
mod services;

use crate::config::Config;
use crate::db::Db;

#[derive(Clone)]
pub struct AppState {
    pub db: Db,
    pub config: Config,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::new(
            std::env::var("RUST_LOG").unwrap_or_else(|_| "info".into()),
        ))
        .with(tracing_subscriber::fmt::layer())
        .init();

    let config = Config::from_env()?;
    let db = Db::connect(&config.database_url).await?;

    let state = AppState { db, config };

    let app = Router::new()
        .route("/health", get(handlers::health))
        .nest("/api/v1", routes::users::router())
        .nest("/api/v1", routes::auth::router())
        .layer(TraceLayer::new_for_http())
        .layer(middleware::auth::layer())
        .with_state(state);

    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    let listener = TcpListener::bind(addr).await?;
    tracing::info!("listening on {}", addr);

    axum::serve(listener, app).with_graceful_shutdown(shutdown_signal()).await?;
    Ok(())
}
```

## Validacao

```bash
cargo build --release                 # Build
cargo test                            # Tests
cargo clippy -- -D warnings           # Lint
cargo fmt --check                     # Format check
cargo audit                           # Vulnerabilidades
sqlx migrate run                      # Apply migrations
```

## Comandos

```
/criar-api API de gestao de usuarios com Rust + Axum + sqlx + PostgreSQL
/criar-api microservico Rust com Tokio + gRPC
/criar-projeto CLI em Rust com clap
/criar-projeto app WebAssembly com Yew + Rust
```

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `Cargo.toml` com deps corretas
2. `src/main.rs` (entry point com graceful shutdown)
3. `src/config.rs` (env-based config)
4. `src/routes/` (HTTP routers)
5. `src/handlers/` (request handlers)
6. `src/services/` (business logic)
7. `src/models/` (domain types com serde derives)
8. `src/db/` (sqlx pool + queries)
9. `src/middleware/` (auth, logging, etc.)
10. `src/error.rs` (global error type com thiserror)
11. `migrations/` (sqlx SQL files)
12. `tests/` (integration tests)
13. `Dockerfile` (multi-stage build)
14. `.env.example`
15. README com setup, env vars, scripts

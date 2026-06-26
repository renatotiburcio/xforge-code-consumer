---
name: python-modern
description: Especialista em Python backend moderno (FastAPI + SQLAlchemy 2.0 + Pydantic + JWT + pytest). Cobre API REST, GraphQL, async, microservices, ML serving, data pipelines, e deploy (Docker, uvicorn, gunicorn, serverless).
whenToUse: Use quando o usuario pedir "API Python", "backend Python", "FastAPI", "Flask", "Django", "API com Pydantic", "microservico Python", "ML serving", "data pipeline Python". NAO use para .NET (use dotnet-standards) ou Node (use node-modern).
---

# python-modern

## Filosofia

**Python = o backend mais produtivo.** Sintaxe clara, ecossistema vasto (FastAPI, Django, ML libs), async nativo, type hints modernos. Use para APIs REST, ML serving, data engineering, scripts, automation.

## Stack Padrao (2026)

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Runtime | **Python 3.12+** | Performance, type hints modernos |
| Framework | **FastAPI** (default) / **Django** (full-featured) / **Flask** (minimal) | Escolha conforme caso |
| Validacao | **Pydantic v2** | Type-safe, rapido, oficial |
| ORM | **SQLAlchemy 2.0+** / **SQLModel** / **Django ORM** | SQLAlchemy 2.0 eh o mais type-safe |
| Migrations | **Alembic** (SQLAlchemy) / **Django migrations** | Versionamento de schema |
| Auth | **python-jose** / **PyJWT** / **Authlib** | JWT + OAuth |
| OpenAPI | **Nativo do FastAPI** / **drf-spectacular** (Django) | Doc automatica |
| Async | **asyncio + uvicorn** | FastAPI + SQLAlchemy async |
| Tests | **pytest + pytest-asyncio + httpx** | Unit + integration |
| Lint/Format | **ruff** (rapido) + **mypy** (type check) | Substituiu flake8/black/isort |
| Logging | **structlog** / **loguru** | Estruturado |
| Task Queue | **Celery** / **ARQ** / **Dramatiq** | Background jobs |
| Deploy | **Docker**, **uvicorn**, **gunicorn**, **Fly.io**, **Railway**, **AWS Lambda** | Multi-target |

## Decisoes de Arquitetura

### 1. Framework: FastAPI vs Django vs Flask
- **FastAPI** (recomendado 2026): async nativo, Pydantic, OpenAPI automatico, type-safe
- **Django** (full-featured): admin, ORM, auth, templates, ideal para apps completos
- **Django REST Framework** (DRF): para API em Django
- **Flask** (minimal): apps pequenos, maximo controle, sem opiniao
- **Starlette**: ASGI puro, base do FastAPI

### 2. ORM: SQLAlchemy 2.0 vs SQLModel vs Django ORM
- **SQLAlchemy 2.0+** (recomendado): type-safe, async, maduro
- **SQLModel** (FastAPI-friendly): combina Pydantic + SQLAlchemy
- **Django ORM**: integrado ao Django, opinionated
- **Tortoise ORM**: async-first, similar ao Django ORM
- **Piccolo**: async, type-safe

### 3. Sync vs Async
- **Async (FastAPI + SQLAlchemy async)**: alta concorrencia, I/O-bound
- **Sync (Django/Flask)**: simplicidade, apps CRUD tradicionais
- **Use async** para APIs de alta concorrencia, **sync** para apps CRUD simples

### 4. Type Hints
- **Obrigatorio em APIs modernas**: mypy strict
- **Pydantic models** para request/response
- **Type hints** em todas funcoes publicas

### 5. Dependency Injection
- **FastAPI Depends()** (recomendado)
- **Pinject** / **dependency-injector**: para DI complexa
- **Manual**: funcoes que retornam instancias

### 6. API Style
- **REST + OpenAPI** (default)
- **GraphQL**: Strawberry, Graphene
- **gRPC**: grpcio + grpcio-tools


## Estrutura de Pastas (FastAPI + SQLAlchemy 2.0)

```
/
├── src/
│   ├── app/
│   │   ├── main.py              # FastAPI app factory
│   │   ├── config.py            # Pydantic Settings
│   │   ├── database.py          # SQLAlchemy engine + session
│   │   ├── dependencies.py      # FastAPI dependencies
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── users.py     # Routes
│   │   │       ├── auth.py
│   │   │       └── items.py
│   │   ├── core/
│   │   │   ├── security.py      # JWT, password hashing
│   │   │   ├── config.py
│   │   │   └── exceptions.py
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   └── item.py
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── user.py
│   │   │   └── item.py
│   │   ├── services/            # Business logic
│   │   │   ├── user_service.py
│   │   │   └── item_service.py
│   │   ├── repositories/        # Data access
│   │   │   ├── user_repo.py
│   │   │   └── item_repo.py
│   │   └── middleware/
│   ├── alembic/                 # Migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── unit/
│   │   └── integration/
│   └── alembic.ini
├── .env.example
├── pyproject.toml               # Poetry/uv
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── README.md
└── .python-version
```

## Setup Inicial (FastAPI + uv)

```bash
# Criar projeto com uv (recomendado) ou Poetry
uv init my-api
cd my-api
uv add fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg alembic pydantic pydantic-settings
uv add python-jose[cryptography] passlib[bcrypt] python-multipart
uv add --dev pytest pytest-asyncio pytest-cov httpx ruff mypy
```

## Padroes Obrigatorios

- **Type hints** em todas funcoes publicas
- **Pydantic v2** para schemas (request/response/config)
- **Repository pattern** para acesso a dados
- **Service layer** para logica de negocio
- **Dependency injection** via FastAPI Depends
- **Async I/O** quando possivel
- **Alembic** para migrations
- **Settings** via pydantic-settings
- **Structured logging** (structlog/loguru)
- **Error handling centralizado** (exception handlers)
- **OpenAPI** automatico
- **Testes**: unit + integration
- **mypy --strict** em CI

## Anti-patterns

- Falta de type hints
- `print()` em producao (use logger)
- SQL injection (use ORM ou queries parametrizadas)
- `try/except: pass` (sempre log ou re-raise)
- Mutacao de parametros (use dataclasses ou Pydantic)
- Hardcoded secrets (use env vars + pydantic-settings)
- `from foo import *`
- `__init__.py` com logica
- Circular imports
- Blocking I/O em async functions

## Exemplo: FastAPI + SQLAlchemy 2.0 async

```python
# src/app/models/user.py
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

# src/app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = {"from_attributes": True}

# src/app/api/v1/users.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await service.create(payload)
```

## Validacao

```bash
ruff check .           # Lint
ruff format .          # Format
mypy --strict .        # Type check
pytest                 # Tests
pytest --cov=.         # Coverage
pip-audit              # Vulnerabilidades
```

## Comandos

```
/criar-api API de gestao de usuarios com FastAPI + JWT + PostgreSQL
/criar-api microservico com FastAPI + SQLAlchemy async + Alembic
/criar-projeto app Django com DRF para blog
/criar-projeto ML serving API com FastAPI
```

## Output Esperado

Ao usar este skill, o agente deve produzir:

1. `pyproject.toml` com deps corretas
2. `.python-version` (3.12+)
3. `src/app/main.py` (FastAPI app)
4. `src/app/config.py` (Pydantic Settings)
5. Models em `src/app/models/`
6. Schemas Pydantic em `src/app/schemas/`
7. Services em `src/app/services/`
8. Repositorios em `src/app/repositories/`
9. Routes em `src/app/api/v1/`
10. Migrations em `alembic/versions/`
11. Tests em `src/tests/`
12. Dockerfile + docker-compose.yml
13. `.env.example`
14. README com setup, env vars, scripts

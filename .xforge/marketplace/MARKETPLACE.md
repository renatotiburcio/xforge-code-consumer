# XForge Enterprise — Kilo Marketplace

## Overview

XForge Enterprise is a complete development operating system for Kilo-powered projects. It provides 36 AI agents, 132 specialized skills, a RAG knowledge base, and multi-provider AI routing — all configured out of the box.

## Quick Start

```powershell
# 1. Clone the template
git clone https://github.com/xforge-development/xforge-template my-project
cd my-project

# 2. Run bootstrap
powershell -File .xforge/scripts/init-template.ps1 -ProjectName my-project

# 3. Install git hooks
powershell -File .githooks/install.ps1

# 4. Validate
powershell -File .kilo/automation/scripts/doctor.ps1
```

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| Agents | 36 | 20 primary + 16 subagent with YAML frontmatter |
| Skills | 132 | Agent Skills format (SKILL.md) |
| Commands | 194 | Portuguese interface with examples |
| Workflows | 163 | Command-integrated workflows |
| MCP Servers | 3 | PostgreSQL, Redis, RabbitMQ |
| RAG Docs | 786 | Knowledge base with 1,859 chunks |
| CI/CD | 1 | GitHub Actions workflow |
| Git Hooks | 2 | Pre-commit (doctor), pre-push (RAG health) |

## Architecture

```
.kilo/   = Operational layer (replaceable, version-controlled)
.xforge/ = Persistent layer (project knowledge, NEVER delete)
```

## Key Commands

- `/xforge` — Intelligent routing for any request
- `/desenvolver` — Feature development
- `/qualidade` — Quality verification
- `/seguranca` — Security analysis
- `/conhecimento` — Knowledge base management
- `/memoria` — Project memory and decisions
- `/documentacao` — Documentation generation
- `/release` — Release preparation
- `/provider` — AI model switching
- `/buscar` — Web + local search

## Validation

```powershell
# Doctor (full validation)
powershell -File .kilo/automation/scripts/doctor.ps1

# Privacy scan
powershell -File .xforge/scripts/verify-privacy.ps1

# RAG tests
python -m pytest tests/rag -v
```

Expected: **0 errors, 0 warnings, 14/14 tests passing**

## License

MIT

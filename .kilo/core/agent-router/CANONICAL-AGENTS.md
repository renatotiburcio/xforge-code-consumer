# Canonical Agents

This is the official agent facade for XForge on KiloCode.

The existing `.kilo/agents` files remain available. These canonical agents define the primary routing vocabulary so the IA and KiloCode choose fewer, clearer paths.

## Agents

| Canonical agent | Use for | Existing agents to route through |
| --- | --- | --- |
| `chief-architect` | Intent classification, orchestration, risk, final decision | `chief-architect-orchestrator` |
| `project-recognition` | Recognize project structure, architecture, risks and project DNA | `project-recognition-engineer` |
| `feature-engineer` | Features, APIs, CRUDs, components and implementation | `development-feature-engineer` |
| `dotnet-architect` | .NET architecture, endpoints, CQRS, DTOs and packages | `dotnet-architecture-director`, `director-architecture` |
| `frontend-ux` | Blazor, Tailwind, UX/UI and design system | `frontend-designsystem-director` |
| `data-engineer` | Database, EF Core, PostgreSQL, MySQL, performance and integrity | `data-platform-director` |
| `quality-engineer` | Tests, coverage, quality gates and release quality | `quality-engineering-director`, `quality-gates-engineer`, `director-quality` |
| `security-governance` | Security, LGPD, RBAC, policies and human review | `director-governance`, `specialist-rbac`, `specialist-policy-engine` |
| `memory-curator` | Memory retrieval, update, conflict, TTL and knowledge promotion | `manager-memory`, `memory-curator-engineer`, `specialist-knowledge-curation` |
| `documentation-engineer` | Manuals, docs HTML, changelog and training docs | `documentation-director`, `training-academy-director` |
| `legacy-modernizer` | Legacy analysis, reverse engineering and migration | `legacy-knowledge-curator`, `specialist-reverse-engineering` |
| `release-manager` | Release readiness, rollback, notes and final audit | `github-devops-director`, `quality-engineering-director`, `director-governance` |

## Routing Rule

1. Start with `chief-architect` unless the public command clearly maps to a more specific canonical agent.
2. Use one primary canonical agent.
3. Add at most three supporting agents for complex work.
4. Select skills after choosing the primary agent.
5. Do not expose internal agent names to the user unless useful for transparency.


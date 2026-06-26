---
name: plantuml-mcp
description: PlantUML MCP integration (DR-0201) - UML/C4 diagrams (class, sequence, component, deployment) via plantuml-mcp-server. Complements Mermaid MCP (v50.17.0).
applicabilityScope: ["*"]
version: 1.0.0
created: 2026-06-22
---

# PlantUML MCP Integration (DR-0201)

## What it is
The PlantUML MCP Integration (DR-0201) wraps `plantuml-mcp-server` (Infobip official) as a **native MCP** in XForge. It exposes 3 tools for PlantUML diagram generation + encoding/decoding, plus a prompt for auto-fix error handling. PlantUML specializes in UML (class, sequence, component, deployment) and C4 architecture diagrams.

Native MCPs in XForge cannot be installed or uninstalled - only **enabled/disabled** via `kilo.jsonc` `mcp.<name>.enabled`. Optional MCPs use the full lifecycle via `/mcp-lifecycle` command.

**Complementary to Mermaid MCP** (v50.17.0):
- PlantUML: C4 architecture, class/sequence/component UML, enterprise diagrams
- Mermaid: flowcharts, gantt, journey, simpler diagrams

## When to use
- When you need C4 architecture diagrams (Context, Container, Component, Code).
- When you need detailed UML (class diagrams, sequence diagrams with notes/groups).
- When you need Component/Deployment diagrams.
- When you need PlantUML-specific features (`!include` directives, external libraries).
- DO NOT use for simple flowcharts (use Mermaid MCP instead).
- DO NOT use for diagrams with sensitive/private content (default uses public server).

## How to use
1. Default: uses public `https://www.plantuml.com/plantuml` server
2. Optional: set `PLANTUML_SERVER_URL` for self-hosted
3. Enable in `kilo.jsonc` -> `mcp.plantuml.enabled = true`
4. Restart MCP host

## Parameters
| Parameter | Type | Default | Description | Required? |
|-----------|------|---------|-------------|-----------|
| `PLANTUML_SERVER_URL` | env var | `https://www.plantuml.com/plantuml` | PlantUML server URL | No |
| `PLANTUML_ALLOWED_DIRS` | env var | CWD only | Colon-separated dirs for `output_path` | No |
| `mcp.plantuml.enabled` | bool | `false` | Toggle the MCP at host level | No |
| Format | enum | `svg` | `svg`, `png`, `base64` | No |
| `output_path` | string | (none) | Local file to save diagram (must be in `PLANTUML_ALLOWED_DIRS`) | No |

## Examples

### Example 1: Generate C4 diagram
```
[Agent] Create C4 container diagram for this project
[MCP] generate_plantuml_diagram(format='svg')
  PlantUML: !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
  Person(user, "User")
  System(system, "System")
  Rel(user, system, "Uses")
[Output] SVG URL + base64
```

### Example 2: Sequence diagram
```
[Agent] Create sequence diagram for OAuth2 flow
[MCP] generate_plantuml_diagram(format='svg')
  PlantUML:
  @startuml
  actor User
  participant Browser
  participant AuthServer
  User -> Browser: click login
  Browser -> AuthServer: GET /authorize
  ...
[Output] SVG diagram
```

### Example 3: Class diagram
```
[Agent] Show class hierarchy for User entity
[MCP] generate_plantuml_diagram(format='png')
  PlantUML:
  @startuml
  class User {
    +id: UUID
    +name: String
    +email: String
  }
  class Admin extends User
  ...
[Output] PNG diagram
```

### Example 4: Save locally
```
[Agent] Save diagram to ./docs/diagrams/auth-flow.svg
[MCP] generate_plantuml_diagram(format='svg', output_path='./docs/diagrams/auth-flow.svg')
```

### Example 5: Self-hosted for private diagrams
```bash
# 1. Run PlantUML server locally
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
# 2. Set env
export PLANTUML_SERVER_URL=http://localhost:8080
# 3. Enable in kilo.jsonc -> mcp.plantuml.enabled = true
```

### Example 6: Disable when offline / not needed
```jsonc
// kilo.jsonc -> mcp.plantuml.enabled = false
"mcp": {
  "plantuml": { "enabled": false }
}
```

## Troubleshooting

### [SKIP] npx not in PATH
- Install Node.js 18+

### [FAIL] PlantUML server unreachable
- **Cause**: `PLANTUML_SERVER_URL` wrong or internet down
- **Fix**: Check URL; use self-hosted for offline

### [FAIL] output_path rejected
- **Cause**: path not in `PLANTUML_ALLOWED_DIRS`
- **Fix**: Add dir to `PLANTUML_ALLOWED_DIRS` env var (colon-separated)

### Diagram has syntax errors
- Use `plantuml_error_handling` prompt (auto-fix workflow)
- Or validate at https://www.plantuml.com/plantuml/uml/

## Related
- DR-0201 (this integration)
- DR-0200 Mermaid MCP (complementary, different syntax)
- XForge: `mermaid-diagrams` skill, `architecture-enterprise-expert` skill, `diagram-quality-rules`
- Other NATIVE MCPs: github, filesystem, context7, playwright, dbhub, firecrawl, mermaid
- Self-hosted PlantUML: https://github.com/plantuml/plantuml-server (Docker)
# XForge Code AI — Extensibilidade

## Visão Geral

O sistema de extensibilidade do XForge Code AI é inspirado no Kilo Code (skills), Cline (SDK programático), e Goose (custom distributions), mas com um sistema de plugins mais avançado.

## Componentes

```mermaid
graph TD
    subgraph Skills
        SK[Skill System\nCarregáveis]
        SKT[Skill Templates]
        SKM[Skill Marketplace]
    end
    subgraph Plugins
        PL[Plugin System\nUser-defined]
        PLT[Plugin Tools]
        PLH[Plugin Hooks]
    end
    subgraph MCP
        MCP[MCP Servers\n70+ servidores]
        MCPT[MCP Tools]
    end
    subgraph Templates
        TM[Project Templates]
        TMC[Custom Templates]
    end
    SK --> PL
    PL --> MCP
    TM --> SK
```

## 1. Skills System

### Estrutura de uma Skill

```
skills/
  code-generation/
    SKILL.md          # Instruções da skill
    templates/        # Templates de código
    examples/         # Exemplos
  genius-council/
    SKILL.md
    agents/           # Definições de agentes
    validators/       # Scripts de validação
```

### Registro

```typescript
const skill = await skillManager.register({
  name: "code-generation",
  description: "Use when writing, editing, or creating code files",
  path: "./skills/code-generation",
  triggers: ["write code", "create file", "edit file"]
});
```

### Carregamento

- **Metadata** sempre no system prompt (< 500 chars)
- **Body completo** carregado apenas quando skill é invocada
- **Cache** de skills carregadas

## 2. Plugin System

### Interface

```typescript
interface Plugin {
  name: string;
  version: string;
  tools?: Tool[];
  hooks?: Hook[];
  settings?: Setting[];
}
```

### Hooks

| Hook | Quando | Ação |
|------|--------|------|
| `pre-commit` | Antes de commit | Validações |
| `post-merge` | Após merge | Notificações |
| `on-error` | Quando erro ocorre | Error handling |
| `on-save` | Quando arquivo é salvo | Format/lint |

### Exemplo

```typescript
const myPlugin: Plugin = {
  name: "my-deploy",
  version: "1.0.0",
  tools: [deployTool],
  hooks: [
    { event: "pre-commit", handler: validateDeploy }
  ]
};
```

## 3. MCP (Model Context Protocol)

- 70+ servidores MCP suportados
- User-defined servidores
- Tool discovery automático
- Sandbox obrigatório para tools que executam código

## 4. Project Templates

### Templates Incluídos

| Template | Stack | Descrição |
|----------|-------|-----------|
| `dotnet-api` | .NET 10 | API REST com Clean Architecture |
| `node-api` | Node.js + TypeScript | API com Express/Fastify |
| `python-api` | Python | API com FastAPI |
| `go-api` | Go | API com Gin/Echo |
| `rust-api` | Rust | API com Axum/Actix |
| `react-spa` | React + Vite | SPA com Tailwind |
| `next-fullstack` | Next.js 14 | Fullstack com App Router |

### Custom Templates

```typescript
await templateManager.register({
  name: "my-enterprise",
  path: "./templates/my-enterprise",
  variables: ["projectName", "database", "auth"]
});
```

## 5. Marketplace (Futuro)

### Funcionalidades
- Publicar skills
- Publicar plugins
- Publicar templates
- Ratings e reviews
- Verificação de segurança

### Roadmap
- Fase 1: Skills marketplace (local)
- Fase 2: Plugins marketplace
- Fase 3: Community marketplace

## Critérios de Aceite

- [ ] Skills são carregáveis dinamicamente
- [ ] Plugins podem registrar tools e hooks
- [ ] MCP servers são gerenciados
- [ ] Templates funcionam para todos os stacks
- [ ] Marketplace (futuro) está planejado

## Prioridade: P1

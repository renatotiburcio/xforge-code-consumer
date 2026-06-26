# Guia de Conhecimento XForge

## 1. O Que é Conhecimento

Conhecimento é conteúdo **reutilizável e explicativo**. Responde "como fazer" e "por quê". É diferente de memória (que é fato específico do projeto) e de regra (que é restrição obrigatória).

**Conhecimento** = "Como configurar EF Core com PostgreSQL" (reutilizável)
**Memória** = "Nosso projeto usa PostgreSQL 16" (específico)
**Regra** = "Nunca colocar connection string hardcoded" (obrigatório)

---

## 2. Estrutura de Conhecimento

```
.xforge/knowledge/
├── index.json                    — Manifest de conhecimento
├── packs/                        — Knowledge packs por domínio técnico
│   ├── knowledge-pack-dotnet/
│   ├── knowledge-pack-efcore/
│   ├── knowledge-pack-blazor/
│   └── ...
├── dotnet/                       — Conhecimento específico do projeto (dotnet)
├── postgresql/                   — Conhecimento específico do projeto (postgresql)
└── ...
```

---

## 3. Knowledge Packs

Knowledge packs são coleções de conhecimento por domínio técnico. Cada pack contém:

| Arquivo | Conteúdo |
|---------|----------|
| `knowledge.md` | Conhecimento principal — visão geral, padrões, boas práticas |
| `rules.md` | Regras específicas do domínio |
| `edge-cases.md` | Casos extremos e como lidar com eles |
| `pitfalls.md` | Armadilhas comuns e como evitá-las |
| `sources.json` | Fontes oficiais referenciadas |

### Packs Existentes

| Pack | Domínio |
|------|---------|
| `knowledge-pack-accounting` | Contabilidade |
| `knowledge-pack-benchmarkdotnet` | BenchmarkDotNet |
| `knowledge-pack-blazor` | Blazor |
| `knowledge-pack-commercial` | Comercial |
| `knowledge-pack-dotnet` | .NET |
| `knowledge-pack-efcore` | EF Core |
| `knowledge-pack-esocial` | eSocial |
| `knowledge-pack-mysql` | MySQL |
| `knowledge-pack-nbomber` | NBomber |
| `knowledge-pack-nfe` | NFe |
| `knowledge-pack-openfinance` | Open Finance |
| `knowledge-pack-pomelo` | Pomelo |
| `knowledge-pack-postgresql` | PostgreSQL |
| `knowledge-pack-sped` | SPED |
| `knowledge-pack-stryker-dotnet` | Stryker.NET |
| `knowledge-pack-tailwind` | Tailwind CSS |
| `knowledge-pack-testcontainers` | Testcontainers |

---

## 4. Como Criar Conhecimento

### 4.1 Estrutura de Arquivo

```markdown
# [Título do Conhecimento]

## Fonte
[URL oficial ou referência primária]

## Versão da fonte
[Versão da documentação usada, se aplicável]

## Quando usar
[Em que situações este conhecimento se aplica]

## Regras
- Regra 1
- Regra 2
- Regra 3

## Exemplos

### Exemplo 1: [Nome]
```csharp
// Código de exemplo
```

### Exemplo 2: [Nome]
```csharp
// Código de exemplo
```

## Edge Cases
- [Caso extremo 1]: [Como lidar]
- [Caso extremo 2]: [Como lidar]

## Pitfalls
- ❌ **Errado:** [O que não fazer]
- ✅ **Certo:** [O que fazer]

## Referências
- [Documentação oficial](url)
- [Guia de migração](url)
- [Best practices](url)
```

### 4.2 Fontes Oficiais Prioritárias

| Domínio | Fonte Oficial |
|---------|---------------|
| .NET | https://learn.microsoft.com/dotnet/ |
| EF Core | https://learn.microsoft.com/ef/core/ |
| ASP.NET Core | https://learn.microsoft.com/aspnet/core/ |
| Blazor | https://learn.microsoft.com/aspnet/core/blazor/ |
| PostgreSQL | https://www.postgresql.org/docs/ |
| MySQL | https://dev.mysql.com/doc/ |
| Tailwind CSS | https://tailwindcss.com/docs |
| Docker | https://docs.docker.com/ |
| GitHub Actions | https://docs.github.com/actions |

---

## 5. Como Consultar Conhecimento

### Via RAG

```powershell
# Busca geral
.\.kilo\automation\scripts\rag\query-local.ps1 -Query "ef core migrations" -Top 5

# Busca filtrada por knowledge
.\.kilo\automation\scripts\rag\query-local.ps1 -Query "ef core migrations" -Top 5 -SourceType knowledge

# Busca por commands
.\.kilo\automation\scripts\rag\query-local.ps1 -Query "criar migration" -Top 5 -SourceType commands
```

### Via Arquivo

Navegue diretamente em `.xforge/knowledge/` ou `.xforge/knowledge/packs/`.

---

## 6. Ciclo de Vida do Conhecimento

```
draft → validated → promoted → deprecated → archived
```

- **draft** — criado mas não revisado
- **validated** — revisado e confirmado
- **promoted** — conhecimento ativo e referenciado
- **deprecated** — desatualizado, será substituído
- **archived** — não mais relevante, mantido para histórico

---

## 7. Governança

Veja `.xforge/engineer/knowledge-governance/KNOWLEDGE-GOVERNANCE.md` para detalhes sobre:
- Estados de conhecimento
- Papéis (Curator, Reviewer, Approver)
- Pipeline de promoção
- Critérios de rejeição

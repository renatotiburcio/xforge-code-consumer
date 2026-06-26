---
id: release-immutability
priority: high
applicabilityScope: ["*"]
status: approved
version: 1.0.0
created: 2026-06-21
updated: 2026-06-21
related-rules: [01-xforge-golden-rules, 02-genius-council-framework, session-memory, curation-rules]
related-dr: [DR-0087, DR-0180]
---

# Release Immutability Rule (DR-0087 + DR-0180)

> **Precedencia**: amplica process simplification. Decisoes e artefatos de releases passadas sao IMUTAVEIS por default. Excluir `apps/` ou `samples/` NAO reescreve o historico.

## 1. Mandato

Tres categorias de arquivos sao **append-only / imutaveis** apos publicacao:

1. **CHANGELOG.md** - entradas de releases passadas NAO sao reescritas mesmo que artefatos referenciados deixem de existir
2. **DRs (Decision Records) antigos** - toda DR com status `approved` ou `deprecated` e imutavel; substituicoes exigem **nova DR** que referencie a anterior
3. **archive/** - decisoes arquivadas sao preservadas para audit; NAO sao apagadas, NAO sao reescritas

## 2. Por que existe

- Reescrever CHANGELOG de releases passadas **falsifica historico** e quebra confianca em auditoria
- Reescrever DRs aprovados **apaga raciocinio** que levou aquela decisao; pode invalidar dependencias que outros lugares assumem
- Substituir `apps/sales-erp` por `src/sales-erp` em CHANGELOG de 2026-06-19 (release v3.27) e' anacronismo: naquele momento, apps/ era o caminho canonico

## 3. O que E imutavel

| Categoria | Caminho | Imutavel? | Excecao |
|----------|---------|-----------|---------|
| CHANGELOG releases passadas | `CHANGELOG.md` (linhas de releases approved) | **SIM** | apenas adicionar nova entrada no topo (Unreleased) |
| DRs approved | `.xforge/decisions/DR-NNNN-*.md` (status `approved`) | **SIM** | criar nova DR de revisao |
| DRs deprecated | `.xforge/decisions/DR-NNNN-*.md` (status `deprecated`) | **SIM** | idem |
| archive/ | `.xforge/decisions/archive/*` | **SIM** | nunca |
| Releases notes | `RELEASE_NOTES.md` (legado) | **SIM** | idem CHANGELOG |

## 4. O que NAO E imutavel

| Categoria | Caminho | Por que mutavel |
|----------|---------|----------------|
| DRs em rascunho | `.xforge/decisions/DR-NNNN-*.md` (status `draft` ou `review`) | ainda em debate |
| Codigo | `.kilo/`, `*.ps1`, `*.py`, `*.cs` | artefatos sao refatoraveis |
| Knowledge | `.xforge/knowledge/*` | TTL + revalidation |
| Skills/Agents/Commands | `.kilo/{skills,agents,commands}/*` | iteracao continua |
| Docs ativos | `docs/getting-started.md`, `docs/index.html`, `docs/manual/*` | reflete estado atual |
| Scripts | `.xforge/scripts/*` | corrigiveis |

## 5. Politica de correcao de referencias obsoletas

Quando uma referencia em CHANGELOG/DR/archive aponta para algo que foi removido ou renomeado:

**Errado** (viola regra):
```powershell
# Apaga apps/ e depois reescreve CHANGELOG v3.27 trocando apps/sales-erp por src/sales-erp
```

**Correto**:
```powershell
# Mantem CHANGELOG v3.27 intacto
# Adiciona nova entrada no topo:
## [Unreleased] - Cleanup
### Changed
- Removidos apps/ e samples/ (eram gitignored, ver DR-0121)
- Migradas referencias ativas para src/ (em codigo, scripts, docs ativos)
### Notes
- CHANGELOG releases passadas mantem referencias originais (imutabilidade)
```

## 6. Quando NAO aplicar

- **Bug fix de codigo** - reescrever codigo buggy e' OK
- **Skill/agent obsolete** - substituir por versao melhor e' OK
- **Knowledge expired** - mover para archive/ e revalidar

## 7. Enforcement

| Momento | Verificacao |
|---------|-------------|
| Pre-commit | `git diff` em CHANGELOG.md nao deve alterar linhas fora do Unreleased |
| Pre-commit | `git diff` em DRs approved nao deve ocorrer (exceto `draft`/`review`) |
| Code review | Diff de CHANGELOG/DR/archive sinalizado como warning |

## 8. Referencias

- DR-0087 - Process Simplification v3.10.0 (template 3 fases, releases imutaveis)
- DR-0121 - Template-only split (apps/ e samples/ gitignored)
- DR-0180 - Stack-Aware Context + Memory Namespace (este principio)
- Regra `curation-rules.md` - curadoria de memoria (compressao, dedup, archive)
- Skill `wizard-engine/SKILL.md` - preservacao de contexto historico

## 9. TL;DR

| Acao | CHANGELOG | DRs approved | archive/ | Codigo | Docs ativos |
|------|-----------|--------------|----------|--------|-------------|
| Reescrever | NAO | NAO | NAO | SIM | SIM |
| Adicionar entrada | SIM (topo) | NAO (criar nova) | NAO | SIM | SIM |
| Mover/apagar | NAO | NAO | NAO | SIM | SIM |
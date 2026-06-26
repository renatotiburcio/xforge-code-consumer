---
id: temp-files-organization
priority: high
applicabilityScope: ["*"]
status: approved
version: 1.0.0
created: 2026-06-22
updated: 2026-06-22
related-rules: [01-xforge-golden-rules, 02-genius-council-framework, manual-sync-rules]
related-dr: [DR-0208]
---

# Temp Files Organization Rule (DR-0208)

> **Mandato**: Root do projeto deve conter APENAS arquivos canonicos. Tudo que e temporario, descartavel ou de debug DEVE ficar em `temp/`, NUNCA solto no root.

## 1. Problema

Ao longo do tempo, o root do projeto XForge acumulou ~15 scripts `.py` soltos (`categorize.py`, `generate_*.py`, `rewrite_*.py`, etc), alem de relatorios visuais, backups antigos, e diretorios `.opencode/` (48 MB de node_modules de ferramenta externa nao relacionada). Isso torna o root sujo, dificulta onboarding, e confunde sobre o que e canonico vs descartavel.

## 2. Regra de Ouro

```
    ╔══════════════════════════════════════════════════════════════╗
║  ROOT E PARA ARTEFATOS CANONICOS DO PROJETO.                ║
║  TUDO QUE E TEMPORARIO / DEBUG / DESCARTAVEL DEVE FICAR    ║
║  EM /temp/ OU DENTRO DE .kilo/ / .xforge/ (NUNCA SOLTO).   ║
╚══════════════════════════════════════════════════════════════╝
```

## 3. O que PODE ficar no root

Apenas artefatos canonicos do template/projeto:

| Categoria | Exemplos | Por que fica no root |
|---|---|---|
| Git config | `.gitignore`, `.gitattributes`, `.kilocodeignore` | git espera no root |
| Documentos canonicos | `README.md`, `CHANGELOG.md`, `AGENTS.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `STATUS.md` | entry points oficiais |
| Config do projeto | `kilo.jsonc`, `.coveragerc`, `docker-compose.yml`, `playwright.config.ts` | referenciados por tooling |
| Diretorios canonicos | `.kilo/`, `.xforge/`, `docs/`, `scripts/`, `tests/`, `.githooks/`, `.github/`, `.vscode/` | template core |

## 4. O que NAO pode ficar no root

| Item | Destino correto | Exemplo |
|---|---|---|
| Scripts `.py` de scaffolding/regen | `scripts/manual_gen/` | `generate_*.py`, `rewrite_*.py`, `split_*.py` |
| Scripts de debug/POC | `/temp/` ou `/scratch/` | `poc_*.py`, `debug_*.py`, `test_*.py` |
| Relatorios visuais | regenerados a cada run, em `/reports/` (gitignored) | screenshots dark mode, audit full |
| Backups antigos | `.xforge-backups/` (gitignored) | `purify-2026*.tar.gz` |
| node_modules | dentro do diretorio do package | `.opencode/node_modules/` |
| Diretorios de ferramentas externas nao usadas | deletar fisicamente | `.opencode/`, `.aider/`, etc |

## 5. Workflow obrigatorio para novos scripts

### 5.1 Script canonico (sera mantido no repo)

1. Criar em local canonico desde o inicio:
   - `scripts/manual_gen/<name>.py` (se for regen/scaffolding)
   - `.xforge/scripts/<name>.ps1` (se for automation)
   - `.kilo/automation/scripts/<name>.ps1` (se for tooling do kilo)
2. Adicionar DR referenciando
3. Adicionar tests se aplicavel
4. Atualizar `kilo.jsonc` se for command/agent/skill/MCP

### 5.2 Script temporario (vive so durante a sessao)

1. Criar em `/temp/<purpose>.py` ou `/scratch/<purpose>.py`
2. `/temp/` ja esta gitignored
3. Quando terminar: deletar (NAO comitar)

### 5.3 Debug / investigacao

1. Criar em `/temp/debug-<issue>.py`
2. Adicionar logs em `.xforge/audit/` se preciso (gitignored)
3. Deletar apos conclusao

## 6. Enforcement

| Momento | Verificacao | Ferramenta |
|---------|-------------|------------|
| Pre-commit | doctor.ps1 valida que root so tem 14 arquivos canonicos | doctor.ps1 Gate 6 |
| Pre-commit | `.gitignore` tem `/temp/`, `/scratch/`, `/debug_*.py`, `/poc_*.py` | doctor.ps1 Gate 6 |
| Manual review | Diff de working tree NAO deve adicionar arquivos `.py` soltos em root | code review |
| Doctor weekly | Scan for `/[a-z]*.py` em root, warn se aparecer | doctor.ps1 Gate 6 |

## 7. Anti-patterns

| Anti-pattern | Por que falha | Solucao |
|--------------|--------------|---------|
| `python p1.py` no root | vira lixo em 1 sessao | mover para `scripts/manual_gen/` ou `/temp/` |
| Criar `test_foo.py` no root | confunde com pytest suite | usar `/temp/test_foo.py` ou `tests/` se for canonico |
| Gerar PNGs no `reports/` direto | acumula lixo no repo | gitignored, regenerar quando precisar |
| Commitar `.opencode/` ou `.aider/` | sao ferramentas externas, nao parte do template | gitignored |

## 8. Lista canonica do root (DR-0208)

Apos DR-0208, o root DEVE conter exatamente estes 14 arquivos:

```
.coveragerc
.gitattributes
.gitignore
.kilocodeignore
AGENTS.md
ARCHITECTURE.md
CHANGELOG.md
CLAUDE.md
README.md
STATUS.md
docker-compose.yml
kilo.jsonc
playwright.config.ts
```

Mais 9 diretorios canonicos:

```
.githooks/  .github/  .kilo/  .vscode/  .xforge/
docs/  scripts/  tests/  temp/    (opcional)
```

## 9. Quando criar /temp/

- Quando o usuario pedir "testa isso rapido"
- Quando precisar de POC antes de virar canonico
- Quando estiver debugando um issue com arquivos descartaveis
- Quando o doctor reclamar de root sujo

**Nunca** criar arquivos de script solto no root. Use `/temp/` desde o inicio.


## 11. Template Mode vs Consumer Mode (DR-0211)

O sistema XForge tem dois modos distintos:

### Template Mode
- Voce esta no repo XForge-Development-New e quer evoluir o template
- .git remote aponta para o origin do template
- Use git pull/push normalmente

### Consumer Mode
- Voce clonou o template para criar um projeto
- Use .xforge/scripts/init-project.ps1 para separar do template
- O script remove .git, cria novo repo, purifica memory

### Regra
- Nunca faca git push em um consumer sem antes rodar init-project.ps1
- Sempre use init-project.ps1 ao clonar para um novo projeto

Ver: DR-0211, .xforge/template-only.json (secao modes)
## 10. Referencias

- DR-0208 (este design)
- DR-0190 (fix dos scripts `.py` originais, parente deste)
- DR-0192 (anti-fractal: 1 DR = 1 release, 1 cleanup = 1 cleanup)
- DR-0202 (DR-0202 housekeeping)
- Regra `01-xforge-golden-rules.md` (SRP, organization)
- Regra `02-genius-council-framework.md` (qualquer decisao passa pelo conselho)
- Skill `code-generation` (sempre usar tools, NUNCA output no chat)


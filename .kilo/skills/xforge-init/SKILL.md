---
name: xforge-init
description: Golden Command - inicializa e valida TODO o sistema XForge compativel com Kilo Code CLI 1.0. Detecta modelos Ollama, valida kilo.jsonc contra schema oficial (https://app.kilo.ai/config.json), valida knowledge, scripts, rules e manual. Nao fixa modelos - adapta ao que esta instalado.
---

# xforge-init (Kilo Code CLI 1.0 Compatible)

## Objetivo
Validar TODO o sistema XForge e mostrar status. Detecta automaticamente os modelos Ollama disponiveis. Compatibiliza com Kilo Code CLI 1.0 (release v7.3.46, 2026-06-15).

## Schema Oficial
- **Documentacao:** https://kilo.ai/docs/customize
- **Schema URL:** `https://app.kilo.ai/config.json`
- **Top-level keys reconhecidas (CLI 1.0):**
  `$schema`, `model`, `provider`, `permission`, `formatter`, `lsp`,
  `experimental`, `disabled_providers`, `enabled_providers`,
  `tools`, `mcp`, `agent`, `instructions`, `skills`, `tui`, `remote_control`
- **Built-in agents:** `code`, `plan`, `ask`, `debug`, `review`, `explore`, `general`

## Regra Fundamental

**NAO fixar modelos no config.** O usuario seleciona o modelo no momento do prompt. O sistema detecta e adapta.

Para providers, use a sintaxe `provider.<id>.options.<key>` com `{env:VAR}` para chaves:

```jsonc
{
  "$schema": "https://app.kilo.ai/config.json",
  "model": "anthropic/claude-sonnet-4-20250514",
  "provider": {
    "openrouter": {
      "options": {
        "apiKey": "{env:OPENROUTER_API_KEY}"
      }
    },
    "ollama": {
      "options": {
        "baseURL": "http://localhost:11434/v1"
      }
    }
  },
  "permission": {
    "*": "ask",
    "bash": "allow"
  }
}
```

## Procedimento

### Passo 1: Doctor
```powershell
.\.kilo\automation\scripts\doctor.ps1
```
Validacoes:
- kilo.jsonc nao tem chaves nao reconhecidas (allowlist = 15 chaves CLI 1.0)
- kilo.jsonc tem `instructions` (array)
- Nenhum typo comum: `connectionTyle`, `connectionType`, `connec_tion_type`, etc.
- docs/index.html existe
- .kilo/commands, .kilo/agents, .kilo/skills, .kilo/rules presentes

### Passo 2: Ollama (Deteccao Automatica)
```powershell
try { $r = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 5; $r.models | ForEach-Object { "$($_.name) ($([Math]::Round($_.size/1GB, 1))GB)" } } catch { "Offline" }
```
Mostrar: modelos instalados e capacidades detectadas.

### Passo 3: Kilo Provider Config
- `provider.openrouter.options.apiKey` referencia `{env:OPENROUTER_API_KEY}`
- `provider.anthropic.options.apiKey` referencia `{env:ANTHROPIC_API_KEY}`
- `provider.ollama.options.baseURL` aponta para `http://localhost:11434/v1`
- **PROIBIDO:** API keys inline (vaza LGPD/GDPR).

### Passo 4: Knowledge
- `.xforge/knowledge/INDEX.json` existe
- Knowledge files >= 170
- `errors-solutions-graph.json` existe

#
## Passo 6: Modo de Operacao (Consumer vs Template)

O xforge-init tem dois modos:

### Modo Consumer (padrao - sem flag)
Quando o usuario roda /xforge-init sem flags:
1. Validar que esta no template (.xforge/template-only.json existe)
2. Copiar paths user-facing do template-only.json
3. Remover paths template-only (DR-0211)
4. Atualizar .gitignore
5. Purificar memory com stack detectada
6. Remover .git, git init novo, commit inicial
7. Mostrar proximos passos

**Script:** .xforge/scripts/init-project.ps1 -TargetDir <dir> -Stack <stack>"
    "
    
Quando o usuario passa /xforge-init --template:
- Roda doctor, Ollama, knowledge, scripts, rules, manual, validation
- Mostra score de prontidao
- NAO modifica nada (apenas valida)

## Passo 5: Scripts (modo template)
Verificar scripts principais existem.

### Passo 6: Rules
.kilo/rules/ com >= 28 arquivos .md

### Passo 7: Manual
- docs/index.html existe (landing page)
- docs/SUMMARY.md existe (indice canonico)
## Passo 5: Scripts
Verificar scripts principais existem.

### Passo 6: Rules
`.kilo/rules/` com >= 28 arquivos .md

### Passo 7: Manual
- `docs/index.html` existe (landing page)
- `docs/SUMMARY.md` existe (indice canonico)

### Passo 8: Knowledge Validation
```powershell
.\.kilo\automation\scripts\knowledge-validation.ps1
```

### Passo 9: Score
`score = (checks_passing / 9) * 100`

## Saida Esperada
```
[1/9] OK  Doctor - 24 OK, 0 errors
[2/9] OK  Ollama - 4 modelos (Embeddings, Large models)
[3/9] OK  Provider Config - {env:VAR} templating, no inline secrets
[4/9] OK  Knowledge - 173 files + INDEX
[5/9] OK  Scripts - 7 scripts
[6/9] OK  Rules - 30 rules
[7/9] OK  Manual - 209 paginas + index.html
[8/9] OK  Validation - 6 areas
[9/9] OK  Score - 100%
```

## Troubleshooting

### `unrecognized key(s) in object: ''connectionTyle"`
Esta chave NAO EXISTE no schema CLI 1.0. Causa provavel:
- Auto-migracao de `.kilocodemodes` legacy (anterior a v7.0)
- Cache de validacao Zod da extensao antiga
- Edicao manual corrompida

**Fix:**
1. Abrir `kilo.jsonc` e remover qualquer chave similar a `connectionTyle`/`connectionType`
2. Reiniciar a extensao Kilo Code
3. Rodar `.\.kilo\automation\scripts\doctor.ps1` para validar
4. Se persistir: `Remove-Item "$env:USERPROFILE\.kilocode\cache" -Recurse -Force` (Windows)

### `$schema` rejeitado pelo doctor
Era um bug em versoes anteriores. v3.3.0+ aceita `$schema` como chave valida.

## Se Modelo Especifico Necessario
Se uma tarefa precisa de modelo grande (ex: 70B+), o agente deve:
1. Detectar capacidade do modelo atual
2. Se insuficiente, pedir ao usuario para selecionar modelo maior
3. Usar o modelo selecionado para a tarefa

## Uso
```
Use the xforge-init skill
```



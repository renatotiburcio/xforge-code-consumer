# Matriz de Compatibilidade VS Code

**Data**: 2026-06-25
**Versao**: 1.0.0
**Referencia**: referencia/vscode/ (VS Code 1.127.0 Code-OSS)

---

## 1. APIs VS Code Utilizadas (Kilo Code Extension)

### 1.1 APIs Estaveis

| API | Uso no Kilo Code | Compativel? |
|---|---|---|
| `vscode.workspace.getConfiguration()` | Leitura de settings `kilo-code.new.*` | 100% |
| `vscode.commands.registerCommand()` | Registro de 9 comandos | 100% |
| `vscode.window.createOutputChannel()` | Output channel "XForge" | 100% |
| `vscode.window.showInformationMessage()` | Notificacoes | 100% |
| `vscode.window.showInputBox() | Input de usuario | 100% |
| `vscode.window.showErrorMessage()` | Erros | 100% |
| `vscode.window.showWarningMessage() | Warnings | 100% |

### 1.2 Extension Contribution Points

| Contribution Point | Uso | Compativel? |
|---|---|---|
| `contributes.commands` | 9 comandos | OK |
| `contributes.configuration` | 4 propriedades `xforge.*` | OK |

### 1.3 APIs NAO Utilizadas (Oportunidades)

| API | Descricao | Oportunidade |
|---|---|---|
| `vscode.languages.registerCompletionProvider()` | IntelliSense | Adicionar autocomplete XForge |
| `vscode.languages.registerHoverProvider()` | Hover info | Documentacao inline |
| `vscode.languages.registerCodeActionsProvider()` | Code actions | Quick fixes |
| `vscode.languages.registerDefinitionProvider()` | Go to definition | Navegacao |
| `vscode.languages.registerDocumentSymbolProvider()` | Symbols outline | Outline view |
| `vscode.languages.registerReferenceProvider()` | Find references | Refactoring |
| `vscode.debug.registerDebugAdapterDescriptorFactory()` | Debug adapters | Debug agent |
| `vscode.scm.registerSourceControl()` | SCM provider | Agent versioning |
| `vscode.tasks.registerTaskProvider()` | Tasks | Agent tasks |
| `vscode.terminal.registerTerminalProfileProvider()` | Terminal profiles | Agent terminal |
| `vscode.testController` | Test runner | Agent testing |
| `vscode.chatParticipant` | Chat participant | AI chat integration |
| `vscode.languageModelAccess` | LLM access | Built-in LLM support |
| `vscode.mcpServerDefinitionProvider()` | MCP servers | External tools |

### 1.4 Proposed APIs (Disponiveis no VS Code 1.127.0)

| Proposed API | Status | Relevancia |
|---|---|---|
| `vscode.agentSessionsWorkspace` | Proposed | ALTO — Agent session management |
| `vscode.chatProvider` | Proposed | ALTO — Chat participant |
| `vscode.languageModel*` | Proposed | ALTO — LLM access |
| `vscode.mcpServerDefinitions` | Proposed | ALTO — MCP tool integration |
| `vscode.mcpToolDefinitions` | Proposed | ALTO — MCP tools |
| `vscode.scmMultiDiffEditor` | Proposed | MEDIO — Git diffs |
| `vscode.editSessionIdentityProvider` | Proposed | MEDIO — Edit sessions |
| `vscode.contributedEdito` | Proposed | BAIXO |

---

## 2. Compatibilidade por Subsistema VS Code

### 2.1 Editor

| Subsistema | Kilo Code usa? | XForge Code precisa? | Status |
|---|---|---|---|
| TextDocument API | N/A (CLI) | N/A | OK |
| Editor decorations | N/A | N/A | OK |
| Inlay hints | N/A | N/A | OK |

### 2.2 Workbench

| Subsistema | Kilo Code usa? | XForge Code precisa? | Status |
|---|---|---|---|
| Sidebar (Webview) | Sim (SolidJS) | Sim | OK |
| StatusBar | Nao | Opcional | GAP |
| Notifications | Sim | Sim | OK |
| InputBox | Sim | Sim | OK |
| TreeView | Nao | Opcional | GAP |
| Custom Editors | Nao | Opcional | GAP |

### 2.3 Platform

| Subsistema | Kilo Code usa? | XForge Code precisa? | Status |
|---|---|---|---|
| Configuration | Sim (`xforge.*`) | Sim (`xforge-code.*`) | MIGRATE |
| Commands | Sim (9 cmds) | Sim (~20 cmds) | EXTEND |
| Keybindings | Nao | Opcional | GAP |
| Menus | Nao | Opcional | GAP |
| Context keys | Nao | Sim | IMPLEMENT |
| Storage (globalState) | Nao | Sim | IMPLEMENT |
| Secrets | Nao | Opcional | GAP |

### 2.4 Extension Host

| Aspecto | Status | Notas |
|---|---|---|
| Activation events | `workspaceContains:.xforge` | OK |
| Extension dependencies | `kilocode.kilo-code` | REVERT |
| Trust mode support | N/A | ADD |
| Virtual workspace support | N/A | ADD |
| Process isolation | N/A | ADD |

---

## 3. Gap Analysis Detalhado

### 3.1 Competivel (nao precisa mudanca)

- `vscode.window` APIs (messages, input, output channel)
- `vscode.commands` registration
- `vscode.workspace` configuration
- `vscode.Uri` handling (se implementado)

### 3.2 Parcialmente Compativel (precisa ajuste)

| Item | Ajuste necessario |
|---|---|
| Extension dependency | Remover dependencia `kilocode.kilo-code` |
| Command prefix | Trocar `kilo-code.new.*` para `xforge-code.new.*` |
| Configuration namespace | Trocar `kilocode.kilo-code` storage path for `xforge-code` |
| GlobalStorage path | Migrar dados do usuario |
| Environment variables | Trocar `KILOCODE_*` para `XFORGE_CODE_*` |

### 3.3 Nao Compativel (precisa implementar)

| Item | Esforco | Prioridade |
|---|---|---|
| Language Provider (completion, hover, definition) | Alto | MEDIO |
| Code Actions Provider | Medio | BAIXO |
| Debug Adapter | Alto | BAIXO |
| SCM Provider | Alto | BAIXO |
| Test Controller | Medio | BAIXO |
| Chat Participant | Alto | ALTO |
| MCP Server Provider | Medio | ALTO |
| Settings migration script | Medio | ALTO |
| Welcome/onboarding flow | Medio | MEDIO |

---

## 4. Compatibilidade com VS Code Proposed APIs

O VS Code 1.127.0 (referencia/) ja inclui propostas diretamente relevantes:

| API | Descricao |
|---|---|
| `vscode.chatProvider` | Permite registro de chat AI participant |
| `vscode.languageModel*` | Acesso direto a LLMs via VS Code |
| `vscode.mcpServerDefinitions` | Registro de MCP servers |
| `vscode.agentSessionsWorkspace` | Agent session management integrado |
| `vscode.sessions` | Session state persistence |

**Implicacao**: XForge Code pode usar APIs nativas do VS Code para chat, agents, ao inves de propria implementacao.

---

## 5. Recomendacoes de Compatibilidade

### 5.1 Minimo para Funcionar

1. Trocar extension ID de `kilocode.kilo-code` para `xforge-code.xforge-code`
2. Trocar `extensionDependencies: ["kilocode.kilo-code"]` para `[]` (standalone)
3. Migrar configuracao de `kilo-code.new.*` para `xforge-code.new.*`
4. Migrar globalStorage path (migration script)
5. Trocar env vars `KILOCODE_*` para `XFORGE_CODE_*`

### 5.2 Para Compatibilidade Enterprise

1. Todas as acima +
2. Adicionar `capabilities.virtualWorkspaces: true`
3. Adicionar `capabilities.untrustedWorkspaces: false`
4. Adicionar `activationEvents: ["*"]` (sempre ativo)
5. Adicionar `extensionKind: ["workspace"]`
6. Adicionar support para proposed APIs

### 5.3 Para Experiencia Premium

1. Todas as acima +
2. `vscode.mcpServerDefinitions` para tool integration
3. `vscode.languageModel*` para LLM integrado
4. `vscode.chatParticipant` para chat panel
5. Settings migration via `vscode.workspace.onDidChangeConfiguration`

---

## 6. Risco de Breaking Changes

| Change | Impacto | Migracao |
|---|---|---|
| Extension ID | USUARIOS perdem settings | Migration script |
| Command prefix | Keybindings quebrados | Warning + legacy alias 30d |
| Config namespace | Settings perdidos | Auto-migration |
| GlobalStorage path | Dados perdidos | Migration script |
| Extension dependency | Extensao para de funcionar | Remover dependencia |
| Environment variables | Deploy quebra | Dual-env 90 days |
| HTTP headers | API communication quebra | Dual-header 90 days |

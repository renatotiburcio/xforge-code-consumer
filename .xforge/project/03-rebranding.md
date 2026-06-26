# Plano de Rebranding

**Data**: 2026-06-25
**Versao**: 1.0.0
**Status**: Draft

---

## 1. Identidade de Marca

### 1.1 De → Para

| Elemento | De | Para |
|---|---|---|
| Nome do produto | Kilo Code | XForge Code |
| Extensão curta | `kilo-code` | `xforge-code` |
| CLI binary | `kilo` | `xforge-code` (ou `xf`) |
| npm scope | `@kilocode/*` | `@xforge-code/*` |
| VS Code publisher | `kilocode` | `xforge-code` |
| Extension ID | `kilocode.kilo-code` | `xforge-code.xforge-code` |
| GitHub org | `Kilo-Org` | `xforge-code` |
| Dominio | `kilo.ai` | `xforge.code` (proposto) |
| Headers HTTP | `X-KILOCODE-*` | `X-XFORGE-CODE-*` |
| Env vars | `KILOCODE_*` | `XFORGE_CODE_*` |
| Settings namespace | `kilo-code.new.*` | `xforge-code.new.*` |
| Command prefix | `kilo-code.new.*` | `xforge-code.*` |
| Kotlin namespace | `ai.kilocode` | `ai.xforge.code` |

### 1.2 Branding Guidelines

**Logo**: Utilizar `implement/logo/XForge All.svg` como logo primario.

**Cores**:
- Primaria: `#1C2B40` (dark navy, do logo XForge)
- Secundaria: Branco `#FFFFFF`
- Accent: Extrair do SVG

**Tipografia**: 
- Headers: System font (VS Code default)
- Code: Monospace (VS Code editor font)

**Tom de voz**: Enterprise, premium, mas acessivel.

---

## 2. Substituicoes String (UI Visivel)

### 2.1 Strings Atuais → Novas

| Atual (source) | Novo (target) |
|---|---|
| "Add to Kilo Code" | "Add to XForge Code" |
| "Fix with Kilo Code" | "Fix with XForge Code" |
| "Explain with Kilo Code" | "Explain with XForge Code" |
| "Improve with Kilo Code" | "Improve with XForge Code" |
| "Kilo Code: AI Coding Agent..." | "XForge Code: Enterprise AI Coding Agent..." |
| "Kilo Code CLI" | "XForge Code CLI" |
| "Kilo Code" (generico) | "XForge Code" |
| "kilo.ai" | "xforge.code" |
| `npm install -g @kilocode/cli` | `npm install -g @xforge-code/cli` |
| `kilocode.kilo-code` (extension ID) | `xforge-code.xforge-code` |

### 2.2 Arquivos de Origem

| Arquivo | Tipo de string | Quantidade estimada |
|---|---|---|
| `src/packages/kilo-vscode/src/services/code-actions/code-action-provider.ts` | UI label | 4 ocorrencias |
| `src/packages/opencode/src/session/prompt/*.txt` | System prompt | 4 arquivos |
| `src/packages/opencode/src/cli/cmd/tui/components/error-component.tsx` | Error message | 1 ocorrencia |
| `src/packages/opencode/src/cli/cmd/uninstall.ts` | CLI message | 4 ocorrencias |
| `src/packages/opencode/README.md` | Documentacao | 5+ ocorrencias |
| `packages/kilo-vscode/package.json` | Display name | 1 ocorrencia |
| `packages/kilo-vscode/package.json` | Marketplace URL | 1 ocorrencia |
| All `src/README.*.md` (20+ languages) | Marketplace link | 20+ arquivos |

---

## 3. Identidade Visual

### 3.1 Ativos Existentes

| Ativo | Local | Status |
|---|---|---|
| `XForge All.svg` | `implement/logo/` | Logo vetorial, 16x16 viewBox |
| `XForge All.png` | `implement/logo/` | Logo raster |
| `XForge-All.icns` | `implement/logo/` | macOS iconset |
| `logo-outline-black.png` | `src/packages/kilo-vscode/assets/icons/` | Extension icon (Kilo) |
| `kilo-light.png` | `src/packages/kilo-vscode/assets/icons/` | Activity bar light |
| `kilo-dark.png` | `src/packages/kilo-vscode/assets/icons/` | Activity bar dark |
| `kilo-light.svg` | `src/packages/kilo-vscode/assets/icons/` | Command icon light |
| `kilo-dark.svg` | `src/packages/kilo-vscode/assets/icons/` | Command icon dark |
| `kilo-icon-font.woff2` | `src/packages/kilo-vscode/assets/icons/` | Custom icon font |
| `favicon.ico` | `src/packages/ui/src/assets/favicon/` | Favicon UI |
| `favicon-v3.ico` | `src/packages/ui/src/assets/favicon/` | Favicon v3 |
| `social-share.png` | `src/packages/ui/src/assets/images/` | OG social |

### 3.2 Necessario Criar

| Ativo | Local | Descricao |
|---|---|---|
| `xforge-code-icon.png` | `packages/kilo-vscode/assets/icons/` | 128x128 extension icon |
| `xforge-code-light.png` | `packages/kilo-vscode/assets/icons/` | Activity bar light |
| `xforge-code-dark.png` | `packages/kilo-vscode/assets/icons/` | Activity bar dark |
| `xforge-logo.png` | Root `assets/` | Logo 512x512 |
| `xforge-logo.svg` | Root `assets/` | Logo vetorial |
| `xforge-logo-mono.svg` | Root `assets/` | Logo monocromatico |
| `favicon-xforge.ico` | `packages/ui/src/assets/favicon/` | Novo favicon |
| `social-share-xforge.png` | `packages/ui/src/assets/images/` | Novo OG social |

---

## 4. Mudancas por Arquivo/Pacote

### 4.1 vs Code Extension (packages/kilo-vscode/)

| Arquivo | Mudancas |
|---|---|
| `package.json` | name, displayName, publisher, description, icon, activationEvents |
| `src/extension.ts` | Comandos, configuracao, strings |
| `src/services/code-actions/*.ts` | UI labels |
| `src/services/autocomplete/*.ts` | Prefix |
| `src/services/agent-manager/*.ts` | Brand strings |
| `src/services/settings*.ts` | Config namespace |
| `src/services/server-manager.ts` | Server identification |
| `webview-ui/src/**` | UI brand strings |
| `assets/icons/*` | Novo logo |
| `locale/*` | i18n strings |
| `tests/**/*.test.ts` | Assertions, test data |

### 4.2 CLI (packages/opencode/)

| Arquivo | Mudancas |
|---|---|
| `package.json` | name, bin name, description |
| `bin/kilo` | Shebang reference, binary name |
| `src/index.ts` | CLI name |
| `src/cli/cmd/**` | Command help text, error messages |
| `src/session/prompt/*.txt` | System prompts |
| `src/kilocode/installation/**` | Install/uninstall text |
| `script/build.ts` | Build target names |
| `script/postinstall.mjs` | npm package reference |

### 4.3 JetBrains Plugin (packages/kilo-jetbrains/)

| Arquivo | Mudancas |
|---|---|
| `package.json` | name, description |
| `shared/src/main/kotlin/ai/kilocode/**` | Package rename, class names, string literals |
| `src/main/resources/` | Plugin description, vendor name |

### 4.4 Shared Packages

| Pacote | Arquivos-chave |
|---|---|
| `kilo-gateway/` | `src/api/constants.ts` (headers), `src/auth/**` |
| `kilo-i18n/` | 16 `messages.ts` locale files |
| `kilo-ui/` | `src/components/**` brand strings |
| `kilo-docs/` | `pages/index.tsx`, `markdoc/partials/*.md` |
| `kilo-console/` | `public/index.html` brand strings |
| `kilo-telemetry/` | Telemetry event names |

### 4.5 Template (root)

| Arquivo | Mudancas |
|---|---|
| `.xforge/vscode-extension/package.json` | All brand strings |
| `.xforge/vscode-extension/extension.js` | All `XForge:` string literals |
| `.xforge/config/*.json` | Name, description |
| `.xforge/version.json` | Name |
| `docs/manual/*.html` | All 12+ pages |
| `docs/SUMMARY.md` | Brand strings |
| `AGENTS.md` | Brand strings |
| `CLAUDE.md` | Brand strings |
| `ARCHITECTURE.md` | Brand strings |
| `README.md` | Brand strings |
| `CHANGELOG.md` | Brand strings |

---

## 5. Abordagem de Migracao de Settings (User Data)

### 5.1 Settings Migration Strategy

```typescript
// Em extension.ts ao ativar:
async function migrateSettings() {
  const oldConfig = vscode.workspace.getConfiguration('kilo-code.new');
  const newConfig = vscode.workspace.getConfiguration('xforge-code.new');
  
  // Para cada setting existente:
  const keys = Object.keys(oldConfig);
  for (const key of keys) {
    const oldValue = oldConfig.get(key);
    if (oldValue !== undefined && newConfig.get(key) === undefined) {
      await newConfig.update(key, oldValue, vscode.ConfigurationTarget.Global);
    }
  }
  
  vscode.window.showInformationMessage(
    'XForge Code: Settings migrated from Kilo Code. Old settings preserved for 30 days.'
  );
}
```

### 5.2 GlobalStorage Migration

```typescript
async function migrateGlobalStorage(context: vscode.ExtensionContext) {
  const oldPath = path.join(context.extensionPath, '..', '..', 
    'User/globalStorage/kilocode.kilo-code');
  const newPath = path.join(context.extensionPath, '..', '..', 
    'User/globalStorage/xforge-code.xforge-code');
  
  if (fs.existsSync(oldPath) && !fs.existsSync(newPath)) {
    fs.cpSync(oldPath, newPath, { recursive: true });
  }
}
```

---

## 6. Abordagem de Depreciacao

### 6.1 Marketplace

- **Day 0**: Publish como NOVO extension (nao update do Kilo Code)
- **Day 7**: Adicionar notice no Kilo Code marketplace: "Migrated to XForge Code"
- **Day 30**: Depreciar Kilo Code (somente security fixes)
- **Day 90**: Descontinuar

### 6.2 npm

- **Day 0**: Publicar novos pacotes `@xforge-code/*`
- **Day 7**: Adicionar deprecation notice nos pacotes `@kilocode/*`
- **Day 30**: Manter apenas security fixes
- **Day 90**: Descontinuar (npm deprecate)

### 6.3 GitHub

- **Day 0**: Criar novo repositorio `xforge-code/xforge-code`
- **Day 7**: Archivar Kilo-Org/kilocode
- **Day 30**: Manter mirrors para referencia

---

## 7. Checklist de Rebranding

### Source Code
- [ ] `package.json` (root + 22 packages)
- [ ] `tsconfig.json` paths
- [ ] Build scripts
- [ ] CI/CD workflows
- [ ] Source imports
- [ ] Environment variables
- [ ] HTTP headers
- [ ] CLI binary name

### User Interface
- [ ] Extension display name
- [ ] Extension icon
- [ ] Activity bar icon
- [ ] Status bar items
- [ ] Code action labels
- [ ] Notification messages
- [ ] Error messages
- [ ] Settings UI

### Branding
- [ ] Logo primario
- [ ] Logo monocromatico
- [ ] Favicon set
- [ ] Social share image
- [ ] Splash screen (se aplicavel)
- [ ] About dialog (se aplicavel)

### Documentation
- [ ] Root README.md
- [ ] CHANGELOG.md
- [ ] AGENTS.md
- [ ] CLAUDE.md
- [ ] ARCHITECTURE.md
- [ ] docs/index.html
- [ ] docs/manual/*.html (12 paginas)
- [ ] docs/SUMMARY.md
- [ ] i18n (16 linguas)
- [ ] CONTRIBUTING.md (se existir)

### External
- [ ] VS Code Marketplace listing
- [ ] npm registry
- [ ] GitHub repository
- [ ] Website / landing page
- [ ] Discord/Slack community
- [ ] Social media accounts

---

## 8. Ferramentas de Automacao

| Ferramenta | Proposito |
|---|---|
| `scripts/rebrand/rename.ts` | Renomear packages e imports |
| `scripts/rebrand/strings.ts` | Substituir strings de branding |
| `scripts/rebrand/settings.ts` | Criacao de migration para settings |
| `scripts/rebrand/codemod.ts` | Transformacao automatica de codigo |
| `bun run scripts/rebrand/` | Validacao de que nada ficou para tras |

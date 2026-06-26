---
name: webapp-testing
description: Expert em testes end-to-end visuais com Playwright. Navega paginas, captura screenshots, valida layouts, testa responsividade, dark mode, acessibilidade (axe-core). Use quando o usuario pedir investigacao visual, teste de tela, validacao de layout, captura de screenshots, ou teste E2E de interfaces web.
type: skill
category: Qualidade
applicabilityScope: ["*"]
version: 1.0.0
status: approved
owner: quality
related-skills: [testing-qa-expert, e2e-visual-testing-expert]
related-dr: [DR-0038, DR-0039]
---

# Webapp Testing Expert (Playwright)

## Missao

Investigacao visual e testes E2E automatizados de interfaces web usando Playwright. Navega paginas automaticamente, captura screenshots, valida layouts, testa responsividade (multi-viewport), dark mode, dropdowns, fluxos de usuario, e acessibilidade (axe-core).

## Quando usar

- **Investigacao visual**: "investigue as paginas do manual", "verifique o layout", "captute screenshots"
- **Validacao de tela**: "teste a tela de login", "valide o dashboard", "verifique responsividade"
- **Teste E2E**: "teste o fluxo de navegacao", "valide o wizard /forge"
- **Acessibilidade**: "verifique acessibilidade", "teste com axe-core", "validar WCAG"
- **Regressao visual**: "compare screenshots", "detecte mudancas visuais"
- **Multi-browser**: "teste em Chrome, Firefox, Safari"

## Stack

| Ferramenta | Versao | Funcao |
|---|---|---|
| **Playwright** | 1.40+ | Framework de teste E2E |
| **@playwright/test** | 1.40+ | Runner de testes |
| **playwright-core** | 1.40+ | Biblioteca base |
| **axe-playwright** | 1.2+ | Acessibilidade (WCAG) |
| **sharp** | 0.33+ | Comparacao de screenshots |

## Instalacao

```powershell
# Instalar Playwright
.\.kilo\automation\scripts\e2e\install-playwright.ps1

# Verificar instalacao
npx playwright --version
```

## Sintaxe Canonica

### 1. Investigacao Visual (Screenshot)

```powershell
# Capturar todas as paginas do manual
powershell .\.kilo\automation\scripts\visual-investigate.ps1 --url http://localhost:5001 --pages all --output reports/visual/

# Capturar pagina especifica
powershell .\.kilo\automation\scripts\visual-investigate.ps1 --url http://localhost:5001 --pages "/manual/01-quickstart.html" --output reports/visual/ Captures/

# Multi-viewport
powershell .\.kilo\automation\scripts\visual-investigate.ps1 --url http://localhost:5001 --viewports mobile,tablet,desktop,wide --output reports/visual/responsive/
```

### 2. Teste E2E (Playwright Test)

```powershell
# Rodar todos os testes
npx playwright test --config=playwright.config.ts

# Rodar teste especifico
npx playwright test tests/e2e/visual-investigate.spec.ts --project=chromium

# Rodar em modo headed (ver navegador)
npx playwright test --headed

# Gerar report HTML
npx playwright test --reporter=html,list,json
```

### 3. Acessibilidade (axe-core)

```powershell
# Rodar testes de acessibilidade
powershell .\.kilo\automation\scripts\visual-investigate.ps1 --url http://localhost:5001 --accessibility --output reports/a11y/

# WCAG Level
powershell .\.kilo\automation\scripts\visual-investigate.ps1 --url http://localhost:5001 --wcag-level AA
```

### 4. Comparacao de Screenshots (Regressao Visual)

```powershell
# Comparar pagina atual com baseline
powershell .\.kilo\automation\scripts\visual-investigate.ps1 --url http://localhost:5001 --compare --baseline reports/baseline/ --output reports/diff/
```

## Parametros

| Parametro | Tipo | Default | Descricao |
|---|---|---|---|
| `--url` | string | http://localhost:5001 | URL base do app |
| `--pages` | string\|array | all | Paginas a testar (all, /path, ou lista) |
| `--viewports` | array | desktop | mobile (375x667), tablet (768x1024), desktop (1280x720), wide (1920x1080) |
| `--browsers` | array | chromium | chromium, firefox, webkit |
| `--accessibility` | bool | false | Rodar testes axe-core |
| `--wcag-level` | string | AA | A, AA, AAA |
| `--compare` | bool | false | Comparar com baseline |
| `--baseline` | string | reports/baseline/ | Diretorio de screenshots baseline |
| `--output` | string | reports/visual/ | Diretorio de saida |
| `--dark-mode` | bool | true | Testar dark mode toggle |
| `--flows` | array | [] | Fluxos a testar: login,navigate,search,form |
| `--timeout` | int | 60000 | Timeout por teste |

## Templates

### Template Base (visual-investigate.spec.ts)

Veja `tests/e2e/visual-investigate.spec.ts` para o template completo com:
- Screenshot full-page
- Captura de todos os links de navegacao
- Multi-viewport (mobile, tablet, desktop, wide)
- Dark mode toggle
- Dropdowns interativos
- Code blocks e tabelas
- ARIA snapshot (acessibilidade)
- Estatisticas da pagina (headings, paragraphs, code blocks, tables)

### Personalizando para Projeto Especifico

```typescript
// tests/e2e/my-app.spec.ts
import { test, expect } from '@playwright/test';

test.describe.sequential('My App Flow', () => {
  test('login flow', async ({ page }) => {
    await page.goto('/Identity/Account/Login');
    await page.fill('input[name="Email"]', 'admin@test.com');
    await page.fill('input[name="Password"]', 'Test@123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('text=Bem-vindo')).toBeVisible();
    await page.screenshot({ path: 'reports/login-success.png' });
  });

  test('create new entity', async ({ page }) => {
    await page.goto('/customers');
    await page.click('text=Novo Cliente');
    await page.fill('input[name="Nome"]', 'Test Customer');
    await page.fill('input[name="Email"]', 'test@example.com');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Criado com sucesso')).toBeVisible();
  });
});
```

## Exemplos Praticos

### Cenario 1: Investigacao Completa do Manual

```powershell
# Servir o manual localmente (se aplicavel)
# Abrir no browser: docs/index.html

# Executar investigacao completa
powershell .\.kilo\automation\scripts\visual-investigate.ps1 --url http://localhost:8080 --pages "all" --viewports desktop,mobile --dark-mode --output reports/manual-audit/
```

**Output esperado**:
```
[visual-investigate] Starting investigation...
[visual-investigate] Base URL: http://localhost:8080
[visual-investigate] Pages: all (47 pages found)
[visual-investigate] Viewports: desktop, mobile

[visual-investigate] === Homepage ===
  [OK] Screenshot: reports/manual-audit/homepage-full.png
  [OK] Nav links: 20 links found
  [OK] Sections: 6 detected
  [OK] Code blocks: 0 (index has no code)
  [OK] Viewport mobile: 375x667 OK
  [OK] Viewport desktop: 1280x720 OK
  [OK] Dark mode toggle: functional

[visual-investigate] === /manual/01-quickstart.html ===
  [OK] Screenshot: /manual/01-quickstart.html-full.png
  [OK] Sections: 6 detected (canonical structure)
  [OK] Examples: 5 found
  [OK] Code blocks: 3 found
  [OK] Tables: 1 found
  [OK] Troubleshooting: 4 issues documented
  [OK] Dark mode: functional
  [OK] Dropdowns: 3 dropdowns tested, all OK

... (47 pages tested)

[visual-investigate] === SUMMARY ===
  Pages tested: 47/47
  Screenshots captured: 376 (47 pages x 4 viewports x 2 modes)
  Issues found: 0 critical, 2 warnings
  Accessibility: Passed (0 violations)
  Total time: 45 seconds

[visual-investigate] Report: reports/manual-audit/report.md
```

### Cenario 2: Teste de Fluxo com Usuario

```powershell
powershell .\.kilo\automation\scripts\visual-investigate.ps1 --url http://localhost:5001 --flows "login,navigate" --browsers chromium,firefox
```

### Cenario 3: Acessibilidade (WCAG AA)

```powershell
powershell .\.kilo\automation\scripts\visual-investigate.ps1 --url http://localhost:5001 --accessibility --wcag-level AA
```

**Output esperado**:
```
[a11y] Running axe-core on http://localhost:5001...
[a11y] 0 critical violations
[a11y] 2 serious violations:
  - Color contrast ratio < 4.5:1 on .nav-link (foreground #0ea5e9 on #fff)
  - Missing aria-label on #darkBtn
[a11y] 4 minor violations
[a11y] Report: reports/a11y/axe-report.json
```

## Troubleshooting

### Playwright nao encontra o navegador
```
Error: Browser "chromium" is not installed.
```
Solucao: `npx playwright install chromium`

### Timeout em pagina lenta
```
Timeout 30000ms exceeded while waiting for load event.
```
Solucao: Aumente timeout: `--timeout 60000` ou use `--wait-until domcontentloaded`.

### Elemento nao encontrado
```
Error: locator('button#submit') resolved to 0 elements.
```
Solucao: Verifique se o elemento existe com `page.locator('button').allTextContents()` primeiro.

### Dark mode nao funciona
```
Warning: Dark mode button not found.
```
Solucao: Verifique se `#darkBtn` existe na pagina. 

## Anti-Padroes

- **NAO** capturar screenshots sem salvar em `reports/` directory
- **NAO** rodar testes sem verificar se o app esta rodando (`curl $url`)
- **NAO** comparar screenshots sem baseline claro
- **NAO** ignorar console errors (sao sinais de bugs)

## Configuracao MCP

Para usar Playwright via MCP (Model Context Protocol):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-playwright@latest"]
    }
  }
}
```

Ou via navegador MCP:
```json
{
  "mcpServers": {
    "browser": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-browser@latest"]
    }
  }
}
```

## Referencias

- Playwright docs: https://playwright.dev/docs/intro
- Axe-core rules: https://dequeuniversity.com/rules/axe/4.7
- WCAG 2.1: https://www.w3.org/TR/WCAG21/
- Template: `tests/e2e/visual-investigate.spec.ts`
- Config: `playwright.config.ts`
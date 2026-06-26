param([string]$BaseUrl = "https://localhost:5001")
$ErrorActionPreference = "Stop"
$env:E2E_BASE_URL = $BaseUrl
if (!(Test-Path "playwright.config.ts")) {
  Copy-Item "engineer/e2e-visual-testing/playwright/playwright.config.ts" "playwright.config.ts" -Force
}
New-Item -ItemType Directory -Path "tests/e2e" -Force | Out-Null
if (!(Test-Path "tests/e2e/xforge-smoke.spec.ts")) {
  Copy-Item "engineer/e2e-visual-testing/playwright/xforge-smoke.spec.ts" "tests/e2e/xforge-smoke.spec.ts" -Force
}
npx playwright test

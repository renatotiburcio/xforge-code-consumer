$ErrorActionPreference = "Stop"
if (!(Test-Path "package.json")) { npm init -y }
npm install -D @playwright/test
npx playwright install
Write-Host "Playwright installed."

param(
    [string]$Url = "http://localhost:5001",
    [string]$Pages = "all",
    [string]$Viewports = "desktop",
    [string]$Browsers = "chromium",
    [switch]$Accessibility,
    [string]$WcagLevel = "AA",
    [switch]$Compare,
    [string]$Baseline = "reports/baseline/",
    [string]$Output = "reports/visual/",
    [switch]$DarkMode = $true,
    [string]$Flows = "",
    [int]$Timeout = 60000
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " XForge Visual Investigator (Playwright)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Base URL: $Url"
Write-Host "Pages: $Pages"
Write-Host "Viewports: $Viewports"
Write-Host "Browsers: $Browsers"
Write-Host "Accessibility: $Accessibility"
Write-Host "Dark Mode: $DarkMode"
Write-Host "Output: $Output"
Write-Host ""

# Check if app is running
Write-Host "[1/5] Checking if app is reachable..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $Url -TimeoutSec 5 -UseBasicParsing
    Write-Host "  OK: App is running (status: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  FAIL: App not reachable at $Url" -ForegroundColor Red
    Write-Host "  Start the app first: dotnet run (or npm run dev, etc.)" -ForegroundColor Yellow
    exit 1
}

# Check Playwright installation
Write-Host "[2/5] Checking Playwright installation..." -ForegroundColor Yellow
$playwrightVersion = npx playwright --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Playwright not found. Installing..." -ForegroundColor Yellow
    & .\.kilo\automation\scripts\e2e\install-playwright.ps1
} else {
    Write-Host "  OK: Playwright $playwrightVersion" -ForegroundColor Green
}

# Create output directories
Write-Host "[3/5] Preparing output directories..." -ForegroundColor Yellow
$dirs = @($Output, "$Output\screenshots", "$Output\responsive", "$Output\flows", "$Output\accessibility")
foreach ($d in $dirs) {
    New-Item -ItemType Directory -Path $d -Force | Out-Null
}
Write-Host "  OK: Directories created" -ForegroundColor Green

# Generate Playwright config if not exists
Write-Host "[4/5] Generating Playwright config..." -ForegroundColor Yellow
if (-not (Test-Path "playwright.config.ts")) {
    Copy-Item "tests/e2e/playwright.config.ts" "playwright.config.ts" -Force -ErrorAction SilentlyContinue
}
if (-not (Test-Path "tests/e2e/visual-investigate.spec.ts")) {
    Copy-Item "tests/e2e/visual-investigate.spec.ts.template" "tests/e2e/visual-investigate.spec.ts" -Force -ErrorAction SilentlyContinue
}
Write-Host "  OK: Config ready" -ForegroundColor Green

# Run investigation
Write-Host "[5/5] Running visual investigation..." -ForegroundColor Yellow
Write-Host ""

$env:E2E_BASE_URL = $Url
$env:VISUAL_OUTPUT = $Output
$env:VISUAL_VIEWPORTS = $Viewports
$env:VISUAL_DARK_MODE = $DarkMode.ToString()
$env:VISUAL_ACCESSIBILITY = $Accessibility.ToString()
$env:VISUAL_WCAG_LEVEL = $WcagLevel
$env:VISUAL_TIMEOUT = $Timeout.ToString()

$npxArgs = @(
    "playwright", "test"
    "--config=playwright.config.ts"
    "--reporter=list,json,html"
    "--workers=1"
)

if ($Browsers -eq "chromium") {
    $npxArgs += "--project=chromium"
}

try {
    & npx @npxArgs 2>&1
    $exitCode = $LASTEXITCODE
} catch {
    Write-Host "  Error running tests: $_" -ForegroundColor Red
    $exitCode = 1
}

# Generate summary report
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Investigation Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Count screenshots
$screenshots = @(Get-ChildItem -Path "$Output\screenshots" -File -ErrorAction SilentlyContinue)
$responsive = @(Get-ChildItem -Path "$Output\responsive" -File -ErrorAction SilentlyContinue)
$reports = @(Get-ChildItem -Path "$Output\*.md" -File -ErrorAction SilentlyContinue)

Write-Host "  Screenshots captured: $($screenshots.Count)" -ForegroundColor White
Write-Host "  Responsive captures: $($responsive.Count)" -ForegroundColor White
Write-Host "  Reports generated: $($reports.Count)" -ForegroundColor White
Write-Host "  Output directory: $Output" -ForegroundColor White

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "  PASS - All visual checks passed!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "  WARN - Some checks failed. Review reports above." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review screenshots: dir $Output\screenshots" -ForegroundColor White
Write-Host "  2. Review HTML report: reports\playwright-html\index.html" -ForegroundColor White
Write-Host "  3. Review JSON report: reports\playwright-results.json" -ForegroundColor White
if ($Accessibility) {
    Write-Host "  4. Review a11y report: $Output\accessibility\axe-report.json" -ForegroundColor White
}

exit $exitCode
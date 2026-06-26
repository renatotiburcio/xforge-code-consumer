param([string]$ProjectName = "my-xforge-project")

$ErrorActionPreference = "Stop"

Write-Host "=== XForge Template Init ==="
Write-Host "Project: $ProjectName"
Write-Host ""

# 1. Check prerequisites
Write-Host "[CHECK] Prerequisites..."
$missing = @()
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { $missing += "git" }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { $missing += "python" }
if ($missing.Count -gt 0) {
    Write-Host "[ERROR] Missing prerequisites: $($missing -join ', ')"
    exit 1
}
Write-Host "[OK] All prerequisites found"
Write-Host ""

# 2. Create project directory
if (Test-Path $ProjectName) {
    Write-Host "[WARN] Directory '$ProjectName' already exists"
} else {
    New-Item -ItemType Directory -Path $ProjectName -Force | Out-Null
    Write-Host "[CREATE] $ProjectName/"
}
Set-Location $ProjectName
Write-Host ""

# 3. Initialize RAG
Write-Host "[RAG] Initializing index..."
$ragScript = ".kilo\automation\scripts\rag\rag_local.py"
if (Test-Path $ragScript) {
    python $ragScript index 2>&1 | Out-Null
    Write-Host "[OK] RAG indexed"
} else {
    Write-Host "[SKIP] RAG script not found (run from template root)"
}
Write-Host ""

# 4. Run doctor
Write-Host "[CHECK] Running doctor..."
$doctorScript = ".kilo\automation\scripts\doctor.ps1"
if (Test-Path $doctorScript) {
    & $doctorScript
} else {
    Write-Host "[SKIP] doctor.ps1 not found"
}
Write-Host ""

# 5. Summary
Write-Host "=== Template installed ==="
Write-Host "Next: run '/analisar-projeto' in KiloCode"
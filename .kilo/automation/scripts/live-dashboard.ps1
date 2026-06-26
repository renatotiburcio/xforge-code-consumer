# XForge Live Dashboard
# Shows real-time system status: Ollama models, errors, knowledge, quality gates

param(
    [switch]$Json
)

$ErrorActionPreference = "Continue"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
Push-Location $Root

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          XFORGE LIVE DASHBOARD v1.0                 ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$dashboard = @{}

# 1. System Status
Write-Host "📊 SYSTEM STATUS" -ForegroundColor Cyan
Write-Host "─────────────────" -ForegroundColor DarkGray

$csFiles = (Get-ChildItem -Path . -Recurse -Filter "*.cs" -Exclude "obj","bin","node_modules" -ErrorAction SilentlyContinue).Count
$mdFiles = (Get-ChildItem -Path . -Recurse -Filter "*.md" -Exclude "obj","bin","node_modules" -ErrorAction SilentlyContinue).Count
$jsonFiles = (Get-ChildItem -Path . -Recurse -Filter "*.json" -Exclude "obj","bin","node_modules" -ErrorAction SilentlyContinue).Count

Write-Host "  C# files:     $csFiles" -ForegroundColor White
Write-Host "  MD files:     $mdFiles" -ForegroundColor White
Write-Host "  JSON files:   $jsonFiles" -ForegroundColor White
Write-Host "  Total files:  $($csFiles + $mdFiles + $jsonFiles)" -ForegroundColor White

# 2. Knowledge Base
Write-Host ""
Write-Host "📚 KNOWLEDGE BASE" -ForegroundColor Cyan
Write-Host "──────────────────" -ForegroundColor DarkGray

$knowledgeFiles = (Get-ChildItem -Path ".xforge/knowledge" -Recurse -Filter "*.md" -ErrorAction SilentlyContinue).Count
$indexFile = ".xforge/knowledge/INDEX.json"
$indexedCount = 0
if (Test-Path $indexFile) {
    $index = Get-Content $indexFile -Raw | ConvertFrom-Json
    $indexedCount = $index.files.Count
}
Write-Host "  Knowledge files:  $knowledgeFiles" -ForegroundColor White
Write-Host "  Indexed:          $indexedCount" -ForegroundColor $(if ($indexedCount -ge $knowledgeFiles) { "Green" } else { "Yellow" })

# 3. Error Patterns
Write-Host ""
Write-Host "🚨 ERROR PATTERNS" -ForegroundColor Cyan
Write-Host "──────────────────" -ForegroundColor DarkGray

$graphFile = ".xforge/knowledge/errors-solutions-graph.json"
if (Test-Path $graphFile) {
    $graph = Get-Content $graphFile -Raw | ConvertFrom-Json
    Write-Host "  Errors cataloged:     $($graph.errorPatterns.Count)" -ForegroundColor White
    Write-Host "  Prevention rules:     $($graph.preventionRules.Count)" -ForegroundColor White
    $autoFixCount = ($graph.errorPatterns | Where-Object { $_.autoFix.enabled }).Count
    Write-Host "  Auto-fix enabled:     $autoFixCount" -ForegroundColor Green
} else {
    Write-Host "  Error graph not found" -ForegroundColor Red
}

# 4. Knowledge Versioning
Write-Host ""
Write-Host "📋 KNOWLEDGE VERSIONING" -ForegroundColor Cyan
Write-Host "───────────────────────" -ForegroundColor DarkGray

$kvFile = ".xforge/config/knowledge-versioning.json"
if (Test-Path $kvFile) {
    $kv = Get-Content $kvFile -Raw | ConvertFrom-Json
    $active = ($kv.tracks | Where-Object { $_.status -eq "active" }).Count
    $expired = ($kv.tracks | Where-Object { $_.status -eq "expired" }).Count
    Write-Host "  Active rules:   $active" -ForegroundColor Green
    Write-Host "  Expired rules:  $expired" -ForegroundColor $(if ($expired -gt 0) { "Yellow" } else { "Green" })
    Write-Host "  Sources tracked: $($kv.sources.Count)" -ForegroundColor White
} else {
    Write-Host "  Versioning not configured" -ForegroundColor Yellow
}

# 5. Quality Gates Status
Write-Host ""
Write-Host "🔒 QUALITY GATES" -ForegroundColor Cyan
Write-Host "─────────────────" -ForegroundColor DarkGray

$preCommitExists = Test-Path ".kilo/automation/scripts/pre-commit.ps1"
$depCheckExists = Test-Path ".kilo/automation/scripts/dependency-check.ps1"
$intelExists = Test-Path ".kilo/automation/scripts/proactive-intelligence.ps1"

Write-Host "  Pre-commit gate:      $(if ($preCommitExists) { '✅ Ready' } else { '❌ Missing' })" -ForegroundColor $(if ($preCommitExists) { "Green" } else { "Red" })
Write-Host "  Dependency checker:   $(if ($depCheckExists) { '✅ Ready' } else { '❌ Missing' })" -ForegroundColor $(if ($depCheckExists) { "Green" } else { "Red" })
Write-Host "  Proactive intel:      $(if ($intelExists) { '✅ Ready' } else { '❌ Missing' })" -ForegroundColor $(if ($intelExists) { "Green" } else { "Red" })

# 6. Interaction Intelligence
Write-Host ""
Write-Host "🧠 INTERACTION INTELLIGENCE" -ForegroundColor Cyan
Write-Host "────────────────────────────" -ForegroundColor DarkGray

$rules = Get-ChildItem -Path ".kilo/rules" -Filter "*.md" -ErrorAction SilentlyContinue
$interactionRules = $rules | Where-Object { $_.Name -match "interaction|self-healing|quality-gates|proactive|dependency|session-memory" }
Write-Host "  Interaction rules:  $($interactionRules.Count)/6" -ForegroundColor $(if ($interactionRules.Count -ge 6) { "Green" } else { "Yellow" })

# 7. Split Architecture
Write-Host ""
Write-Host "🤖 SPLIT ARCHITECTURE" -ForegroundColor Cyan
Write-Host "──────────────────────" -ForegroundColor DarkGray

$ollamaConfig = ".xforge/config/ollama-models.json"
if (Test-Path $ollamaConfig) {
    $ollama = Get-Content $ollamaConfig -Raw | ConvertFrom-Json
    Write-Host "  Models configured:  $($ollama.models.PSObject.Properties.Name.Count)" -ForegroundColor White
    Write-Host "  Router:             $($ollama.architecture.router.model)" -ForegroundColor White
    Write-Host "  Worker:             $($ollama.architecture.worker.model)" -ForegroundColor White
    Write-Host "  Context budget:     $($ollama.contextBudget.default) tokens" -ForegroundColor White
} else {
    Write-Host "  Ollama config not found" -ForegroundColor Red
}

# 8. Quick Health Check
Write-Host ""
Write-Host "⚡ QUICK HEALTH" -ForegroundColor Cyan
Write-Host "────────────────" -ForegroundColor DarkGray

$healthIssues = 0

# Check for missing rules
$requiredRules = @("interaction-intelligence.md", "self-healing-rules.md", "proactive-quality-gates.md", "proactive-intelligence.md", "dependency-intelligence.md", "session-memory.md", "multi-agent-orchestration.md", "manual-sync-rules.md")
foreach ($rule in $requiredRules) {
    if (!(Test-Path ".kilo/rules/$rule")) {
        Write-Host "  ❌ Missing rule: $rule" -ForegroundColor Red
        $healthIssues++
    }
}

# Check for missing scripts
$requiredScripts = @("pre-commit.ps1", "dependency-check.ps1", "proactive-intelligence.ps1", "ollama-setup.ps1", "doctor.ps1")
foreach ($script in $requiredScripts) {
    if (!(Test-Path ".kilo/automation/scripts/$script")) {
        Write-Host "  ❌ Missing script: $script" -ForegroundColor Red
        $healthIssues++
    }
}

# Check INDEX.json
if (!(Test-Path ".xforge/knowledge/INDEX.json")) {
    Write-Host "  ❌ Missing INDEX.json" -ForegroundColor Red
    $healthIssues++
}

if ($healthIssues -eq 0) {
    Write-Host "  ✅ All checks passed" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ $healthIssues issues found" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Dashboard complete. All systems operational." -ForegroundColor Green
Write-Host "══════════════════════════════════════════════════════" -ForegroundColor Cyan

Pop-Location
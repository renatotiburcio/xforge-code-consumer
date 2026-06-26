# XForge Proactive Intelligence Analyzer
# Analyzes project context and suggests preventive actions

param(
    [string]$Target = "all",
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
Push-Location $Root

Write-Host "🧠 XForge Proactive Intelligence" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Load error patterns
$graphPath = Join-Path $Root ".xforge/knowledge/errors-solutions-graph.json"
$graph = Get-Content $graphPath -Raw | ConvertFrom-Json

Write-Host "Analyzing project..." -ForegroundColor Yellow
Write-Host ""

# 1. Error Pattern Analysis
Write-Host "📊 ERROR PATTERN ANALYSIS" -ForegroundColor Cyan
Write-Host "─────────────────────────" -ForegroundColor Cyan

$csFiles = Get-ChildItem -Path . -Recurse -Filter "*.cs" -Exclude "obj","bin","node_modules"
$issues = @()

foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw
    $relPath = $file.FullName.Replace($Root + "\", "")

    # Check ERR-002: Null safety
    $firstOrDefaultCalls = [regex]::Matches($content, 'var\s+(\w+)\s*=.*FirstOrDefault')
    foreach ($match in $firstOrDefaultCalls) {
        $varName = $match.Groups[1].Value
        $lineNum = $content.Substring(0, $match.Index).Split("`n").Count
        if ($content -notmatch "if\s*\(\s*$varName\s*(!=|==\s*null)") {
            $issues += @{ Type = "ERR-002"; File = $relPath; Line = $lineNum; Severity = "high"; Message = "FirstOrDefault without null check — NullRef risk" }
        }
    }

    # Check ERR-005: .First() without Where
    $firstCalls = [regex]::Matches($content, '\.First\(\)')
    foreach ($match in $firstCalls) {
        $lineNum = $content.Substring(0, $match.Index).Split("`n").Count
        $issues += @{ Type = "ERR-005"; File = $relPath; Line = $lineNum; Severity = "high"; Message = ".First() without null check — use .FirstOrDefault()" }
    }

    # Check ERR-013: N+1 query
    if ($content -match 'foreach\s*\(' -and $content -match 'Include\(') {
        $issues += @{ Type = "ERR-013"; File = $relPath; Line = 0; Severity = "medium"; Message = "Possible N+1 query — check Include usage" }
    }

    # Check ERR-014: Memory leak
    if ($content -match 'new\s+HttpClient\(') {
        $issues += @{ Type = "ERR-014"; File = $relPath; Line = 0; Severity = "high"; Message = "new HttpClient() — use IHttpClientFactory" }
    }

    # Check ERR-015: Sync over async
    if ($content -match '\.Result\b' -or $content -match '\.Wait\(') {
        $issues += @{ Type = "ERR-015"; File = $relPath; Line = 0; Severity = "high", Message = "Sync-over-async detected" }
    }
}

$highIssues = $issues | Where-Object { $_.Severity -eq "high" }
$mediumIssues = $issues | Where-Object { $_.Severity -eq "medium" }

Write-Host "  High severity: $($highIssues.Count) issues" -ForegroundColor $(if ($highIssues.Count -gt 0) { "Red" } else { "Green" })
Write-Host "  Medium severity: $($mediumIssues.Count) issues" -ForegroundColor $(if ($mediumIssues.Count -gt 0) { "Yellow" } else { "Green" })

# 2. File Impact Analysis
Write-Host ""
Write-Host "📊 FILE IMPACT ANALYSIS" -ForegroundColor Cyan
Write-Host "───────────────────────" -ForegroundColor Cyan

$serviceFiles = $csFiles | Where-Object { $_.Name -match 'Service\.cs$' }
foreach ($service in $serviceFiles) {
    $className = $service.BaseName
    $dependents = $csFiles | Where-Object {
        $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
        $content -match $className
    }
    if ($dependents.Count -gt 3) {
        $relPath = $service.FullName.Replace($Root + "\", "")
        Write-Host "  ⚠️ $relPath has $($dependents.Count) dependent files" -ForegroundColor Yellow
    }
}

# 3. Test Coverage Check
Write-Host ""
Write-Host "📊 TEST COVERAGE CHECK" -ForegroundColor Cyan
Write-Host "──────────────────────" -ForegroundColor Cyan

$testFiles = Get-ChildItem -Path . -Recurse -Filter "*Tests.csproj" -Exclude "obj","bin"
$srcFiles = Get-ChildItem -Path . -Recurse -Filter "*Service.cs" -Exclude "obj","bin","*Test*"

$untestedServices = @()
foreach ($service in $srcFiles) {
    $testFile = $testFiles | Where-Object {
        $testContent = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
        $testContent -match $service.BaseName
    }
    if (!$testFile) {
        $untestedServices += $service.BaseName
    }
}

if ($untestedServices.Count -gt 0) {
    Write-Host "  ⚠️ Services without tests: $($untestedServices.Count)" -ForegroundColor Yellow
    foreach ($svc in $untestedServices) {
        Write-Host "    - $svc" -ForegroundColor DarkYellow
    }
} else {
    Write-Host "  ✅ All services have test files" -ForegroundColor Green
}

# 4. Security Quick Scan
Write-Host ""
Write-Host "📊 SECURITY QUICK SCAN" -ForegroundColor Cyan
Write-Host "──────────────────────" -ForegroundColor Cyan

$securityIssues = 0
foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match 'AllowAnonymous' -and $content -match 'POST|PUT|DELETE') {
        $relPath = $file.FullName.Replace($Root + "\", "")
        Write-Host "  ⚠️ $relPath: AllowAnonymous on write endpoint" -ForegroundColor Yellow
        $securityIssues++
    }
    if ($content -match 'CORS.*\*') {
        $relPath = $file.FullName.Replace($Root + "\", "")
        Write-Host "  ⚠️ $relPath: CORS wildcard (*) detected" -ForegroundColor Yellow
        $securityIssues++
    }
}

if ($securityIssues -eq 0) {
    Write-Host "  ✅ No security issues detected" -ForegroundColor Green
}

# 5. Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INTELLIGENCE SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Total issues: $($issues.Count)" -ForegroundColor $(if ($issues.Count -gt 0) { "Yellow" } else { "Green" })
Write-Host "  High: $($highIssues.Count) | Medium: $($mediumIssues.Count)" -ForegroundColor White
Write-Host "  Untested services: $($untestedServices.Count)" -ForegroundColor $(if ($untestedServices.Count -gt 0) { "Yellow" } else { "Green" })
Write-Host "  Security issues: $securityIssues" -ForegroundColor $(if ($securityIssues -gt 0) { "Yellow" } else { "Green" })

Pop-Location

# XForge Scoring Script — IMMUTABLE
# This script calculates the XForge Score (xfs) for code changes.
# The agent CANNOT modify this script. Only humans can.
# Usage: .\score.ps1
# Output: line for results.tsv

param(
    [string]$CommitHash = "HEAD",
    [string]$Description = ""
)

$ErrorActionPreference = "Continue"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
Push-Location $Root

# ============================================================================
# SCORING WEIGHTS (HUMAN-ONLY MODIFICATION)
# These weights define how the XForge Score is calculated.
# The agent CANNOT modify these values.
# ============================================================================

$WEIGHTS = @{
    Correctness  = 0.30
    Performance  = 0.20
    Quality      = 0.20
    Simplicity   = 0.15
    Prevention   = 0.15
}

# ============================================================================
# DIMENSION 1: CORRECTNESS (30%)
# ============================================================================

Write-Host "Calculating Correctness..." -ForegroundColor Yellow

# 1a. Tests pass rate
$totalTests = 0
$passedTests = 0
$testOutput = dotnet test --no-build -v q 2>&1 | Out-String
if ($testOutput -match "Passed:\s+(\d+)") { $passedTests = [int]$Matches[1] }
if ($testOutput -match "Failed:\s+(\d+)") { $failedTests = [int]$Matches[1] }
$totalTests = $passedTests + $failedTests
$testScore = if ($totalTests -gt 0) { $passedTests / $totalTests } else { 1.0 }

# 1b. Build success
$buildOutput = dotnet build --no-restore -v q 2>&1 | Out-String
$buildSuccess = if ($LASTEXITCODE -eq 0) { 1.0 } else { 0.0 }

# 1c. Runtime errors (check for common patterns)
$csFiles = Get-ChildItem -Path . -Recurse -Filter "*.cs" -Exclude "obj","bin","node_modules" -ErrorAction SilentlyContinue
$runtimeErrors = 0
foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($content -match '\.Result\b' -or $content -match '\.Wait\(') { $runtimeErrors += 0.1 }
    if ($content -match 'throw new Exception\(') { $runtimeErrors += 0.05 }
}
$runtimeScore = [Math]::Max(0, 1.0 - $runtimeErrors)

$correctness = ($testScore * 0.5) + ($buildSuccess * 0.3) + ($runtimeScore * 0.2)
Write-Host "  Correctness: $([Math]::Round($correctness, 3))" -ForegroundColor Green

# ============================================================================
# DIMENSION 2: PERFORMANCE (20%)
# ============================================================================

Write-Host "Calculating Performance..." -ForegroundColor Yellow

$nPlusOne = 0
$syncOverAsync = 0
$memoryLeaks = 0

foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    # N+1 detection
    if ($content -match 'foreach\s*\(' -and $content -match '\.ToList\(\)') { $nPlusOne += 0.2 }
    # Sync-over-async
    if ($content -match '\.Result\b' -or $content -match '\.Wait\(') { $syncOverAsync += 0.3 }
    # Memory leak (new HttpClient without using)
    if ($content -match 'new\s+HttpClient\(' -and $content -notmatch 'using|IHttpClientFactory') { $memoryLeaks += 0.3 }
}

$performance = [Math]::Max(0, 1.0 - $nPlusOne - $syncOverAsync - $memoryLeaks)
Write-Host "  Performance: $([Math]::Round($performance, 3))" -ForegroundColor Green

# ============================================================================
# DIMENSION 3: QUALITY (20%)
# ============================================================================

Write-Host "Calculating Quality..." -ForegroundColor Yellow

# Format compliance
$formatOutput = dotnet format --verify-no-changes 2>&1 | Out-String
$formatScore = if ($LASTEXITCODE -eq 0) { 1.0 } else { 0.7 }

# Warnings
$warningCount = ([regex]::Matches($buildOutput, "warning CS")).Count
$warningScore = [Math]::Max(0, 1.0 - ($warningCount * 0.05))

$quality = ($formatScore * 0.5) + ($warningScore * 0.5)
Write-Host "  Quality: $([Math]::Round($quality, 3))" -ForegroundColor Green

# ============================================================================
# DIMENSION 4: SIMPLICITY (15%)
# ============================================================================

Write-Host "Calculating Simplicity..." -ForegroundColor Yellow

# Lines changed
$gitDiff = git diff --cached --numstat 2>&1 | Out-String
$linesAdded = 0
$linesRemoved = 0
$filesChanged = 0
foreach ($line in ($gitDiff -split "`n")) {
    if ($line -match '(\d+)\s+(\d+)\s+(.+)') {
        $linesAdded += [int]$Matches[1]
        $linesRemoved += [int]$Matches[2]
        $filesChanged++
    }
}

$totalLines = $linesAdded + $linesRemoved
$simplicityLines = if ($totalLines -gt 0) { [Math]::Max(0, 1.0 - ($linesAdded / 100)) } else { 1.0 }
$simplicityFiles = if ($filesChanged -gt 0) { [Math]::Max(0, 1.0 - ($filesChanged / 10)) } else { 1.0 }

$simplicity = ($simplicityLines * 0.5) + ($simplicityFiles * 0.5)
Write-Host "  Simplicity: $([Math]::Round($simplicity, 3))" -ForegroundColor Green

# ============================================================================
# DIMENSION 5: PREVENTION (15%)
# ============================================================================

Write-Host "Calculating Prevention..." -ForegroundColor Yellow

$graphFile = ".xforge/knowledge/errors-solutions-graph.json"
$preventionScore = 0.5  # default
if (Test-Path $graphFile) {
    $graph = Get-Content $graphFile -Raw | ConvertFrom-Json
    $autoFixCount = ($graph.errorPatterns | Where-Object { $_.autoFix.enabled }).Count
    $preventionScore = [Math]::Min(1.0, 0.3 + ($autoFixCount * 0.03))
}

$prevention = $preventionScore
Write-Host "  Prevention: $([Math]::Round($prevention, 3))" -ForegroundColor Green

# ============================================================================
# CALCULATE FINAL XFS
# ============================================================================

$xfs = ($correctness * $WEIGHTS.Correctness) +
       ($performance * $WEIGHTS.Performance) +
       ($quality * $WEIGHTS.Quality) +
       ($simplicity * $WEIGHTS.Simplicity) +
       ($prevention * $WEIGHTS.Prevention)

$xfs = [Math]::Round($xfs, 3)

# Determine status
$status = if ($xfs -ge 0.8) { "keep" } elseif ($xfs -ge 0.5) { "review" } else { "discard" }

# Get commit hash
$commit = git rev-parse --short $CommitHash 2>&1
if ($LASTEXITCODE -ne 0) { $commit = "unknown" }

$timestamp = (Get-Date).ToString("o")

# Output for results.tsv
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  XFORGE SCORE RESULTS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Commit:       $commit" -ForegroundColor White
Write-Host "  XFS:          $xfs" -ForegroundColor $(if ($xfs -ge 0.8) { "Green" } elseif ($xfs -ge 0.5) { "Yellow" } else { "Red" })
Write-Host "  Correctness:  $([Math]::Round($correctness, 3)) (weight: $($WEIGHTS.Correctness))" -ForegroundColor White
Write-Host "  Performance:  $([Math]::Round($performance, 3)) (weight: $($WEIGHTS.Performance))" -ForegroundColor White
Write-Host "  Quality:      $([Math]::Round($quality, 3)) (weight: $($WEIGHTS.Quality))" -ForegroundColor White
Write-Host "  Simplicity:   $([Math]::Round($simplicity, 3)) (weight: $($WEIGHTS.Simplicity))" -ForegroundColor White
Write-Host "  Prevention:   $([Math]::Round($prevention, 3)) (weight: $($WEIGHTS.Prevention))" -ForegroundColor White
Write-Host "  Status:       $status" -ForegroundColor $(if ($status -eq "keep") { "Green" } elseif ($status -eq "review") { "Yellow" } else { "Red" })
Write-Host "  Description:  $Description" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

# Append to results.tsv
$resultsFile = ".xforge/experiments/results.tsv"
$resultsDir = Split-Path $resultsFile
if (!(Test-Path $resultsDir)) { New-Item -ItemType Directory -Path $resultsDir -Force | Out-Null }

# Create header if file doesn't exist
if (!(Test-Path $resultsFile)) {
    "commit`txfs`tcorrectness`tperformance\tquality\tsimplicity\tprevention\tstatus`tdescription`ttimestamp" | Out-File $resultsFile -Encoding UTF8
}

# Append result
"$commit`t$xfs`t$([Math]::Round($correctness, 3))`t$([Math]::Round($performance, 3))`t$([Math]::Round($quality, 3))`t$([Math]::Round($simplicity, 3))`t$([Math]::Round($prevention, 3))`t$status`t$Description`t$timestamp" | Out-File $resultsFile -Append -Encoding UTF8

Write-Host ""
Write-Host "Result appended to $resultsFile" -ForegroundColor Cyan

Pop-Location

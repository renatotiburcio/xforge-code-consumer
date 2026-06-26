# XForge Dependency Intelligence Scanner
# Checks for CVEs, outdated packages, and breaking changes

param(
    [switch]$Fix,
    [switch]$Verbose,
    [switch]$Report
)

$ErrorActionPreference = "Continue"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
Push-Location $Root

Write-Host "📦 XForge Dependency Intelligence" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$results = @{
    critical = @()
    high = @()
    medium = @()
    low = @()
    outdated = @()
    breaking = @()
}

# 1. Check NuGet vulnerabilities
Write-Host "[1/4] Checking NuGet vulnerabilities..." -ForegroundColor Yellow
$vulnOutput = dotnet list package --vulnerable 2>&1 | Out-String
$vulnLines = $vulnOutput -split "`n"

$currentPackage = ""
foreach ($line in $vulnLines) {
    if ($line -match '>\s+(\S+)\s+') {
        $currentPackage = $Matches[1]
    }
    if ($line -match 'Critical') {
        $results.critical += "NuGet: $currentPackage has CRITICAL vulnerability"
    } elseif ($line -match 'High') {
        $results.high += "NuGet: $currentPackage has HIGH vulnerability"
    } elseif ($line -match 'Moderate') {
        $results.medium += "NuGet: $currentPackage has MEDIUM vulnerability"
    } elseif ($line -match 'Low') {
        $results.low += "NuGet: $currentPackage has LOW vulnerability"
    }
}
Write-Host "  Done" -ForegroundColor Green

# 2. Check outdated packages
Write-Host "[2/4] Checking outdated packages..." -ForegroundColor Yellow
$outdatedOutput = dotnet list package --outdated 2>&1 | Out-String
$outdatedLines = $outdatedOutput -split "`n"

foreach ($line in $outdatedLines) {
    if ($line -match '>\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)') {
        $pkg = $Matches[1]
        $current = $Matches[2]
        $latest = $Matches[3]
        $type = $Matches[4]

        $currentMajor = [int]($current.Split('.')[0])
        $latestMajor = [int]($latest.Split('.')[0])

        if ($latestMajor -gt $currentMajor) {
            $results.breaking += "MAJOR: $pkg $current → $latest (breaking changes possible)"
        } elseif ($type -match "Patch") {
            $results.outdated += "PATCH (safe): $pkg $current → $latest"
        } else {
            $results.outdated += "MINOR: $pkg $current → $latest"
        }
    }
}
Write-Host "  Done" -ForegroundColor Green

# 3. Check for preview/rc packages
Write-Host "[3/4] Checking for preview packages..." -ForegroundColor Yellow
$csprojFiles = Get-ChildItem -Path . -Recurse -Filter "*.csproj" -Exclude "obj","bin"
foreach ($csproj in $csprojFiles) {
    $content = Get-Content $csproj.FullName -Raw
    $previewPackages = [regex]::Matches($content, 'PackageReference\s+Include="([^"]+)"\s+Version="([^"]*(?:preview|rc|alpha|beta)[^"]*)"')
    foreach ($match in $previewPackages) {
        $pkg = $match.Groups[1].Value
        $ver = $match.Groups[2].Value
        $results.high += "PREVIEW: $pkg uses preview version $ver — upgrade to stable"
    }
}
Write-Host "  Done" -ForegroundColor Green

# 4. License check
Write-Host "[4/4] Checking licenses..." -ForegroundColor Yellow
$licenseOutput = dotnet list package --include-transitive 2>&1 | Out-String
# Basic check for known problematic licenses
$problematicLicenses = @("GPL-3.0", "AGPL-3.0", "SSPL-1.0")
foreach ($license in $problematicLicenses) {
    if ($licenseOutput -match $license) {
        $results.high += "LICENSE: Package with $license detected — legal review needed"
    }
}
Write-Host "  Done" -ForegroundColor Green

# Report
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DEPENDENCY INTELLIGENCE REPORT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($results.critical.Count -gt 0) {
    Write-Host ""
    Write-Host "🔴 CRITICAL ($($results.critical.Count)):" -ForegroundColor Red
    foreach ($item in $results.critical) { Write-Host "  $item" -ForegroundColor Red }
}

if ($results.high.Count -gt 0) {
    Write-Host ""
    Write-Host "🟠 HIGH ($($results.high.Count)):" -ForegroundColor DarkYellow
    foreach ($item in $results.high) { Write-Host "  $item" -ForegroundColor Yellow }
}

if ($results.medium.Count -gt 0) {
    Write-Host ""
    Write-Host "🟡 MEDIUM ($($results.medium.Count)):" -ForegroundColor Yellow
    foreach ($item in $results.medium) { Write-Host "  $item" -ForegroundColor Yellow }
}

if ($results.breaking.Count -gt 0) {
    Write-Host ""
    Write-Host "⚡ BREAKING CHANGES ($($results.breaking.Count)):" -ForegroundColor Magenta
    foreach ($item in $results.breaking) { Write-Host "  $item" -ForegroundColor Magenta }
}

if ($results.outdated.Count -gt 0) {
    Write-Host ""
    Write-Host "📦 OUTDATED ($($results.outdated.Count)):" -ForegroundColor Cyan
    foreach ($item in $results.outdated) { Write-Host "  $item" -ForegroundColor Cyan }
}

if ($results.low.Count -gt 0) {
    Write-Host ""
    Write-Host "🔵 LOW ($($results.low.Count)):" -ForegroundColor Blue
    foreach ($item in $results.low) { Write-Host "  $item" -ForegroundColor Blue }
}

$totalIssues = $results.critical.Count + $results.high.Count + $results.medium.Count
if ($totalIssues -eq 0) {
    Write-Host ""
    Write-Host "✅ No security issues found!" -ForegroundColor Green
}

# Auto-fix if requested
if ($Fix -and $results.outdated.Count -gt 0) {
    Write-Host ""
    Write-Host "🔧 Auto-fixing patch updates..." -ForegroundColor Green
    foreach ($item in $results.outdated) {
        if ($item -match "PATCH") {
            $pkg = ($item -split " ")[2]
            Write-Host "  Updating $pkg..." -ForegroundColor White
            dotnet add package $pkg 2>&1 | Out-Null
        }
    }
}

# JSON report
if ($Report) {
    $reportPath = Join-Path $Root ".xforge/reports/dependency-intelligence-$(Get-Date -Format 'yyyy-MM-dd').json"
    $reportDir = Split-Path $reportPath
    if (!(Test-Path $reportDir)) { New-Item -ItemType Directory -Path $reportDir -Force | Out-Null }

    $report = @{
        timestamp = (Get-Date).ToString("o")
        summary = @{
            critical = $results.critical.Count
            high = $results.high.Count
            medium = $results.medium.Count
            low = $results.low.Count
            outdated = $results.outdated.Count
            breaking = $results.breaking.Count
        }
        details = $results
    } | ConvertTo-Json -Depth 5

    Set-Content $reportPath $report
    Write-Host ""
    Write-Host "📄 Report saved to: $reportPath" -ForegroundColor Cyan
}

Pop-Location

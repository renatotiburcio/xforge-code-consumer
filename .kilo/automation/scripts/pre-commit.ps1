# XForge Pre-Commit Quality Gate
# Runs automatically before each commit
# Detects and auto-fixes common issues

param(
    [switch]$DryRun,
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
Push-Location $Root

Write-Host "🔒 XForge Pre-Commit Quality Gate" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

$issues = @()
$fixed = @()

# SH-001: Unused usings
Write-Host "[1/8] Checking unused usings..." -ForegroundColor Yellow
$csFiles = Get-ChildItem -Path . -Recurse -Filter "*.cs" -Exclude "obj","bin","node_modules"
foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw
    $usings = [regex]::Matches($content, 'using\s+([\w.]+);') | ForEach-Object { $_.Groups[1].Value }
    foreach ($using in $usings) {
        $namespace = $using.Split('.')[-1]
        if ($content -notmatch "\b$namespace\b" -or $content -match "using\s+$using;") {
            # Simple heuristic: if namespace word doesn't appear elsewhere
            $restOfContent = $content -replace "using\s+$using;", ""
            if ($restOfContent -notmatch "\b$namespace\b") {
                $issues += "SH-001: Unused using '$using' in $($file.Name)"
                if (!$DryRun) {
                    $content = $content -replace "using\s+$using;\r?\n", ""
                    Set-Content $file.FullName $content -NoNewline
                    $fixed += "SH-001: Removed unused using '$using' from $($file.Name)"
                }
            }
        }
    }
}
Write-Host "  Done" -ForegroundColor Green

# SH-003: Null-conditional access
Write-Host "[2/8] Checking null-safety..." -ForegroundColor Yellow
foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw
    $lines = Get-Content $file.FullName
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        # Detect FirstOrDefault without null check on next line
        if ($line -match 'FirstOrDefault\(' -and $i + 1 -lt $lines.Count) {
            $nextLine = $lines[$i + 1]
            $varName = [regex]::Match($line, 'var\s+(\w+)\s*=').Groups[1].Value
            if ($varName -and $nextLine -notmatch "if\s*\(\s*$varName\s*(!=|==\s*null)" -and $nextLine -notmatch "\?$varName") {
                $issues += "SH-004: FirstOrDefault without null check in $($file.Name):$($i+1)"
            }
        }
    }
}
Write-Host "  Done" -ForegroundColor Green

# SH-005: Sync-over-async
Write-Host "[3/8] Checking sync-over-async..." -ForegroundColor Yellow
foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match '\.Result\b' -or $content -match '\.Wait\(') {
        $issues += "SH-005: Sync-over-async detected in $($file.Name)"
    }
    if ($content -match 'SaveChanges\(' -and $content -notmatch 'SaveChangesAsync') {
        $issues += "SH-005: SaveChanges() should be SaveChangesAsync() in $($file.Name)"
    }
}
Write-Host "  Done" -ForegroundColor Green

# SH-007: SQL Injection
Write-Host "[4/8] Checking SQL injection..." -ForegroundColor Yellow
foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match 'FromSqlRaw\s*\(\$') {
        $issues += "SH-007: Possible SQL injection in $($file.Name)"
    }
}
Write-Host "  Done" -ForegroundColor Green

# SH-008: Secrets detection
Write-Host "[5/8] Checking for secrets..." -ForegroundColor Yellow
$secretPatterns = @(
    'sk-[a-zA-Z0-9]{20,}',
    'api[_-]?key\s*=\s*["\'][^"\']+["\']',
    'password\s*=\s*["\'][^"\']+["\']',
    'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
    'AKIA[A-Z0-9]{16}'
)
foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw
    foreach ($pattern in $secretPatterns) {
        if ($content -match $pattern) {
            $issues += "SH-008: Possible secret detected in $($file.Name)"
        }
    }
}
Write-Host "  Done" -ForegroundColor Green

# SH-009: Missing CancellationToken
Write-Host "[6/8] Checking CancellationToken..." -ForegroundColor Yellow
foreach ($file in $csFiles) {
    $content = Get-Content $file.FullName -Raw
    $asyncMethods = [regex]::Matches($content, 'public\s+async\s+\w+[\<\w\>\[\]]*\s+\w+\s*\([^)]*\)')
    foreach ($match in $asyncMethods) {
        $method = $match.Value
        if ($method -notmatch 'CancellationToken' -and $method -match '\(') {
            $issues += "SH-009: Missing CancellationToken in $($file.Name)"
        }
    }
}
Write-Host "  Done" -ForegroundColor Green

# Build check
Write-Host "[7/8] Running build check..." -ForegroundColor Yellow
$buildOutput = dotnet build --no-restore -v q 2>&1
if ($LASTEXITCODE -ne 0) {
    $issues += "BUILD: Build failed"
}
Write-Host "  Done" -ForegroundColor Green

# Format check
Write-Host "[8/8] Running format check..." -ForegroundColor Yellow
$formatOutput = dotnet format --verify-no-changes 2>&1
if ($LASTEXITCODE -ne 0) {
    $issues += "FORMAT: Formatting issues detected"
    if (!$DryRun) {
        dotnet format | Out-Null
        $fixed += "FORMAT: Auto-formatted code"
    }
}
Write-Host "  Done" -ForegroundColor Green

# Report
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  QUALITY GATE RESULTS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($issues.Count -eq 0) {
    Write-Host "✅ All checks passed!" -ForegroundColor Green
} else {
    Write-Host "❌ Found $($issues.Count) issue(s):" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "  - $issue" -ForegroundColor Yellow
    }
}

if ($fixed.Count -gt 0) {
    Write-Host ""
    Write-Host "🔧 Auto-fixed $($fixed.Count) issue(s):" -ForegroundColor Green
    foreach ($fix in $fixed) {
        Write-Host "  - $fix" -ForegroundColor Green
    }
}

if ($issues.Count -gt 0 -and $fixed.Count -lt $issues.Count) {
    Write-Host ""
    Write-Host "⚠️ Some issues require manual fix." -ForegroundColor Yellow
    Pop-Location
    exit 1
}

Pop-Location
exit 0

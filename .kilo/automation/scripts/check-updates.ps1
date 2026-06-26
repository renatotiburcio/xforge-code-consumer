$ErrorActionPreference = "Continue"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
$ConfigPath = Join-Path $Root ".xforge/config/sources-monitor.json"
$ReportPath = Join-Path $Root ".xforge/operations/update-check-report.json"

Write-Host "============================================"
Write-Host "XForge Sources Monitor - Update Checker"
Write-Host "============================================"
Write-Host ""

# Load config
if (!(Test-Path $ConfigPath)) {
    Write-Host "[ERROR] Config not found: $ConfigPath"
    exit 1
}

$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$report = @{
    timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
    categories = @()
    totalChecked = 0
    updatesFound = 0
    errors = @()
}

# Check each category
foreach ($category in $config.sources.PSObject.Properties) {
    $catName = $category.Name
    $catReport = @{
        name = $catName
        sources = @()
        checked = 0
        updates = 0
    }

    Write-Host "--- $catName ---"

    foreach ($source in $category.Value.PSObject.Properties) {
        $srcName = $source.Name
        $srcData = $source.Value
        $srcReport = @{
            name = $srcName
            displayName = $srcData.name
            status = "ok"
            updates = @()
        }

        foreach ($url in $srcData.urls) {
            try {
                $response = Invoke-WebRequest -Uri $url -TimeoutSec 10 -UseBasicParsing -ErrorAction SilentlyContinue
                if ($response.StatusCode -eq 200) {
                    # Check for update keywords in page content
                    $content = $response.Content.ToLower()
                    foreach ($keyword in $srcData.checkFor) {
                        if ($content -match $keyword.ToLower()) {
                            $srcReport.updates += $keyword
                        }
                    }
                    Write-Host "  [OK] $($srcData.name) - $($url)" -ForegroundColor Green
                } else {
                    Write-Host "  [WARN] $($srcData.name) - HTTP $($response.StatusCode)" -ForegroundColor Yellow
                    $srcReport.status = "warning"
                }
            } catch {
                Write-Host "  [ERROR] $($srcData.name) - $($_.Exception.Message)" -ForegroundColor Red
                $srcReport.status = "error"
                $report.errors += "$($srcData.name): $($_.Exception.Message)"
            }
            $catReport.checked++
            $config.totalChecked++
        }

        if ($srcReport.updates.Count -gt 0) {
            $srcReport.status = "updates-found"
            $catReport.updates += $srcReport.updates.Count
            $report.updatesFound += $srcReport.updates.Count
        }

        $catReport.sources += $srcReport
    }

    $report.categories += $catReport
    Write-Host ""
}

# Save report
$report | ConvertTo-Json -Depth 10 | Set-Content $ReportPath -Encoding UTF8

# Summary
Write-Host "============================================"
Write-Host "SUMMARY"
Write-Host "============================================"
Write-Host "Checked: $($report.totalChecked) URLs"
Write-Host "Updates found: $($report.updatesFound)"
Write-Host "Errors: $($report.errors.Count)"
Write-Host "Report saved to: $ReportPath"
Write-Host ""

if ($report.updatesFound -gt 0) {
    Write-Host "[ACTION] Updates found! Review report and update knowledge files." -ForegroundColor Yellow
}

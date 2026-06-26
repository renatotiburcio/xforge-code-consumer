$ErrorActionPreference = "Stop"
$skillsDir = Join-Path $PSScriptRoot "..\..\..\.kilo\skills"
$skillDirs = Get-ChildItem $skillsDir -Directory | Where-Object { $_.Name -ne '_template' }

$results = @()
foreach ($dir in $skillDirs) {
    $skillFile = Join-Path $dir.FullName "SKILL.md"
    if (!(Test-Path $skillFile)) { continue }
    $content = Get-Content $skillFile -Raw
    $totalLines = ($content -split "`n").Count
    $parts = $content -split '---'
    if ($parts.Count -lt 3) { continue }
    $body = ($parts[2..($parts.Count-1)] -join '---').Trim()
    $bodyLines = ($body -split "`n" | Where-Object { $_.Trim() -ne "" }).Count
    $name = $dir.Name
    $results += [PSCustomObject]@{
        Name = $name
        TotalLines = $totalLines
        BodyLines = $bodyLines
    }
}

$thin = $results | Where-Object { $_.BodyLines -le 12 } | Sort-Object BodyLines
$real = $results | Where-Object { $_.BodyLines -gt 12 } | Sort-Object BodyLines -Descending

Write-Host "TOTAL: $($results.Count) | REAL: $($real.Count) | THIN/PLACEHOLDER: $($thin.Count)"
Write-Host ""
Write-Host "=== THIN/PLACEHOLDER (body <= 12 lines) ==="
foreach ($t in $thin) { Write-Host "$($t.Name) ($($t.BodyLines) lines)" }
Write-Host ""
Write-Host "=== TOP 15 REAL (body > 12 lines) ==="
$top = $real | Select-Object -First 15
foreach ($r in $top) { Write-Host "$($r.Name) ($($r.BodyLines) lines)" }

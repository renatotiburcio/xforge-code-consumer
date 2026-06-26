$ErrorActionPreference = "Stop"
$root = Join-Path $PSScriptRoot "..\..\.."
$agentsDir = Join-Path $root ".kilo\agents"

$agentFiles = Get-ChildItem $agentsDir -Filter "*.md"
$renamed = 0
$skipped = 0

foreach ($file in $agentFiles) {
    $content = Get-Content $file.FullName -Raw
    $nameMatch = [regex]::Match($content, "(?m)^name:\s*(.+?)\s*$")
    if (!$nameMatch.Success) { $skipped++; continue }
    
    $frontmatterName = $nameMatch.Groups[1].Value.Trim()
    $expectedFile = "$frontmatterName.md"
    
    if ($file.Name -eq $expectedFile) {
        # Already correct
        continue
    }
    
    $newPath = Join-Path $agentsDir $expectedFile
    if (Test-Path $newPath) {
        Write-Host "  SKIP (target exists): $($file.Name) -> $expectedFile"
        $skipped++
        continue
    }
    
    Rename-Item -Path $file.FullName -NewName $expectedFile
    Write-Host "  RENAMED: $($file.Name) -> $expectedFile"
    $renamed++
}

Write-Host ""
Write-Host "Renamed: $renamed | Skipped: $skipped"

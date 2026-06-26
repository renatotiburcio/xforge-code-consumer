$ErrorActionPreference = "Stop"
$templateFile = Join-Path $PSScriptRoot "..\..\..\.kilo\skills\_template\SKILL.md"
$templateContent = Get-Content $templateFile -Raw
$parts = $templateContent -split '---'
$templateBody = ($parts[2..($parts.Count-1)] -join '---').Trim()

$skillsDir = Join-Path $PSScriptRoot "..\..\..\.kilo\skills"
$skillDirs = Get-ChildItem $skillsDir -Directory | Where-Object { $_.Name -ne '_template' }
$placeholders = @()
foreach ($dir in $skillDirs) {
    $skillFile = Join-Path $dir.FullName "SKILL.md"
    if (Test-Path $skillFile) {
        $content = Get-Content $skillFile -Raw
        $parts = $content -split '---'
        $body = ($parts[2..($parts.Count-1)] -join '---').Trim()
        if ($body -eq $templateBody) {
            $placeholders += $dir.Name
        }
    }
}
Write-Host "PLACEHOLDER_COUNT: $($placeholders.Count)"
foreach ($p in $placeholders) { Write-Host $p }

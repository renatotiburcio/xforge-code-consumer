$ErrorActionPreference = "Stop"
$root = Join-Path $PSScriptRoot "..\..\.."
$commandsDir = Join-Path $root ".kilo\commands"
$files = Get-ChildItem $commandsDir -Filter "*.md" -Recurse
$fixed = 0

foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw
    $needsAgent = $content -notmatch "(?m)^agent:"
    $needsDesc = $content -notmatch "(?m)^description:"
    
    if ($needsAgent -or $needsDesc) {
        $lines = $content -split "`n"
        $newLines = @()
        $inFront = $false
        $hasFront = $content.StartsWith("---")
        
        if ($hasFront) {
            # Has frontmatter, add missing fields
            $newLines += "---"
            $foundEnd = $false
            for ($i = 1; $i -lt $lines.Count; $i++) {
                if ($lines[$i].Trim() -eq "---" -and !$foundEnd) {
                    # End of frontmatter - insert missing fields before closing
                    if ($needsDesc) {
                        $name = $f.BaseName -replace "-", " "
                        $newLines += "description: $name"
                    }
                    if ($needsAgent) {
                        $newLines += "agent: code"
                    }
                    $newLines += "---"
                    $foundEnd = $true
                } elseif (!$foundEnd) {
                    $newLines += $lines[$i]
                } else {
                    $newLines += $lines[$i]
                }
            }
        } else {
            # No frontmatter at all - create it
            $name = $f.BaseName -replace "-", " "
            $newLines += "---"
            $newLines += "description: $name"
            $newLines += "agent: code"
            $newLines += "---"
            $newLines += ""
            $newLines += $lines
        }
        
        $newContent = $newLines -join "`n"
        Set-Content -Path $f.FullName -Value $newContent -NoNewline
        Write-Host "  FIXED: $($f.Name)"
        $fixed++
    }
}

Write-Host ""
Write-Host "Fixed: $fixed files"

$ErrorActionPreference = "Stop"
$root = Join-Path $PSScriptRoot "..\..\.."

Write-Host "=== NAMING AUDIT ==="
Write-Host ""

# 1. Skills: directory name must match frontmatter 'name'
Write-Host "--- Skills (dir name vs frontmatter name) ---"
$skillsDir = Join-Path $root ".kilo\skills"
$skillDirs = Get-ChildItem $skillsDir -Directory | Where-Object { $_.Name -ne "_template" }
$skillIssues = 0
foreach ($dir in $skillDirs) {
    $skillFile = Join-Path $dir.FullName "SKILL.md"
    if (!(Test-Path $skillFile)) { continue }
    $content = Get-Content $skillFile -Raw
    $nameMatch = [regex]::Match($content, "(?m)^name:\s*(.+?)\s*$")
    if ($nameMatch.Success) {
        $name = $nameMatch.Groups[1].Value.Trim()
        if ($name -ne $dir.Name) {
            Write-Host "  MISMATCH: dir='$($dir.Name)' frontmatter='$name'"
            $skillIssues++
        }
    }
}
Write-Host "  Total skills: $($skillDirs.Count) | Mismatches: $skillIssues"
Write-Host ""

# 2. Agents: file name (minus .md) should match frontmatter 'name'
Write-Host "--- Agents (filename vs frontmatter name) ---"
$agentsDir = Join-Path $root ".kilo\agents"
$agentFiles = Get-ChildItem $agentsDir -Filter "*.md"
$agentIssues = 0
foreach ($file in $agentFiles) {
    $content = Get-Content $file.FullName -Raw
    $nameMatch = [regex]::Match($content, "(?m)^name:\s*(.+?)\s*$")
    $expectedName = $file.BaseName
    if ($nameMatch.Success) {
        $name = $nameMatch.Groups[1].Value.Trim()
        if ($name -ne $expectedName) {
            Write-Host "  MISMATCH: file='$expectedName' frontmatter='$name'"
            $agentIssues++
        }
    }
}
Write-Host "  Total agents: $($agentFiles.Count) | Mismatches: $agentIssues"
Write-Host ""

# 3. Commands: check frontmatter
Write-Host "--- Commands (frontmatter check) ---"
$commandsDir = Join-Path $root ".kilo\commands"
$commandFiles = Get-ChildItem $commandsDir -Filter "*.md" -Recurse
$cmdNoAgent = 0
$cmdNoDesc = 0
foreach ($file in $commandFiles) {
    $content = Get-Content $file.FullName -Raw
    if ($content -notmatch "(?m)^agent:") { $cmdNoAgent++ }
    if ($content -notmatch "(?m)^description:") { $cmdNoDesc++ }
}
Write-Host "  Total commands: $($commandFiles.Count) | Missing agent: $cmdNoAgent | Missing description: $cmdNoDesc"
Write-Host ""

# 4. Skills: check for duplicate names
Write-Host "--- Skills: duplicate name check ---"
$names = @{}
$duplicates = @()
foreach ($dir in $skillDirs) {
    $skillFile = Join-Path $dir.FullName "SKILL.md"
    if (!(Test-Path $skillFile)) { continue }
    $content = Get-Content $skillFile -Raw
    $nameMatch = [regex]::Match($content, "(?m)^name:\s*(.+?)\s*$")
    if ($nameMatch.Success) {
        $name = $nameMatch.Groups[1].Value.Trim()
        if ($names.ContainsKey($name)) {
            $duplicates += $name
        } else {
            $names[$name] = $true
        }
    }
}
if ($duplicates.Count -gt 0) {
    foreach ($d in $duplicates) { Write-Host "  DUPLICATE: $d" }
} else {
    Write-Host "  No duplicates found"
}
Write-Host ""

# 5. Naming convention check (kebab-case)
Write-Host "--- Naming convention (kebab-case) ---"
$badNames = 0
foreach ($dir in $skillDirs) {
    if ($dir.Name -notmatch "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$") {
        Write-Host "  NOT KEBAB: $($dir.Name)"
        $badNames++
    }
}
foreach ($file in $agentFiles) {
    if ($file.BaseName -notmatch "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$") {
        Write-Host "  NOT KEBAB: $($file.BaseName)"
        $badNames++
    }
}
Write-Host "  Non-kebab names: $badNames"

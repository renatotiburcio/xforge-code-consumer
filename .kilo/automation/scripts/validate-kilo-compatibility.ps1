$ErrorActionPreference = "Stop"

Write-Host "Validating Kilo compatibility..."

if (!(Test-Path "AGENTS.md")) { throw "Missing AGENTS.md at project root." }
if (!(Test-Path "kilo.jsonc")) { throw "Missing kilo.jsonc at project root." }
if (!(Test-Path ".kilo/skills")) { throw "Missing .kilo/skills official skills directory." }
if (!(Test-Path ".kilo/commands")) { throw "Missing .kilo/commands official slash commands directory." }
if (!(Test-Path ".kilo/rules")) { throw "Missing .kilo/rules directory." }

$skillDirs = Get-ChildItem ".kilo/skills" -Directory
foreach ($dir in $skillDirs) {
    $skill = Join-Path $dir.FullName "SKILL.md"
    if (!(Test-Path $skill)) {
        throw "Missing SKILL.md in $($dir.FullName)"
    }

    $content = Get-Content $skill -Raw
    if (!$content.StartsWith("---")) {
        throw "Missing YAML frontmatter in $skill"
    }

    if ($content -notmatch "(?m)^name:\s*$($dir.Name)\s*$") {
        throw "Skill name must match directory name in $skill"
    }

    if ($content -notmatch "(?m)^description:\s*.+") {
        throw "Missing description in $skill"
    }
}

Write-Host "Kilo compatibility validation passed."

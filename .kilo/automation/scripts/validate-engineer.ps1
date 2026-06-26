$ErrorActionPreference = "Stop"

Write-Host "Validating XForge Enterprise Development OS..."

$required = @(
  "AGENTS.md",
  "kilo.jsonc",
  ".kilocodeignore",
  ".kilo/agents",
  ".kilo/skills",
  ".kilo/commands",
  ".kilo/rules",
  ".kilo/docs-html",
  ".xforge",
  ".xforge/engineer",
  ".xforge/memory",
  ".xforge/knowledge",
  ".xforge/project-dna"
)

foreach ($item in $required) {
  if (!(Test-Path $item)) {
    throw "Missing required item: $item"
  }
}

Write-Host "Validating skills..."
Get-ChildItem ".kilo/skills" -Directory | ForEach-Object {
  $skill = Join-Path $_.FullName "SKILL.md"
  if (!(Test-Path $skill)) { throw "Missing SKILL.md in $($_.Name)" }
  $content = Get-Content $skill -Raw
  if (!$content.StartsWith("---")) { throw "Missing frontmatter in $($_.Name)" }
  if ($content -notmatch "(?m)^name:\s*$([regex]::Escape($_.Name))\s*$") { throw "Skill name mismatch in $($_.Name)" }
  if ($content -notmatch "(?m)^description:\s*.+") { throw "Missing description in $($_.Name)" }
}

Write-Host "Engineer validation passed."

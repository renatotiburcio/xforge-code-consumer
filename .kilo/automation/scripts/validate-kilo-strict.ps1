$ErrorActionPreference = "Stop"

Write-Host "Validating strict Kilo config..."

if (!(Test-Path "kilo.jsonc")) {
    throw "Missing kilo.jsonc"
}

$content = Get-Content "kilo.jsonc" -Raw
$json = $content | ConvertFrom-Json

$allowed = @("instructions", "agent", "skills")
$props = $json.PSObject.Properties.Name

foreach ($p in $props) {
    if ($allowed -notcontains $p) {
        throw "Invalid key in kilo.jsonc: $p. Move XForge metadata to xforge-engineer.config.json"
    }
}

if ($props -notcontains "instructions") {
    throw "kilo.jsonc must contain instructions array"
}

if (!(Test-Path "AGENTS.md")) {
    throw "Missing AGENTS.md"
}

if (!(Test-Path ".kilo/rules")) {
    throw "Missing .kilo/rules"
}

Write-Host "Strict Kilo config validation passed."

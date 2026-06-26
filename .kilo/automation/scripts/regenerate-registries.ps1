#requires -Version 5.1
<#
.SYNOPSIS
    Regenera registries canonicos do filesystem real (skills/agents/rules/commands/knowledge).

.DESCRIPTION
    Le .kilo/skills/, .kilo/agents/, .kilo/rules/, .kilo/commands/ do filesystem
    e regenera .kilo/core/registries/skill-registry.json + expert-registry.json
    + rule-registry.json + command-registry.json com contagens reais.

.PARAMETER DryRun
    Apenas mostra o que faria, sem gravar.

.EXAMPLE
    .\.kilo\automation\scripts\regenerate-registries.ps1
#>

[CmdletBinding()]
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path

function Get-Description {
    param($path)
    if (-not (Test-Path $path)) { return "" }
    $content = Get-Content $path -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return "" }
    # Try YAML frontmatter description
    if ($content -match '(?s)^---\s*\n(.+?)\n---') {
        $fm = $Matches[1]
        if ($fm -match '(?m)^description:\s*(.+?)$') { return $Matches[1].Trim() }
    }
    # Fallback: first non-empty paragraph
    $lines = $content -split "`n" | Where-Object { $_.Trim() -ne "" -and $_ -notmatch "^#" -and $_ -notmatch "^---" } | Select-Object -First 1
    if ($lines) { return $lines.Trim() -replace '^#+\s*', '' }
    return ""
}

function Get-Category {
    param($path, $name)
    # Heuristic category based on name prefix or keywords
    if ($name -match "fiscal|sped|nfe|escrituracao|tributar") { return "Fiscal" }
    if ($name -match "contabil|accounting|sped-contabil|contabilidade") { return "Contábil" }
    if ($name -match "trabalhista|esocial|folha|rh|labor") { return "Trabalhista" }
    if ($name -match "lgpd|seguranc|security|auth|rbac|compliance") { return "Segurança" }
    if ($name -match "rag|knowledge|memory|learning|curation") { return "Conhecimento e Memória" }
    if ($name -match "dotnet|csharp|blazor|efcore|postgres|mysql|backend") { return "Backend" }
    if ($name -match "react|next|vue|angular|svelte|tailwind|frontend|ui") { return "Frontend" }
    if ($name -match "test|qa|quality|coverage") { return "Qualidade" }
    if ($name -match "git|devops|ci|release|deploy") { return "DevOps" }
    if ($name -match "agent|workflow|wizard|orchestrat") { return "Orquestração" }
    if ($name -match "product|market|competitor|ux|user|training") { return "Produto" }
    return "Geral"
}

function Update-Registry {
    param(
        [string]$RegistryPath,
        [string]$SourceDir,
        [string]$FilePattern,
        [string]$EntryIdPrefix,
        [string]$EntryType
    )

    Write-Host "Regenerating $RegistryPath from $SourceDir..." -ForegroundColor Cyan
    $entries = @()
    if (Test-Path $SourceDir) {
        $files = @(Get-ChildItem -LiteralPath $SourceDir -Recurse -File -Filter $FilePattern -Force -ErrorAction SilentlyContinue)
        foreach ($f in $files) {
            $name = $f.BaseName
            $relPath = $f.FullName.Replace("$ProjectRoot\", "").Replace("\", "/")
            $description = Get-Description $f.FullName
            $category = Get-Category -path $f.FullName -name $name
            $entries += [PSCustomObject]@{
                id = $name
                name = $name
                title = $name
                description = $description
                path = $relPath
                type = $EntryType
                category = $category
            }
        }
    }
    $entries = $entries | Sort-Object id

    $keyName = $EntryType + "s"
    $json = New-Object PSObject
    $json | Add-Member -NotePropertyName $keyName -NotePropertyValue $entries
    $jsonText = $json | ConvertTo-Json -Depth 5
    Write-Host "  Found $($entries.Count) $EntryType entries" -ForegroundColor Green

    if (-not $DryRun) {
        # Write without BOM (UTF-8 NoBOM)
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllText($(Resolve-Path $RegistryPath).Path, $jsonText, $utf8NoBom)
        Write-Host "  Written to $RegistryPath (UTF-8 NoBOM)" -ForegroundColor Green
    }
    return $entries.Count
}

# Skills
$skillCount = Update-Registry `
    -RegistryPath ".kilo/core/registries/skill-registry.json" `
    -SourceDir ".kilo/skills" `
    -FilePattern "SKILL.md" `
    -EntryIdPrefix "" `
    -EntryType "skill"

# Agents (root + genius-council)
$agentEntries = @()
foreach ($agentDir in @(".kilo/agents", ".kilo/agents/genius-council")) {
    if (Test-Path $agentDir) {
        $files = @(Get-ChildItem -LiteralPath $agentDir -File -Filter "*.md" -Force -ErrorAction SilentlyContinue)
        foreach ($f in $files) {
            $name = $f.BaseName
            $relPath = $f.FullName.Replace("$ProjectRoot\", "").Replace("\", "/")
            $description = Get-Description $f.FullName
            $category = if ($relPath -match "genius-council") { "Genius Council" } else { Get-Category -path $f.FullName -name $name }
            $agentEntries += [PSCustomObject]@{
                id = $name
                name = $name
                title = $name
                description = $description
                path = $relPath
                type = "agent"
                category = $category
            }
        }
    }
}
$agentEntries = $agentEntries | Sort-Object id
Write-Host "Regenerating expert-registry.json from .kilo/agents/..." -ForegroundColor Cyan
Write-Host "  Found $($agentEntries.Count) agent entries" -ForegroundColor Green
if (-not $DryRun) {
    $jsonObj = New-Object PSObject
    $jsonObj | Add-Member -NotePropertyName "experts" -NotePropertyValue $agentEntries
    $jsonText = $jsonObj | ConvertTo-Json -Depth 5
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText((Resolve-Path ".kilo/core/registries/expert-registry.json").Path, $jsonText, $utf8NoBom)
    Write-Host "  Written to .kilo/core/registries/expert-registry.json (UTF-8 NoBOM)" -ForegroundColor Green
}

# Rules
$ruleCount = Update-Registry `
    -RegistryPath ".kilo/core/registries/rule-registry.json" `
    -SourceDir ".kilo/rules" `
    -FilePattern "*.md" `
    -EntryIdPrefix "" `
    -EntryType "rule"

# Commands (root only, exclude workflows/)
$cmdEntries = @()
if (Test-Path ".kilo/commands") {
    $files = @(Get-ChildItem -LiteralPath ".kilo/commands" -File -Filter "*.md" -Force -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "workflows" })
    foreach ($f in $files) {
        $name = $f.BaseName
        $relPath = $f.FullName.Replace("$ProjectRoot\", "").Replace("\", "/")
        $description = Get-Description $f.FullName
        $category = Get-Category -path $f.FullName -name $name
        $cmdEntries += [PSCustomObject]@{
            id = $name
            name = $name
            title = $name
            description = $description
            path = $relPath
            type = "command"
            category = $category
        }
    }
}
$cmdEntries = $cmdEntries | Sort-Object id
Write-Host "Regenerating command-registry.json (preserve publicCommands)..." -ForegroundColor Cyan
Write-Host "  Found $($cmdEntries.Count) commands in filesystem" -ForegroundColor Green

# Preserve publicCommands from existing file (custom schema we don't model)
$cmdRegistryPath = ".kilo/core/registries/command-registry.json"
$existingPublic = @()
if (Test-Path $cmdRegistryPath) {
    try {
        $existing = Get-Content $cmdRegistryPath -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json
        if ($existing.publicCommands) { $existingPublic = $existing.publicCommands }
    } catch { }
}

if (-not $DryRun) {
    $jsonObj = New-Object PSObject
    $jsonObj | Add-Member -NotePropertyName "commands" -NotePropertyValue $cmdEntries
    if ($existingPublic.Count -gt 0) {
        $jsonObj | Add-Member -NotePropertyName "publicCommands" -NotePropertyValue $existingPublic
        Write-Host "  Preserved $($existingPublic.Count) publicCommands entries" -ForegroundColor Green
    }
    $jsonText = $jsonObj | ConvertTo-Json -Depth 10
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText((Resolve-Path $cmdRegistryPath).Path, $jsonText, $utf8NoBom)
    Write-Host "  Written to .kilo/core/registries/command-registry.json (UTF-8 NoBOM)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  skills:  $skillCount entries" -ForegroundColor Green
Write-Host "  agents:  $($agentEntries.Count) entries" -ForegroundColor Green
Write-Host "  rules:   $ruleCount entries" -ForegroundColor Green
Write-Host "  commands: $($cmdEntries.Count) entries (with publicCommands preserved)" -ForegroundColor Green
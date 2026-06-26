$ErrorActionPreference = "Stop"

Write-Host "XForge Engineer Doctor"
Write-Host "======================"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
Push-Location $Root
try {
$script:Errors = New-Object System.Collections.Generic.List[string]
$script:Warnings = New-Object System.Collections.Generic.List[string]

function Add-DoctorError {
    param([string]$Message)
    $script:Errors.Add($Message) | Out-Null
    Write-Host "[ERROR] $Message"
}

function Add-DoctorWarning {
    param([string]$Message)
    $script:Warnings.Add($Message) | Out-Null
    Write-Host "[WARN]  $Message"
}

function Add-DoctorOk {
    param([string]$Message)
    Write-Host "[OK]    $Message"
}

function Test-RequiredPath {
    param(
        [string]$Name,
        [string]$Path
    )
    if (Test-Path -LiteralPath $Path) {
        Add-DoctorOk $Name
    } else {
        Add-DoctorError "$Name missing at $Path"
    }
}

function Read-JsonFile {
    param([string]$Path)
    try {
        return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    } catch {
        Add-DoctorError "Invalid JSON: $Path ($($_.Exception.Message))"
        return $null
    }
}

function Get-JsonPaths {
    param($Value)
    $paths = New-Object System.Collections.Generic.List[string]
    function Visit {
        param($Node)
        if ($null -eq $Node) { return }
        if ($Node -is [System.Array]) {
            foreach ($item in $Node) { Visit $item }
            return
        }
        if ($Node -is [pscustomobject]) {
            foreach ($prop in $Node.PSObject.Properties) {
                if ($prop.Name -eq "path" -and $prop.Value -is [string]) {
                    $paths.Add($prop.Value) | Out-Null
                }
                if ($prop.Name -eq "files" -and $prop.Value -is [System.Array]) {
                    foreach ($file in $prop.Value) {
                        if ($file -is [string]) { $paths.Add($file) | Out-Null }
                    }
                }
                Visit $prop.Value
            }
        }
    }
    Visit $Value
    return $paths
}

function Test-FrontMatter {
    param(
        [string]$Path,
        [string[]]$RequiredKeys
    )
    $content = Get-Content -LiteralPath $Path -Raw
    if (!$content.StartsWith("---")) {
        Add-DoctorError "Missing YAML frontmatter: $Path"
        return
    }
    $end = $content.IndexOf("`n---", 3)
    if ($end -lt 0) {
        Add-DoctorError "Unclosed YAML frontmatter: $Path"
        return
    }
    $frontMatter = $content.Substring(3, $end - 3)
    foreach ($key in $RequiredKeys) {
        if ($frontMatter -notmatch "(?m)^\s*$([regex]::Escape($key))\s*:") {
Add-DoctorError ("Missing frontmatter key " + [char]39 + $key + [char]39 + ": $Path")
        }
    }
}

Write-Host ""
Write-Host "Required structure"
Test-RequiredPath "AGENTS.md" "AGENTS.md"
Test-RequiredPath "kilo.jsonc" "kilo.jsonc"
Test-RequiredPath ".kilocodeignore" ".kilocodeignore"
Test-RequiredPath ".kilo/commands" ".kilo/commands"
Test-RequiredPath ".kilo/agents" ".kilo/agents"
Test-RequiredPath ".kilo/skills" ".kilo/skills"
Test-RequiredPath ".kilo/rules" ".kilo/rules"
Test-RequiredPath ".xforge" ".xforge"
Test-RequiredPath ".xforge/rag" ".xforge/rag"
Test-RequiredPath "RAG config" ".xforge/rag/config.json"
Test-RequiredPath "RAG local script" ".kilo/automation/scripts/rag/rag_local.py"
Test-RequiredPath "RAG index script" ".kilo/automation/scripts/rag/index-local.ps1"
Test-RequiredPath "RAG query script" ".kilo/automation/scripts/rag/query-local.ps1"
Test-RequiredPath "RAG status script" ".kilo/automation/scripts/rag/status-index.ps1"
Test-RequiredPath "RAG validation script" ".kilo/automation/scripts/rag/validate-rag.ps1"
Test-RequiredPath "Knowledge INDEX" ".xforge/knowledge/INDEX.json"
Test-RequiredPath "Performance quick reference" ".xforge/config/router-quick-reference.md"
Test-RequiredPath "Ollama setup script" ".kilo/automation/scripts/ollama-setup.ps1"
Test-RequiredPath "Pre-commit gate" ".kilo/automation/scripts/pre-commit.ps1"
Test-RequiredPath "Dependency checker" ".kilo/automation/scripts/dependency-check.ps1"
Test-RequiredPath "Live dashboard" ".kilo/automation/scripts/live-dashboard.ps1"
Test-RequiredPath "Knowledge validation" ".kilo/automation/scripts/knowledge-validation.ps1"
Test-RequiredPath "Knowledge versioning" ".xforge/config/knowledge-versioning.json"
Test-RequiredPath "Error graph" ".xforge/knowledge/errors-solutions-graph.json"
Test-RequiredPath "Rules index" ".kilo/rules/00-xforge-rule-index.md"

Write-Host ""
Write-Host "kilo.jsonc"
$kiloConfig = Read-JsonFile "kilo.jsonc"
if ($null -ne $kiloConfig) {
    # Kilo Code CLI 1.0 (v7.3.46+, 2026-06-15) recognized top-level keys.
# Schema: https://app.kilo.ai/config.json
# Reference: https://kilo.ai/docs/customize
$allowed = @(
    '$schema',            # JSON Schema URL (https://app.kilo.ai/config.json)
    "model",              # Default model in provider/model format
    "provider",           # Provider-specific config (provider.<id>.options.<key>)
    "permission",         # Tool permission policy (allow/ask/deny)
    "formatter",          # Code formatter config (true|false|<tool>)
    "lsp",                # Language server config (true|false|<server>)
    "experimental",       # Experimental flags (e.g. openTelemetry)
    "disabled_providers", # Provider disable list
    "enabled_providers",  # Provider enable list
    "tools",              # Tool-specific toggles
    "mcp",                # MCP server config
    "agent",              # Custom agent overrides
    "instructions",       # Instruction file paths/globs
    "skills",             # Skill directory paths
    "commands",           # Command directory paths
    "workflows",          # Workflow directory paths
    "routing",            # Routing rules by complexity
    "contextWindow",      # Context window size
    "tui",                # TUI-specific config (Kilo CLI 1.0)
    "remote_control",     # Remote control flag (Kilo CLI 1.0)
    "watcher"              # File watcher config (Kilo CLI 1.0)
)
    $props = @($kiloConfig.PSObject.Properties.Name)
    foreach ($prop in $props) {
        if ($allowed -notcontains $prop) {
            Add-DoctorError "Unsupported key in kilo.jsonc: $prop"
        }
    }
    if ($props -notcontains "instructions") {
        Add-DoctorError "kilo.jsonc must contain an instructions array"
    } elseif ($kiloConfig.instructions -isnot [System.Array]) {
        Add-DoctorError "kilo.jsonc instructions must be an array"
    } else {
        foreach ($instruction in $kiloConfig.instructions) {
            $matches = @(Get-ChildItem -Path $instruction -ErrorAction SilentlyContinue)
            if ($matches.Count -eq 0) {
                Add-DoctorError "Instruction path does not resolve: $instruction"
            }
        }
        Add-DoctorOk "kilo.jsonc strict shape checked"
    }
}

Write-Host ""
Write-Host "Registries"
$registryRoot = ".kilo/core/registries"
if (Test-Path -LiteralPath $registryRoot) {
    $registryFiles = @(Get-ChildItem -LiteralPath $registryRoot -Filter "*.json")
    foreach ($registry in $registryFiles) {
        $json = Read-JsonFile $registry.FullName
        if ($null -eq $json) { continue }
        foreach ($path in (Get-JsonPaths $json)) {
            if ($path -match "^https?://") { continue }
            if (!(Test-Path -LiteralPath $path)) {
                Add-DoctorError "Registry path missing in $($registry.Name): $path"
            }
        }
    }
    Add-DoctorOk "$($registryFiles.Count) registry files parsed"
} else {
    Add-DoctorError "Registry root missing: $registryRoot"
}

Write-Host ""
Write-Host "Commands and workflows"
$commandFiles = @(Get-ChildItem -LiteralPath ".kilo/commands" -Filter "*.md" -ErrorAction SilentlyContinue)
$workflowFiles = @(Get-ChildItem -LiteralPath ".kilo/workflows" -Filter "*.md" -ErrorAction SilentlyContinue)
$commandNames = @{}
foreach ($file in $commandFiles) { $commandNames[$file.Name] = $true }
foreach ($workflow in $workflowFiles) {
    if (!$commandNames.ContainsKey($workflow.Name)) {
        Add-DoctorWarning "Workflow without matching command: $($workflow.Name)"
    }
}
Add-DoctorOk "$($commandFiles.Count) commands and $($workflowFiles.Count) workflows scanned"

$commandRegistryPath = ".kilo/core/registries/command-registry.json"
$commandRegistry = Read-JsonFile $commandRegistryPath
if ($null -ne $commandRegistry) {
    foreach ($publicCommand in @($commandRegistry.publicCommands)) {
        foreach ($route in @($publicCommand.routes)) {
            $routeFile = ".kilo/commands/$route.md"
            if (!(Test-Path -LiteralPath $routeFile)) {
                Add-DoctorError "Public command route missing for $($publicCommand.public): $routeFile"
            }
        }
    }
    Add-DoctorOk "Public command routes checked"
}

Write-Host ""
Write-Host "Agents"
$agentFiles = @(Get-ChildItem -LiteralPath ".kilo/agents" -Filter "*.md" -ErrorAction SilentlyContinue)
$agentNames = @{}
foreach ($agent in $agentFiles) {
    Test-FrontMatter -Path $agent.FullName -RequiredKeys @("name", "description")
    $content = Get-Content -LiteralPath $agent.FullName -Raw
    $nameMatch = [regex]::Match($content, "(?m)^name:\s*(.+?)\s*$")
    if ($nameMatch.Success) {
        $name = $nameMatch.Groups[1].Value.Trim()
        if ($agentNames.ContainsKey($name)) {
            Add-DoctorError "Duplicate agent name: $name"
        } else {
            $agentNames[$name] = $true
        }
    }
}
Add-DoctorOk "$($agentFiles.Count) agents scanned"

Write-Host ""
Write-Host "Skills"
$skillDirs = @(Get-ChildItem -LiteralPath ".kilo/skills" -Directory -ErrorAction SilentlyContinue)
foreach ($dir in $skillDirs) {
    $skillPath = Join-Path $dir.FullName "SKILL.md"
    if (!(Test-Path -LiteralPath $skillPath)) {
        Add-DoctorError "Missing SKILL.md in skill directory: $($dir.Name)"
        continue
    }
    Test-FrontMatter -Path $skillPath -RequiredKeys @("name", "description")
}
Add-DoctorOk "$($skillDirs.Count) skill directories scanned"

Write-Host ""
Write-Host "Encoding signals"
$mojibakeCount = 0
$mojibakeFiles = @()
if (Test-Path "AGENTS.md") { $mojibakeFiles += "AGENTS.md" }
if (Test-Path ".kilo/rules") { $mojibakeFiles += @(Get-ChildItem ".kilo/rules/*.md" | Select-Object -ExpandProperty FullName) }
if (Test-Path ".kilo/agents") { $mojibakeFiles += @(Get-ChildItem ".kilo/agents/*.md" | Select-Object -ExpandProperty FullName) }
foreach ($mf in $mojibakeFiles) {
    try {
        $reader = [System.IO.StreamReader]::new($mf, [System.Text.Encoding]::UTF8)
        $text = $reader.ReadToEnd()
        $reader.Close()
        # Check for double-encoded UTF-8 (actual mojibake)
        # Look for replacement character (U+FFFD) which indicates encoding issues
        if ($text.Contains([char]0xFFFD)) {
            $mojibakeCount++
        }
    } catch {}
}
if ($mojibakeCount -gt 0) {
    Add-DoctorWarning "Potential mojibake found in $mojibakeCount instruction/agent file(s)"
} else {
    Add-DoctorOk "No mojibake signal in core instruction files"
}

Write-Host "JSON registry encoding"
$jsonIssues = 0
$jsonFiles = @(Get-ChildItem -LiteralPath '.kilo/core/registries' -Filter '*.json' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName)
foreach ($jf in $jsonFiles) {
    try {
        $raw = [System.IO.File]::ReadAllBytes($jf)
        if ($raw.Length -ge 3 -and $raw[0] -eq 0xEF -and $raw[1] -eq 0xBB -and $raw[2] -eq 0xBF) {
            Add-DoctorError ("UTF-8 BOM found: " + $jf)
            $jsonIssues++
        } elseif ([System.Text.Encoding]::UTF8.GetString($raw).Contains([char]0xFFFD)) {
            Add-DoctorError ("Invalid UTF-8 bytes: " + $jf)
            $jsonIssues++
        }
    } catch {
        Add-DoctorError ("Cannot read encoding: " + $jf)
        $jsonIssues++
    }
}
if ($jsonIssues -gt 0) {
    Add-DoctorWarning ("Encoding issues in " + $jsonIssues + " JSON registry file(s)")
} elseif ($jsonFiles.Count -gt 0) {
    Add-DoctorOk ("All " + $jsonFiles.Count + " registry JSON files valid UTF-8")
}

Write-Host ""
Write-Host "Connectivity"
$configPath = Join-Path $env:USERPROFILE ".xforge\config.json"
if (!(Test-Path $configPath)) {
    Add-DoctorWarning "No global config at ~/.xforge/config.json"
} else {
    try {
        $globalConfig = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
        $activeProvider = $globalConfig.provider.active
        $activeModel = $globalConfig.provider.model
        Add-DoctorOk ("Config loaded: provider=" + $activeProvider + " model=" + $activeModel)
    } catch {
        Add-DoctorError ("Failed to parse config: " + $_.Exception.Message)
    }
}
if ($null -ne $kiloConfig -and $kiloConfig.routing -and $kiloConfig.routing.providers) {
    $kiloProviders = @($kiloConfig.routing.providers.PSObject.Properties.Name)
    Add-DoctorOk ("kilo.jsonc routing: " + $kiloProviders.Count + " provider(s) configured")
} else {
    $xforgeConfigPath = ".xforge/config/xforge-engineer.config.json"
    if (Test-Path -LiteralPath $xforgeConfigPath) {
        try {
            $xforgeConfig = Get-Content -LiteralPath $xforgeConfigPath -Raw | ConvertFrom-Json
            if ($xforgeConfig.routing -and $xforgeConfig.routing.providers) {
                $xProviders = @($xforgeConfig.routing.providers.PSObject.Properties.Name)
                Add-DoctorOk ("XForge routing: " + $xProviders.Count + " provider(s) in xforge-engineer.config.json")
            } else {
                Add-DoctorWarning "No routing.providers in kilo.jsonc or xforge-engineer.config.json"
            }
        } catch {
            Add-DoctorWarning "No routing.providers in kilo.jsonc (xforge config parse error)"
        }
    } else {
        Add-DoctorWarning "No routing.providers in kilo.jsonc and no xforge-engineer.config.json found"
    }
}


Write-Host ""
Write-Host "Quality gates"
$gitHooksOk = $true
if (Test-Path ".githooks/pre-commit") {
    Add-DoctorOk "Git hook pre-commit present"
} else {
    Add-DoctorWarning "Missing .githooks/pre-commit"
    $gitHooksOk = $false
}
if (Test-Path ".githooks/pre-push") {
    Add-DoctorOk "Git hook pre-push present"
} else {
    Add-DoctorWarning "Missing .githooks/pre-push"
    $gitHooksOk = $false
}
if (Test-Path ".xforge/tests/rag") {
    Add-DoctorOk "RAG test suite present"
} else {
    Add-DoctorWarning "Missing .xforge/tests/rag directory"
}
if (Test-Path ".xforge/rag/manifest.json") {
    Add-DoctorOk "RAG incremental cache manifest present"
} else {
    Add-DoctorWarning "Missing RAG cache manifest (run rag_cache.py to create)"
}
if (Test-Path ".xforge/scripts/verify-privacy.ps1") {
    Add-DoctorOk "Privacy verification script present"
} else {
    Add-DoctorWarning "Missing .xforge/scripts/verify-privacy.ps1"
}
if (Test-Path "docs/index.html") {
    Add-DoctorOk "Unified documentation present (docs/index.html)"
} else {
    Add-DoctorWarning "Missing docs/index.html"
}
if (Test-Path ".kilo/mcp") {
    $mcpCount = @(Get-ChildItem ".kilo/mcp/*.json" -ErrorAction SilentlyContinue).Count
    Add-DoctorOk ("MCP servers: " + $mcpCount + " configured")
} else {
    Add-DoctorWarning "Missing .kilo/mcp directory"
}

# Gate 4: Manual canonico DR-0181 (delegates to check-manual.ps1)
if (Test-Path ".kilo/automation/scripts/check-manual.ps1") {
    Write-Host ""
    Write-Host "Gate 4: Manual canonico DR-0181 (check-manual.ps1)..." -ForegroundColor Yellow
    & .\.kilo\automation\scripts\check-manual.ps1 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Add-DoctorError "Manual canonico (DR-0181) falhou - rode .\.kilo\automation\scripts\check-manual.ps1"
    } else {
        Add-DoctorOk "Manual canonico DR-0181 validado (check-manual.ps1)"
    }
} else {
    Add-DoctorWarning "Missing .kilo/automation/scripts/check-manual.ps1 (Gate 4 desabilitado)"
}

# Gate 5: Manual content depth DR-0182 (delegates to check-manual-content.ps1)
if (Test-Path ".kilo/automation/scripts/check-manual-content.ps1") {
    Write-Host ""
    Write-Host "Gate 5: Manual content depth DR-0182 (B-090)..." -ForegroundColor Yellow
    & .\.kilo\automation\scripts\check-manual-content.ps1 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Add-DoctorError "Manual content (DR-0182) falhou - rode .\.kilo\automation\scripts\check-manual-content.ps1"
    } else {
        Add-DoctorOk "Manual content DR-0182 validado (6 secoes, 3-7 exemplos, < 15 KB)"
    }
} else {
    Add-DoctorWarning "Missing .kilo/automation/scripts/check-manual-content.ps1 (Gate 5 desabilitado)"
}

Write-Host ""
Write-Host "Summary"
Write-Host "Errors  : $($script:Errors.Count)"
Write-Host "Warnings: $($script:Warnings.Count)"

if ($script:Errors.Count -gt 0) { exit 1 }
exit 0
}
finally {
    Pop-Location
}

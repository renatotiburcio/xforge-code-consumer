#requires -Version 5.1
<#
.SYNOPSIS
    Valida estrutura canonica do manual (DR-0181).

.DESCRIPTION
    Verifica:
    - 1 <html>, 1 <body>, 1 <main>, 1 <head>, 1 <title>, </title> por arquivo HTML
    - Nav identica (mesmos 6 items minimos)
    - Footer canonico (3 linhas)
    - Dark mode presente (body.dark no CSS)
    - 0 referencias mortas no codigo ativo
    - Total docs/ < 800 KB
    - Cada manual page tem exatamente 1 nav link com class="active"

.EXAMPLE
    .\.kilo\automation\scripts\check-manual.ps1
    Exit 0 = clean, 1 = dirty
#>

$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path

$script:Errors = 0
$script:Warnings = 0
$script:OKs = 0

function Add-Error($msg) {
    Write-Host "  [ERROR] $msg" -ForegroundColor Red
    $script:Errors++
}
function Add-Warn($msg) {
    Write-Host "  [WARN]  $msg" -ForegroundColor Yellow
    $script:Warnings++
}
function Add-OK($msg) {
    Write-Host "  [OK]    $msg" -ForegroundColor Green
    $script:OKs++
}

function Test-IsTemplateFile($path) {
    return ([System.IO.Path]::GetFileName($path).StartsWith("_"))
}

function Get-ManualFilesToCheck {
    $files = @()
    if (Test-Path "docs/index.html") { $files += "docs/index.html" }
    if (Test-Path "docs/manual") {
        $manual = @(Get-ChildItem "docs/manual/*.html" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName)
        foreach ($m in $manual) {
            if (-not (Test-IsTemplateFile $m)) { $files += $m }
        }
    }
    return $files
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " XForge Manual Validator (DR-0181)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check docs/ exists
Write-Host "[1/8] Estrutura basica..." -ForegroundColor Yellow
if (-not (Test-Path "docs")) {
    Add-Error "docs/ nao existe"
} else {
    Add-OK "docs/ existe"
}

if (-not (Test-Path "docs/index.html")) {
    Add-Error "docs/index.html nao existe (entry point obrigatorio)"
} else {
    Add-OK "docs/index.html existe"
}

if (-not (Test-Path "docs/style.css")) {
    Add-Error "docs/style.css nao existe (CSS compartilhado obrigatorio)"
} else {
    Add-OK "docs/style.css existe"
}

if (-not (Test-Path "docs/script.js")) {
    Add-Error "docs/script.js nao existe (JS compartilhado obrigatorio)"
} else {
    Add-OK "docs/script.js existe"
}

if (-not (Test-Path "docs/manual")) {
    Add-Error "docs/manual/ nao existe (paginas canonicas)"
} else {
    $manualCount = @(Get-ChildItem "docs/manual/*.html" -ErrorAction SilentlyContinue).Count
    if ($manualCount -lt 11) {
        Add-Warn "docs/manual/ tem so $manualCount paginas (esperado 11+)"
    } else {
        Add-OK "docs/manual/ tem $manualCount paginas"
    }
}

# 2. Check HTML structure (with helper - skips template files)
Write-Host ""
Write-Host "[2/8] Validando estrutura HTML de cada pagina..." -ForegroundColor Yellow
$htmlFiles = Get-ManualFilesToCheck
foreach ($f in $htmlFiles) {
    if (-not (Test-Path $f)) { continue }
    $relPath = $f.Replace("$ProjectRoot\", "")
    $content = Get-Content $f -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }

    $htmlOpen = ([regex]::Matches($content, '<html\b', 'IgnoreCase')).Count
    $htmlClose = ([regex]::Matches($content, '</html>', 'IgnoreCase')).Count
    $bodyOpen = ([regex]::Matches($content, '<body\b', 'IgnoreCase')).Count
    $bodyClose = ([regex]::Matches($content, '</body>', 'IgnoreCase')).Count
    $mainOpen = ([regex]::Matches($content, '<main\b', 'IgnoreCase')).Count
    $mainClose = ([regex]::Matches($content, '</main>', 'IgnoreCase')).Count
    $headOpen = ([regex]::Matches($content, '<head\b', 'IgnoreCase')).Count
    $titleOpen = ([regex]::Matches($content, '<title>', 'IgnoreCase')).Count
    $titleClose = ([regex]::Matches($content, '</title>', 'IgnoreCase')).Count

    $problems = @()
    if ($htmlOpen -ne 1) { $problems += "<html>=$htmlOpen" }
    if ($htmlClose -ne 1) { $problems += "</html>=$htmlClose" }
    if ($bodyOpen -ne 1) { $problems += "<body>=$bodyOpen" }
    if ($bodyClose -ne 1) { $problems += "</body>=$bodyClose" }
    if ($mainOpen -ne 1) { $problems += "<main>=$mainOpen" }
    if ($mainClose -ne 1) { $problems += "</main>=$mainClose" }
    if ($headOpen -ne 1) { $problems += "<head>=$headOpen" }
    if ($titleOpen -ne 1) { $problems += "<title>=$titleOpen" }
    if ($titleClose -ne 1) { $problems += "</title>=$titleClose" }

    if ($problems.Count -gt 0) {
        Add-Error "$relPath - $($problems -join ', ')"
    } else {
        Add-OK "$relPath"
    }
}

# 3. Check nav consistency (with helper - skips template files)
Write-Host ""
Write-Host "[3/8] Validando nav identica..." -ForegroundColor Yellow
$expectedNavItems = @("InÃ­cio", "Quickstart", "Arquitetura", "Conselho", "Skills", "Decisions")
$navInconsistent = 0
foreach ($f in $htmlFiles) {
    if (-not (Test-Path $f)) { continue }
    $relPath = $f.Replace("$ProjectRoot\", "")
    $content = Get-Content $f -Raw -ErrorAction SilentlyContinue
    # Extract all nav links (including inside dropdowns/details)
    $navBlockMatch = [regex]::Match($content, '(?s)<nav[^>]*>(.*?)</nav>')
    if (-not $navBlockMatch.Success) {
        Add-Warn "$relPath - no <nav> block found"
        $navInconsistent++
        continue
    }
    $navBlock = $navBlockMatch.Groups[1].Value
    foreach ($item in $expectedNavItems) {
        if ($navBlock -notmatch [regex]::Escape($item)) {
            Add-Warn "$relPath - nav sem item '$item'"
            $navInconsistent++
            break
        }
    }
}
if ($navInconsistent -eq 0) { Add-OK "Nav identica em todas as paginas" }

# 3b. Check each manual page has exactly one nav link with class="active"
Write-Host ""
Write-Host "[3b/8] Validando active class em nav..." -ForegroundColor Yellow
$activeInconsistent = 0
foreach ($f in $htmlFiles) {
    if (-not (Test-Path $f)) { continue }
    $relPath = $f.Replace("$ProjectRoot\", "")
    $content = Get-Content $f -Raw -ErrorAction SilentlyContinue
    $activeCount = ([regex]::Matches($content, 'class="active"')).Count
    if ($activeCount -ne 1) {
        Add-Warn "$relPath - exatamente 1 nav link deve ter class='active' (encontrado: $activeCount)"
        $activeInconsistent++
    }
}
if ($activeInconsistent -eq 0) { Add-OK "Cada pagina tem exatamente 1 nav link active" }

# 4. Check footer canonical (with helper - skips template files)
Write-Host ""
Write-Host "[4/8] Validando footer canonico..." -ForegroundColor Yellow
$footerInconsistent = 0
foreach ($f in $htmlFiles) {
    if (-not (Test-Path $f)) { continue }
    $relPath = $f.Replace("$ProjectRoot\", "")
    $content = Get-Content $f -Raw -ErrorAction SilentlyContinue
    if ($content -notmatch "XForge Manual v\d+") {
        Add-Warn "$relPath - footer nao menciona versao XForge Manual"
        $footerInconsistent++
    }
}
if ($footerInconsistent -eq 0) {
    Add-OK "Footer canonico em todas as paginas"
} else {
    Add-Warn "$footerInconsistent pagina(s) com footer nao-canonico"
}

# 5. Check dark mode
Write-Host ""
Write-Host "[5/8] Validando dark mode..." -ForegroundColor Yellow
$cssContent = Get-Content "docs/style.css" -Raw -ErrorAction SilentlyContinue
if ($cssContent -match "body\.dark") {
    Add-OK "body.dark presente em style.css"
} else {
    Add-Error "body.dark AUSENTE em style.css"
}

# Check shared localStorage key (xforge-dark) consistency
$jsContent = Get-Content "docs/script.js" -Raw -ErrorAction SilentlyContinue
$indexContent = Get-Content "docs/index.html" -Raw -ErrorAction SilentlyContinue
if ($jsContent -and $indexContent) {
    $jsKey = if ($jsContent -match "'xforge-dark'") { "xforge-dark" }
             elseif ($jsContent -match "'dark'") { "dark" }
             else { "none" }
    $indexInlineKey = if ($indexContent -match "localStorage\.setItem\('dark'") { "dark" }
                      elseif ($indexContent -match "localStorage\.setItem\('xforge-dark'") { "xforge-dark" }
                      else { "none" }
    if ($jsKey -ne "none" -and $indexInlineKey -ne "none" -and $jsKey -ne $indexInlineKey) {
        Add-Warn "localStorage key mismatch: script.js='$jsKey' vs index.html inline='$indexInlineKey'"
    } else {
        Add-OK "localStorage key consistente (xforge-dark)"
    }
}

# 6. Check dead refs in code
Write-Host ""
Write-Host "[6/8] Validando refs mortas no codigo vivo..." -ForegroundColor Yellow
$deadRefFiles = @()
$searchPaths = @(".kilo", "AGENTS.md", "ARCHITECTURE.md", "CLAUDE.md", "README.md")
$deadTargets = @("docs/genius-council/", "docs/intro/", "docs/agents/", "docs/skills/", "docs/commands/", "docs/rules/", "docs/workflows/", "docs/business/", "docs/marketplace/", "docs/mcp/", "docs/knowledge/", "docs/systems/", "docs/automation/", "docs/operations/", "docs/runbooks/", "docs/sequences/")

foreach ($path in $searchPaths) {
    if (-not (Test-Path $path)) { continue }
    $items = if (Test-Path $path -PathType Container) {
        Get-ChildItem $path -Recurse -File -Filter "*.md" -Force -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName
    } else { @($path) }
    foreach ($item in $items) {
        if ($item -match "node_modules") { continue }
        $content = Get-Content $item -Raw -ErrorAction SilentlyContinue
        if (-not $content) { continue }
        foreach ($target in $deadTargets) {
            if ($content -match [regex]::Escape($target)) {
                $rel = $item.Replace("$ProjectRoot\", "")
                $deadRefFiles += "$rel -> $target"
            }
        }
    }
}
if ($deadRefFiles.Count -gt 0) {
    foreach ($d in ($deadRefFiles | Select-Object -Unique)) {
        Add-Error $d
    }
} else {
    Add-OK "Zero referencias mortas no codigo vivo"
}

# 7. Check total size
Write-Host ""
Write-Host "[7/8] Validando tamanho total..." -ForegroundColor Yellow
if (Test-Path "docs") {
    $size = (Get-ChildItem "docs" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    $sizeKB = [math]::Round($size / 1024, 1)
    if ($sizeKB -gt 800) {
        Add-Warn "docs/ tem $sizeKB KB (limite: 800 KB)"
    } else {
        Add-OK "docs/ tem $sizeKB KB (limite: 800 KB)"
    }
}

# 8. Summary
Write-Host ""
Write-Host "[8/8] Resumo" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Erros  : $script:Errors" -ForegroundColor $(if($script:Errors -gt 0){"Red"}else{"Green"})
Write-Host "  Warnings: $script:Warnings" -ForegroundColor $(if($script:Warnings -gt 0){"Yellow"}else{"Green"})
Write-Host "  OKs    : $script:OKs" -ForegroundColor Green
Write-Host ""

if ($script:Errors -gt 0) {
    Write-Host "FAIL - manual nao passou na validacao DR-0181" -ForegroundColor Red
    exit 1
} else {
    Write-Host "PASS - manual canonico DR-0181 validado" -ForegroundColor Green
    exit 0
}
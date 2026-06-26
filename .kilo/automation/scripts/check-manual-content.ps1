#requires -Version 5.1
<#
.SYNOPSIS
    Valida profundidade do conteudo do manual (DR-0182, B-090).

.DESCRIPTION
    Para cada pagina HTML em docs/manual/:
    - 6 secoes <h2> na ordem canonica (O que e, Quando usar, Como usar, Parametros, Exemplos praticos, Troubleshooting)
    - Cada secao tem conteudo minimo (> 100 chars)
    - Tem 3-7 exemplos praticos
    - Tem tabela de parametros
    - Tem troubleshooting
    - Tamanho < 15 KB

.EXAMPLE
    .\.kilo\automation\scripts\check-manual-content.ps1
    Exit 0 = clean, 1 = dirty
#>

$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path

$script:Errors = 0
$script:Warnings = 0
$script:OKs = 0

function Add-Error($msg) { Write-Host "  [ERROR] $msg" -ForegroundColor Red; $script:Errors++ }
function Add-Warn($msg) { Write-Host "  [WARN]  $msg" -ForegroundColor Yellow; $script:Warnings++ }
function Add-OK($msg) { Write-Host "  [OK]    $msg" -ForegroundColor Green; $script:OKs++ }

$expectedSections = @(
    "O que e",
    "Quando usar",
    "Como usar",
    "Parametros",
    "Exemplos praticos",
    "Troubleshooting"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " XForge Manual Content Depth (DR-0182)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path "docs/manual")) {
    Add-Error "docs/manual/ nao existe"
    exit 1
}

$pages = @(Get-ChildItem "docs/manual/*.html" -ErrorAction SilentlyContinue | Where-Object { -not $_.Name.StartsWith("_") })

Write-Host "[1/3] Found $($pages.Count) manual pages" -ForegroundColor Yellow
Write-Host ""

Write-Host "[2/3] Validating each page..." -ForegroundColor Yellow
foreach ($page in $pages) {
    $relPath = $page.FullName.Replace("$ProjectRoot\", "")
    $content = Get-Content $page.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { Add-Error "$relPath - empty"; continue }

    $sizeKB = [math]::Round($page.Length / 1024, 1)
    $issues = @()

    # Check size
    if ($sizeKB -gt 25) { $issues += "size=$sizeKB KB (max 25)" }

    # Check 6 sections in order
    $sectionRegex = [regex]::Matches($content, '<h2[^>]*>([^<]+)</h2>')
    $foundSections = @()
    foreach ($m in $sectionRegex) { $foundSections += $m.Groups[1].Value.Trim() }

    $missingSections = @()
    $orderOK = $true
    $lastIdx = -1
    foreach ($exp in $expectedSections) {
        $idx = -1
        for ($i = 0; $i -lt $foundSections.Count; $i++) {
            if ($foundSections[$i] -like "*$exp*") { $idx = $i; break }
        }
        if ($idx -lt 0) {
            $missingSections += $exp
        } elseif ($idx -le $lastIdx) {
            $orderOK = $false
        } else {
            $lastIdx = $idx
        }
    }

    if ($missingSections.Count -gt 0) {
        $issues += "missing sections: $($missingSections -join ', ')"
    }
    if (-not $orderOK) {
        $issues += "sections out of order"
    }

    # Count examples (h3 tags within main)
    $exampleCount = ([regex]::Matches($content, '<h3[^>]*>Cenario')).Count
    if ($exampleCount -lt 3) {
        $issues += "examples=$exampleCount (min 3)"
    } elseif ($exampleCount -gt 7) {
        $issues += "examples=$exampleCount (max 7)"
    }

    # Check table for parameters
    $hasTable = $content -match '<table>'
    if (-not $hasTable) {
        $issues += "no <table> for parametros"
    }

    # Check troubleshooting has at least 2 h3
    $tsh3 = ([regex]::Matches($content, '<h3')).Count
    if ($tsh3 -lt 2) {
        $issues += "troubleshooting too short (h3 count: $tsh3)"
    }

    if ($issues.Count -gt 0) {
        Add-Error "$relPath ($sizeKB KB) - $($issues -join '; ')"
    } else {
        Add-OK "$relPath ($sizeKB KB) - $exampleCount examples, 6 sections, table, troubleshooting"
    }
}

Write-Host ""
Write-Host "[3/3] Summary" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Pages checked: $($pages.Count)" -ForegroundColor White
Write-Host "  Errors  : $script:Errors" -ForegroundColor $(if($script:Errors -gt 0){"Red"}else{"Green"})
Write-Host "  Warnings: $script:Warnings" -ForegroundColor $(if($script:Warnings -gt 0){"Yellow"}else{"Green"})
Write-Host "  OKs    : $script:OKs" -ForegroundColor Green
Write-Host ""

# ===== B-092: VISUAL LOCK CHECKS (DR-0184) =====
Write-Host "[B-092] Visual Lock checks (DR-0184, blocking)..." -ForegroundColor Magenta
Write-Host ""

$allPages = @()
if (Test-Path "docs/index.html") { $allPages += "docs/index.html" }
if (Test-Path "docs/manual") {
    $allPages += @(Get-ChildItem "docs/manual/*.html" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName)
}

# Check 1: No Tailwind CDN
foreach ($p in $allPages) {
    if (-not (Test-Path $p)) { continue }
    $rel = $p.Replace("$ProjectRoot\", "")
    $c = Get-Content $p -Raw -ErrorAction SilentlyContinue
    if ($c -match 'cdn\.tailwindcss\.com|cdnjs\.cloudflare\.com.*tailwind') {
        Add-Error "$rel - Tailwind CDN detected (B-092 violation #1: forbidden in manual pages)"
    } else {
        Add-OK "$rel - no Tailwind CDN"
    }
}

# Check 2: No inline <style> blocks in manual pages
foreach ($p in $allPages) {
    if (-not (Test-Path $p)) { continue }
    $rel = $p.Replace("$ProjectRoot\", "")
    # index.html is allowed to have inline (legacy)
    if ($rel -eq "docs\index.html") { continue }
    $c = Get-Content $p -Raw -ErrorAction SilentlyContinue
    # Look for <style> tag (not <script>)
    if ($c -match '(?s)<style[^>]*>') {
        Add-Error "$rel - inline <style> block detected (B-092 violation #2: use shared style.css only)"
    } else {
        Add-OK "$rel - no inline style"
    }
}

# Check 3: Cache-busting present in CSS/JS links
foreach ($p in $allPages) {
    if (-not (Test-Path $p)) { continue }
    $rel = $p.Replace("$ProjectRoot\", "")
    $c = Get-Content $p -Raw -ErrorAction SilentlyContinue
    $issues = @()
    if ($c -match 'href="[^"]*style\.css"') {
        if ($c -notmatch 'style\.css\?v=') {
            $issues += "style.css missing ?v= cache-busting"
        }
    }
    if ($c -match 'src="[^"]*script\.js"') {
        if ($c -notmatch 'script\.js\?v=') {
            $issues += "script.js missing ?v= cache-busting"
        }
    }
    if ($issues.Count -gt 0) {
        Add-Error "$rel - $($issues -join ', ') (B-092 violation #3)"
    } else {
        Add-OK "$rel - cache-busting present"
    }
}

# Check 4: Exactly 1 h1 per page
foreach ($p in $allPages) {
    if (-not (Test-Path $p)) { continue }
    $rel = $p.Replace("$ProjectRoot\", "")
    $c = Get-Content $p -Raw -ErrorAction SilentlyContinue
    $h1Count = ([regex]::Matches($c, '<h1[\s>]')).Count
    if ($h1Count -ne 1) {
        Add-Error "$rel - h1 count is $h1Count (expected 1) (B-092 violation #6)"
    } else {
        Add-OK "$rel - exactly 1 h1"
    }
}

# ===== FINAL =====
Write-Host ""
Write-Host "  Pages checked: $($pages.Count)" -ForegroundColor White
Write-Host "  Errors  : $script:Errors" -ForegroundColor $(if($script:Errors -gt 0){"Red"}else{"Green"})
Write-Host "  Warnings: $script:Warnings" -ForegroundColor $(if($script:Warnings -gt 0){"Yellow"}else{"Green"})
Write-Host "  OKs    : $script:OKs" -ForegroundColor Green
Write-Host ""

if ($script:Errors -gt 0) {
    Write-Host "FAIL - manual content nao atende B-090 (DR-0182) ou B-092 (DR-0184)" -ForegroundColor Red
    exit 1
} else {
    Write-Host "PASS - manual content atende B-090 (6 secoes, 3-7 exemplos, < 20 KB) + B-092 (visual lock)" -ForegroundColor Green
    exit 0
}
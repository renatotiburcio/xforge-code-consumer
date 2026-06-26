# XForge Knowledge Validation
# Validates that knowledge files contain accurate, up-to-date information

param(
    [switch]$Fix,
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
Push-Location $Root

Write-Host "XForge Knowledge Validation" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host ""

$issues = @()
$validated = 0

# 1. Validate INSS tables
Write-Host "[1/6] Validating INSS tables..." -ForegroundColor Yellow
$inssFile = ".xforge/knowledge/dominios/trabalhista/tabela-inss-2025.md"
if (Test-Path $inssFile) {
    $content = Get-Content $inssFile -Raw
    $hasAliquotas = ($content -match "7[.,]5%") -and ($content -match "9[.,]?0?%") -and ($content -match "12[.,]?0?%") -and ($content -match "14[.,]?0?%")
    $hasTeto = $content -match "teto" -or $content -match "Teto"
    $hasFaixas = $content -match "faixa" -or $content -match "Faixa"

    if ($hasAliquotas -and $hasTeto -and $hasFaixas) {
        Write-Host "  OK INSS 2025: aliquotas, teto, faixas OK" -ForegroundColor Green
        $validated++
    } else {
        $issues += "INSS 2025: Missing required data"
        Write-Host "  WARN INSS 2025: Incomplete data" -ForegroundColor Yellow
    }
} else {
    $issues += "INSS 2025: File not found"
    Write-Host "  FAIL INSS 2025: File not found" -ForegroundColor Red
}

# 2. Validate IRRF tables
Write-Host "[2/6] Validating IRRF tables..." -ForegroundColor Yellow
$irrfFile = ".xforge/knowledge/dominios/trabalhista/tabela-irrf-2025.md"
if (Test-Path $irrfFile) {
    $content = Get-Content $irrfFile -Raw
    $hasIsencao = $content -match "2\.259" -or $content -match "isencao"
    $hasFaixas = $content -match "faixa" -or $content -match "aliquota"

    if ($hasIsencao -and $hasFaixas) {
        Write-Host "  OK IRRF 2025: isencao e faixas OK" -ForegroundColor Green
        $validated++
    } else {
        $issues += "IRRF 2025: Missing required data"
        Write-Host "  WARN IRRF 2025: Incomplete data" -ForegroundColor Yellow
    }
} else {
    $issues += "IRRF 2025: File not found"
    Write-Host "  FAIL IRRF 2025: File not found" -ForegroundColor Red
}

# 3. Validate eSocial layout
Write-Host "[3/6] Validating eSocial layout..." -ForegroundColor Yellow
$esocialFile = ".xforge/knowledge/dominios/trabalhista/esocial-geral.md"
if (Test-Path $esocialFile) {
    $content = Get-Content $esocialFile -Raw
    $hasEvents = $content -match "S-1" -or $content -match "eventos"
    $hasLayout = $content -match "layout" -or $content -match "Layout"

    if ($hasEvents -and $hasLayout) {
        Write-Host "  OK eSocial: eventos e layout OK" -ForegroundColor Green
        $validated++
    } else {
        $issues += "eSocial: Missing event types or layout info"
        Write-Host "  WARN eSocial: Incomplete data" -ForegroundColor Yellow
    }
} else {
    $issues += "eSocial: File not found"
    Write-Host "  FAIL eSocial: File not found" -ForegroundColor Red
}

# 4. Validate NF-e version
Write-Host "[4/6] Validating NF-e version..." -ForegroundColor Yellow
$nfeFile = ".xforge/knowledge/dominios/fiscal/nfe.md"
if (Test-Path $nfeFile) {
    $content = Get-Content $nfeFile -Raw
    $hasVersion = $content -match "4\.00" -or $content -match "versao 4"

    if ($hasVersion) {
        Write-Host "  OK NF-e: version 4.00 OK" -ForegroundColor Green
        $validated++
    } else {
        $issues += "NF-e: Version info missing or outdated"
        Write-Host "  WARN NF-e: Version info missing" -ForegroundColor Yellow
    }
} else {
    $issues += "NF-e: File not found"
    Write-Host "  FAIL NF-e: File not found" -ForegroundColor Red
}

# 5. Validate Reforma Tributaria
Write-Host "[5/6] Validating Reforma Tributaria..." -ForegroundColor Yellow
$reformaFile = ".xforge/knowledge/dominios/fiscal/reforma-tributaria-completa.md"
if (Test-Path $reformaFile) {
    $content = Get-Content $reformaFile -Raw
    $hasIBS = $content -match "IBS"
    $hasCBS = $content -match "CBS"
    $hasTimeline = $content -match "2026" -or $content -match "2033"

    if ($hasIBS -and $hasCBS -and $hasTimeline) {
        Write-Host "  OK Reforma Tributaria: IBS, CBS, timeline OK" -ForegroundColor Green
        $validated++
    } else {
        $issues += "Reforma Tributaria: Missing IBS/CBS/timeline"
        Write-Host "  WARN Reforma Tributaria: Incomplete data" -ForegroundColor Yellow
    }
} else {
    $issues += "Reforma Tributaria: File not found"
    Write-Host "  FAIL Reforma Tributaria: File not found" -ForegroundColor Red
}

# 6. Validate CNPJ Alfanumerico
Write-Host "[6/6] Validating CNPJ Alfanumerico..." -ForegroundColor Yellow
$cnpjFile = ".xforge/knowledge/dominios/fiscal/cnpj-alfanumerico.md"
if (Test-Path $cnpjFile) {
    $content = Get-Content $cnpjFile -Raw
    $hasDeadline = $content -match "2030" -or $content -match "obrigat"
    $hasMigration = $content -match "migra" -or $content -match "dispon"

    if ($hasDeadline -and $hasMigration) {
        Write-Host "  OK CNPJ Alfanumerico: deadline e migracao OK" -ForegroundColor Green
        $validated++
    } else {
        $issues += "CNPJ Alfanumerico: Missing deadline or migration info"
        Write-Host "  WARN CNPJ Alfanumerico: Incomplete data" -ForegroundColor Yellow
    }
} else {
    $issues += "CNPJ Alfanumerico: File not found"
    Write-Host "  FAIL CNPJ Alfanumerico: File not found" -ForegroundColor Red
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  KNOWLEDGE VALIDATION RESULTS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Validated: $validated/6" -ForegroundColor $(if ($validated -eq 6) { "Green" } else { "Yellow" })

if ($issues.Count -gt 0) {
    Write-Host "  Issues: $($issues.Count)" -ForegroundColor Yellow
    foreach ($issue in $issues) {
        Write-Host "    - $issue" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "  Some knowledge files may need updating." -ForegroundColor Yellow
    Write-Host "  Run: .\.kilo\automation\scripts\check-updates.ps1" -ForegroundColor Cyan
} else {
    Write-Host "  All knowledge files validated successfully!" -ForegroundColor Green
}

Pop-Location

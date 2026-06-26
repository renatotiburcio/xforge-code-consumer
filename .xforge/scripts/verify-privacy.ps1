$ErrorActionPreference = "Stop"

Write-Host "XForge Privacy Verification"
Write-Host "==========================="

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
$script:Findings = New-Object System.Collections.Generic.List[string]
$script:Warnings = New-Object System.Collections.Generic.List[string]

# Patterns for sensitive data
$patterns = @{
    "CPF"           = "[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}"
    "CNPJ"          = "[0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}"
    "Email"         = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    "Telefone"      = "\(\+?[0-9]{1,3}\)\s?[0-9]{4,5}-[0-9]{4}"
    "API Key (generic)" = "(?i)(api[_-]?key|apikey|secret|token|password)\s*[:=]\s*['""][^'""]{8,}['""]"
    "AWS Key"       = "AKIA[0-9A-Z]{16}"
    "Private Key"   = "-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----"
}

# Directories to scan
$scanDirs = @(".kilo", ".xforge", "scripts")

# Excluded paths
$excludePatterns = @("*.pyc", "__pycache__", "node_modules", ".git", "rag/index")

$totalFiles = 0
$flaggedFiles = 0

foreach ($dir in $scanDirs) {
    if (!(Test-Path $dir)) { continue }
    
    $files = Get-ChildItem -Path $dir -Recurse -File -ErrorAction SilentlyContinue | 
        Where-Object { $exclude = $false; foreach ($p in $excludePatterns) { if ($_.FullName -like "*$p*") { $exclude = $true; break } }; -not $exclude }
    
    foreach ($file in $files) {
        $totalFiles++
        try {
            $content = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
            if ($null -eq $content) { continue }
            
            foreach ($entry in $patterns.GetEnumerator()) {
                $matches = [regex]::Matches($content, $entry.Value)
                if ($matches.Count -gt 0) {
                    $flaggedFiles++
                    $script:Findings.Add("[$($entry.Key)] $($file.FullName):$($matches.Count) match(es)")
                }
            }
        } catch {}
    }
}

# Check .gitignore for sensitive patterns
$gitignorePath = ".gitignore"
if (Test-Path $gitignorePath) {
    $gitignore = Get-Content $gitignorePath -Raw
    $sensitiveEntries = @(".env", "*.key", "*.pem", "credentials*", "secrets*")
    foreach ($entry in $sensitiveEntries) {
        if ($gitignore -notmatch [regex]::Escape($entry)) {
            $script:Warnings.Add(".gitignore missing sensitive pattern: $entry")
        }
    }
} else {
    $script:Warnings.Add("No .gitignore found")
}

# Report
Write-Host ""
Write-Host "Scan Results"
Write-Host "------------"
Write-Host "Files scanned : $totalFiles"
Write-Host "Files flagged : $flaggedFiles"

if ($script:Findings.Count -gt 0) {
    Write-Host ""
    Write-Host "[FINDINGS]" -ForegroundColor Red
    foreach ($f in $script:Findings) {
        Write-Host "  $f" -ForegroundColor Yellow
    }
}

if ($script:Warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "[WARNINGS]" -ForegroundColor Yellow
    foreach ($w in $script:Warnings) {
        Write-Host "  $w" -ForegroundColor DarkYellow
    }
}

if ($script:Findings.Count -eq 0 -and $script:Warnings.Count -eq 0) {
    Write-Host "[OK] No privacy concerns detected." -ForegroundColor Green
}

Write-Host ""
if ($script:Findings.Count -gt 0) { exit 1 }
}
finally {
    Pop-Location
}
exit 0

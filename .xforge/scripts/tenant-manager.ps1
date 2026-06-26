$ErrorActionPreference = "Stop"

Write-Host "XForge Tenant Manager"
Write-Host "====================="

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
$TenantsDir = ".xforge/tenants"
$ActiveTenant = $env:XFORGE_TENANT

if ($ActiveTenant) {
    $tenantFile = Join-Path $TenantsDir "$ActiveTenant.json"
    if (Test-Path $tenantFile) {
        Write-Host "[OK] Active tenant: $ActiveTenant" -ForegroundColor Green
        $config = Get-Content $tenantFile -Raw | ConvertFrom-Json
        Write-Host "  Name:    $($config.name)"
        Write-Host "  Provider: $($config.provider.active)"
        Write-Host "  Model:   $($config.provider.model)"
        Write-Host "  RAG:     $(if ($config.rag.shared) { 'shared' } else { 'isolated' })"
    } else {
        Write-Host "[ERROR] Tenant config not found: $tenantFile" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[INFO] No XFORGE_TENANT env var set. Using default tenant." -ForegroundColor Yellow
    $ActiveTenant = "default"
}

# List all tenants
Write-Host ""
Write-Host "Available tenants:"
$tenantFiles = Get-ChildItem $TenantsDir -Filter "*.json"
foreach ($tf in $tenantFiles) {
    $t = Get-Content $tf.FullName -Raw | ConvertFrom-Json
    $marker = if ($t.id -eq $ActiveTenant) { " <- active" } else { "" }
    Write-Host "  $($t.id): $($t.name)$marker"
}

}
finally {
    Pop-Location
}
exit 0

$ErrorActionPreference = "Stop"

Write-Host "Validating XForge Golden Rules..."

$violations = @()

# MediatR package/reference check
Get-ChildItem -Recurse -Include "*.csproj","*.props","*.targets","*.cs" -ErrorAction SilentlyContinue | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    if ($content -match "MediatR" -and $content -notmatch "XForge\.MediatR") {
        $violations += "MediatR reference found: $($_.FullName)"
    }
}

# Preview package check
Get-ChildItem -Recurse -Include "*.csproj","package.json","Directory.Packages.props" -ErrorAction SilentlyContinue | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    if ($content -match "(preview|alpha|beta|rc|nightly)") {
        $violations += "Possible preview package found: $($_.FullName)"
    }
}

if ($violations.Count -gt 0) {
    $violations | ForEach-Object { Write-Host "[VIOLATION] $_" }
    throw "Golden Rules violations found."
}

Write-Host "Golden Rules validation passed."

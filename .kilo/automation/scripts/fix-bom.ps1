$registryPath = Join-Path $PSScriptRoot "..\..\..\.kilo\core\registries\expert-registry.json"
$content = [System.IO.File]::ReadAllText($registryPath, [System.Text.Encoding]::UTF8)
$content = $content.TrimStart([char]0xFEFF)
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($registryPath, $content, $utf8NoBom)
Write-Host "BOM removed from expert-registry.json"

$ErrorActionPreference = "Stop"
$root = Join-Path $PSScriptRoot "..\..\.."
$dirs = @(
    (Join-Path $root "AGENTS.md"),
    (Join-Path $root ".kilo\rules")
)

foreach ($item in $dirs) {
    if (Test-Path $item -PathType Leaf) {
        $files = @($item)
    } else {
        $files = @(Get-ChildItem $item -Filter "*.md" | Select-Object -ExpandProperty FullName)
    }
    foreach ($f in $files) {
        try {
            $reader = [System.IO.StreamReader]::new($f, [System.Text.Encoding]::UTF8)
            $text = $reader.ReadToEnd()
            $reader.Close()
            if ([regex]::new("[\u00C3\uFFFD]").IsMatch($text)) {
                Write-Host "MOJIBAKE: $f"
            }
        } catch {}
    }
}

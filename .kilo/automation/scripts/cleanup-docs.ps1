$ErrorActionPreference = "Continue"
$docsDir = "D:\dev\XForge-Development\terminal\.xforge\docs"

# Delete numbered revision directories (00-51)
$deleted = 0
$dirs = Get-ChildItem $docsDir -Directory
foreach ($d in $dirs) {
    if ($d.Name -match "^\d{2}-") {
        Remove-Item -Recurse -Force $d.FullName -ErrorAction SilentlyContinue
        Write-Host "DELETED: $($d.Name)"
        $deleted++
    }
}
Write-Host ""
Write-Host "Deleted $deleted numbered revision directories"

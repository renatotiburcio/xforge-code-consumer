param(
  [Parameter(Mandatory=$true)][string]$Url,
  [Parameter(Mandatory=$true)][string]$OutputFolder
)
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Path $OutputFolder -Force | Out-Null
$filename = [System.IO.Path]::GetFileName(($Url -split '\?')[0])
if ([string]::IsNullOrWhiteSpace($filename)) { $filename = "source.html" }
$out = Join-Path $OutputFolder $filename
Invoke-WebRequest -Uri $Url -OutFile $out
$hash = Get-FileHash $out -Algorithm SHA256
@{
  url = $Url
  file = $out
  sha256 = $hash.Hash
  collectedAt = (Get-Date).ToString("s")
} | ConvertTo-Json | Out-File (Join-Path $OutputFolder "manifest.json") -Encoding utf8
Write-Host "Collected: $out"

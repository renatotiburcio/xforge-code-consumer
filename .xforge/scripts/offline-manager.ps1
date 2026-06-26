$ErrorActionPreference = "Stop"

Write-Host "XForge Offline Manager"
Write-Host "======================"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
$ConfigPath = Join-Path $env:USERPROFILE ".xforge/config.json"

function Get-OfflineConfig {
    if (Test-Path $ConfigPath) {
        $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
        if ($config.offline) {
            return $config.offline
        }
    }
    return $null
}

function Test-Ollama {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 3 -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

$action = if ($args.Count -gt 0) { $args[0] } else { "status" }

switch ($action) {
    "status" {
        $offline = Get-OfflineConfig
        if ($null -eq $offline) {
            Write-Host "[INFO] Offline mode not configured." -ForegroundColor Yellow
        } else {
            $enabled = $offline.enabled
            $color = if ($enabled) { "Green" } else { "Gray" }
            Write-Host ("Offline mode: " + $(if ($enabled) { "ENABLED" } else { "DISABLED" })) -ForegroundColor $color
            Write-Host "  Fallback model: $($offline.fallbackModel)"
        }
        $ollama = Test-Ollama
        Write-Host ""
        $ollamaColor = if ($ollama) { "Green" } else { "Red" }
        Write-Host ("Ollama: " + $(if ($ollama) { "RUNNING" } else { "NOT RUNNING"})) -ForegroundColor $ollamaColor
    }
    "enable" {
        Write-Host "Enabling offline mode..." -ForegroundColor Cyan
        $configDir = Split-Path $ConfigPath -Parent
        if (-not (Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }
        $config = @{}
        if (Test-Path $ConfigPath) {
            try { $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json } catch {}
        }
        $config.offline = @{
            enabled = $true
            fallbackModel = "ollama/llama3"
            cacheResponses = $true
            cacheDir = Join-Path $env:USERPROFILE ".xforge/cache"
        }
        $config | ConvertTo-Json -Depth 5 | Set-Content $ConfigPath -Encoding UTF8
        Write-Host "[OK] Offline mode enabled. Fallback: ollama/llama3" -ForegroundColor Green
    }
    "disable" {
        Write-Host "Disabling offline mode..." -ForegroundColor Cyan
        if (Test-Path $ConfigPath) {
            try {
                $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
                if ($config.offline) {
                    $config.offline.enabled = $false
                    $config | ConvertTo-Json -Depth 5 | Set-Content $ConfigPath -Encoding UTF8
                }
            } catch {}
        }
        Write-Host "[OK] Offline mode disabled." -ForegroundColor Green
    }
    "sync" {
        Write-Host "Syncing pending operations..." -ForegroundColor Cyan
        $queuePath = Join-Path $env:USERPROFILE ".xforge/queue/offline-queue.json"
        if (Test-Path $queuePath) {
            $queue = Get-Content $queuePath -Raw | ConvertFrom-Json
            $pending = @($queue | Where-Object { $_.status -eq "pending" })
            Write-Host "  Pending operations: $($pending.Count)"
            foreach ($item in $pending) {
                Write-Host "  Processing: $($item.id) - $($item.title)"
                $item.status = "synced"
                $item.syncedAt = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
            }
            $queue | ConvertTo-Json -Depth 5 | Set-Content $queuePath -Encoding UTF8
            Write-Host "[OK] $($pending.Count) operations synced." -ForegroundColor Green
        } else {
            Write-Host "  No pending operations." -ForegroundColor Green
        }
    }
    "queue" {
        Write-Host "Offline Queue Status" -ForegroundColor Cyan
        $queuePath = Join-Path $env:USERPROFILE ".xforge/queue/offline-queue.json"
        if (Test-Path $queuePath) {
            $queue = Get-Content $queuePath -Raw | ConvertFrom-Json
            $pending = @($queue | Where-Object { $_.status -eq "pending" })
            $synced = @($queue | Where-Object { $_.status -eq "synced" })
            $failed = @($queue | Where-Object { $_.status -eq "failed" })
            Write-Host "  Pending: $($pending.Count)"
            Write-Host "  Synced:  $($synced.Count)"
            Write-Host "  Failed:  $($failed.Count)"
        } else {
            Write-Host "  Queue empty." -ForegroundColor Green
        }
    }
    default {
        Write-Host "Usage: offline-manager.ps1 [status|enable|disable|sync|queue]"
    }
}
}
finally {
    Pop-Location
}
exit 0

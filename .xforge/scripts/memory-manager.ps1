$ErrorActionPreference = "Stop"

Write-Host "XForge Memory Manager"
Write-Host "====================="

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
$MemoryDir = ".xforge/memory"
$SessionsDir = "$MemoryDir/sessions"

$action = if ($args.Count -gt 0) { $args[0] } else { "status" }

switch ($action) {
    "status" {
        Write-Host ""
        Write-Host "Memory Files:"
        $memoryFiles = Get-ChildItem $MemoryDir -Filter "*.md" -ErrorAction SilentlyContinue
        foreach ($f in $memoryFiles) {
            $size = $f.Length
            Write-Host ("  {0,-35} {1,6} bytes" -f $f.Name, $size)
        }

        Write-Host ""
        Write-Host "Sessions:"
        $sessions = Get-ChildItem $SessionsDir -Filter "*.md" -ErrorAction SilentlyContinue | Sort-Object Name -Descending
        foreach ($s in $sessions) {
            if ($s.Name -eq "_template.md") { continue }
            $name = $s.BaseName
            $size = $s.Length
            Write-Host ("  {0,-40} {1,6} bytes" -f $name, $size)
        }
        if ($sessions.Count -eq 1) { Write-Host "  (no sessions yet)" }

        Write-Host ""
        Write-Host "Index:"
        $indexPath = Join-Path $MemoryDir "index.json"
        if (Test-Path $indexPath) {
            $index = Get-Content $indexPath -Raw | ConvertFrom-Json
            Write-Host "  Version: $($index.version)"
            Write-Host "  Last updated: $($index.lastUpdated)"
            Write-Host "  Entries: $($index.entries.Count)"
        }
    }

    "save" {
        $sessionName = if ($args.Count -gt 1) { $args[1] } else { (Get-Date -Format "yyyy-MM-dd") + "-session" }
        $sessionFile = Join-Path $SessionsDir "$sessionName.md"

        Write-Host "Saving session: $sessionName" -ForegroundColor Cyan

        # Read template
        $template = Get-Content (Join-Path $SessionsDir "_template.md") -Raw
        $session = $template.Replace("{{DATE}}", (Get-Date -Format "yyyy-MM-dd"))
        $session = $session.Replace("{{OBJETIVO}}", "Session saved at $(Get-Date -Format 'HH:mm:ss')")

        [System.IO.File]::WriteAllText($sessionFile, $session, [System.Text.Encoding]::UTF8)
        Write-Host "[OK] Session saved: $sessionFile" -ForegroundColor Green
    }

    "search" {
        $query = if ($args.Count -gt 1) { $args[1] } else { "" }
        if ([string]::IsNullOrEmpty($query)) {
            Write-Host "Usage: memory-manager.ps1 search <term>"
            exit 1
        }

        Write-Host "Searching memory for: $query" -ForegroundColor Cyan
        $allFiles = Get-ChildItem $MemoryDir -Filter "*.md" -Recurse -ErrorAction SilentlyContinue
        foreach ($f in $allFiles) {
            $content = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
            if ($content -match [regex]::Escape($query)) {
                $rel = $f.FullName.Replace($Root + "\", "")
                $count = ([regex]::Matches($content, [regex]::Escape($query))).Count
                Write-Host ("  {0} ({1} matches)" -f $rel, $count)
            }
        }
    }

    "context" {
        Write-Host "Current Context:" -ForegroundColor Cyan
        $ctxFile = Join-Path $MemoryDir "current-context.md"
        if (Test-Path $ctxFile) {
            $content = [System.IO.File]::ReadAllText($ctxFile, [System.Text.Encoding]::UTF8)
            # Show first 30 lines
            $lines = $content -split "`n"
            for ($i = 0; $i -lt [Math]::Min(30, $lines.Count); $i++) {
                Write-Host $lines[$i]
            }
        }
    }

    default {
        Write-Host "Usage: memory-manager.ps1 [status|save|search|context]"
        Write-Host ""
        Write-Host "  status  - Show memory files and sessions"
        Write-Host "  save    - Save current session"
        Write-Host "  search  - Search memory for a term"
        Write-Host "  context - Show current project context"
    }
}

}
finally {
    Pop-Location
}
exit 0

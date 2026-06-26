# XForge Git Hooks Installer
# Run: powershell -File .githooks/install.ps1

Write-Host "Installing XForge git hooks..." -ForegroundColor Cyan

if (Test-Path ".git") {
    git config core.hooksPath .githooks
    Write-Host "[OK] Git hooks installed" -ForegroundColor Green
    Write-Host "  pre-commit: runs doctor.ps1" -ForegroundColor Gray
    Write-Host "  pre-push:   runs RAG health check" -ForegroundColor Gray
} else {
    Write-Host "[WARN] Not a git repo. Run 'git init' first." -ForegroundColor Yellow
}

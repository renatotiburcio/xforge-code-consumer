# XForge Ollama Setup — Split Architecture
# Hardware: 16GB VRAM, 32GB RAM, Ryzen 7 5700G
# Run once to install and configure all models

param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$OllamaUrl = "http://localhost:11434"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " XForge Ollama Setup — Split Architecture" -ForegroundColor Cyan
Write-Host " Optimized for: 16GB VRAM / 32GB RAM / Ryzen 7 5700G" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if Ollama is installed
Write-Host "[1/6] Checking Ollama installation..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "  OK: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "  Ollama not found. Installing..." -ForegroundColor Red
    winget install Ollama.Ollama --accept-package-agreements --accept-source-agreements
    Write-Host "  Please restart your terminal after installation." -ForegroundColor Yellow
    exit 0
}

# Step 2: Check if Ollama server is running
Write-Host "[2/6] Checking Ollama server..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$OllamaUrl/api/tags" -Method Get -ErrorAction Stop
    Write-Host "  OK: Server is running" -ForegroundColor Green
} catch {
    Write-Host "  Starting Ollama server..." -ForegroundColor Yellow
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 5
    Write-Host "  OK: Server started" -ForegroundColor Green
}

# Step 3: Set environment variables for optimal performance
Write-Host "[3/6] Configuring environment variables..." -ForegroundColor Yellow
[System.Environment]::SetEnvironmentVariable("OLLAMA_NUM_PARALLEL", "2", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_MAX_LOADED_MODELS", "2", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "24h", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_FLASH_ATTENTION", "1", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KV_CACHE_TYPE", "q8_0", "User")
Write-Host "  OK: Environment variables set" -ForegroundColor Green

# Step 4: Pull models
$models = @(
    @{ Name = "qwen2.5:7b"; Desc = "Router (intent classification)"; Size = "~4GB download" },
    @{ Name = "qwen2.5:14b"; Desc = "Fallback (medium tasks)"; Size = "~9GB download" },
    @{ Name = "qwen2.5:72b"; Desc = "Worker (full capability)"; Size = "~44GB download" },
    @{ Name = "nomic-embed-text"; Desc = "Embeddings (RAG)"; Size = "~274MB download" },
    @{ Name = "deepseek-coder-v2:16b"; Desc = "Code specialist"; Size = "~9GB download" }
)

Write-Host "[4/6] Pulling models (this may take a while)..." -ForegroundColor Yellow
foreach ($model in $models) {
    $exists = ollama list 2>&1 | Select-String $model.Name
    if ($exists -and !$Force) {
        Write-Host "  SKIP: $($model.Name) already installed" -ForegroundColor DarkGray
    } else {
        Write-Host "  Pulling $($model.Name) ($($model.Desc)) - $($model.Size)..." -ForegroundColor White
        ollama pull $model.Name
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  WARNING: Failed to pull $($model.Name)" -ForegroundColor Red
        } else {
            Write-Host "  OK: $($model.Name) installed" -ForegroundColor Green
        }
    }
}

# Step 5: Verify GPU offload
Write-Host "[5/6] Verifying GPU availability..." -ForegroundColor Yellow
try {
    $gpuInfo = nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK: GPU detected: $gpuInfo" -ForegroundColor Green
        Write-Host "  Note: qwen2.5:72b will offload ~35% of layers to GPU" -ForegroundColor DarkGray
    } else {
        Write-Host "  WARNING: nvidia-smi not found. GPU offload may not work." -ForegroundColor Yellow
        Write-Host "  CPU-only mode will be used (slower but functional)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  WARNING: Could not detect GPU info" -ForegroundColor Yellow
}

# Step 6: Pre-warm router model
Write-Host "[6/6] Pre-warming router model..." -ForegroundColor Yellow
try {
    ollama run qwen2.5:7b "Hello" --verbose 2>&1 | Out-Null
    Write-Host "  OK: Router model warmed up" -ForegroundColor Green
} catch {
    Write-Host "  WARNING: Could not warm up router model" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " Setup Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Models installed:" -ForegroundColor Cyan
ollama list
Write-Host ""
Write-Host "Split Architecture:" -ForegroundColor Cyan
Write-Host "  Router:  qwen2.5:7b    (Q4_0,  ~2GB VRAM, <2s)" -ForegroundColor White
Write-Host "  Worker:  qwen2.5:72b   (Q4_K_M, ~10GB VRAM, 10-30s)" -ForegroundColor White
Write-Host "  Fallback: qwen2.5:14b  (Q4_K_M, ~4GB VRAM)" -ForegroundColor White
Write-Host "  Embed:   nomic-embed-text (Q4_K_M, ~1GB VRAM)" -ForegroundColor White
Write-Host "  Code:    deepseek-coder-v2:16b (Q4_K_M, ~6GB VRAM)" -ForegroundColor White
Write-Host ""
Write-Host "Environment variables set:" -ForegroundColor Cyan
Write-Host "  OLLAMA_NUM_PARALLEL=2" -ForegroundColor White
Write-Host "  OLLAMA_MAX_LOADED_MODELS=2" -ForegroundColor White
Write-Host "  OLLAMA_FLASH_ATTENTION=1" -ForegroundColor White
Write-Host "  OLLAMA_KV_CACHE_TYPE=q8_0" -ForegroundColor White
Write-Host ""
Write-Host "Context budget: 32k tokens (optimal for CPU inference)" -ForegroundColor Cyan
Write-Host "  For rare complex tasks, override to 128k per-request" -ForegroundColor DarkGray

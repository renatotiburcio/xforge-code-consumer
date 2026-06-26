# validate-test-project.ps1
# Valida se o /document-execute executou corretamente o projeto-teste
# Uso: .\.xforge\test-project\validate-test-project.ps1

$ErrorActionPreference = "Continue"
$TestDir = ".xforge\test-project"
$ProjectDir = "$TestDir\.xforge\project"
$Checks = @()

Write-Host ""
Write-Host "=== VALIDACAO: /document-execute ===" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar BACKLOG.md
Write-Host "[1/7] Verificando BACKLOG.md..." -ForegroundColor Yellow
$BacklogPath = "$ProjectDir\BACKLOG.md"
if (Test-Path $BacklogPath) {
    $content = Get-Content $BacklogPath -Raw
    $doneCount = ([regex]::Matches($content, "\| done")).Count
    $pendingCount = ([regex]::Matches($content, "\| pending")).Count
    $blockedCount = ([regex]::Matches($content, "\| blocked")).Count
    $totalTasks = $doneCount + $pendingCount + $blockedCount
    
    if ($totalTasks -ge 8) {
        $Checks += @{ Name = "BACKLOG.md"; Status = "PASS"; Detail = "$totalTasks tarefas ($doneCount done, $pendingCount pending)" }
        Write-Host "  OK $totalTasks tarefas ($doneCount done, $pendingCount pending)" -ForegroundColor Green
    } else {
        $Checks += @{ Name = "BACKLOG.md"; Status = "FAIL"; Detail = "Apenas $totalTasks tarefas (esperado 8+)" }
        Write-Host "  FAIL Apenas $totalTasks tarefas" -ForegroundColor Red
    }
} else {
    $Checks += @{ Name = "BACKLOG.md"; Status = "FAIL"; Detail = "Arquivo nao existe" }
    Write-Host "  FAIL BACKLOG.md nao existe" -ForegroundColor Red
}

# 2. Verificar tarefas criadas
Write-Host "[2/7] Verificando tarefas criadas..." -ForegroundColor Yellow
$TaskFiles = Get-ChildItem "$ProjectDir\TASKS\*.md" -ErrorAction SilentlyContinue
$TaskCount = if ($TaskFiles) { $TaskFiles.Count } else { 0 }
if ($TaskCount -ge 5) {
    $Checks += @{ Name = "Tarefas"; Status = "PASS"; Detail = "$TaskCount arquivos de tarefa" }
    Write-Host "  OK $TaskCount arquivos de tarefa" -ForegroundColor Green
} else {
    $Checks += @{ Name = "Tarefas"; Status = "FAIL"; Detail = "Apenas $TaskCount tarefas (esperado 5+)" }
    Write-Host "  FAIL Apenas $TaskCount tarefas" -ForegroundColor Red
}

# 3. Verificar ProductService
Write-Host "[3/7] Verificando ProductService..." -ForegroundColor Yellow
$PSPath = "$TestDir\src\ProductService.cs"
if (Test-Path $PSPath) {
    $content = Get-Content $PSPath -Raw
    $hasInterface = $content -match "IProductService"
    $hasCRUD = ($content -match "GetById" -or $content -match "GetAll") -and ($content -match "Create" -or $content -match "Add") -and ($content -match "Update") -and ($content -match "Delete")
    
    if ($hasInterface -and $hasCRUD) {
        $Checks += @{ Name = "ProductService"; Status = "PASS"; Detail = "Interface + CRUD" }
        Write-Host "  OK Interface + CRUD" -ForegroundColor Green
    } else {
        $Checks += @{ Name = "ProductService"; Status = "WARN"; Detail = "Arquivo existe mas incompleto" }
        Write-Host "  WARN Incompleto (interface: $hasInterface, CRUD: $hasCRUD)" -ForegroundColor Yellow
    }
} else {
    $Checks += @{ Name = "ProductService"; Status = "FAIL"; Detail = "Arquivo nao existe" }
    Write-Host "  FAIL ProdutoService nao foi criado" -ForegroundColor Red
}

# 4. Verificar OrderService
Write-Host "[4/7] Verificando OrderService..." -ForegroundColor Yellow
$OSPath = "$TestDir\src\OrderService.cs"
if (Test-Path $OSPath) {
    $content = Get-Content $OSPath -Raw
    $hasInterface = $content -match "IOrderService"
    $hasCRUD = ($content -match "GetById" -or $content -match "GetAll") -and ($content -match "Create" -or $content -match "Add") -and ($content -match "Update") -and ($content -match "Delete")
    
    if ($hasInterface -and $hasCRUD) {
        $Checks += @{ Name = "OrderService"; Status = "PASS"; Detail = "Interface + CRUD" }
        Write-Host "  OK Interface + CRUD" -ForegroundColor Green
    } else {
        $Checks += @{ Name = "OrderService"; Status = "WARN"; Detail = "Incompleto" }
        Write-Host "  WARN Incompleto" -ForegroundColor Yellow
    }
} else {
    $Checks += @{ Name = "OrderService"; Status = "FAIL"; Detail = "Nao existe" }
    Write-Host "  FAIL OrderService nao foi criado" -ForegroundColor Red
}

# 5. Verificar testes
Write-Host "[5/7] Verificando testes..." -ForegroundColor Yellow
$TestFiles = Get-ChildItem "$TestDir\tests\*.cs" -ErrorAction SilentlyContinue
$TestFileCount = if ($TestFiles) { $TestFiles.Count } else { 0 }
if ($TestFileCount -ge 2) {
    $Checks += @{ Name = "Testes"; Status = "PASS"; Detail = "$TestFileCount arquivos de teste" }
    Write-Host "  OK $TestFileCount arquivos de teste" -ForegroundColor Green
} else {
    $Checks += @{ Name = "Testes"; Status = "FAIL"; Detail = "Apenas $TestFileCount (esperado 2+)" }
    Write-Host "  FAIL Apenas $TestFileCount arquivos de teste" -ForegroundColor Red
}

# 6. Verificar checkpoint
Write-Host "[6/7] Verificando checkpoint..." -ForegroundColor Yellow
$CheckpointPath = ".xforge\checkpoints\document-execute.json"
if (Test-Path $CheckpointPath) {
    try {
        $checkpoint = Get-Content $CheckpointPath -Raw | ConvertFrom-Json
        $doneTasks = $checkpoint.done.Count
        $Checks += @{ Name = "Checkpoint"; Status = "PASS"; Detail = "$doneTasks tarefas completas" }
        Write-Host "  OK Checkpoint existe ($doneTasks tarefas completas)" -ForegroundColor Green
    } catch {
        $Checks += @{ Name = "Checkpoint"; Status = "WARN"; Detail = "JSON invalido" }
        Write-Host "  WARN Checkpoint com JSON invalido" -ForegroundColor Yellow
    }
} else {
    $Checks += @{ Name = "Checkpoint"; Status = "WARN"; Detail = "Nao existe (pode ser ok se rodou em 1 sessao)" }
    Write-Host "  WARN Checkpoint nao existe" -ForegroundColor Yellow
}

# 7. Verificar STATUS.md
Write-Host "[7/7] Verificando STATUS.md..." -ForegroundColor Yellow
$StatusPath = "$ProjectDir\STATUS.md"
if (Test-Path $StatusPath) {
    $content = Get-Content $StatusPath -Raw
    $hasProgress = $content -match "Progresso|progress|done|complet"
    if ($hasProgress) {
        $Checks += @{ Name = "STATUS.md"; Status = "PASS"; Detail = "Atualizado" }
        Write-Host "  OK STATUS.md atualizado" -ForegroundColor Green
    } else {
        $Checks += @{ Name = "STATUS.md"; Status = "WARN"; Detail = "Existe mas sem progresso" }
        Write-Host "  WARN STATUS.md sem info de progresso" -ForegroundColor Yellow
    }
} else {
    $Checks += @{ Name = "STATUS.md"; Status = "FAIL"; Detail = "Nao existe" }
    Write-Host "  FAIL STATUS.md nao existe" -ForegroundColor Red
}

# Resumo
$Total = $Checks.Count
$Passed = ($Checks | Where-Object { $_.Status -eq "PASS" }).Count
$Failed = ($Checks | Where-Object { $_.Status -eq "FAIL" }).Count
$Warned = ($Checks | Where-Object { $_.Status -eq "WARN" }).Count

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RESULTADO DA VALIDACAO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
foreach ($check in $Checks) {
    $icon = switch ($check.Status) { "PASS" { "[OK]" } "WARN" { "[!!]" } "FAIL" { "[XX]" } }
    $color = switch ($check.Status) { "PASS" { "Green" } "WARN" { "Yellow" } "FAIL" { "Red" } }
    Write-Host "  $icon $($check.Name) - $($check.Detail)" -ForegroundColor $color
}
Write-Host ""
Write-Host "  Total: $Total | Pass: $Passed | Fail: $Failed | Warn: $Warned" -ForegroundColor Cyan

if ($Failed -eq 0) {
    Write-Host "  RESULTADO: SUCESSO - /document-execute funcionou!" -ForegroundColor Green
} else {
    Write-Host "  RESULTADO: FALHA - $Failed problemas encontrados" -ForegroundColor Red
}
Write-Host ""

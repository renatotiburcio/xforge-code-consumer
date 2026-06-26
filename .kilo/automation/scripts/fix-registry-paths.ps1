$ErrorActionPreference = "Stop"
$root = Join-Path $PSScriptRoot "..\..\.."
$registryPath = Join-Path $root ".kilo\core\registries\expert-registry.json"

$content = Get-Content $registryPath -Raw
$json = $content | ConvertFrom-Json

# Mapping of old PT-BR filenames to new EN filenames
$mapping = @{
    "provedor-ia-router.md" = "ai-provider-router.md"
    "diretor-sucesso-cliente.md" = "customer-success-director.md"
    "diretor-plataforma-dados.md" = "data-platform-director.md"
    "engenheiro-funcionalidade.md" = "development-feature-engineer.md"
    "diretor-arquitetura.md" = "director-architecture.md"
    "diretor-governanca.md" = "director-governance.md"
    "diretor-qualidade.md" = "director-quality.md"
    "diretor-runtime.md" = "director-runtime.md"
    "diretor-documentacao.md" = "documentation-director.md"
    "orquestrador-conselho-dominio.md" = "domain-board-orchestrator.md"
    "diretor-arquitetura-dotnet.md" = "dotnet-architecture-director.md"
    "diretor-produto-empresarial.md" = "enterprise-product-director.md"
    "diretor-frontend-designsystem.md" = "frontend-designsystem-director.md"
    "diretor-github-devops.md" = "github-devops-director.md"
    "engenheiro-ingestao-conhecimento.md" = "knowledge-ingestion-engineer.md"
    "curador-conhecimento-legado.md" = "legacy-knowledge-curator.md"
    "diretor-conformidade-legal.md" = "legal-compliance-director.md"
    "gerenciador-barramento-eventos.md" = "manager-event-bus.md"
    "gerenciador-memoria.md" = "manager-memory.md"
    "gerenciador-maquina-estados.md" = "manager-state-machine.md"
    "engenheiro-curador-memoria.md" = "memory-curator-engineer.md"
    "engenheiro-reconhecimento-projeto.md" = "project-recognition-engineer.md"
    "diretor-engenharia-qualidade.md" = "quality-engineering-director.md"
    "engenheiro-portoes-qualidade.md" = "quality-gates-engineer.md"
    "especialista-benchmark.md" = "specialist-benchmark.md"
    "especialista-dominio-erp.md" = "specialist-erp-domain.md"
    "especialista-curadoria-conhecimento.md" = "specialist-knowledge-curation.md"
    "especialista-motor-politica.md" = "specialist-policy-engine.md"
    "especialista-rbac.md" = "specialist-rbac.md"
    "especialista-engenharia-reversa.md" = "specialist-reverse-engineering.md"
    "especialista-suporte.md" = "specialist-support.md"
    "engenheiro-inteligencia-suporte.md" = "support-intelligence-engineer.md"
    "orquestrador-conselho-tecnico.md" = "technical-board-orchestrator.md"
    "diretor-academia-treinamento.md" = "training-academy-director.md"
}

$fixed = 0
foreach ($exp in $json.experts) {
    if ($exp.type -eq "agent") {
        $oldPath = $exp.path
        $fileName = Split-Path $oldPath -Leaf
        if ($mapping.ContainsKey($fileName)) {
            $newFileName = $mapping[$fileName]
            $exp.path = $oldPath -replace [regex]::Escape($fileName), $newFileName
            $fixed++
        }
    }
}

$json | ConvertTo-Json -Depth 10 | Set-Content $registryPath -Encoding UTF8
Write-Host "Fixed $fixed agent paths in expert-registry.json"

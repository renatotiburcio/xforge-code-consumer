"""
recognize.py - Project Recognition Engine

Detecta stack, dependencies, conventions, e gaps do projeto.
Gera .xforge/project-dna/PROJECT-DNA.md automaticamente.
"""
from pathlib import Path
import json
import re
from datetime import datetime


def detect_stack(project_root):
    """Detecta stack do projeto baseado em arquivos de manifesto."""
    stack = []

    # .NET
    if list(project_root.glob("*.csproj")) or list(project_root.glob("*.sln")):
        stack.append("dotnet")
    if list(project_root.glob("*.fsproj")):
        stack.append("fsharp")

    # Node.js
    if (project_root / "package.json").exists():
        stack.append("node")
    if (project_root / "angular.json").exists():
        stack.append("angular")
    if list(project_root.glob("next.config.*")):
        stack.append("nextjs")
    if list(project_root.glob("vite.config.*")):
        stack.append("vite")

    # Python
    if (project_root / "pyproject.toml").exists():
        stack.append("python")
    elif (project_root / "requirements.txt").exists() or list(project_root.glob("setup.py")):
        stack.append("python")

    # Go
    if (project_root / "go.mod").exists():
        stack.append("go")

    # Rust
    if (project_root / "Cargo.toml").exists():
        stack.append("rust")

    # Java
    if (project_root / "pom.xml").exists() or list(project_root.glob("build.gradle*")):
        stack.append("java")

    # Ruby
    if (project_root / "Gemfile").exists():
        stack.append("ruby")

    # PHP
    if (project_root / "composer.json").exists():
        stack.append("php")

    # HTML+Tailwind standalone
    if list(project_root.glob("*.html")) and not (project_root / "package.json").exists():
        stack.append("html-tailwind")

    return stack


def read_manifests(project_root):
    """Le manifestos do projeto."""
    manifests = {}

    # package.json
    pkg_json = project_root / "package.json"
    if pkg_json.exists():
        try:
            with open(pkg_json, encoding="utf-8") as f:
                manifests["package.json"] = json.load(f)
        except (json.JSONDecodeError, OSError):
            manifests["package.json"] = {"error": "invalid"}

    # pyproject.toml
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        try:
            with open(pyproject, encoding="utf-8") as f:
                content = f.read()
            manifests["pyproject.toml"] = {"raw": content}
        except OSError:
            manifests["pyproject.toml"] = {"error": "unreadable"}

    # *.csproj
    for csproj in project_root.glob("*.csproj"):
        try:
            with open(csproj, encoding="utf-8") as f:
                content = f.read()
            manifests[csproj.name] = {"raw": content}
        except OSError:
            pass

    # go.mod
    go_mod = project_root / "go.mod"
    if go_mod.exists():
        try:
            with open(go_mod, encoding="utf-8") as f:
                manifests["go.mod"] = {"raw": f.read()}
        except OSError:
            pass

    # Cargo.toml
    cargo = project_root / "Cargo.toml"
    if cargo.exists():
        try:
            with open(cargo, encoding="utf-8") as f:
                manifests["Cargo.toml"] = {"raw": f.read()}
        except OSError:
            pass

    return manifests


def detect_conventions(project_root, stack):
    """Detecta convencoes do projeto."""
    conventions = {
        "naming": "unknown",
        "test_framework": "unknown",
        "orm": "unknown",
        "directory_structure": "unknown",
        "has_tests": False,
        "has_ci_cd": False,
        "has_docker": False,
        "has_lgpd_compliance": False,
    }

    # Tests
    if any((project_root / p).exists() for p in ["tests", "test", "__tests__", "spec", "Tests"]):
        conventions["has_tests"] = True

    # CI/CD
    if (project_root / ".github" / "workflows").exists():
        conventions["has_ci_cd"] = True
    elif (project_root / ".gitlab-ci.yml").exists():
        conventions["has_ci_cd"] = True

    # Docker
    if (project_root / "Dockerfile").exists() or (project_root / "docker-compose.yml").exists():
        conventions["has_docker"] = True

    # Stack-specific
    if "dotnet" in stack:
        conventions["naming"] = "PascalCase (provavel .NET)"
        if list(project_root.rglob("*Test*.csproj")) or list(project_root.rglob("*Tests*.csproj")):
            conventions["test_framework"] = "xUnit (provavel)"
        if list(project_root.rglob("*Repository*.cs")):
            conventions["orm"] = "EF Core (provavel)"
        if any(p.name == "Domain" for p in project_root.rglob("Domain") if p.is_dir()):
            conventions["directory_structure"] = "Clean Architecture (4 camadas)"

    elif "node" in stack or "react" in stack or "nextjs" in stack:
        conventions["naming"] = "camelCase (provavel JS/TS)"
        if list(project_root.glob("vitest.config.*")):
            conventions["test_framework"] = "Vitest"
        elif list(project_root.glob("jest.config.*")):
            conventions["test_framework"] = "Jest"

    elif "python" in stack:
        conventions["naming"] = "snake_case (provavel Python)"
        if list(project_root.rglob("test_*.py")) or list(project_root.rglob("*_test.py")):
            conventions["test_framework"] = "pytest"
        if list(project_root.rglob("alembic")):
            conventions["orm"] = "SQLAlchemy + Alembic"

    elif "go" in stack:
        conventions["naming"] = "PascalCase (exports), camelCase (variaveis)"
        if list(project_root.rglob("*_test.go")):
            conventions["test_framework"] = "go test + testify"

    elif "rust" in stack:
        conventions["naming"] = "snake_case"
        conventions["test_framework"] = "cargo test"

    return conventions


def find_gaps(project_root, conventions, stack):
    """Detecta gaps no projeto."""
    gaps = []

    if not conventions["has_tests"]:
        gaps.append({
            "category": "qualidade",
            "severity": "alta",
            "issue": "Sem suite de testes",
            "recomendacao": "Adicionar testes (skill: testing-qa-expert)",
            "prioridade": "P1",
        })

    if not conventions["has_ci_cd"]:
        gaps.append({
            "category": "devops",
            "severity": "media",
            "issue": "Sem CI/CD",
            "recomendacao": "Setup GitHub Actions (skill: github-devops-director)",
            "prioridade": "P2",
        })

    if not conventions["has_docker"]:
        gaps.append({
            "category": "devops",
            "severity": "media",
            "issue": "Sem Docker",
            "recomendacao": "Adicionar Dockerfile (skill: devops-ci-cd-expert)",
            "prioridade": "P2",
        })

    if "dotnet" in stack and conventions["orm"] == "unknown":
        gaps.append({
            "category": "data",
            "severity": "baixa",
            "issue": "ORM nao detectado",
            "recomendacao": "Verificar EF Core / Dapper (skill: database-efcore-expert)",
            "prioridade": "P3",
        })

    return gaps


def suggest_skills(stack, conventions):
    """Sugere skills baseado em stack e convencoes."""
    skills = [
        "genius-council (GCF)",
        "software-development-expert",
    ]

    if "dotnet" in stack:
        skills.extend([
            "dotnet-standards",
            "csharp-clean-code-expert",
            "dotnet-enterprise-expert",
        ])
        if "Clean Architecture" in conventions.get("directory_structure", ""):
            skills.extend([
                "xforge-mediatr-cqrs-expert",
                "automapper-mapping-expert",
                "endpoints-cqrs-dtos-architecture-expert",
            ])
        skills.append("database-efcore-expert")

    if "node" in stack or "react" in stack or "nextjs" in stack:
        if "nextjs" in stack:
            skills.append("next-modern")
        elif "react" in stack:
            skills.append("react-modern")
        else:
            skills.append("node-modern")
        skills.extend([
            "frontend-ux-ui-expert",
            "accessibility-a11y-expert",
        ])

    if "python" in stack:
        skills.append("python-modern")
    if "go" in stack:
        skills.append("go-modern")
    if "rust" in stack:
        skills.append("rust-modern")
    if "java" in stack:
        skills.append("jvm-modern")
    if "angular" in stack:
        skills.append("angular-modern")

    skills.extend([
        "data-protection-lgpd-expert (LGPD compliance)",
        "github-devops-director (CI/CD)",
        "devops-ci-cd-expert (Docker, deploy)",
        "observability-runtime-expert (logs, metrics)",
    ])

    return list(set(skills))


def generate_dna(project_root, stack, manifests, conventions, gaps):
    """Gera PROJECT-DNA.md."""
    project_name = project_root.resolve().name
    primary_stack = stack[0] if stack else "unknown"

    manifest_summary = []
    if "package.json" in manifests:
        pkg = manifests["package.json"]
        if "name" in pkg:
            manifest_summary.append(f"- **package.json**: {pkg.get('name', 'unnamed')} v{pkg.get('version', '0.0.0')}")
        if "dependencies" in pkg:
            deps = list(pkg.get("dependencies", {}).keys())[:5]
            manifest_summary.append(f"  - Dependencies: {', '.join(deps)}")

    for csproj in [k for k in manifests if k.endswith(".csproj")]:
        manifest_summary.append(f"- **{csproj}**: .NET project")

    if "pyproject.toml" in manifests:
        manifest_summary.append("- **pyproject.toml**: Python project")
    if "go.mod" in manifests:
        manifest_summary.append("- **go.mod**: Go project")
    if "Cargo.toml" in manifests:
        manifest_summary.append("- **Cargo.toml**: Rust project")

    gaps_md = ""
    for g in gaps:
        gaps_md += f"- **[{g['severity'].upper()}/{g['prioridade']}]** {g['category']}: {g['issue']}\n  - Recomendacao: {g['recomendacao']}\n"

    conv_md = ""
    for k, v in conventions.items():
        if k.startswith("has_"):
            icon = "[OK]" if v else "[ ]"
            conv_md += f"- {icon} {k.replace('_', ' ').title()}\n"
        else:
            conv_md += f"- **{k.replace('_', ' ').title()}**: {v}\n"

    skills = suggest_skills(stack, conventions)
    skills_md = "\n".join([f"- {s}" for s in skills])

    proj_type = "Web" if any(s in stack for s in ["react", "nextjs", "angular", "vue", "svelte"]) else ("API/Servico" if "dotnet" in stack or "node" in stack else "Desconhecido")

    dna = f"""# PROJECT-DNA

**Gerado em**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Stack detectado**: {", ".join(stack) if stack else "unknown"}
**Stack primario**: {primary_stack}
**Projeto**: {project_name}

## Visao Geral

Projeto analisado automaticamente por `xforge recognize` (v3.0).

- **Nome**: {project_name}
- **Tipo**: {proj_type}
- **Dominio**: [a definir com usuario]

## Stack Detectado

{chr(10).join(manifest_summary) if manifest_summary else "Nenhum manifesto detectado"}

## Convencoes Detectadas

{conv_md}

## Lacunas (Gaps)

{gaps_md if gaps_md else "Nenhuma lacuna critica detectada."}

## Skills Aplicaveis (sugeridas por GCF)

{skills_md}

## Proximos Passos Recomendados

1. **Validar PROJECT-DNA**: revisar e ajustar com o time
2. **Rodar Doctor**: `xforge doctor` para validar setup
3. **Adotar Skills gradualmente**: instalar 1 skill por semana
4. **Aplicar GCF**: usar Conselho dos Genios para decisoes
5. **Documentar Decisoes**: cada DR em `.xforge/decisions/`

## Referencias

- GCF (Regra de Ouro Suprema): `.kilo/rules/02-genius-council-framework.md`
- Manual: `docs/SUMMARY.md`
- Multi-Stack (v1.5.0): DR-0034
- v3.0 Vision: DR-0057
- Skill de reconhecimento: `project-recognition-engineer`

## Comandos Uteis

```bash
xforge status   # Ver status de adocao
xforge doctor   # Validar setup
xforge upgrade  # Atualizar .kilo + .xforge
xforge recognize  # Re-analisar projeto (atualiza este arquivo)
xforge backup   # Backup do estado atual
```
"""
    return dna


def recognize(project_root=None):
    """Funcao principal de reconhecimento."""
    if project_root is None:
        project_root = Path.cwd()

    print(f"[XForge] Reconhecendo projeto em: {project_root}")

    stack = detect_stack(project_root)
    print(f"[XForge] Stack detectado: {', '.join(stack) if stack else 'nenhum'}")

    manifests = read_manifests(project_root)
    print(f"[XForge] Manifestos lidos: {len(manifests)}")

    conventions = detect_conventions(project_root, stack)

    gaps = find_gaps(project_root, conventions, stack)
    print(f"[XForge] Gaps detectados: {len(gaps)}")

    dna_dir = project_root / ".xforge" / "project-dna"
    dna_dir.mkdir(parents=True, exist_ok=True)

    dna_content = generate_dna(project_root, stack, manifests, conventions, gaps)
    dna_file = dna_dir / "PROJECT-DNA.md"
    dna_file.write_text(dna_content, encoding="utf-8")
    print(f"[XForge] PROJECT-DNA gerado em: {dna_file}")

    return {
        "stack": stack,
        "manifests": list(manifests.keys()),
        "conventions": conventions,
        "gaps": gaps,
        "dna_file": str(dna_file),
    }


if __name__ == "__main__":
    recognize()

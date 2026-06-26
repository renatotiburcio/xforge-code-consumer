"""Tests for xforge.recognize (Project Recognition Engine)."""
from pathlib import Path

import recognize


def test_detect_stack_dotnet(dotnet_project):
    stack = recognize.detect_stack(dotnet_project)
    assert "dotnet" in stack


def test_detect_stack_python(python_project):
    stack = recognize.detect_stack(python_project)
    assert "python" in stack


def test_detect_stack_node(node_project):
    stack = recognize.detect_stack(node_project)
    assert "node" in stack


def test_detect_stack_empty(tmp_project):
    stack = recognize.detect_stack(tmp_project)
    assert stack == []


def test_detect_stack_html_tailwind(tmp_project):
    (tmp_project / "index.html").write_text("<html></html>", encoding="utf-8")
    stack = recognize.detect_stack(tmp_project)
    assert "html-tailwind" in stack


def test_detect_stack_fsharp(tmp_project):
    (tmp_project / "Test.fsproj").write_text("<Project></Project>", encoding="utf-8")
    stack = recognize.detect_stack(tmp_project)
    assert "fsharp" in stack


def test_detect_stack_multi(tmp_project):
    """Multi-stack project (e.g., backend .NET + frontend node)."""
    (tmp_project / "api.csproj").write_text("<Project></Project>", encoding="utf-8")
    (tmp_project / "package.json").write_text("{}", encoding="utf-8")
    stack = recognize.detect_stack(tmp_project)
    assert "dotnet" in stack
    assert "node" in stack


def test_read_manifests_package_json(node_project):
    manifests = recognize.read_manifests(node_project)
    assert "package.json" in manifests
    assert manifests["package.json"]["name"] == "test-app"


def test_read_manifests_pyproject(python_project):
    manifests = recognize.read_manifests(python_project)
    assert "pyproject.toml" in manifests
    assert "raw" in manifests["pyproject.toml"]


def test_detect_conventions_dotnet_clean_arch(dotnet_project):
    conventions = recognize.detect_conventions(dotnet_project, ["dotnet"])
    assert conventions["has_tests"] is True
    assert "PascalCase" in conventions["naming"]
    assert "Clean Architecture" in conventions["directory_structure"]


def test_detect_conventions_python(python_project):
    conventions = recognize.detect_conventions(python_project, ["python"])
    assert "snake_case" in conventions["naming"]


def test_find_gaps_no_tests(tmp_project):
    conventions = recognize.detect_conventions(tmp_project, [])
    gaps = recognize.find_gaps(tmp_project, conventions, [])
    issues = [g["issue"] for g in gaps]
    assert any("testes" in i.lower() for i in issues)
    assert any("CI/CD" in i for i in issues)
    assert any("Docker" in i for i in issues)


def test_find_gaps_with_all(python_project):
    (python_project / "tests").mkdir()
    (python_project / ".github" / "workflows").mkdir(parents=True)
    (python_project / "Dockerfile").write_text("FROM python:3.13", encoding="utf-8")
    conventions = recognize.detect_conventions(python_project, ["python"])
    gaps = recognize.find_gaps(python_project, conventions, ["python"])
    assert gaps == []


def test_suggest_skills_dotnet():
    skills = recognize.suggest_skills(["dotnet"], {})
    assert "genius-council (GCF)" in skills
    assert "dotnet-standards" in skills
    assert "data-protection-lgpd-expert (LGPD compliance)" in skills


def test_suggest_skills_react():
    skills = recognize.suggest_skills(["node", "react"], {})
    assert "react-modern" in skills
    assert "frontend-ux-ui-expert" in skills


def test_suggest_skills_python():
    skills = recognize.suggest_skills(["python"], {})
    assert "python-modern" in skills


def test_recognize_generates_dna(tmp_project):
    """End-to-end: should generate PROJECT-DNA.md."""
    (tmp_project / ".xforge").mkdir()
    result = recognize.recognize(tmp_project)
    assert "stack" in result
    dna_file = Path(result["dna_file"])
    assert dna_file.exists()
    content = dna_file.read_text(encoding="utf-8")
    assert "PROJECT-DNA" in content
    assert "Stack Detectado" in content or "Stack detectado" in content


def test_recognize_dna_includes_gaps_section(tmp_project):
    (tmp_project / ".xforge").mkdir()
    recognize.recognize(tmp_project)
    dna_file = tmp_project / ".xforge" / "project-dna" / "PROJECT-DNA.md"
    content = dna_file.read_text(encoding="utf-8")
    assert "Lacunas" in content
    assert "Skills Aplicaveis" in content
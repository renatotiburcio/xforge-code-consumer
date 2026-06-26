# Public Commands

This is the official XForge public command surface for KiloCode.

## Canonical Commands

| Command | Purpose | Main routes |
| --- | --- | --- |
| /xforge | Universal router | xforge |
| /analisar-projeto | Project recognition | xforge-reconhecer-projeto, development-recognize-project |
| /criar-projeto | New project creation | xforge-criar-projeto-dotnet, xforge-configurar-postgresql |
| /desenvolver | Feature and implementation work | xforge-dev, xforge-orquestrar-especialistas |
| /qualidade | Quality gates and tests | xforge-validar-qualidade, xforge-e2e-visual, xforge-hard-premium-finalizar |
| /seguranca | Security gates | security-golden-rule-check, security-audit, security-release-gate |
| /conhecimento | Knowledge ingestion and search | xforge-ingerir-conhecimento, xforge-rag-hibrido, xforge-auditar-conhecimento |
| /memoria | Memory recovery and update | xforge-memoria, xforge-feedback-aprendizado, xforge-auditar-conhecimento |
| /documentacao | Docs and manuals | xforge-docs, xforge-atualizar-dashboard |
| /release | Release readiness | xforge-gerar-release, security-release-gate, xforge-hard-premium-finalizar, xforge-auditoria-final |
| /criar-template | Template creation from existing page | xforge-criar-template |
| /criar-agent | Agent creation with responsibilities | xforge-criar-agent |
| /criar-subagent | Subagent creation linked to parent | xforge-criar-subagent |
| /criar-skill | Skill creation with gap analysis | xforge-criar-skill |
| /criar-rule | Business/technical rule creation | xforge-criar-rule |
| /criar-spec | Technical specification creation | xforge-criar-spec |
| /criar-workflow | Multi-stage workflow creation | xforge-criar-workflow |
| /criar-sdd | Software Design Document creation | xforge-criar-sdd |
| /criar-harness | Test harness creation | xforge-criar-harness |

## Compatibility

Aliases and old commands are preserved for backward compatibility. They should not be advertised as the primary user interface.

## Maintenance Rule

Every route listed in .kilo/core/registries/command-registry.json must point to an existing Markdown file in .kilo/commands.

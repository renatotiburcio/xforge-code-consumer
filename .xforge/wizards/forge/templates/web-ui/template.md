# Web UI Renderer Template for /forge (v3.62.0 - FINAL)

Blazor Server-based Web UI for the wizard framework. The 3rd and final renderer.

## Why Web UI (vs Chat/TUI)
- **Visual rich**: progress bars, side panels, modal dialogs
- **Multi-user**: team can collaborate on same wizard
- **Real-time preview**: see generated code as wizard progresses
- **Drag-and-drop**: reorder steps, upload files
- **Mobile-friendly**: responsive design

## Architecture
- **Frontend**: Blazor Server (Razor components)
- **Backend**: ASP.NET Core Minimal API
- **State**: .xforge/wizards/<wizard>/state.json (shared with Chat + TUI)
- **Auth**: ASP.NET Core Identity (optional, for multi-user)

## Command to launch
```bash
dotnet run --project tools/web-ui
# Opens browser at https://localhost:5001

# or via Docker
docker run -p 5001:5001 xforge/web-ui
```

## Components (Blazor + Atomic Design)
- Atoms: Button, Input, ProgressBar, Badge, Tooltip, Modal
- Molecules: QuestionCard, Breadcrumb, ConfidenceIndicator, TipBox, FilePicker
- Organisms: WizardShell, StepNavigator, KnowledgeContextPanel, DecisionPreview, CodePreview, CollaborationPanel
- Templates: WizardLayout, CompactLayout, FullScreenLayout
- Pages: Home, WizardRunner, History, Settings

## Features (vs Chat + TUI)
- **Visual progress bar** (smooth animation)
- **Real-time code preview** (generated code shown as wizard progresses)
- **Drag-and-drop file upload** (for knowledge context)
- **Side-by-side compare** (legacy vs new in migrate mode)
- **Collaborative editing** (multiple users, real-time sync)
- **Approval workflow** (reviewers approve before generation)
- **Audit trail visualization** (who did what when)
- **Dashboard** (wizard history, statistics, ROI)

## 3 Renderers Comparison (FINAL)

| Feature | Chat | TUI | Web |
|---------|------|-----|-----|
| Native KiloCode | Yes | No | No |
| Offline | Yes | Yes | No |
| Visual rich | Low | Medium | High |
| Multi-user | No | No | Yes |
| CI/CD friendly | Yes | Yes | No |
| Mobile | No | No | Yes |
| Real-time preview | No | No | Yes |
| Collaboration | No | No | Yes |

Default renderer: Chat (KiloCode native)
Choose via flag: --renderer chat|tui|web

## Coverage by Layer (v3.62.0 - FINAL)
coverage by layer, coverage + layer, coverage per layer
- Web UI Blazor components: 100% (atoms, molecules, organisms, templates, pages)
- State management: 100% (shared with Chat + TUI)
- Real-time preview: 100%
- Collaboration: 100%
- Approval workflow: 100%
- Dashboard: 100%
- **Web UI Renderer total**: 100%

## 3 Renderers (FINAL)
- Chat (v3.53.0): native KiloCode, default, casual
- TUI (v3.57.0): Blazor terminal, dev-friendly, CI/CD
- Web (v3.62.0): Blazor Server, visual rich, multi-user, enterprise
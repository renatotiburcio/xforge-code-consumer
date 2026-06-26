# TUI Blazor Renderer Template for /forge (v3.57.0)

Blazor-based Terminal UI for /forge wizard. Runs as standalone .NET app, communicates with KiloCode via JSON-RPC or file-based protocol.

## Why TUI (not Web)
- **Offline-first**: runs without browser, no web server needed
- **Dev-friendly**: terminal-native, keyboard-driven
- **Lightweight**: ~5MB vs 200MB for browser-based Web UI
- **Reuses XForge stack**: Blazor components work in console via Blazor.TUI
- **Same components as Web UI**: TUI is just another renderer

## Command to launch TUI
```bash
# Option A: as .NET tool (recommended)
dotnet tool install -g XForge.Tui
xforge-tui

# Option B: from source
cd tools/tui
dotnet run

# Option C: in CI/CD (headless mode)
xforge-tui --headless --wizard forge --mode new --auto-yes
```

## TUI Layout (ASCII mockup)
```
+---------------------------------------------------------------+
| /forge  -  Step 4/12  -  [##########----------] 33%         |
+---------------------------------------------------------------+
|                                                               |
| 4. Database                                                   |
|                                                               |
| Qual banco de dados voce quer usar?                         |
|                                                               |
|   ( ) MySQL 8.x          (recomendado para .NET 10)         |
|   ( ) PostgreSQL 16      (melhor para alta concorrencia)     |
|   ( ) SQL Server 2022    (enterprise, license required)     |
|   ( ) SQLite             (dev/test, zero-config)             |
|   ( ) None               (sem persistencia)                 |
|                                                               |
| [<- Back]                              [Skip]  [Next ->]     |
+---------------------------------------------------------------+
| Tip: MySQL + .NET 10 downgrades EF Core para .NET 9          |
+---------------------------------------------------------------+
```

## Components (Blazor)

### Atoms
- Button (primary, secondary, danger)
- Input (text, number, checkbox, radio)
- ProgressBar (percentage, steps)
- Badge (info, warn, success, error)

### Molecules
- QuestionCard (title, description, options, help)
- Breadcrumb (step 4/12, clickable to go back)
- ConfidenceIndicator (percentage + color: green/yellow/red)
- TipBox (contextual help, collapsible)

### Organisms
- WizardShell (header + main + footer)
- StepNavigator (previous/next/skip buttons)
- KnowledgeContextPanel (sidebar showing detected code/docs/ideas)
- DecisionPreview (right sidebar showing what will be generated)

### Templates
- WizardLayout (full screen with shell + 3 panels)
- CompactLayout (single panel, for small terminals)

## Features
- **Progress bar** (visual feedback, % complete)
- **Breadcrumb** (clickable steps, go back)
- **Keyboard shortcuts** (Tab, Enter, Esc, arrow keys)
- **Auto-save state** (resume after Ctrl+C)
- **Confidence indicators** (color-coded per decision)
- **Side panels** (knowledge context + decision preview)
- **Contextual help** (F1 for help, inline tooltips)
- **Dry-run mode** (--dry-run flag, generates preview only)
- **Headless mode** (for CI/CD, no UI, auto-yes)

## State Management

TUI reads/writes to .xforge/wizards/<wizard>/state.json (same as Chat renderer).
- Resume: open TUI, it reads state.json, continues from last step
- Cancel: Ctrl+C, state saved, can resume later
- Multiple sessions: file lock via .xforge/wizards/<wizard>/state.lock

## Renderer Selection
```
Choose renderer:
  (1) Chat (default, native KiloCode)
  (2) TUI (Blazor terminal UI, this)
  (3) Web (Blazor Server, v3.62.0)
```

Or via flag: /forge new App --renderer tui

## Coverage by Layer (v3.57.0)
coverage by layer, coverage + layer, coverage per layer
- TUI Blazor components: 100% (atoms, molecules, organisms, templates)
- State management: 100% (file-based, same as Chat)
- Keyboard shortcuts: 100%
- Progress bar: 100%
- Knowledge context panel: 100%
- Decision preview panel: 100%
- Headless mode (CI/CD): 100%
- **TUI Renderer total**: 100%
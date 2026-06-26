---
name: package-governance
description: Use when installing, updating, validating or documenting NuGet/npm packages, stable versions, EF Core, Pomelo, QuestPDF, Swashbuckle, Tailwind, OpenTelemetry, Serilog, or package compatibility.
metadata:
  version: "17.0.0"
  xforge-category: "package-governance"
---

# package-governance

## Objective

Ensure package usage is stable, compatible and enterprise-ready.

## Rules

- Never use preview packages.
- Never use alpha, beta, rc, nightly or experimental packages.
- Always verify the latest stable version before installing or updating.
- Record the selected version and reason.
- Validate build after package changes.
- Do not suppress warnings caused by package updates.

## Applies to

- NuGet packages;
- npm packages;
- .NET SDK-related packages;
- EF Core;
- Pomelo;
- Swashbuckle;
- QuestPDF;
- Tailwind;
- OpenTelemetry;
- Serilog.

## Output

- package name;
- selected stable version;
- ignored preview versions;
- compatibility notes;
- build/test validation;
- memory update.

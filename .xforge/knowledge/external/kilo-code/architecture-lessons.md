---
id: KILO-LESSONS-001
title: Lessons from Kilo Code Architecture for XForge
source: Kilo Code Official Documentation (kilo-docs)
trustScore: 90
applicabilityScope: ["*"]
category: learning
subcategory: architecture-lessons
status: active
created: 2026-06-27
updated: 2026-06-27
tags: [lessons, architecture, kilo, best-practices, agent-design]
---

# Lessons from Kilo Code Architecture

## 1. Skills as On-Demand Context Loading

**Pattern**: Skills are NOT loaded into context at startup. Only metadata (name, description) is included in system prompt. Full instructions loaded on-demand when agent determines task matches.

**Benefit**: Dramatically reduces baseline token usage. Agent has access to unlimited skills without context pollution.

**XForge Application**: Our current skills are loaded fully at session start. Consider implementing lazy-loading for skills with large instruction bodies.

## 2. Description-Based Skill Matching

**Pattern**: Agent LLM decides whether to use a skill based on description field. No keyword matching or semantic search.

**Implication**: Description wording must match how users phrase requests. "Write descriptions that match how users phrase requests."

**XForge Application**: Review all skill descriptions for alignment with common user request patterns.

## 3. Per-Directory Instructions (AGENTS.md)

**Pattern**: AGENTS.md files in subdirectories are loaded dynamically when the Read tool accesses files in that directory. Contents injected as `<system-reminder>` tags.

**Benefit**: Monorepo support without duplicating instructions. Context-specific guidance loaded only when relevant.

**XForge Application**: Could improve our monorepo support by loading domain-specific rules only when working in those directories.

## 4. URL-Based Instructions

**Pattern**: `instructions` array in kilo.jsonc accepts URLs. Fetched at session start with 5-second timeout.

**Benefit**: Centralized team instructions without manual distribution.

**XForge Application**: Could enable remote instruction loading for enterprise teams.

## 5. Permission System Design

**Pattern**: Three actions (allow/ask/deny) with glob pattern matching. Last matching rule wins. Broad fallbacks first, exceptions after.

**Benefit**: Flexible security model that scales from permissive to restrictive.

**XForge Application**: Our RBAC system could benefit from glob-pattern-based command permissions.

## 6. Subagent Isolation Model

**Pattern**: Subagents run in isolated sessions with separate conversation history. Results flow back as summaries.

**Benefit**: Context pollution prevention. Each subagent starts clean for its specific task.

**XForge Application**: Our subagent system already uses this pattern. Kilo's implementation confirms the approach.

## 7. Think-Then-Do Prompting

**Pattern**: Guide agent through Analyze → Plan → Execute → Review cycle.

**Benefit**: Prevents wasted tokens on wrong approaches. Higher quality output.

**XForge Application**: Could be formalized as a standard operating procedure in our golden rules.

## 8. Composable Workflows

**Pattern**: Slash commands are markdown files with step-by-step instructions. Can chain multiple tools and operations.

**Benefit**: Complex automation without code. Version controllable. Shareable.

**XForge Application**: Our command system already supports this. Kilo's implementation validates the pattern.

## 9. Configuration Precedence Chain

**Pattern**: Built-in defaults → Global config → Project config → Global agents → Project agents. Later overrides earlier.

**Benefit**: Sensible defaults with progressive customization. Enterprise defaults with project overrides.

**XForge Application**: Our configuration system follows a similar pattern. Could be documented more explicitly.

## 10. Sensitive File Protection

**Pattern**: `.env` and `.env.*` always require explicit approval, even with broad read permissions. Built-in, not configurable.

**Benefit**: Defense in depth against accidental secret exposure.

**XForge Application**: Should implement similar built-in protection for sensitive file patterns.

## 11. Naming Enforcement

**Pattern**: Kilo Code enforces single-word variable names. Multi-word only when genuinely ambiguous.

**Benefit**: Consistent, readable code. Reduces cognitive load.

**XForge Application**: Could be adopted as a coding standard in our rules.

## 12. No Empty Catch Blocks

**Pattern**: Mandatory error handling. At minimum, log via `log.error("...", { err })`.

**Benefit**: Failures are visible. Bugs don't hide in silence.

**XForge Application**: Already a good practice. Could be enforced more explicitly.

## 13. Markdown Table Formatting

**Pattern**: No padding for alignment. Compact form with single-space-padded cells.

**Benefit**: Smaller diffs. Less noise in reviews.

**XForge Application**: Could be adopted for our documentation standards.

## 14. Fork Merge Minimization

**Pattern**: Kilo Code (fork of OpenCode) uses `kilocode_change` markers, prefers `kilocode/` directories, minimizes shared file changes.

**Benefit**: Clean upstream merges. Clear attribution of customizations.

**XForge Application**: If we ever fork or upstream-sync, this pattern is critical.

## 15. Auto-Discovery of Config Files

**Pattern**: Kilo discovers AGENTS.md, CLAUDE.md, CONTEXT.md via `findUp` from project root and parent directories.

**Benefit**: Zero-config setup. Instructions "just work" when placed in standard locations.

**XForge Application**: Our AGENTS.md loading could be extended to support auto-discovery in subdirectories.

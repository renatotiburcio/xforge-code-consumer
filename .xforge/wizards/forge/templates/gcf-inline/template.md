# GCF Inline Template for /forge (v3.56.0)

Invoke the genius-orchestrator subagent inline for non-trivial decisions. Apply 5 Guardians + AG999 + confidence scores.

## When to invoke GCF

Auto-invoke when decision is:
- **Architecture**: stack choice, pattern, framework
- **Security**: auth, LGPD, secrets, threat model
- **Stack**: .NET vs Python vs Go, MySQL vs PostgreSQL
- **Provider**: Stripe vs Mercado Pago, Twilio vs Z-API
- **Pattern**: CQRS vs CRUD, XForge.MediatR vs MediatR
- **Trade-off**: speed vs quality, simplicity vs completeness

Skip GCF when decision is:
- Trivial (file name, color, formatting)
- User explicit (--stack dotnet10)
- Default from template (no ambiguity)

## GCF Inline Flow (5 steps)

1. **Identify 3-8 relevant Geniuses** from .kilo/agents/genius-council/
2. **Collect opinions** (each Genius responds)
3. **Apply AG999 Devil's Advocate** (7 questions)
4. **Validate 5 Guardians** (Architecture, Simplicity, Security, Quality, Documentation)
5. **Return consensus JSON** with confidence score

## 3 Complexity Levels

### --quick (0 questions, all defaults)
Use when: trust defaults, fast iteration, prototype
```bash
/forge new App --quick --stack dotnet10 --db mysql --auth identity
```
Behavior: skip ALL questions, use best-guess defaults, generate immediately

### intermediate (DEFAULT, 5-7 questions, smart defaults)
Use when: standard projects, want guidance
```bash
/forge new App
```
Behavior: 5-7 critical questions, smart defaults pre-filled, GCF invoked for non-trivial

### --expert (10+ questions, full override)
Use when: enterprise, custom requirements, full control
```bash
/forge new App --expert
```
Behavior: 10+ questions including edge cases, all options shown, GCF for all decisions

## Confidence Score System

After each decision, GCF returns confidence (0-100%):

| Score | Action |
|-------|--------|
| >= 80% | Auto-apply (high confidence) |
| 50-79% | Ask user (medium confidence) |
| < 50% | Must research more (low confidence) |
| 0% | No opinion, fallback to default |

**Output example:**
```
Decision: Use .NET 10 (vs .NET 9 LTS)
Confidence: 92% (auto-apply)
Votes: AG010 approve, AG012 approve, AG017 approve, AG999 concern: migration effort
Guardians: Architecture OK, Simplicity OK, Security OK, Quality OK, Documentation OK
Risks: breaking change for existing .NET 8 users
Mitigations: keep .NET 9 LTS option as alternative
```

## Coverage by Layer (v3.56.0)
coverage by layer, coverage + layer, coverage per layer
- GCF Inline invocation: 100% (auto-trigger for non-trivial)
- 3 Complexity Levels: 100% (quick, intermediate, expert)
- Confidence Score system: 100% (4 levels: auto/ask/research/fallback)
- 5 Guardians validation: 100%
- AG999 Devil Advocate: 100% (7 questions)
- GCF Inline total: 100%
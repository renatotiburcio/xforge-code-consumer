---
id: KILO-PROMPT-ENGINEERING-001
title: Prompt Engineering Best Practices from Kilo Code
source: Kilo Code Official Documentation (kilo-docs)
trustScore: 95
applicabilityScope: ["*"]
category: patterns
subcategory: prompt-engineering
status: active
created: 2026-06-27
updated: 2026-06-27
tags: [prompt-engineering, best-practices, context-mentions, think-then-do]
---

# Prompt Engineering Best Practices

## 1. General Principles

### Be Clear and Specific
- **Bad:** Fix the code.
- **Good:** Fix the bug in the `calculateTotal` function that causes it to return incorrect results.

### Provide Context
- Use Context Mentions: `@/src/utils.ts` Refactor the `calculateTotal` function to use async/await.

### Break Down Tasks
- Divide complex tasks into smaller, well-defined steps

### Give Examples
- If you have a specific coding style, provide examples

### Specify Output Format
- If output needs to be JSON, Markdown, etc., specify in prompt

### Iterate
- Refine prompt if initial results aren't what you expected

## 2. Think-Then-Do Pattern

1. **Analyze**: Ask agent to analyze current code, identify problems, plan approach
2. **Plan**: Have agent outline steps to complete the task
3. **Execute**: Instruct agent to implement plan, one step at a time
4. **Review**: Carefully review results of each step before proceeding

## 3. Handling Ambiguity

If request is ambiguous:
- Agent might make assumptions (may not match intent)
- Agent might ask follow-up questions via `ask_followup_question` tool

Better to provide clear instructions from the start.

## 4. Providing Feedback

When results aren't desired:
- **Reject Actions**: Click "Reject" button with explanation
- **Explain Why**: Helps agent learn from mistakes
- **Reword Request**: Rephrase task or provide more specific instructions
- **Manually Correct**: Directly modify code before accepting changes

## 5. Good vs Bad Prompts

| Bad | Good |
|-----|------|
| Fix the button | `@/src/components/Button.tsx` Refactor to use useState instead of useReducer |
| Write some Python code | Create `utils.py` with `calculate_average(numbers)` function |
| Fix everything | `@problems` Address all errors and warnings in current file |
| Make it faster | Optimize the SQL query in `getUserById` to eliminate N+1 pattern |

## 6. Context Mentions

Use `@` prefix to reference specific files/folders:
- `@/src/utils.ts` — specific file
- `@/src/components/` — folder
- `@problems` — problem set

Agent reads referenced content into context before proceeding.

## Key Insights

- Specificity > generality in prompts
- Context mentions reduce ambiguity significantly
- Think-then-do prevents wasted tokens on wrong approaches
- Feedback loops improve agent performance over time
- Output format specification prevents rework

# Agent Runner

## Purpose

Orchestrates the multi-agent workflow.

## Execution order

1. Planner
2. Architect
3. Coder
4. Reviewer
5. Tester
6. Debugger
7. Refactor
8. Docs

## Inputs passed to each agent

- User task
- Project analysis
- Previous agent outputs
- Recent run memory

## Required behavior

- Execute agents sequentially
- Keep each response structured
- Re-analyze the project after file-changing steps
- Save run history for future context

## Expected agent response shape

```json
{
  "summary": "Short result",
  "files": [
    {
      "path": "src/example.js",
      "action": "create",
      "content": "..."
    }
  ],
  "notes": [],
  "issues": []
}
```
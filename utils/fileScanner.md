# File Scanner

## Purpose

Scans the project and returns a compact inventory.

## Responsibilities

- Walk the repository recursively
- Ignore noisy directories like `.git` and `node_modules`
- Collect files and directories
- Produce a lightweight tree summary

## Suggested ignore list

- `.git`
- `node_modules`
- `.ai-agent-history`
- `dist`
- `build`
- `coverage`

## Output expectations

- file list
- directory list
- trimmed tree view for prompt context
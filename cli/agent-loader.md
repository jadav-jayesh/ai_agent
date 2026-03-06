# Agent Loader

## Purpose

Loads agent definitions from Markdown files.

## Source directory

Default agent directory: `.ai-agents/`

## Loading rules

- Only load files ending in `.md`
- Use the filename as the agent id
- Use the first Markdown heading as the title
- Preserve the file body as the instruction set

## Default workflow order

- `planner`
- `architect`
- `coder`
- `reviewer`
- `tester`
- `debugger`
- `refactor`
- `docs`

## Extensibility

New agents can be added by placing additional Markdown files in `.ai-agents/`.
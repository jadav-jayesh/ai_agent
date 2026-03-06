# Agent CLI

## Purpose

Defines the terminal interface for the autonomous agent framework.

## CLI name

`ai-agent`

## Commands

### `ai-agent run "task"`
- Analyze the project
- Load Markdown agents
- Execute agents in sequence
- Pass forward prior outputs
- Apply approved file operations

### `ai-agent analyze`
- Scan the repository
- Detect languages, dependencies, framework hints, and structure
- Print analysis context for the workflow

### `ai-agent agents`
- List available `.md` agent definitions
- Show load order and role

### `ai-agent doctor`
- Check config presence
- Check agent directory exists
- Check provider selection
- Check required environment variables

## Expected output

All commands should print concise structured output suitable for terminal use.
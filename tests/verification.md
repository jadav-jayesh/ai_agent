# Verification Checklist

## Goal

Validate the framework design before building an executable version.

## Checklist

- Agent directory exists
- All required agents are defined as Markdown files
- CLI commands are documented
- Provider requirements are documented
- Config format is documented
- Workflow order is documented
- Project analysis behavior is documented
- Output JSON shape is documented

## Manual review examples

- Confirm `planner.md` does not write code
- Confirm `coder.md` returns file operations
- Confirm `docs.md` updates documentation only
# Agent Config

## Purpose

Defines runtime configuration for the framework.

The executable command reads the first fenced `json` block in this file as the active runtime config.

## Example config

```json
{
  "provider": "groq",
  "model": "llama3-70b",
  "agentsPath": ".ai-agents",
  "maxSteps": 10,
  "historyPath": ".ai-agent-history",
  "temperature": 0.2,
  "applyChanges": true
}
```

## Field descriptions

- `provider`: selected LLM provider
- `model`: provider model name
- `agentsPath`: folder containing agent Markdown files
- `maxSteps`: workflow step limit
- `historyPath`: location for run memory
- `temperature`: generation creativity
- `applyChanges`: whether file actions are executed automatically
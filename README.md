# ai-agent

Markdown-driven autonomous AI agent framework with a reusable CLI.

## Important note

This repository is **Markdown-driven** and now also includes a lightweight executable command.

The agents remain Markdown files, and the command loads those Markdown definitions at runtime.

## Goal

Provide a lightweight autonomous AI agent system with Markdown-based agent definitions and a reusable command that can run in other projects.

## What this repository contains

This repository is a **design pack plus a runnable command** for an autonomous AI agent framework.

It documents:

- the multi-agent workflow
- the intended CLI behavior
- the provider abstraction
- the project analysis process
- the expected config format
- the required output contract

The main idea is simple:

1. define each agent in Markdown
2. analyze the target project
3. run agents in sequence
4. pass outputs from one agent to the next
5. create, review, test, refine, and document changes

## Included structure

- `.ai-agents/` → agent definitions
- `bin/ai-agent` → executable command
- `cli/*.md` → CLI behavior specification
- `config/*.md` → config schema and example
- `utils/*.md` → utility behavior specs
- `tests/*.md` → verification checklist

## Folder map

```text
.ai-agents/
  planner.md
  architect.md
  coder.md
  reviewer.md
  tester.md
  debugger.md
  refactor.md
  docs.md

bin/
  ai-agent

cli/
  agent-cli.md
  agent-loader.md
  agent-runner.md
  ai-provider.md

config/
  agent.config.md

utils/
  fileScanner.md
  projectAnalyzer.md
  logger.md

tests/
  verification.md
```

## Agent definitions

The repository includes the following Markdown agents:

- `planner.md` → understands the task and builds the plan
- `architect.md` → defines system structure and design direction
- `coder.md` → proposes implementation changes
- `reviewer.md` → improves quality and correctness
- `tester.md` → adds or plans test coverage
- `debugger.md` → resolves likely defects
- `refactor.md` → simplifies and improves maintainability
- `docs.md` → updates developer-facing documentation

## Agent workflow

1. Planner
2. Architect
3. Coder
4. Reviewer
5. Tester
6. Debugger
7. Refactor
8. Docs

## End-to-end workflow intent

When a future implementation runs a command like `ai-agent run "Create login API"`, the intended flow is:

1. analyze the repository
2. load all Markdown agent instructions
3. send the user task plus project context to the planner
4. pass the planner output to the architect
5. continue through coder, reviewer, tester, debugger, refactor, and docs
6. collect structured file actions and summaries from each step
7. optionally persist history for future runs

## Install command globally

Make the command executable and symlink it into your local bin directory:

```bash
chmod +x /path/to/ai_agent/bin/ai-agent
mkdir -p ~/.local/bin
ln -sf /path/to/ai_agent/bin/ai-agent ~/.local/bin/ai-agent
export PATH="$HOME/.local/bin:$PATH"
```

After that, you can use `ai-agent` from any other project.

## Use in another project

Open any target project and run:

```bash
ai-agent analyze
ai-agent agents
ai-agent doctor
ai-agent run "Create login API"
```

You can also point it at a different project path:

```bash
ai-agent analyze --project /path/to/another-project
ai-agent run "Add auth" --project /path/to/another-project
```

## Desired commands

The intended CLI contract is:

- `ai-agent run "task"`
- `ai-agent analyze`
- `ai-agent agents`
- `ai-agent doctor`

These commands are documented in `cli/agent-cli.md`.

## Agent file format

Each agent is written in Markdown and should include:

- Role
- Responsibilities
- Rules
- Output format

This keeps the framework easy to extend because adding a new agent only requires adding another Markdown file with the same structure.

## Output contract

Agents should return structured JSON like this:

```json
{
  "summary": "...",
  "files": [
    {
      "path": "src/auth/login.ts",
      "action": "create",
      "content": "..."
    }
  ],
  "notes": [],
  "issues": []
}
```

## Provider support

The documented provider layer supports:

- OpenAI
- Groq
- OpenRouter
- Ollama

See `cli/ai-provider.md`.

The expected provider abstraction is intentionally simple:

- receive prompts and generation settings
- call the selected LLM backend
- return plain text that can be parsed into structured output

Provider credentials can be supplied through shell environment variables or a `.env` file.

Example:

```bash
export GROQ_API_KEY="your_key_here"
export AI_AGENT_PROVIDER="groq"
export AI_AGENT_MODEL="llama3-70b"
```

## Project analysis

Before execution, the framework should gather:

- languages
- framework hints
- dependencies
- folder structure

See `utils/projectAnalyzer.md` and `utils/fileScanner.md`.

This analysis step is important because it gives each agent shared context about:

- current languages in use
- framework or runtime hints
- dependency signals
- high-level folder layout
- important files worth inspecting first

## Config

See `config/agent.config.md` for the documented runtime config format.

The example config documents fields such as:

- provider
- model
- agent path
- max steps
- history path
- temperature
- whether file changes should be applied automatically

## Verification

See `tests/verification.md` for the Markdown-only acceptance checklist.

## How to use this blueprint

You can use this repository in two ways:

### 1. As a runnable cross-project command

Install `bin/ai-agent` once, then run it inside any project directory.

### 2. As a prompt pack

Use the files in `.ai-agents/` directly as role definitions for a manual or semi-manual AI workflow.

### 3. As an implementation spec

Use the files in `cli/`, `config/`, and `utils/` as the design reference for building a real CLI in the language of your choice.

## If you want the next step

I can now turn this Markdown-only blueprint into either:

1. a **Markdown-only expanded spec pack**, or
2. a **real executable CLI** in a language of your choice.

# HR Autonomous Agent Configuration Reference

## Purpose

This document summarizes the effective configuration of the HR Autonomous Agent defined in this repository. It is intended to be a compact 2–4 page reference for operators, maintainers, and reviewers who need to understand how the agent starts, what it depends on, how it behaves, and where its runtime state is stored.

The authoritative source files remain:

- `hr-autonomous-agent/agent.md`
- `hr-autonomous-agent/config/agent-config.md`
- `hr-autonomous-agent/rules.md`
- `hr-autonomous-agent/strategy.md`
- `hr-autonomous-agent/agents/*.md`

If this summary and the source files ever disagree, the source files win.

## 1. Runtime Identity and Invocation

The repository defines an **HR-oriented autonomous CLI agent**. Its mission is to interpret user requests through an HR operations lens, inspect the target HR tracker repository, infer the safest workflow, execute the smallest justified action, recover from failures, and improve over time through reflection.

### Canonical entry command

- Command: `agent run "<goal>"`
- Goal extraction rule: only the quoted payload after `run` is treated as the goal.
- Preferred mode: explicit command first.
- Fallback: plain-language requests may still be handled, but the quoted command is the official contract.

### Workflow authority

The runtime must follow the repo-local workflow files and must not replace them with global or generic defaults. If a required file cannot be loaded, execution must stop rather than proceed on assumptions.

## 2. Core Environment Configuration

The current environment configuration is defined in `config/agent-config.md`.

### Repository and backend target

| Setting | Current Value |
|---|---|
| Repository Path | `C:\Users\DELL\Desktop\Work_Projects\Groovy%20Webwork` |
| Backend Path | `modern-admin/backend` |
| Backend Start Command | `npm start:dev` |
| Backend Host | `127.0.0.1` |
| Backend Port | `4000` |
| Backend Check Order | `filesystem path` → `tcp port` → `auth endpoint` |
| Auth Endpoint | `/auth/login` |
| Auth Verification Endpoint | `/auth/token-details` |
| Runtime Shell | `powershell` |

### Authentication settings

- Authentication before task execution: `true`
- Authenticate immediately after port check: `true`
- Credentials are configured in `config/agent-config.md`.
- For documentation safety, the password is **not repeated here** and should be replaced before any production use.

### Environment behavior

- The configured repository path is treated as authoritative.
- The agent should not broad-scan for repositories unless the configured path fails.
- The backend path is resolved relative to the configured repository path.
- The agent first checks whether the backend is already reachable on the configured host and port.
- If the TCP probe succeeds, the agent authenticates immediately and verifies the session before deeper discovery.

## 3. Operational Defaults

The runtime is optimized for **HR business operations first**, not developer-first execution.

### Current defaults

| Setting | Current Value |
|---|---|
| Default Persona | `hr operations specialist` |
| Goal Interpretation Mode | `business-operation-first` |
| Start Backend If Needed | `true` |
| Startup Mode | `configured-path warm-start` |
| Warm Cache Files | `state/workflow_state.md`, `context/system_map.md`, `context/module_map.md` |
| Reuse Warm Cache When Path Matches | `true` |
| Repository Discovery Depth | `configured-path-first, full-scan-fallback-only` |
| Discovery Scope Preference | `targeted-refresh-before-full-rediscovery` |
| Preferred Inspection Targets | `controllers`, `services`, `repositories`, `entities`, `dtos` |
| Retry Limit | `3` |
| Pre-Execution Reasoning Output Required | `true` |
| CLI Status Style | `structured-short-task-list-status` |
| CLI File Read Visibility | `summary-only` |
| CLI Error Visibility | `hidden-from-user-facing-output` |
| Final Status Summary Required | `true` |
| Require Action Reason Before Execution | `true` |
| Require Explicit Escalation Reason | `true` |
| Update Memory After Each Task | `true` |
| Reflection Required | `true` |

### Practical meaning

In practice, these defaults mean the agent should reuse known repository facts whenever possible, avoid unnecessary rescans, inspect only the modules needed for the active goal, and explain its reasoning before any mutating action. It is expected to behave as an HR operator first and use engineering inspection only to support safe HR outcomes.

## 4. Safety, Scope, and Decision Policy

Safety is a first-class configuration concern.

### Safety settings

| Setting | Current Value |
|---|---|
| Safe Mode | `enabled` |
| Auto-Approve Low-Risk Corrections | `true` |
| Escalate Suspicious Cases | `true` |
| Allow Bulk Operations | `false` unless reasoning explicitly marks them safe |

### Operating rules derived from `rules.md`

- Always analyze the repository before execution.
- Always inspect code before mutating application state.
- Prefer safe operations over fast ones.
- Use minimum necessary scope.
- Prefer read-only verification before writes.
- Prefer HR operational remedies such as regularization, approval, reconciliation, scoped recomputation, or targeted backfill before considering code changes.
- Avoid bulk changes unless the reasoning output explicitly justifies them.
- Re-check uncertain authentication, repository mapping, or endpoint inference before continuing.

### Confidence model from `strategy.md`

- **High**: module, endpoint, business meaning, and data flow are verified.
- **Medium**: most of the path is supported, but one inference remains indirect.
- **Low**: key parts are uncertain; the agent should inspect more or escalate.

## 5. Runtime Workflow Configuration

The configured boot workflow is sequential and explicit:

1. Recognize `agent run "<goal>"`.
2. Load `agent.md` as the primary workflow contract.
3. Load `config/agent-config.md`, `rules.md`, `strategy.md`, and all role files under `agents/`.
4. Warm-load `state/workflow_state.md`, `context/system_map.md`, and `context/module_map.md`.
5. Resolve the configured repository path.
6. Confirm backend availability and authenticate.
7. Reuse cache when it still matches the configured target.
8. Perform only the minimum discovery and code inspection needed.
9. Write reasoning output to `tasks/reasoning_output.md`.
10. Execute, verify, log, recover if needed, update memory, and reflect.

### Required user-visible execution style

The runtime should present user-facing progress as short structured status lines instead of verbose reasoning or raw errors.

The normal user-facing stream should read like a compact task list of major phases, not a transcript of every internal read, command, or retry detail.

Recommended examples:

- `Processing: locating repository path...`
- `Completed: repository path located.`
- `Processing: authenticating session...`
- `Failed: authentication step failed.`
- `Retrying: authentication step (attempt 2 of 3)...`
- `Completed: task completed.`

Detailed reasons, evidence, and exact error text should remain in logs and task artifacts, not in the normal terminal output.

The normal terminal output should also suppress raw file-read traces, search hits, line dumps, shell stderr/stdout, and parser errors; those details belong in logs, not in the user-facing stream.

It should also avoid mentioning internal file paths, endpoints, commands, ports, ids, and other implementation detail unless the operator explicitly asks for that level of detail.

## 6. Agent Role Configuration

The system is decomposed into reusable role documents.

### `agents/reasoning_agent.md`

- Classifies the task.
- Translates vague business verbs into HR intent.
- Selects relevant modules and files.
- Produces the execution strategy.
- Declares confidence, risks, action reasons, and escalation conditions.
- Writes output to `tasks/reasoning_output.md`.

### `agents/repo_discovery_agent.md`

- Resolves repository and backend paths.
- Reuses warm cache when valid.
- Detects framework, entrypoints, modules, controllers, services, auth flow, and routes.
- Writes `context/system_map.md` and `context/module_map.md`.
- Prevents execution from starting before current discovery exists.

### `agents/execution_agent.md`

- Executes one step at a time.
- Confirms auth state and endpoint path.
- Verifies every result before success is recorded.
- Updates `logs/execution_logs.md` and `state/workflow_state.md`.

### `agents/recovery_agent.md`

- Classifies failures.
- Records evidence and probable cause.
- Applies the narrowest safe fix.
- Retries up to `3` times.
- Escalates when the root cause persists or the risk becomes unacceptable.

### `agents/reflection_agent.md`

- Reviews the completed run.
- Compares plan versus outcome.
- Records lessons, confidence review, and strategy improvements.
- Stores the reflection in `logs/reflection_logs.md`.

## 7. State, Memory, and Logging

The agent is configured to persist operational memory across runs.

### State and cache files

- `state/workflow_state.md`: current run state and resumability checkpoint
- `context/system_map.md`: discovered repository/system summary
- `context/module_map.md`: module-level knowledge
- `context/task_history.md`: historical task memory

### Output and log files

- `tasks/reasoning_output.md`: pre-execution reasoning and plan
- `tasks/completed_tasks.md`: completed task summaries
- `logs/execution_logs.md`: step-by-step action log
- `logs/failure_logs.md`: failure evidence and retry decisions
- `logs/reflection_logs.md`: post-run lessons and improvements

### Completion criteria

A run is complete only when it reaches a terminal state (`completed`, `failed`, or `escalated`) and the execution logs, failure logs, workflow state, memory, and reflection files have all been updated.

## 8. Maintenance Guidance

This configuration is designed to be updated primarily through the Markdown control files rather than code changes.

- If repository locations or backend paths change, update `config/agent-config.md`.
- If decision policy changes, update `rules.md` or `strategy.md`.
- If a role changes, update the corresponding file under `agents/`.
- If credentials are still placeholders or test values, replace them before real-world use.
- Keep this reference document in sync whenever major configuration changes are introduced.

In short, this repository is configured as a **repo-local, HR-first, safety-biased autonomous agent** with explicit startup rules, warm-cache reuse, mandatory reasoning, scoped execution, bounded retries, and persistent reflection.
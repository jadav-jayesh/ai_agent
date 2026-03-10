# Operating Rules

## Core Rules

1. Always analyze the repository before executing tasks.
2. Always perform a code inspection step before mutating application state.
3. Prefer safe operations over fast operations.
4. Interpret business requests using HR domain semantics before engineering semantics.
5. Escalate uncertain cases rather than guessing.
6. Log all actions, outcomes, failures, and retries.
7. State the reason for every action, skip, rejection, escalation, and retry.
8. Retry failures up to 3 times, and explain the reasoning for each retry.
9. Update memory after each task and after each meaningful state transition.
10. Improve future strategy through reflection after every run.

## User-Facing Output Rules

- Show progress in short structured status lines such as `Processing: <step>...`, `Completed: <step>.`, `Failed: <step>.`, and `Retrying: <step> (attempt n of 3)...`.
- Treat this status-only format as mandatory for every normal `agent run`.
- Prefer simple generic step labels for common phases such as path resolution, authentication, repository inspection, endpoint lookup, execution, verification, and completion.
- Keep the transcript phase-level and task-list-like; do not narrate every low-level read, probe, command, or lookup.
- Do not print raw error text, stack traces, or lengthy diagnostic output to the terminal during normal operation.
- Do not print shell stderr/stdout dumps, parser errors, command traces, or search-match output directly to the user-facing terminal stream.
- Do not print file bodies, line-numbered read output, search hits, or raw `Read <file>` progress lines during normal operation.
- Do not print internal file paths, module names, endpoints, ports, commands, ids, or similar implementation details unless the user explicitly asked for them or a minimal final result requires them.
- When inspection is needed, summarize the purpose and result in status form instead, for example `Processing: confirming review endpoint...` and `Completed: review endpoint confirmed.`
- If an internal tool emits verbose output, suppress it from the terminal and replace it with one brief status line.
- Keep detailed error evidence, blockers, and retry reasoning in logs and task files instead of the user-facing terminal stream.
- End each run with a single terminal summary line that states the terminal status.

## Command Recognition Rules

- Recognize `agent run "<goal>"` as the canonical command that starts the workflow.
- Extract only the quoted payload as the goal.
- If the command is malformed or the goal is missing, do not guess; ask for the corrected command.
- Do not ask for extra confirmation when a valid `agent run "<goal>"` command is provided unless safety policy requires clarification about the goal itself.

## Safety Rules

- Use the minimum scope needed to satisfy the goal.
- Prefer read-only verification before write actions.
- Prefer HR operational remedies such as regularization, approval, reconciliation, scoped recomputation, or targeted backfill before considering code edits.
- Avoid bulk changes unless the reasoning output explicitly justifies them.
- Do not approve suspicious attendance or HR changes automatically when evidence is weak.
- Do not run attendance ETL or backfill just because attendance looks wrong in one view; first verify whether stored records are actually missing or stale.
- If authentication, repository mapping, or endpoint inference is uncertain, re-check before continuing.

## Inspection Rules

- Identify the relevant module before execution.
- Locate related controllers, services, DTOs, repositories, and entities.
- Identify the relevant HR workflow before execution: regularization, materialization, approval, holiday policy, shift rule, or employee lifecycle timing.
- Infer APIs from code rather than assumptions whenever possible.
- Print the discovered reasoning summary in compact status form before executing actions.
- Keep CLI inspection output concise and summary-only; do not dump full file contents, search results, terminal read output, or a narrated list of every consulted file during normal operation.

## Logging Rules

- Every run must have a run identifier.
- Every step must include timestamp, action, reason, target, result, and next state.
- Every skip, rejection, or escalation entry must include the blocker, evidence, and safer alternative.
- Every failure entry must include error evidence, probable cause, retry decision, and why a retry was or was not justified.

## Recovery Rules

- Retry only when the failure is plausibly recoverable.
- Change something between retries: inputs, timing, service state, auth state, or endpoint selection.
- When attendance verification disagrees, distinguish between regularization issues, materialization issues, ETL gaps, and verification-tool errors before retrying mutation.
- Stop retrying when the same root cause persists after 3 attempts.

## Memory Rules

- Update `context/task_history.md` after each completed or terminally failed run.
- Update `tasks/completed_tasks.md` after every completed task.
- Update `state/workflow_state.md` throughout execution to support resumability.

## Reflection Rules

- Reflection must identify what worked, what failed, and what should change.
- Reflection must improve confidence calibration and operational strategy.
- Reflection output must be stored even when the task fails.
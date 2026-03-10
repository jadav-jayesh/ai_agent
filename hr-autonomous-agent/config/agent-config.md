# Agent Configuration

## Environment

- Repository Path: `C:\Users\DELL\Desktop\Work_Projects\Groovy%20Webwork`
- Backend Path: `modern-admin/backend`
- Backend Start Command: `npm start:dev`
- Backend Host: `127.0.0.1`
- Backend Port: `4000`
- Backend Check Order: `filesystem path`, `tcp port`, `auth endpoint`
- Auth Endpoint: `/auth/login`
- Auth Verification Endpoint: `/auth/token-details`
<!-- - Primary API Base Path: `/api` -->
- Runtime Shell: `powershell`

## Credentials

- Email: `tejas.pawar@groovyweb.co`
- Password: `12345678`

## Operational Defaults

- Default Persona: `hr operations specialist`
- Primary Entry Command: `agent run "<goal>"`
- Command Recognition Mode: `explicit command first`
- Goal Extraction Rule: `take the quoted payload after run as the goal`
- Require Quoted Goal For Canonical Command: `true`
- Goal Interpretation Mode: `business-operation-first`
- Start Backend If Needed: `true`
- Authenticate Before Task Execution: `true`
- Startup Mode: `configured-path warm-start`
- Warm Cache Files: `state/workflow_state.md`, `context/system_map.md`, `context/module_map.md`
- Reuse Warm Cache When Path Matches: `true`
- Authenticate Immediately After Port Check: `true`
- Repository Discovery Depth: `configured-path-first, full-scan-fallback-only`
- Discovery Scope Preference: `targeted-refresh-before-full-rediscovery`
- Preferred Inspection Targets: `controllers`, `services`, `repositories`, `entities`, `dtos`
- Retry Limit: `3`
- Require Pre-Execution Reasoning Output: `true`
- CLI Status Style: `structured-short-status`
- CLI File Read Visibility: `summary-only-no-read-dumps`
- CLI Error Visibility: `status-only-no-raw-error-dumps`
- CLI Allowed User-Facing Statuses: `Processing`, `Completed`, `Failed`, `Retrying`, `Escalated`
- CLI Disallowed User-Facing Content: `file bodies`, `search hits`, `line dumps`, `raw Read messages`, `stdout/stderr dumps`, `stack traces`, `exception text`
- Final Status Summary Required: `true`
- Require Action Reason Before Execution: `true`
- Require Explicit Escalation Reason: `true`
- Update Memory After Each Task: `true`
- Reflection Required: `true`

## Safety Settings

- Safe Mode: `enabled`
- Auto-Approve Low-Risk Corrections: `true`
- Escalate Suspicious Cases: `true`
- Allow Bulk Operations: `false` unless reasoning explicitly marks them safe

## Notes

- Replace credential placeholders before production use.
- Treat `agent run "<goal>"` as the canonical agent launch syntax in this repository.
- Treat `Repository Path` as authoritative on this machine; do not broad-scan for the repo unless this path fails.
- Resolve `Backend Path` relative to `Repository Path` after trimming any leading or trailing slash characters.
- Use the TCP probe on `Backend Host` and `Backend Port` to decide whether the backend is already running before attempting startup.
- When the TCP probe succeeds, authenticate immediately and use `Auth Verification Endpoint` to confirm the acting session before deeper discovery.
- Reuse the warm-cache files when the configured target still matches; refresh only the module knowledge required by the goal.
- Keep terminal output summary-only during file inspection unless the user explicitly asks to see file contents.
- Collapse tool-level read/error output into compact status messages in the normal terminal stream and store exact details only in logs/task artifacts.
- Interpret user requests in HR domain terms before treating them as engineering requests.
- If the target repository structure changes, update paths here rather than changing agent logic files.
- If the backend exposes a different auth path or port, update this file and rerun discovery.

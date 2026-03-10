# Repository Discovery Agent

## Purpose

Scan the target repository, detect the application architecture, identify important modules, and infer the system map required for safe autonomous operation.

## Responsibilities

- scan repository structure
- detect framework such as NestJS, Express, Fastify, or similar
- identify modules and bounded business areas
- locate controllers and services
- locate repositories, entities, DTOs, validators, and auth flow
- infer API endpoints
- detect backend startup and health-check patterns
- reuse warm-cache knowledge when it still matches the configured target
- produce and update `context/system_map.md`
- enrich `context/module_map.md`

## Discovery Sequence

1. Normalize the configured repository and backend paths; if the repository path is relative, resolve it from the directory containing `agent.md`.
2. Verify whether the configured repository path exists and use it immediately when it does.
3. Load the existing `context/system_map.md` and `context/module_map.md` as warm cache and compare their repository path and known auth/backend details with the configured target.
4. Resolve the backend directory from the repository path and verify that it exists before scanning source files.
5. Probe the configured backend host/port before inferring startup behavior or deciding that the backend is down.
6. If the configured path and warm cache match, reuse cached framework, auth, entrypoint, and module facts unless the goal needs uncovered modules.
7. Only if the configured repository path fails, try a small deterministic fallback set; do not begin a broad scan before those fallbacks fail.
8. Read only the repository areas needed to refresh missing or stale facts.
9. Detect package manager and framework from manifest files and source conventions when the cache is missing or stale.
10. Find entrypoints such as `main.ts`, `app.module.ts`, `server.ts`, or `index.ts` when needed.
11. Enumerate only the module folders relevant to the active goal unless a full refresh is justified.
12. Identify controllers and service files.
13. Infer routes from controller decorators or router bindings.
14. Identify authentication strategy and login endpoint.
15. Capture startup commands and health endpoints if present.
16. Write a system summary to `context/system_map.md`.
17. Write module-level details to `context/module_map.md`.

## Required Output Fields

`context/system_map.md` must include:

- repository path
- detected framework
- app entrypoints
- backend start command
- module summary
- controller summary
- service summary
- inferred API summary
- auth flow summary
- operational notes

## Discovery Heuristics

- NestJS signals: `@Module`, `@Controller`, `@Injectable`, `main.ts`, `app.module.ts`
- Express signals: `express()`, `router`, `app.use`, route binding files
- Auth signals: login DTOs, JWT services, guards, passport strategies, `/auth/login`
- Attendance signals: folders or symbols containing `attendance`, `timesheet`, `shift`, `clock`, `checkin`, `checkout`
- On Windows, prefer exact configured paths and PowerShell-compatible path handling over shell-specific heuristics.
- When joining repository and backend paths, backend segments should be treated as relative segments, not rooted paths.

## Safety Requirement

No execution step may begin until repository discovery has produced a current `context/system_map.md` entry for the active run.

## CLI Output Rule

- Report discovery progress as short status lines such as `Processing: locating repository path...` and `Completed: repository path located.`
- Use the same brief format for backend checks and auth prerequisites, such as `Processing: checking backend availability...`.
- If discovery fails, show only a compact line such as `Failed: repository discovery step failed.` and keep detailed evidence in logs.
- Do not echo raw file contents from inspected files into the terminal during discovery.
- Do not echo search results, path dumps, line-numbered excerpts, or raw `Read <file>` actions into the terminal during discovery.
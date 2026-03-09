# Failure Logs

## Purpose

This file stores failed operations, retry reasoning, and recovery outcomes.

## Failure Entry Template

### Run ID: `run-<timestamp>`

#### Failed Step `N`

- Timestamp:
- Current Task:
- Retry Attempt:
- Error Evidence:
- Probable Cause:
- Proposed Fix:
- Retry Decision:
- Retry or Escalation Reason:
- Outcome:

## Failures

### Run ID: `run-20260308-attendance-past-week-proper-flow`

#### Failed Step `4`

- Timestamp: `2026-03-08`
- Current Task: `execute scoped repair`
- Retry Attempt: `1`
- Error Evidence: `tmp_attendance_repair.cjs` printed `REPAIR_DONE` and processed users, but exited with `UnknownElementException` during `app.close()`; Redis connection errors to `127.0.0.1:6379` were also present
- Probable Cause: repair writes completed, then Nest shutdown hit a provider lookup problem unrelated to the attendance row inserts
- Proposed Fix: do not retry mutation immediately; verify the target rows directly in SQL first
- Retry Decision: verification-only retry
- Outcome: direct SQL confirmed the repair succeeded and no second mutation was needed

#### Failed Step `5`

- Timestamp: `2026-03-08`
- Current Task: `post-repair verification`
- Retry Attempt: `1`
- Error Evidence: helper probe still reported `2026-03-07: db=0 missing=17` after the repair log showed new attendance records being finalized
- Probable Cause: probe grouped MySQL `DATE` values using JS `Date -> toISOString()` conversion, shifting dates backward by timezone
- Proposed Fix: verify with direct SQL and update the helper to use `DATE_FORMAT(date, '%Y-%m-%d')`
- Retry Decision: direct SQL check plus helper correction
- Outcome: direct SQL showed `17` rows for `2026-03-07`; helper was corrected and verification aligned
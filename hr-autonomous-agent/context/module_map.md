# Module Map

## Purpose

This file stores module-level operational knowledge extracted from the target repository.

## Update Rules

- Add or refresh entries after repository discovery and relevant code inspection.
- Keep module entries concise and execution-focused.
- Prefer evidence from source files over assumptions.

## Module Entry Template

### Module: `module_name`

- Path:
- Business Purpose:
- Relevant Controllers:
- Relevant Services:
- Repositories / Data Access:
- Entities / DTOs:
- Key Endpoints:
- Side Effects:
- Operational Risks:
- Confidence:

## Current Entries

### Module: `auth`

- Path: `modern-admin/backend/src/auth`
- Business Purpose: authenticate users, attach role/org claims to JWTs, and enforce active-session rules.
- Relevant Controllers: `auth.controller.ts`
- Relevant Services: `auth.service.ts`, `jwt.strategy.ts`
- Repositories / Data Access: `super-admin.entity`, `user-session.entity`, `UsersService`
- Entities / DTOs: JWT payload fields include `sub`, `role`, `organizationId`, `tokenVersion`, and `sessionId`
- Key Endpoints: `POST /auth/login`, `GET /auth/token-details`, `POST /auth/refresh`
- Side Effects: issues tokens, creates or updates session rows, can reject revoked sessions
- Operational Risks: login without correct credentials or stale token version blocks all downstream attendance operations
- Confidence: `high`

### Module: `hrms_attendance_regularization`

- Path: `modern-admin/backend/src/hrms/attendance`
- Business Purpose: expose attendance data, allow employees to request past-date regularizations, and allow HR/org admins to review those requests.
- Relevant Controllers: `attendance.controller.ts`
- Relevant Services: `attendance.service.ts`, `attendance-recalc.service.ts`
- Repositories / Data Access: attendance record, attendance log, regularization, holiday, leave, users, and policy repositories
- Entities / DTOs: `attendance-regularization.entity.ts`, `regularization-response.dto.ts`
- Key Endpoints: `GET /hrms/attendance/today`, `GET /hrms/attendance/me`, `POST /hrms/attendance/regularize`, `GET /hrms/attendance/regularizations`, `PATCH /hrms/attendance/regularizations/:id/review`
- Side Effects: approved reviews update regularization status and enqueue `recalcUserDateRange(userId, date, date)`
- Operational Risks: self-approval is forbidden; request creation requires explicit clock-in/out values; weekends/holidays/future dates are rejected; org-wide creation is not supported by the inspected workflow
- Confidence: `high`

### Module: `hrms_regularization_review_ui`

- Path: `modern-admin/frontend/src/pages/RegularizationReviewPage.tsx`
- Business Purpose: provide HR reviewers a pending/history queue for org regularization requests.
- Relevant Controllers: `attendance.controller.ts` (backend counterpart)
- Relevant Services: frontend `api` client to `/hrms/attendance/regularizations` and `/review`
- Repositories / Data Access: backend regularization repository via API
- Entities / DTOs: regularization response payload rendered inline
- Key Endpoints: `GET /hrms/attendance/regularizations`, `PATCH /hrms/attendance/regularizations/:id/review`
- Side Effects: approve/reject actions mutate pending requests and refresh attendance views
- Operational Risks: UI only supports reviewing submitted requests; it does not provide an org-wide create-on-behalf flow
- Confidence: `medium`

### Module: `reports_tracked_hours`

- Path: `modern-admin/backend/src/reports`
- Business Purpose: generate tracked-hours summaries across the acting user's visible organization/team scope for a selected date range.
- Relevant Controllers: `reports.controller.ts`
- Relevant Services: `reports.service.ts`, `leaders.service.ts`, `permissions.service.ts`
- Repositories / Data Access: `time_tracking`, `manual_time_entry`, visible-user filtering via leader/permission services
- Entities / DTOs: `TrackedHoursQueryDto`, `TimeTracking`, `ManualTimeEntry`
- Key Endpoints: `GET /reports/tracked-hours`
- Side Effects: none; read-only aggregation of auto hours plus approved manual hours
- Operational Risks: result scope is limited by visible-user permissions, so it may not represent an unrestricted org-global export even for HR users
- Confidence: `high`
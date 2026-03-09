# System Map

## Purpose

This file is the current repository-level map produced by the repository discovery workflow.

## Current Status

- Last Scan Time: `2026-03-08`
- Active Run ID: `idle`
- Repository Path: `C:\Users\DELL\Desktop\Work_Projects\Groovy%20Webwork`
- Detected Framework: `NestJS backend with React frontend`

## Application Entry Points

- Backend Entrypoint: `modern-admin/backend/src/main.ts`
- Root Module / Server File: `modern-admin/backend/src/app.module.ts`
- Startup Command: `npm start:dev`
- Health Check Path: `not explicitly discovered; live probe used on tcp://127.0.0.1:4000`

## Authentication Map

- Auth Module Path: `modern-admin/backend/src/auth`
- Login Endpoint: `POST /auth/login`
- Token Strategy: `passport-jwt` bearer tokens via `src/auth/jwt.strategy.ts`
- Guards / Middleware: `JwtAuthGuard`, `RolesGuard`, `FeatureFlagGuard`

## Module Summary

| Module | Path | Purpose | Confidence |
|---|---|---|---|
| auth | `modern-admin/backend/src/auth` | login, bearer-token validation, session enforcement, org/role claims | high |
| reports | `modern-admin/backend/src/reports` | tracked-hours reporting for the acting user's visible org/team scope | high |
| hrms attendance | `modern-admin/backend/src/hrms/attendance` | attendance reads, regularization request/review workflow, recalc/ETL hooks | high |
| hrms regularization review ui | `modern-admin/frontend/src/pages/RegularizationReviewPage.tsx` | HR review surface for pending org regularization requests | medium |

## Controllers

| Controller | Path | Routes | Notes |
|---|---|---|---|
| `AuthController` | `modern-admin/backend/src/auth/auth.controller.ts` | `/auth/login`, `/auth/token-details`, `/auth/refresh` | login is manual body validation; token details returns acting claims |
| `ReportsController` | `modern-admin/backend/src/reports/reports.controller.ts` | `/reports/tracked-hours` | enforces `VIEW_TIME_REPORTS` and filters by visible user IDs |
| `AttendanceController` | `modern-admin/backend/src/hrms/attendance/attendance.controller.ts` | `/hrms/attendance/today`, `/me`, `/regularize`, `/regularizations`, `/regularizations/:id/review` | regularization creation is self-service; review is HR/org-admin/super-admin scoped |

## Services

| Service | Path | Responsibility | Notes |
|---|---|---|---|
| `AuthService` | `modern-admin/backend/src/auth/auth.service.ts` | validate users, issue JWTs, enforce session/device behavior | login payload carries `organizationId` and `role` |
| `ReportsService` | `modern-admin/backend/src/reports/reports.service.ts` | aggregate auto and approved manual tracked hours by user/project/date | summary is read-only and returns merged-duration totals |
| `AttendanceService` | `modern-admin/backend/src/hrms/attendance/attendance.service.ts` | attendance reads, self regularization creation, HR review, exports | approved review triggers targeted recalculation |
| `AttendanceRecalcService` | `modern-admin/backend/src/hrms/attendance/attendance-recalc.service.ts` | enqueue per-user or org attendance recalculation jobs | approval calls `recalcUserDateRange(user, date, date)` |

## Inferred API Surface

| Endpoint | Method | Source Evidence | Notes |
|---|---|---|---|
| `/auth/login` | `POST` | `auth.controller.ts` | returns access/refresh tokens and acting user/org payload |
| `/auth/token-details` | `GET` | `auth.controller.ts` | confirms acting identity and org scope |
| `/reports/tracked-hours` | `GET` | `reports.controller.ts`, `reports.service.ts` | returns tracked-hours rows and summary for the requested date range |
| `/hrms/attendance/today` | `GET` | `attendance.controller.ts` | org-scoped attendance list for a specific date |
| `/hrms/attendance/me` | `GET` | `attendance.controller.ts` | self attendance record for a date; used by self-service regularization UI |
| `/hrms/attendance/regularize` | `POST` | `attendance.controller.ts`, `RequestRegularizationModal.tsx` | employee creates a request for their own past date only |
| `/hrms/attendance/regularizations` | `GET` | `attendance.controller.ts`, `RegularizationReviewPage.tsx` | HR/org-admin review queue |
| `/hrms/attendance/regularizations/:id/review` | `PATCH` | `attendance.controller.ts`, `RegularizationReviewPage.tsx` | approve/reject pending requests; self-approval blocked |

## Operational Notes

- The configured backend path exists and port `4000` has previously been observed live on this machine.
- The configured HR credentials previously authenticated as user `48` in organization `2` (`Groovy Technoweb PVT LTD`); use `/auth/token-details` as the fast verification path on new runs.
- For regularization work, employees submit their own requests with mandatory clock-in/out values; HR only reviews pending requests and cannot safely infer missing clock times org-wide.
- Treat this file as a warm-start cache: refresh only the goal-relevant sections instead of re-discovering the entire repo when the configured target still matches.
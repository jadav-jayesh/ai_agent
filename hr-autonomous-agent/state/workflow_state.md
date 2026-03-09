# Workflow State

## Purpose

This file tracks the active workflow state so the runtime can resume safely after interruption.

## Current State

- Run ID: `run-20260308-last-month-report-and-approvals`
- Current Task: `completed last-month org report generation and pending regularization review`
- Current Step: `saved full report artifact and verified only one self-approval-safe pending request remains`
- Retry Count: `1`
- Status: `completed`
- Last Updated: `2026-03-08`
- Last Successful Checkpoint: `tracked-hours report saved to tasks/last_month_full_report.json; four in-scope pending requests approved; one self-approval-safe skip verified`
- Pending Recovery Action: `none`

## Status Values

- `idle`
- `discovering`
- `inspecting`
- `planning`
- `executing`
- `recovering`
- `reflecting`
- `completed`
- `failed`
- `escalated`

## Update Rule

The runtime must update this file after every major workflow transition and after each retry attempt.
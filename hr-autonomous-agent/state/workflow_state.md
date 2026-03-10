# Workflow State

## Purpose

This file tracks the active workflow state so the runtime can resume safely after interruption.

## Current State

- Run ID: `run-20260310-last-month-regularization-approvals-completed`
- Current Task: `approve pending last-month regularization requests for the acting org`
- Current Step: `approved request ids 15 and 14; verified only self-owned request id 8 on 2026-02-18 remains pending`
- Retry Count: `0`
- Status: `completed`
- Last Updated: `2026-03-10`
- Last Successful Checkpoint: `backend started with npm run start:dev; authenticated as hr user 48 in org 2; approved ids 15 and 14; updated tasks/live_last_month_regularization_result.json`
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
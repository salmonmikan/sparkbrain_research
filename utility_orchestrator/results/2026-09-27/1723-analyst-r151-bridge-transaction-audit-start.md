# Utility autonomous task start

schema_version: 2
autonomous_task_id: UTILITY-AUTO-20260927T172300+0900-ANALYST-R151-BRIDGE-AUDIT
assignment_mode: AUTONOMOUS_IDLE
status: RUNNING
started_at: 2026-09-27T17:23:00+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_PERSISTENCE_TRANSACTION_AUDIT_ONLY
scientific_authority: NONE

## Objective

Independently verify the newest retained Evidence Analyst persistence-bridge transaction for R151 from request publication through receipt and target history/latest/state readback.

## Trigger / source

P0 is closed as recovered, while the Evidence Analyst Actions bridge remains retained hardening. R151 is the newest durable Analyst generation and therefore the highest-value current transaction to audit.

## Ownership checks

- Utility assignment: schema-v2 clean IDLE
- Evidence Analyst: R151; one bounded RD006 v3 D0 matrix allocated to MAIN
- MAIN: R158; RD006 owner remains MAIN
- Relay: dependency-wait suspended; owner CONTROL_BRAIN
- Utility scope overlap: none

## Allowed actions

- Read-only request, receipt, commit-parent and target-content verification.
- Utility-owned result/state publication only.

## Forbidden actions

- No scientific execution, scoring, candidate interpretation or workflow dispatch.
- No mutation of Analyst, MAIN, Control, research, evidence or scheduler state.
- No P0 reopen/closure decision.

## Stop condition

Stop after one bounded transaction audit and Utility-owned durable report.

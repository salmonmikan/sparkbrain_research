# Utility autonomous task start

schema_version: 2
autonomous_task_id: UTILITY-AUTO-20260927T212608+0900-R156-MAIN-EXECUTION-COLLISION
assignment_mode: AUTONOMOUS_IDLE
status: RUNNING
started_at: 2026-09-27T21:26:08+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_HANDOFF_AND_COLLISION_RECONCILIATION_ONLY
scientific_authority: NONE

## Objective

Determine whether Evidence Analyst R156 remains an ordinary MAIN handoff wait or has already entered MAIN-owned execution, while independently checking R156 persistence integrity.

## Trigger / source

The Utility assignment pointer is clean schema-v2 IDLE. Analyst R156 is newer than Utility's prior R153 reconciliation and MAIN's durable R161 report.

## Ownership checks at start

- Utility assignment: schema-v2 clean IDLE.
- Evidence Analyst: R156; exactly one bounded v4 D0 12-cell OFF/ON matrix remains allocated to MAIN.
- MAIN durable report: R161 v4 synthetic preflight.
- Control: R96; MAIN owns RD006 v4 execution.
- Relay: disabled dependency-wait under Control ownership.
- P0: CLOSED_P0_RECOVERED; active pointer debt empty.

## Allowed actions

- Read-only R156 bridge, ownership, branch ancestry and collision checks.
- Utility-owned result/state publication only.

## Forbidden actions

- No RD006 implementation, adapter review, dynamics, matrix execution, scoring, held-out access or workflow dispatch.
- No mutation of Analyst, MAIN, Control, research, evidence or scheduler state.
- No reinterpretation or expansion of R156 authority.

## Stop condition

Stop immediately if MAIN acknowledges the handoff or creates an execution ref, then record the collision guard result.

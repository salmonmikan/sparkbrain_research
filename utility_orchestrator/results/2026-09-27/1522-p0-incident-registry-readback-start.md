# Utility autonomous task start

schema_version: 2
autonomous_task_id: UTILITY-AUTO-20260927T152236+0900-P0-REGISTRY-READBACK
assignment_mode: AUTONOMOUS_IDLE
status: RUNNING
started_at: 2026-09-27T15:22:36+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_CONTROL_PLANE_RECONCILIATION_ONLY
scientific_authority: NONE

## Objective

Independently verify the Control-owned P0 incident-registry reconciliation after Control R91 and determine whether any active pointer debt or Utility-owned repair remains.

## Trigger / source

Control R91 reports that the dedicated incident registry was the last Control-owned pointer debt and is now reconciled to CLOSED_P0_RECOVERED.

## Ownership checks

- Utility assignment: schema-v2 clean IDLE
- Evidence Analyst: R149; RD006 v3 static construction/preflight allocated to MAIN
- MAIN: R157; no Utility ownership
- Relay: dependency-wait suspended; owner CONTROL_BRAIN
- P0 owner: CONTROL_BRAIN

## Allowed actions

- Read-only fetch and cross-check of Control history/latest/state/incident registry.
- Read-only comparison with Analyst and MAIN ownership.
- Utility-owned result/state publication only.

## Forbidden actions

- No scientific execution, scoring, candidate interpretation or workflow dispatch.
- No mutation of Control, Analyst, MAIN, research, evidence or scheduler state.
- No reopening or re-closing of the P0 incident.

## Stop condition

Stop after one bounded read-only reconciliation and Utility-owned durable report.

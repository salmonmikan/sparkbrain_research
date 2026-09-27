# Utility autonomous task start

schema_version: 2
autonomous_task_id: UTILITY-AUTO-20260927T232808+0900-R157-BRIDGE-HANDOFF-RECONCILIATION
assignment_mode: AUTONOMOUS_IDLE
status: RUNNING
started_at: 2026-09-27T23:28:08+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_HANDOFF_AND_PERSISTENCE_RECONCILIATION_ONLY
scientific_authority: NONE

## Objective

Independently verify Evidence Analyst R157 bridge persistence and determine whether MAIN has durably acknowledged the new read-only RD006 v4 preserved-output audit allocation.

## Trigger / source

The Utility assignment pointer is clean schema-v2 IDLE. Analyst R157 is newer than Utility's prior R156 collision reconciliation and MAIN's durable R162 report.

## Ownership checks at start

- Utility assignment: schema-v2 clean IDLE.
- Evidence Analyst: R157; MAIN owns one preserved-output read-only return-alignment audit.
- MAIN durable report: R162; still bound to Analyst R156 and stopped after the one authorized v4 matrix.
- Control: R97; P0 is CLOSED_P0_RECOVERED with no active pointer debt.
- Relay: disabled dependency-wait under Control ownership.
- Open Utility requests: no newer request than the already-reconciled request set was observed.

## Allowed actions

- Read-only R157 request/receipt/history/latest/state and ownership reconciliation.
- Utility-owned result/state publication only.

## Forbidden actions

- No RD006 dynamics, rerun, retune, rescore, second matrix, capability/held-out access or workflow dispatch.
- No mutation of preserved artifacts or Analyst, MAIN, Control, research, evidence or scheduler state.
- No interpretation beyond the exact R157 allocation and preserved funnel fields.

## Stop condition

Stop after bridge verification and handoff classification. If MAIN acknowledges R157 or the object becomes active during the check, record the collision and perform no RD006 work.

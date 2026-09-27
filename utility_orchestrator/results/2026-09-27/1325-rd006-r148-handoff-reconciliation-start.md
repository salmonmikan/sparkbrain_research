# Utility autonomous task start — RD006 R148 handoff reconciliation

schema_version: 2
status: STARTED
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260927T132542+0900-RD006-R148-HANDOFF-RECON
started_at: 2026-09-27T13:25:42+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY
scientific_authority: NONE

## Objective

Determine whether Evidence Analyst R148's newly allocated RD006 v2 preserved static topology/return-edge coverage audit has an unambiguous, collision-safe handoff to MAIN/Relay, without performing that audit or touching the research object.

## Trigger / source

- Utility assignment pointer is schema-v2 clean IDLE.
- Evidence Analyst advanced to R148 and assigned the bounded read-only audit to MAIN.
- MAIN remains at R156, whose terminal stop reason was to wait for Analyst reconciliation.
- Relay remains Control-owned dependency-wait suspended.

## Ownership checks

- RD006 owner: MAIN.
- Analyst allocation: MAIN.
- Relay restart owner: Control Brain.
- Utility overlap: none; this task is cross-stream read-only reconciliation only.
- Utility branch head before start publication: fdb220d7ee6880910d244127bc960b5ba82e7593.

## Allowed actions

- Re-fetch current Analyst, MAIN, Control, Relay-ownership and Utility-assignment state.
- Compare generation/ref bindings and classify handoff readiness.
- Persist Utility-owned start/final records only.

## Forbidden actions

- No RD006 source/artifact audit.
- No dynamics, scoring, experiment or workflow dispatch.
- No v3 design or prospective scientific contract.
- No mutation of Analyst, MAIN, Control, Relay, research, evidence or scheduler state.
- No Funnel typing change.

## Stop condition

One bounded read-only reconciliation, one terminal Utility result/state publication, independent readback, then stop.

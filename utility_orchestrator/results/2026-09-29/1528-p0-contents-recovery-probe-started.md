# Utility P0 Contents Recovery Probe

schema_version: 2
autonomous_task_id: AUTOUTIL-20260929T152817+0900-P0-CONTENTS-RECOVERY-PROBE
produced_at: 2026-09-29T15:28:17+09:00
assignment_mode: AUTONOMOUS_IDLE
status: STARTED
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

## Objective

Test whether the previously successful Utility-owned GitHub Contents create-file surface has recovered after repeated same-surface pre-GitHub refusals, then reconcile the observation against the current P0 classification.

## Trigger / source

- P0 INC-GITHUB-MUTATION-RECURRENCE-20260928-001 remains OPEN.
- Durable Control authority is append-only R120.
- MAIN R191 again observed 5/5 pre-GitHub refusal on required PR creation.
- Utility assignment pointer is current schema-v2 IDLE.

## Ownership checks

- Control: R120
- Evidence Analyst: R169
- MAIN: R191
- Relay allocated: false
- M1-002 owner: PRIMARY MAIN
- M1-002 exact head: 2a21d3e879f1db4e81a58273180ad2124e823a5e
- SB003: ALLOCATED_CONDITIONAL_INACTIVE
- Human Directive index blob: 1ba1e173344f36e14d0e21e6f3e823254e031f7d
- directive delta versus prior durable Utility state: none

## Allowed actions

- Utility-owned persistence/readback only.
- Read-only comparison of current P0 mutation surfaces and durable states.
- No PR creation, merge, workflow dispatch, scheduler mutation, scientific execution, or non-Utility branch mutation.

## Stop condition

Stop after one bounded diagnostic and terminal Utility publication, or fail closed if the authorized persistence retry ceiling is exhausted.

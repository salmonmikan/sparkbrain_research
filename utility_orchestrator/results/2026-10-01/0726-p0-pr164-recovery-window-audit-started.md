# Utility autonomous task — STARTED

schema_version: 2
status: STARTED
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: AUTOUTIL-20261001T072617+0900-P0-PR164-RECOVERY-WINDOW-AUDIT-6C4E2A91
started_at: 2026-10-01T07:26:17+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

## Objective

Perform one bounded read-only P0 recovery-window audit after PRIMARY MAIN R215 reported that the previously persistent `create_pull_request` surface succeeded on attempt 3 and created PR #164. Verify the live PR/exact-head/CI state, cross-stream persistence/pointer state, and whether this observation narrows the incident classification without declaring root cause or P0 closure.

## Trigger / source

- HUMAN-20260925-002 P0 GitHub persistence incident
- HUMAN-20260926-003 accelerated recovery
- HUMAN-20260927-002 five-total-attempt publication contract
- MAIN R215: PR #164 created after two pre-GitHub refusals
- Control latest append-only authority: R143
- Evidence Analyst: R176

## Ownership / collision checks

- Utility assignment: schema-v2 clean IDLE
- Evidence Analyst allocation: M1-002 owned by PRIMARY MAIN; Relay unallocated
- PRIMARY MAIN generation/state/lease: R215 aligned at readback
- M1-002 exact head: 2a21d3e879f1db4e81a58273180ad2124e823a5e
- SB003: ALLOCATED_CONDITIONAL_INACTIVE
- Utility branch head before STARTED publication: bec3d0a87fc44da085bd854b62040d8dbf0f2d16
- Directive index ref: ops/human-directives
- Directive index head: 8ce979b9ec0bc7eede5225c0403698f8886d3e8d
- Directive index blob: 1ba1e173344f36e14d0e21e6f3e823254e031f7d
- Directive delta vs previous Utility durable generation: none

## Allowed actions

- read-only inspection of PR #164, exact source/base refs, CI/check status and current Control/Analyst/MAIN/Relay operational state;
- classify observations under the P0 diagnostic taxonomy;
- publish only Utility-owned append-only terminal result and Utility state.

## Forbidden actions

- no PR merge, close, review, label or mutation;
- no mutation of MAIN, Control, Analyst, Relay, scientific, FORMAL, evidence, freeze, sealed or main refs;
- no scientific execution, scoring, rerun, retune or redispatch;
- no scheduler mutation;
- no Work / Work mode / Cloud Browser / Work-backed execution.

## Stop condition

Stop after this single bounded audit and Utility-owned publication, or earlier on ownership ambiguity, material supersession/collision, integrity conflict, or exhausted publication attempts.

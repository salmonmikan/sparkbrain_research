# Utility autonomous task start — M1-002 exact-head readiness readback

schema_version: 2
started_at: 2026-09-28T09:25:41+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260928T092541+0900-M1-002-EXACT-HEAD-READBACK
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_BUILD_PROVENANCE_AND_CI_RECONCILIATION_ONLY

## Objective

Independently verify the exact M1-002 branch head, scope, provenance, bounded harness contract and CI readiness without changing MAIN-owned implementation or becoming a MAIN dependency.

## Trigger / source

- Utility assignment pointer is schema-v2 clean IDLE with no active assignment.
- HUMAN-20260928-001 prioritizes non-colliding Utility checkpoint/replay, fail-closed testing, CI and provenance support.
- Evidence Analyst R164 retains MAIN-only M1-002 authority and requires exact-head CI followed by fresh Analyst reconciliation.
- The required branch now exists at `2a21d3e879f1db4e81a58273180ad2124e823a5e`, while durable MAIN R169 still predates it.

## Ownership checks at start

- assignment pointer blob: `a88c6cee9ac0608a701d51f083cf275425d44515`
- Control: `CTRL-20260928T084949+0900-R105-M1-ROBUSTNESS-ALLOCATED`
- Evidence Analyst: `EVA-20260928T090051+0900-R164-M1-WAIT-FLY0-HANDOFF-REVIEW`
- MAIN durable state: `MAIN-20260928T072510+0900-PRIMARY-R169-M1-INTEGRATED`
- Relay: intentionally disabled; no competing allocation
- M1-002 owner: MAIN
- main: `59fc994b39d0ba02682e972161bb46801592d25b`
- M1-002 branch: `2a21d3e879f1db4e81a58273180ad2124e823a5e`

## Allowed actions

- Read-only branch/tree/diff/scope/provenance verification.
- Read-only CI and status verification for the exact head.
- Utility-owned start/result/state publication only.

## Forbidden actions

- No M1-002 code, tests, docs, branch, PR, main, Analyst, MAIN, Relay or Control mutation.
- No workflow dispatch, scientific execution, scoring, comparator run, held-out access or claim reinterpretation.
- No FLY-0/SB003 promotion or mixing.
- No scheduler mutation.

## Stop condition

Stop after one bounded readiness report, or immediately if assignment, Analyst, MAIN, Control or exact refs materially supersede ownership before final publication.

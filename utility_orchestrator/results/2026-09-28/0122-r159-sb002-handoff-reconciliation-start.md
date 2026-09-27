# Utility autonomous task start — R159 / SB002 handoff reconciliation

schema_version: 2
started_at: 2026-09-28T01:22:40+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260928T012240+0900-R159-SB002-HANDOFF-RECONCILIATION
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_HANDOFF_AND_PERSISTENCE_RECONCILIATION_ONLY

## Objective

Independently verify the Evidence Analyst R159 persistence transaction and determine whether its SB002 allocation has a clear, collision-safe MAIN handoff target.

## Trigger / source

- Utility assignment pointer is schema-v2 clean IDLE.
- Evidence Analyst latest/state advanced to R159 and allocated non-evidentiary SYSTEM_BUILD SB002 to MAIN.
- MAIN durable state observed before task start remains R163 and predates R159.

## Ownership checks at start

- Control: CTRL-20260927T235243+0900-R98-RD006-V4-AUDIT-RECONCILIATION
- Evidence Analyst: EVA-20260928T010015+0900-R159-SB002-ATOMICITY-CLARIFICATION
- MAIN: MAIN-20260927T233306+0900-PRIMARY-R163-RD006-V4-RETURN-ALIGNMENT-AUDIT
- Relay: DEPENDENCY_WAIT_SUSPENDED under Control
- SB002 owner: MAIN
- SB002 target branch: system-build/sb002-causal-scope-revision-pilot-20260928
- target branch observed at start: absent

## Allowed actions

- Read-only verification of R159 request, receipt, history, latest and state.
- Read-only MAIN/Control/assignment/ref freshness and handoff reconciliation.
- Utility-owned start/result/state publication only.

## Forbidden actions

- No SB002 implementation, build execution or branch creation.
- No scientific execution, scoring, rescore, held-out access or result reinterpretation.
- No mutation of Analyst, MAIN, Control, research/system-build or scheduler state.
- No scheduler changes.

## Stop condition

Stop immediately if MAIN acknowledges R159 or begins SB002, if ownership becomes ambiguous, or after one bounded reconciliation report.

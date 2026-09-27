# Utility autonomous task start — R161 M1 rolling-contract handoff readback

schema_version: 2
started_at: 2026-09-28T05:28:44+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260928T052844+0900-R161-M1-HANDOFF-READBACK
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_INTEGRATION_AND_PROVENANCE_RECONCILIATION_ONLY

## Objective

Independently verify the Evidence Analyst R161 persistence transaction and its exact MAIN handoff target for the four-stage Integrated Prototype Milestone 1 rolling SYSTEM_BUILD contract.

## Trigger / source

- Utility assignment pointer is schema-v2 clean IDLE.
- No new Utility request has been appended since 2026-09-24.
- HUMAN-20260928-001 makes Integrated Prototype Milestone 1 primary and explicitly permits Utility provenance/readback verification outside MAIN's critical path.
- HUMAN-20260928-002 keeps FLY-0 isolated on the Forge lane and outside the M1 dependency graph.
- Evidence Analyst R161 newly grants MAIN a repair-first four-milestone rolling contract, while durable MAIN R166 still records the prior R160 wait state.

## Ownership checks at start

- Control: CTRL-20260928T045012+0900-R102-M1-AUTHORITY-GAP-HOLD
- Evidence Analyst: EVA-20260928T045927+0900-R161-M1-ROLLING-CONTRACT-SB002-INTEGRITY
- MAIN: MAIN-20260928T041557+0900-PRIMARY-R166-SB002-DEFECTS-WAIT-ANALYST
- Relay allocation: none; Relay intentionally disabled by Control
- M1 owner: MAIN
- M1 branch: system-build/ipm1-continuous-revision-20260928
- Required and observed M1 branch base/head: 6b4d219d4cc929a63981b98d6d5d73fd8e175f48

## Allowed actions

- Read-only verification of R161 request, receipt, history, latest and state bindings.
- Read-only verification of the authorized M1 branch/base and current MAIN acknowledgement state.
- Read-only ownership and collision reconciliation.
- Utility-owned start/result/state publication only.

## Forbidden actions

- No M1/SB002 code, tests, branch, PR, main or scientific artifact mutation.
- No scientific execution, comparator run, scoring, rescore, held-out access or result reinterpretation.
- No mutation of Analyst, MAIN, Relay, Control or scheduler state.
- No FLY-0/SB003 work or mixing into M1.

## Stop condition

Stop after one bounded transaction/handoff report, or immediately if Analyst, MAIN, Control, assignment or the exact M1 branch materially supersedes the recorded ownership before publication.

# Utility autonomous task start

schema_version: 2
autonomous_task_id: UTILITY-AUTO-20260927T192400+0900-R153-V4-HANDOFF-RECON
assignment_mode: AUTONOMOUS_IDLE
status: RUNNING
started_at: 2026-09-27T19:24:20+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_HANDOFF_RECONCILIATION_ONLY
scientific_authority: NONE

## Objective

Independently verify that Evidence Analyst R153 is durably published and gives MAIN one unambiguous, bounded RD006 v4 implementation/preflight handoff without granting result-bearing execution.

## Trigger / source

The Utility assignment pointer is clean schema-v2 IDLE. Analyst R153 is newer than MAIN R160 and Control R95, so the current highest-value complementary task is a read-only handoff and collision reconciliation.

## Ownership checks

- Utility assignment: schema-v2 clean IDLE
- Evidence Analyst: R153; RD006 v4 contract implementation and synthetic preflight allocated to MAIN
- MAIN: R160; still bound to R152 and waiting for fresh Analyst reconciliation
- Control: R95; still observes R152 and P0 remains closed
- Relay: intentional dependency-wait under Control ownership
- Utility scope overlap: none

## Allowed actions

- Read-only verification of R153 request/receipt/history/latest/state and MAIN/Control ownership generations.
- Utility-owned result/state publication only.

## Forbidden actions

- No RD006 implementation, dynamics, matrix, scoring, held-out access or workflow dispatch.
- No mutation of Analyst, MAIN, Control, research, evidence or scheduler state.
- No reinterpretation of R153 scientific authority and no P0 reopen/closure decision.

## Stop condition

Stop after one bounded R153-to-MAIN handoff reconciliation and Utility-owned durable report.

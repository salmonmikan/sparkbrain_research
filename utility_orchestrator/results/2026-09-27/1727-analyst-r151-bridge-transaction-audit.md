# Utility result — Evidence Analyst R151 bridge transaction audit

schema_version: 2
generation_id: UTILITY-20260927T172727+0900-ANALYST-R151-BRIDGE-AUDIT
produced_at: 2026-09-27T17:27:27+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260927T172300+0900-ANALYST-R151-BRIDGE-AUDIT
status: COMPLETED
evidentiary_status: NON_EVIDENTIARY_PERSISTENCE_TRANSACTION_AUDIT_ONLY
scientific_authority: NONE
classification: ANALYST_R151_BRIDGE_TRANSACTION_VERIFIED

## Result

The newest retained Evidence Analyst Actions-bridge transaction, R151, is end-to-end consistent.

- Request ID: `EA-R151-20260927T1700JST`
- Request commit: `6586865fe51654d9d8cb63782c6dc2e904f48855`
- Request blob: `e4a69b3af4da1b026360bc1d98a2196202048f40`
- Computed request SHA-256 exactly matches the receipt: `02c4ae731f0a5ed9bffed38b8c10f3d055e5c37cb17d5b0e7b18188b25079da9`
- Expected target head: `32e17655e21c4dbdb686a5234c00f58a854796aa`
- Result commit: `1a0a56b9f9360c95c77ac24d9a217f2945169a6e`
- The result commit's sole parent exactly equals the expected target head.
- Receipt exists with `persistence_complete=true`, workflow attempt 1 and `scientific_execution=false`.
- Request `history_content`, `latest_content` and `state_content` each match the target files byte-for-byte.
- Target history, latest and state all identify Analyst R151; no active pointer debt was observed.

This verifies the tested R151 bridge transaction only. It does not prove the internal root cause of the closed P0 incident or every possible write path.

## Ownership / collision reconciliation

- Utility assignment remains schema-v2 clean IDLE.
- Analyst R151 owns the allocation and assigns exactly one bounded RD006 v3 D0 matrix to MAIN.
- MAIN R158 predates R151 and has not yet durably acknowledged it; this is an ordinary handoff wait, not a persistence fault.
- Relay remains intentionally dependency-wait suspended under Control ownership.
- Utility performed no RD006, MAIN, Relay, Analyst, Control or scheduler mutation.

## Funnel fields observed without reinterpretation

- object_id: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`
- revision: `v3-structural-temporal-role-preflight`
- development_phase: `OPEN_DEVELOPMENT`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- preformal_readiness: `NOT_READY`
- queue_state: `ALLOCATED_ONE_BOUNDED_D0_MATRIX_GATE_CLARIFIED`
- evidentiary_status: `DEVELOPMENT_ZERO_CONFIRMATORY_CREDIT`
- scientific_credit: `0`
- hold_class, hold_reason, terminal_state and system_priority_exception: not serialized in R151; no inference

## Exact refs observed immediately before final publication

- Utility: `97835e1ca4c55c80c22e72220dc8b6aeaa70c608`
- Evidence Analyst: `1a0a56b9f9360c95c77ac24d9a217f2945169a6e`
- Evidence persistence requests: `6586865fe51654d9d8cb63782c6dc2e904f48855`
- Control: `927a2c84dccc49140dc720a48c52f399d4e0692a`
- MAIN reports: `48d02ef9bb015b2c7c30fba0364bea65c6abe665`
- main: `cf0bc45262824f1fe282ccd7b785b3ea50be2099`
- Human Directives: `3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7`

## Hard floor

No experiment, dynamics, scoring, result-bearing workflow, scientific ref, evidence ref, candidate authority, Control state or scheduler state was changed.

stop_reason: ONE_BOUNDED_READ_ONLY_TRANSACTION_AUDIT_COMPLETE
follow_up_recommendation: NONE_BRIDGE_TRANSACTION_CLEAN_MAIN_ACK_PENDING_NORMAL_HANDOFF

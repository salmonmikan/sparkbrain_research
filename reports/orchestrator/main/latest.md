# MAIN RELAY — Receptor simultaneity ordering Architecture cycle 1 completed

Timestamp: `2026-09-20 10:47 JST`  
Worker role: `main`  
Execution mode: `RELAY`  
Evidence Analyst authority: `639a5f7baba926502965bc9fea4cdcfb9f749068`  
Analyst generation: `LEGACY_GENERATION_UNKNOWN`  
Consumed MAIN generation: `LEGACY_GENERATION_UNKNOWN`  
New MAIN generation: `MAIN-20260920T1047+0900-RELAY-RECEPTOR-CI-COMPLETE`  
Research layer: `ARCHITECTURE_STUDY`  
Candidate: `CAND-V05-RECEPTOR-SIMULTANEITY-ORDERING-01`

## Lease / generation reconciliation

The prior PRIMARY lease was `WAITING_EXTERNAL`, not `RUNNING`, with heartbeat `2026-09-20T10:20:00+09:00`. No fresh same-object PRIMARY collision existed. The Analyst and prior MAIN control-plane files predate generation schema v2, so both are treated as `LEGACY_GENERATION_UNKNOWN`; authority was reconciled against current authoritative refs rather than timestamp order. Immediately before continuation, the Analyst tip remained `639a5f7baba926502965bc9fea4cdcfb9f749068`, stable `main` remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, and the exact research branch remained `research/main-v05-receptor-simultaneity-ordering-contract-arch-study-20260920@705b652f0eb426c7e39a75a9f901be10483d0e63`.

SUB is on a separate bounded checkpoint-continuation Discovery object and explicitly avoided the receptor-ordering MAIN lane; no collision exists.

## Exact continuation performed

RELAY performed only the continuation prospectively fixed by PRIMARY and still authorized by the current Analyst handoff: collect ordinary exact-head CI run `35481067945` and, on success, mark the current MAIN object complete and STOP for fresh Analyst review.

Run `35481067945` completed **successfully** on exact head `705b652f0eb426c7e39a75a9f901be10483d0e63`. Both Python `3.11` and `3.13` jobs completed successfully, including install, lint, local readiness, tests, and bundle validation.

The already-fixed NON_EVIDENTIARY Architecture terminal remains **`ORDER_UNSPECIFIED_AND_REACHABILITY_UNESTABLISHED`**. No terminal remapping, dynamic permutation diagnostic, aggregation comparator, cycle 2, production change, official TEST, PRE_FORMAL, FORMAL identity, STARTED, scorer, preserve/evidence mutation, consumed-identity retry, research merge, or Utility request occurred.

New scientific information in this RELAY continuation: **none**. The CI result is repository-integrity confirmation only and does not alter the previously mapped Architecture result.

## Stop state

Integrity status: **`GREEN_STATIC_TERMINAL_EXACT_HEAD_CI_SUCCESS`**.  
Stop reason: **`VALID_STATIC_TERMINAL_AND_EXACT_HEAD_CI_SUCCESS_STOP_FOR_FRESH_ANALYST_REVIEW`**.  
Final lease target: **`COMPLETED`**.  
Next MAIN action: wait for a fresh Evidence Analyst generation/commit. Do not automatically continue this receptor object, run a dynamic comparator, start cycle 2, or advance PRE_FORMAL/FORMAL.

Utility request created: `none`.  
Persistence: MAIN-owned `latest.md`, `state.json`, append-only history, and `lease.json` only on `ops/orchestrator-run-report`; no force push.

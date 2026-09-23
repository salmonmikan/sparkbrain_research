# Utility terminal-pointer reconciliation result

schema_version: 2
generation_id: UTILITY-20260923T192250+0900-PFR1-TERMINAL-POINTER-BLOCKED-R96-1C4E8A72
produced_at: 2026-09-23T19:22:50+09:00
assignment_mode: FAIL_CLOSED
status: BLOCKED
selected_task: PFR1_TERMINAL_ASSIGNMENT_POINTER_RECONCILIATION
fast_forge_support: false
evidentiary_status: NON_EVIDENTIARY_CONTROL_PLANE_ONLY
scientific_authority: NONE

## Authority finding

`utility_orchestrator/assignment/current.md` is still schema-v2 `ACTIVE` for assignment `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` generation `UASSIGN-20260923T155800+0900-PFR1-7B1D4E92`, with `max_runs: 1` and `completion_requires_control_ack: true`.

Utility state for that exact assignment/generation is already terminal `COMPLETED`, `run_count: 1`, `max_runs: 1`, with stop reason `COMPLETED_EXACT_BYTES_PRESERVED_AND_REVERIFIED` and exact-byte durability status `DURABLY_AVAILABLE_EXACT_BYTES_VERIFIED`.

Therefore the current pointer references an already-terminal/max-runs-consumed assignment. Under schema-v2 Utility authority rules this is not executable assignment authority. Because the pointer is not clean IDLE, Utility also MUST NOT fall through to Autonomous Idle or Fast Forge. This run fails closed.

## Ownership / freshness checks

- Evidence Analyst: `EVA-20260923T180248+0900-R96-3F7C92A1` at `ops/evidence-analyst-handoff@df97c2c8830c7d50d23d13c43091866ad5d23c77`; no newer Analyst generation observed.
- MAIN latest durable: `MAIN-20260923T184514+0900-PRIMARY-CAND35-ARCHR2-R96-COMPLETED`; Candidate #35 Architecture R2 NON_RESULT implementation and exact-head CI are complete and returned to Evidence Analyst.
- MAIN active candidate branch authoritative ref: `research/main-cand35-queue-free-subthreshold-architecture-r96-cycle3@8ea6581544c642ad74f1a95955ab2c5f795afccc`.
- Fast Forge latest: `FORGE-20260923T183716+0900-NOOP-CAND35-R2-SHADOW-R96`; no Forge object or Utility request exists there.
- Relay: no distinct fresh Relay branch/state was observed in the currently exposed orchestrator control-plane; no Relay authority was inferred.
- Control strategy: `ops/control-brain-handoff@1592c3b52a8a545aa2503fd4618c0a761921ef1e` (R43); no post-completion Control acknowledgement was observed.
- Stable authoritative `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.
- Utility mailbox branch immediately before mutation: `ops/utility-orchestrator-requests@829e860d191d78970c978d194816d54fa574d7af`.

## Actions

1. Re-read current assignment pointer and terminal Utility state.
2. Re-read latest Evidence Analyst, MAIN ownership/lease, Fast Forge state, Control strategy and authoritative repository refs.
3. Performed no scientific/research mutation and no workflow action.
4. Appended one bounded Control follow-up request asking only for completion acknowledgement and compare-and-swap closure/archive of the exact terminal assignment generation.
5. Persisted this Utility-owned terminal BLOCKED result/state.

## Scientific / integrity impact

- candidate/Funnel mutation: none
- PRE_FORMAL or FORMAL action: none
- scientific identity or STARTED creation: none
- protected outcome access/scoring: none
- consumed identity rerun/retune/rescore: none
- evidence/formal/sealed/control/preserve destructive mutation: none
- research branch mutation: none
- workflow dispatch: none
- scheduler mutation: none
- research PR merge: none
- hidden MAIN dependency: none
- hard-floor actions: NONE

## Observation

Candidate #35 Architecture R2 completed after the prior Utility preservation run, but it remains explicitly NON_RESULT with `claim_ceiling: SYSTEM`, `preformal_eligible: false`, and no candidate response or FORMAL action. Utility does not reinterpret or promote it.

stop_reason: TERMINAL_ASSIGNMENT_STILL_ACTIVE_PENDING_CONTROL_ACK_FAIL_CLOSED
follow_up_recommendation: Control should acknowledge the existing completed Utility result and CAS-close/archive the exact matching assignment generation, returning `assignment/current.md` to clean schema-v2 IDLE if no new assignment is intended.
request_created: utility_orchestrator/requests/UTILREQ-20260923T192250+0900-PFR1-COMPLETION-ACK-POINTER-CLOSE.md

# RELAY MAIN — CAND-TOPK-PA-01 cycle-2 replication dispatched; waiting for exact-head CI/workflow

Timestamp: `2026-09-19 18:48 JST`  
Worker role: `main`  
Execution mode: `RELAY`  
Evidence Analyst authority: `5b63d21f44812ef8d4938c9ad968bb8ab481b3c5`  
Research layer: `ARCHITECTURE_STUDY`  
Evidentiary status: `NON_EVIDENTIARY`

## Continuation performed

Fresh Evidence Analyst authority prospectively authorized exactly one independent-seed replication of `CAND-TOPK-PA-01` from `research/main-topk-persistent-amplification-arch-study-20260919@97f542d86dcd3a609cd039379fcda41ba61e0909`. The only authorized scientific change is model/training seed `41 -> 42`; DEV surface, 48 training episodes, 12 disjoint calibration episodes, probe positions `6/12/18/24`, perturbation seed `20260919`, relative magnitudes `0.01/0.05/0.10`, 8 directions, horizon 6, `full` vs `no_persistent_state`, turnover minimum 20, signal thresholds, and ordinary-reduction thresholds remain unchanged. TEST and all FORMAL surfaces remain forbidden.

RELAY created one fast-forward research commit, `04ced2b97ed088bb2cdb086d164a86212741e601`, directly on the authorized continuation head. The diff is limited to:
- adding `scripts/architecture_studies/topk_persistent_amplification_cycle2.py`, a science-invariant wrapper that reuses the accepted cycle-1 implementation, asserts the fixed contract, and changes only the in-memory model seed from 41 to 42 while binding fresh Analyst authority;
- changing `.github/workflows/ci.yml` so the Python 3.11 tail step runs/uploads cycle 2 instead of rerunning cycle 1.

No cycle-1 rerun was dispatched as an intermediate commit; the two-file change was committed atomically before the branch ref moved.

## Workflow / integrity

Push CI/workflow run `35435714352` is on exact head `04ced2b97ed088bb2cdb086d164a86212741e601`, attempt 1. At checkpoint both `test (3.11)` and `test (3.13)` jobs are `in_progress`; checkout succeeded and Python setup is in progress. Lint, readiness, tests, bundle validation, the cycle-2 DEV execution, and raw artifact upload have not yet completed.

The architecture step is ordered after ordinary lint/readiness/test/bundle validation in the same exact-head workflow. No result has yet become visible and no scientific interpretation has been made. No formal identity, STARTED/control authority, formal preserve/scoring/evidence ref, official TEST access, consumed formal raw, merge, retune, redesign, or Utility request was created.

Collision reconciliation: prior PRIMARY lease was `COMPLETED`; no fresh PRIMARY `RUNNING` lease or same-object mutation was present. SUB remains on independent work and does not own this MAIN candidate.

## Stop

Lease ends `WAITING_EXTERNAL`. Stop reason: `EXACT_HEAD_CYCLE2_CI_AND_DEV_WORKFLOW_IN_PROGRESS`.

Next MAIN action: collect workflow `35435714352` only. If a pre-execution mechanical CI defect occurs before diagnostics are visible, apply only a science-invariant fix and recheck exact-head CI. If any semantic/protocol gap, TEST leakage, or post-execution failure after diagnostics become visible occurs, STOP for Analyst. If the run is valid, first verify the uploaded raw artifact and metadata, then classify strictly under the prospectively fixed cycle-2 mapping and STOP for fresh Analyst review. No same-run retuning or successor construction is authorized.

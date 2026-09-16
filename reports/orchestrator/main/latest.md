# SparkBrain Research Orchestrator — MAIN latest

Timestamp: `2026-09-17T06:33:00+09:00`
Worker role: `main`
Evidence Analyst authority: `7bfef197fe0b255e395d2ea18ebadb59f2ca9fb6`

## MAIN frontier

MAIN advanced the primary C19-v2 frontier through the current Analyst-authorized frozen execution-contract closure on `research/c19-truth-free-symbolic-adapter-v2-20260917`.

Final research head: `66c8eafe9863ed1b2455cc833a3dc498ce7721b0`.
Frozen scientific protocol anchor: `90c936a7abca7eba0dac1f977753503551e73368`.
Planned one-way identity: `c19-external-v2-official-v1` remains fresh, unSTARTED, and unconsumed.

The run started from `17ce3e61d17436337d13c90c6c86184fcad09f22`. No concurrent C19 movement was observed after the initial refetch. Current Analyst `sub_lane=null` / `sub_fallback=null`, so no reserved independent SUB work existed.

## Critical-path fixes completed

MAIN closed the raw-contract mismatch without changing frozen science:

- `official_execution.py` now materializes the exact frozen 16-field target-blind raw schema instead of the prior six-field ad-hoc payload. Raw `record_id` is discarded and only a SHA-256 `record_id_hash` is persisted.
- Raw validation now requires exactly 55 rows × 1,744 unique pair indices, rejects duplicates/missing/out-of-range pairs, and requires the same `(record_id_hash, source_index, step_index)` identity for each pair across all rows.
- The source-bound baseline executor now exposes the already-determined final step index required by the frozen raw contract.
- Synthetic tests exercise the exact 95,920-record contract, fail closed on missing/duplicate coverage and cross-row identity mismatch, retain target-leakage rejection, no-clobber, reconstruction, preservation receipt, and raw-before-score ordering.
- Source-binding tests were kept lightweight and source-only while still traversing all 55 frozen row definitions; implementation-binding Git blob hashes were refreshed.
- `execution_harness_contract.json` was reconciled with the already source-bound condition and baseline executors and now records exact raw-schema/coverage closure instead of calling them unbound.

Exact-head CI run `35152618704` completed successfully on Python 3.11 and 3.13. Install, Lint, Local readiness, Test, and Validate bundle all succeeded.

## Same-run continuation

Consumed prospective branches:

`PRE_START_CONTRACT_MISMATCH` → `PRE_START_COVERAGE_GUARD_INCOMPLETE` → `PRE_START_SCORER_BINDING_INCOMPLETE` → `PRE_START_SCORER_SEMANTICS_AMBIGUOUS`.

MAIN continued through the raw-schema and exact pair-coverage defects because both fixes are mechanically determined by the frozen protocol and explicitly prospectively authorized. After closing them, MAIN inspected the remaining scorer boundary rather than inventing a scorer.

## Why MAIN stopped

The frozen protocol fixes BU-Acc, BM-Acc, BREU, the update/maintain slice counts, 10,000 paired bootstrap resamples, seed `19901`, official-pair resampling, shared resample indices across five seeds, the primary contrast, and PASS/FAIL/INCONCLUSIVE inequalities.

It does not uniquely freeze two concrete scorer choices required for byte-reproducible execution: the exact evaluator-target payload/interface and the exact empirical-quantile/interpolation convention for the two-sided 95% bootstrap CI. Repository history contains other experiment-specific bootstrap conventions, but the frozen C19-v2 protocol does not bind one of them. Selecting one now would add scoring semantics after protocol freeze.

The current Analyst contingency explicitly requires STOP at `PRE_START_SCORER_SEMANTICS_AMBIGUOUS`. MAIN therefore did not implement a scorer, create STARTED, access/verify official Belief-R content, dispatch acquisition, score, preserve official evidence, or consume the planned identity.

## Readiness/scientific result

New scientific measurement: **none**.

New readiness information: the exact target-blind raw schema and complete 55 × 1,744 pair coverage are now fail-closed and green; the remaining scorer ambiguity is explicit rather than hidden behind a generic interface. The preserver remains interface-bound only and no preserve authority was created.

## SUB boundary / collision reconciliation

Current Analyst supplies no independent SUB lane or fallback. MAIN did not absorb independent SUB work and did not delegate any MAIN blocker to SUB. No Analyst split was invalidated for putting a MAIN blocker on SUB.

Independent work intentionally left for SUB: none under the current handoff. SUB should remain no-op until a newer Analyst reserves genuinely independent work.

## Integrity state

- Frozen protocol/metric/threshold/result classes/55-row inventory/seeds/baseline family set/planned identity: unchanged.
- C19 `control/*` and `preserve/*` remain absent at final reconciliation; no STARTED authority exists.
- Official data access: none.
- Identity consumption: none.
- Existing immutable legacy freeze/control/preserve/evidence authorities: untouched.
- PRs/merges: none.
- Human-review override: not used.

## Next MAIN action

Return exact package `research/c19-truth-free-symbolic-adapter-v2-20260917@66c8eafe9863ed1b2455cc833a3dc498ce7721b0`, green CI `35152618704`, exact raw-contract closure, and the explicit scorer-semantics ambiguity to Evidence Analyst. A fresh prospective handoff must bind or otherwise resolve the evaluator-target schema and bootstrap CI convention before MAIN may continue scorer implementation or return to execution admission. Official one-way execution remains forbidden under the current handoff.

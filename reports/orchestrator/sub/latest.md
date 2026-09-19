# SparkBrain Research Orchestrator SUB — 2026-09-20 01:47 JST

## Mode / allocation

- mode: `discovery`
- Evidence Analyst authority: `e781202e8c7ae4562c10fa46cdddfb3b0eb1bc08`
- SUB lane consumed: `BOUNDED_SECONDARY_DISCOVERY`
- formal SUB lane: none
- fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- selected target: `TOPOLOGY_RECEPTOR_FANOUT_ALIASING_DISCOVERY`
- candidate_pool_id: none; one safe bounded SUB self-selection outside the reserved candidate pool
- exploration cycle: `1/3`
- evidentiary status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## MAIN frontier avoided / integrity

Fresh `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` and fresh Evidence Analyst authority remains `e781202e8c7ae4562c10fa46cdddfb3b0eb1bc08`. MAIN is holding after `CAND-TEMPORAL-BATCH-PARTITION-01`; SUB did not continue that line, construct a successor, touch Top-k follow-up, H7 construction, consumed-line rescue, formal/TEST/scoring/preserve/evidence surfaces, or any MAIN blocker. No MAIN active research branch was modified.

Five authoritative evidence tags remain the observed scientific anchors; no new formal/sealed/freeze tag was created and legacy freeze/control/preserve refs were left untouched. Consumed identities were not accessed or rerun.

## Discovery question / implementation

Created non-authoritative branch `research/exploratory-sub-topology-fanout-aliasing-20260920` from exact stable main. The prospective question was bound first in commit `91aaf6c10ed691540689fe3d426d6a9354828e2e`; the deterministic topology test was added in `cdff7a4b29d0fdd4263897c208359e2b90ce4681`. Two subsequent commits (`726aac111720643e6f1475a91477e6db3204372c`, `daaf9a865d4ba5911640d127f55dc8d44a75e078`) changed formatting/import hygiene only. Exact final research head: `daaf9a865d4ba5911640d127f55dc8d44a75e078`.

Question: with `receptor_count=16`, does the fixed v0.5 receptor routing stride `11` create scale-specific physical first-hop projection aliasing when reservoir size shares a factor with 11, and does the default two-receptor input fanout inherit the same collapse?

Fixed synthetic/static matrix: reservoir dimensions `(4,4)`, `(5,5)`, `(6,6)`, `(8,6)`, `(4,11)`, `(5,11)`, `(6,11)`, `(8,11)`. No repository dataset, trained checkpoint, formal raw, held-out TEST, official scorer, or consumed identity was used.

## Observations

For reservoir sizes `16,25,36,48` (coprime with 11), all 16 receptor first-hop signatures remain unique: no collision pairs and maximum alias multiplicity 1. For the resonant sizes `44,55,66,88`, unique receptor signatures collapse to `4,5,6,8` respectively, with collision-pair counts `24,18,14,8` and maximum alias multiplicities `4,4,3,2`.

The exact count is explained by the modular period `N / gcd(N, 11)`: unique signatures equal `min(16, N/gcd(N,11))`. The default two-consecutive-receptor routing path inherits the collapse: the 16 possible start receptors produce only `4,6,7,8` unique first-hop pair projections at `N=44,55,66,88`, versus 16/16 across all four tested coprime sizes. The current default `8x6` reservoir (`N=48`) is non-resonant in this check.

This is an actual physical wiring collision in reservoir targets, not metadata/hash bookkeeping. The immediate cause is nevertheless exactly reducible to deterministic number-theoretic aliasing from the fixed stride `11` modulo reservoir size; no emergent mechanism is claimed.

Ordinary CI initially failed only on Ruff formatting/import hygiene (`35455648337`, then `35455755740`); no scientific assertion failed in those runs because tests were skipped after lint. Exact-head CI `35455915055` then completed `success` on Python 3.11 and 3.13, including lint, readiness, tests, and bundle validation.

## Handoff / stop

Evidentiary status remains `NON_EVIDENTIARY`. Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`, because the aliasing changes physical first-hop connectivity and can reduce 16 nominal receptor routes to as few as four projection classes at resonant reservoir sizes. This is a candidate architecture/scaling constraint, not evidence of functional harm or scientific novelty.

A fresh prospective Architecture Study, if accepted, should use DEV-only inputs and compare the current stride-11 fanout against an identity-neutral/resource-matched collision-free or hash-based fanout at matched edge count/resources across resonant and non-resonant sizes. It should predefine an internal channel-separability observable plus a downstream prediction/action observable and horizon.

The candidate would be reduced to a static engineering wiring constraint if supported production/DEV dimensions never enter resonant regimes, or if a matched collision-free comparator does not improve internal/downstream distinction despite removing projection collisions. Open scientific choices before promotion: DEV dimensions/regimes, channel set, comparator construction/resource matching, internal separability metric, downstream observable, and horizon. SUB does not continue cycle 2 without fresh Analyst repartition.

Utility request created: none. Consumed identities: none. New formal results: zero. STARTED/control/freeze/evidence/official-score actions: zero. Blocker: fresh Evidence Analyst classification/prospective Architecture Study specification only.

Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_DISCOVERY_CYCLE_AND_RETURNED_TOPOLOGY_ARCHITECTURE_PROMOTION_CANDIDATE_FOR_FRESH_ANALYST_REVIEW`.

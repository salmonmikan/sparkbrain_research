# SparkBrain Fast Forge — coverage-aware outcome guard

- schema_version: `2`
- generation_id: `FORGE-20260927T124400+0900-COVERAGE-AWARE-OUTCOME-GUARD-CI-CLEAN`
- produced_at: `2026-09-27T12:44:00+09:00`
- forge_id: `FORGE-COVERAGE-AWARE-OUTCOME-GUARD-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260927-coverage-aware-outcome-guard-a`
- exact_prototype_head: `a946b1713eb8286039aac5457cbc2b32c8d4868b`
- ci_run: `36292138103`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: `0`
- new_scientific_result: `false`

## Target capability

Keep an observed outcome omitted by a top-k prediction pool set-valued instead of silently assigning it probability zero or the whole unexposed tail mass, while preserving the existing exact revision path for exposed outcomes.

## Prototype and diagnostics

Added:

- `forge_prototypes/coverage_aware_outcome_guard.py`
- `forge_prototypes/coverage_aware_outcome_guard.md`
- `tests/test_forge_coverage_aware_outcome_guard.py`

Verified behaviors:

1. exposed outcomes retain the exact `1 - P(y)` revision path;
2. omitted outcomes use `P(y) in [0, tail_mass]` and therefore `error in [exposed_mass, 1]`;
3. both routing endpoints are inspected on an isolated checkpoint copy;
4. an endpoint-stable route is reported without mutating live scope or revision state;
5. a tail interval whose endpoints select different routes becomes explicit abstention/no-write;
6. invalid or overfull exposed probability mass fails closed;
7. even the first omitted outcome cannot create a live empty allocator cache;
8. checkpoint round-trip preserves interval routing.

Local focused tests passed 13/13, all Forge tests passed 61/61 and Ruff passed. Local readiness passed. Repository-wide local collection was unavailable because optional `fastapi`, `torch` and `jsonschema` packages were absent. Exact-head CI run 36292138103 passed on Python 3.11 and 3.13, including lint, local readiness, the full test suite and bundle validation.

## Ordinary reduction

This is ordinary interval/imprecise-probability handling for a truncated categorical distribution plus a monotone endpoint robustness check and checkpoint-isolated inspection. It is not calibrated open-set recognition, a learned uncertainty model, a new memory mechanism or scientific evidence.

## Engineering usefulness

The guard closes the most immediate overconfidence seam in the observed-outcome loop. A missing top-k label no longer masquerades as exact zero probability. The integration can distinguish a routing decision stable across every admissible tail assignment from a decision that depends on an unknown assignment, while keeping every omitted-label path non-mutating because the current revision overlay cannot revise an unexposed value.

## Limitations and claim boundary

- The prediction pool and thresholds remain fixed and uncalibrated.
- The interval assumes the exposed probabilities are normalized against the full categorical support; this holds for the current histogram-derived pool but is not a general API guarantee.
- Endpoint robustness relies on the current router's monotone NEW_SCOPE score with fixed existing-scope scores.
- Stable routing for an omitted outcome is diagnostic only; it does not allocate a scope or revise support.
- No open-set learner, continuous stream, task capability, matched comparator, resource match or interaction ablation is tested.
- The prototype supports a bounded integration guard only, not SYSTEM_BUILD admission, composition contribution or scientific novelty.
- It is not admitted to SB001 or RV02 and creates no candidate/build identity.

## Collision and integrity

Evidence Analyst R147 allocates MAIN only RD006 v2 lag alignment. MAIN's moving report remains R156 while Methodology R129 observes the bounded v2 result; both are owned outside Forge and untouched. SB001 remains integrated complete and Relay remains in dependency wait. No research, main, evidence, preserve, consumed, frozen or FORMAL ref was mutated.

Inputs: main `cf0bc45262824f1fe282ccd7b785b3ea50be2099`; Analyst R147 at `df0ab5d5dc4941de8a9bba95949a00d6a7c4ce16`; MAIN R156 at `8d5b6c36122c3e8a2ee2ada2a9c6d40272131885`; Control R90 at `ca934c91c2e371a41e1a8b88ca8c7827f128f64f`; Methodology R129 at `4763b74f8bc9f9f684cb7ef86e97ea9a7361bcf4`; Utility at `fdb220d7ee6880910d244127bc960b5ba82e7593`; Theory R7, Literature R45 and Audit R10 on external-science head `3538e527ded0e494dca889d4dc55eef34a9d0f3e`; source Forge handoff `66ac0fa9824a6e1a4c9d8fe5763be0f7d1b0e04e`.

## Publication

The prototype was published to an isolated Forge branch and independently read back. One implementation defect found before final handoff—lazy creation of an empty allocator cache on a nominal no-write path—was corrected and covered by a regression test. Exact-current-head CI then passed. P0 remains Control-closed; this record makes no new incident diagnosis.

## Handoff

`FORGE_INTERESTING / SYSTEM_BUILD_INPUT`.

Evidence Analyst may optionally retain this guard with the observed-outcome adapter for a future separately bound SYSTEM_BUILD. No Utility request was created.

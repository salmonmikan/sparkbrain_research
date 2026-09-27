# SparkBrain Fast Forge — observed-outcome revision loop

- schema_version: `2`
- generation_id: `FORGE-20260927T115008+0900-OBSERVED-OUTCOME-REVISION-LOOP-CI-CLEAN`
- produced_at: `2026-09-27T11:50:08+09:00`
- forge_id: `FORGE-OBSERVED-OUTCOME-REVISION-LOOP-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260927-observed-outcome-revision-loop-a`
- exact_prototype_head: `74194d38dddacc1bee6559699b26e5723125719f`
- ci_run: `36289483166`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: `0`
- new_scientific_result: `false`

## Target capability

Drive the existing plural-scope revision bridge from an exposed prediction pool and the actual later observed outcome, without accepting a caller-computed prediction-error scalar or caller-supplied scope identity.

## Prototype and diagnostics

Added:

- `forge_prototypes/observed_outcome_revision_loop.py`
- `forge_prototypes/observed_outcome_revision_loop.md`
- `tests/test_forge_observed_outcome_revision_loop.py`

Verified behaviors:

1. the public mutation API accepts neither `prediction_error` nor scope/regime/episode identity;
2. the adapter derives the bounded residual `1 - P(observed outcome)` from the exposed pool;
3. an exposed low-probability outcome can create a scope and apply revision;
4. a later high-probability outcome can reuse the internally selected scope;
5. an outcome missing from the exposed pool is an explicit zero-mutation diagnostic;
6. invalid probability mass fails closed;
7. bridge state and derived behavior replay deterministically after checkpoint round-trip.

Exact-head CI run 36289483166 passed on Python 3.11 and 3.13, including Ruff, local readiness, full tests and bundle validation. Local focused tests passed 13/13 and all Forge tests passed 54/54. The local environment lacked optional `fastapi`, `torch` and `jsonschema`, so repository-wide collection and local bundle validation were not available there; exact-head CI supplied those dependencies and passed both.

## Ordinary reduction

This is ordinary categorical residual scoring (`1 - P(y)`) plus validation and transactional API-boundary engineering around the existing bridge. It is not a calibrated Bayesian posterior, proper-scoring-rule study, predictive learner, uncertainty mechanism or scientific result.

## Engineering usefulness

The adapter closes the caller-error seam identified in the prior plural-scope revision bridge. Revision routing can now be exercised from observable prediction/outcome data while keeping unexposed outcomes non-mutating. It also makes top-k exposure a visible integration boundary instead of silently treating a missing outcome as revisable.

## Limitations and claim boundary

- The exposed probability pool and all routing/allocation thresholds remain fixed and uncalibrated.
- `1 - P(y)` is only a bounded residual; no proper-scoring-rule comparison is claimed.
- An outcome outside the exposed pool cannot be revised and remains a no-write diagnostic.
- No continuous stream, task capability, comparator, resource match or interaction ablation is run.
- The prototype establishes bounded component composition only, not composition contribution or SYSTEM_BUILD readiness.
- It is not admitted to SB001 or RV02 and creates no candidate/build identity.
- Its engineering usefulness does not establish scientific novelty.

## Collision and integrity

Evidence Analyst R146 allocates FORMAL no action and retains the prior plural-scope bridge only as an optional future separately bound SYSTEM_BUILD input. MAIN R156 completed the preserved-result RD006 diagnostic audit and waits for Analyst; it remains untouched. SB001 remains integrated complete. Relay remains in dependency wait. No research, main, evidence, preserve, consumed, frozen or FORMAL ref was mutated.

Inputs: main `cf0bc45262824f1fe282ccd7b785b3ea50be2099`; Analyst R146 at `a8dfad75ff6d99f184e570d7aeb01b4951446f82`; MAIN R156 at `8d5b6c36122c3e8a2ee2ada2a9c6d40272131885`; Control R90 at `ca934c91c2e371a41e1a8b88ca8c7827f128f64f`; Methodology R128 at `a63e512a1d1e59857d3634b682b2c795f03df6ab`; Utility post-P0 reconciliation at `fdb220d7ee6880910d244127bc960b5ba82e7593`; Theory R7; Literature R45; Audit R10; source Forge bridge handoff `77814d0c2ea97a7c350f443809bc3f23f294c3ce`.

## Publication

The isolated prototype was published atomically and independently read back on the first attempt. The P0 persistence incident is already Control-closed; this record makes no new incident diagnosis.

## Handoff

`FORGE_INTERESTING / SYSTEM_BUILD_INPUT`.

Evidence Analyst may optionally retain this adapter as a companion input to the previously retained bridge for a future separately bound SYSTEM_BUILD. No Utility request was created.

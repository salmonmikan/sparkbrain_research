# SparkBrain Fast Forge — coverage-aware outcome guard

Generation `FORGE-20260927T124400+0900-COVERAGE-AWARE-OUTCOME-GUARD-CI-CLEAN` built one isolated, noncanonical integration guard on branch `forge/20260927-coverage-aware-outcome-guard-a`.

The guard preserves exact revision for exposed outcomes. For a value omitted by a top-k pool, it derives only the admissible probability interval `[0, tail_mass]` and prediction-error interval `[exposed_mass, 1]`. It evaluates both routing endpoints on a checkpoint copy, reports whether the route is stable or tail-sensitive, and never mutates live state for an omitted outcome.

A pre-handoff defect was found after the first branch publication: nominal read-only routing lazily created an empty allocator cache. The final implementation evaluates omissions on a cloned checkpoint; a regression test proves that even the first omitted outcome leaves live state byte-equivalent at the serialized level.

Local focused tests passed 13/13, all Forge tests passed 61/61 and Ruff passed. Local readiness passed; repository-wide local collection lacked optional `fastapi`, `torch` and `jsonschema`. Exact prototype head `a946b1713eb8286039aac5457cbc2b32c8d4868b` passed CI run `36292138103` on Python 3.11 and 3.13, including lint, local readiness, full tests and bundle validation.

Ordinary reduction: interval/imprecise-probability handling for top-k truncation plus monotone endpoint robustness and transactional checkpoint isolation. This is not calibrated open-set recognition, composition evidence, scientific novelty or scientific evidence.

Collision check passed against Analyst R147 / MAIN-owned RD006 v2, completed SB001 and dependency-wait Relay. No canonical, research, evidence, preserve, consumed, frozen or FORMAL ref was modified.

Disposition: `FORGE_INTERESTING / SYSTEM_BUILD_INPUT`. No Utility request was created.

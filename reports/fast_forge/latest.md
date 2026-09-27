# SparkBrain Fast Forge — causal online scope-router probe

- schema_version: 2
- generation_id: `FORGE-20260927T234359+0900-CAUSAL-ONLINE-SCOPE-ROUTER-CI-CLEAN`
- produced_at: `2026-09-27T23:43:59+09:00`
- forge_id: `FORGE-CAUSAL-ONLINE-SCOPE-ROUTER-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260927-causal-online-scope-router-a`
- exact_prototype_head: `f980c13d984460f158a95e8181239db8d19c8468`
- ci_run: `36326791137`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0
- new_scientific_result: false

An isolated causal online two-centroid router recovered the bounded separable A/B fixture in interleaved, blocked and reverse-interleaved arrival orders using only the current observation and prior state. It rejected ambiguous-midpoint and out-of-support queries without mutation. Identical observations stayed collapsed to one component and the conflicting revision remained unresolved. Shared-prefix state/action equality demonstrates that the implementation does not consult future stream suffixes.

Local validation passed all locally available Forge tests 78/78, Ruff and compileall. Exact prototype head `f980c13d984460f158a95e8181239db8d19c8468` passed GitHub CI run `36326791137` on Python 3.11 and 3.13, including lint, readiness, full repository tests and bundle validation.

The implementation reduces to causal streaming two-centroid clustering with a fixed component cap, thresholded birth, online means, and margin/support rejection. K=2 and all thresholds are hand set; the first observation seeds a component; opaque component identity is order dependent; the fixture is hand-built, one-dimensional and deterministic; and no matched system or real-task evaluation exists. This bounded engineering usefulness does not establish comparative support, composition contribution or scientific novelty.

RD006 v4, SB001, MAIN/Relay ownership and all scientific refs remain untouched. The handoff is optional future SYSTEM_BUILD input only.

History: `reports/fast_forge/history/2026-09-27/2343-causal-online-scope-router-ci-clean.md`

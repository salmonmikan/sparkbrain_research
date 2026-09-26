# SparkBrain Fast Forge — Latest
schema_version: 2
generation_id: FORGE-20260926T223612+0900-SCOPED-HYPOTHESIS-REVISION-CI-CLEAN
produced_at: 2026-09-26T22:36:12+09:00
forge_id: FORGE-SCOPED-HYPOTHESIS-REVISION-A
status: FORGE_INTERESTING
recommended_handoff: SYSTEM_BUILD_INPUT
branch: forge/20260926-scoped-hypothesis-revision-a
exact_head: d0b48d76cac47f472ee073462964fd0ad0eabac8
ci_run: 36242697179
ci_result: SUCCESS
evidentiary_status: NON_EVIDENTIARY
scientific_credit: 0
new_scientific_result: false

The scoped late-evidence wrapper is now CI-clean on its exact Forge head. It isolates same-label evidence across different Assemblies and preserves JSON replay by scoping state to Assembly plus the exposed hypothesis set.

This is an engineering input only. It reduces to namespaced keyed state / cache partitioning, creates no scientific promotion, and is not admitted into SB001. Exact hypothesis-set scoping intentionally starts a fresh scope when pool membership changes; that avoids stale support reactivation but may fragment continuity and should be reconsidered prospectively if a later SYSTEM_BUILD has an explicit episode/context identity.

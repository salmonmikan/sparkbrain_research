# FORGE-SCOPED-HYPOTHESIS-REVISION-A

schema_version: 2
generation_id: FORGE-20260926T213500+0900-SCOPED-HYPOTHESIS-REVISION-A
produced_at: 2026-09-26T21:35:00+09:00
forge_id: FORGE-SCOPED-HYPOTHESIS-REVISION-A
status: FORGE_PROTOTYPE
evidentiary_status: NON_EVIDENTIARY
scientific_credit: 0
new_scientific_result: false

The previous late-evidence overlay keeps one global event list. A bounded development diagnostic shows that evidence recorded for assembly-1 changes the decision for assembly-2 when both expose the same hypothesis labels. This is a cross-context persistence leak, not a scientific result.

A Forge-only wrapper now namespaces events by assembly_id plus the exposed hypothesis-label set. Cross-Assembly support no longer transfers, a changed hypothesis set starts a fresh scope, and the scoped state remains JSON-saveable/replayable.

Ordinary reduction: namespaced keyed state / cache partitioning. This is an integration correctness guard, not a new memory or revision mechanism.

recommended_handoff: SYSTEM_BUILD_INPUT_IF_CI_CLEAN
main_collision_check: PASS_R139_R149_SB001_UNTOUCHED
SB001: e9b93456a0c37e2d1393463c167912e0e3968817 untouched
hard_floor_actions: NONE
ci_status: PENDING_POST_PUSH

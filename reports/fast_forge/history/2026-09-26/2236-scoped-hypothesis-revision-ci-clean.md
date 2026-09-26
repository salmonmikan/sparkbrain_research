# Fast Forge — scoped hypothesis revision exact-head validation

- schema_version: 2
- generation_id: FORGE-20260926T223612+0900-SCOPED-HYPOTHESIS-REVISION-CI-CLEAN
- produced_at: 2026-09-26T22:36:12+09:00
- forge_id: FORGE-SCOPED-HYPOTHESIS-REVISION-A
- status: FORGE_INTERESTING
- branch: `forge/20260926-scoped-hypothesis-revision-a`
- exact_head: `d0b48d76cac47f472ee073462964fd0ad0eabac8`
- CI: run `36242697179` — SUCCESS on Python 3.11 and 3.13
- evidentiary_status: NON_EVIDENTIARY
- scientific_credit: 0
- new_scientific_result: false

## Why now

The prior Forge generation left this wrapper at FORGE_PROTOTYPE pending post-push CI. Exact-head readback now shows both CI jobs completed successfully. Current MAIN work is SB001 on PR #152 head `909094a87025b552b96bcac4afb060b91c4f0573`; this Forge branch is separate and does not touch MAIN's build branch, workflow, scorer, identities, or scientific refs.

## Result

The existing bounded tests establish only development behavior:
- the prior unscoped overlay carries same-label support across different Assemblies;
- the scoped wrapper blocks that cross-Assembly carryover;
- changing the exposed hypothesis set starts a fresh scope rather than reactivating stale support;
- serialized state round-trips through JSON and reproduces the scoped evaluation.

This is ordinary engineering state partitioning, not a novel memory mechanism. The simplest explanation remains namespaced keyed state / cache partitioning.

## Engineering usefulness and limitation

The wrapper is useful as a future SYSTEM_BUILD input when multiple Assemblies or contexts may reuse the same hypothesis labels. It should not be mixed into SB001 without a later Analyst build allocation.

The current namespace is `(assembly_id, exposed_hypothesis_set)`. That deliberately prevents stale support from crossing hypothesis-set changes, but it also means valid evidence continuity is fragmented whenever pool membership changes. If a later integrated build has an explicit prospective episode/context identity, that identity may be a cleaner namespace; this is an engineering design question, not a scientific claim.

## Disposition

- FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- no scientific promotion proposed
- no candidate/build ID created
- no Revisit trigger
- no immutable/formal/evidence/preserve refs touched
- no consumed identity used
- no MAIN collision

# Fast Forge — scope-revision boundary stress probe

- schema_version: 2
- generation_id: `FORGE-20260927T204727+0900-SCOPE-REVISION-BOUNDARY-STRESS-CI-CLEAN`
- produced_at: `2026-09-27T20:47:27+09:00`
- forge_id: `FORGE-SCOPE-REVISION-BOUNDARY-STRESS-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260927-scope-revision-boundary-stress-a`
- exact_prototype_head: `89a51ba5a9506afc0f0f77b7ecccca224cd42ce4`
- CI: [run 36316697157](https://github.com/salmonmikan/sparkbrain_research/actions/runs/36316697157) — SUCCESS
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0
- new_scientific_result: false

## Question and why now

The prior continuous interaction ablation used two widely separated hand-built
clusters. This bounded follow-up asks whether the same connected-versus-cut
diagnostic survives small within-cluster jitter and one conflicting label, and
where the fixed router makes the composition unevaluable.

This remains independent of MAIN's RD006 v4 critical path. It does not execute
RD006, alter SB001, or touch any scientific, formal, evidence, preserve or
control ref.

## Prototype

Added:

- `forge_prototypes/scope_revision_boundary_stress.py`
- `forge_prototypes/scope_revision_boundary_stress.md`
- `tests/test_forge_scope_revision_boundary_stress.py`

The probe runs three deterministic synthetic cases with the same fixed
allocator/router/revision configuration and the existing connected/cut arms.
It accepts no caller scope, regime, episode, truth or evaluator identity.

## Diagnostics and observations

1. `moderate_overlap_with_midpoint_reject`
   - both arms committed 4/4 events and generated the same two opaque scopes;
   - connected queries recovered A and B;
   - the cut arm abstained for both contexts after global support collision;
   - both arms abstained at the ambiguous midpoint.
2. `within_reuse_radius_collision`
   - only one scope was formed and only 2/4 events committed;
   - the connected arm recovered A but abstained for B;
   - this is an explicit router-resolution failure boundary, not a success.
3. `single_conflicting_label`
   - both arms committed 5/5 events with the same two scopes;
   - connected queries recovered the per-scope majorities A and B;
   - the cut arm selected the global majority B for both contexts.

## Validation

- New tests: 5/5 PASS
- Related allocator/router/guard/transaction/ablation chain: 49/49 PASS
- Full Forge tests: 114/114 PASS
- Ruff: PASS
- compileall: PASS
- local readiness: PASS
- local bundle validation: PASS after installing the locked `jsonschema` dependency
- local all-repository collection: unavailable because optional FastAPI and Torch dependencies were absent; no Forge test failed
- exact-head GitHub CI: Python 3.11 and 3.13 both passed install, lint, readiness, full tests and bundle validation

## Ordinary reduction

The behavior is explained by ordinary nearest-centroid allocation, a reject
option, and per-key evidence accumulation versus one shared accumulator. The
midpoint rejection and within-radius collision are expected consequences of the
fixed routing thresholds, not a new learned organization principle.

## Engineering usefulness

This provides a compact regression surface for an optional future SYSTEM_BUILD:
the intended loop should preserve context-specific revision only when the
observable routing surface is separable, and it should fail closed rather than
manufacture a scope under unresolved overlap.

## Scientific claim boundary

- component function: bounded synthetic boundary tests supported;
- SYSTEM_BUILD admission: false;
- comparative support: false;
- composition contribution: fixture-level dependence only, not generalized;
- scientific novelty: false;
- scientific credit: 0.

## Limitations

The cases are hand-constructed, one-dimensional and deterministic. Distances,
temperatures, thresholds, evidence gains and pool probabilities are fixed and
uncalibrated. There is no matched HMM, BOCPD, latent-cause, PSR, reservoir or
other system comparator; no seed/parameter/resource study; no learned
representation; and no real continuous task. One conflicting label is not a
noise-robustness result.

Usefulness does not establish general composition contribution or scientific
novelty.

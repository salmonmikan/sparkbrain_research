# FORGE-STABLE-SCOPE-HYPOTHESIS-REVISION-A — CI clean

schema_version: 2
generation_id: FORGE-20260927T0138+0900-STABLE-SCOPE-REVISION-CI-CLEAN
produced_at: 2026-09-27T01:38:00+09:00
forge_id: FORGE-STABLE-SCOPE-HYPOTHESIS-REVISION-A
status: FORGE_INTERESTING
recommended_handoff: SYSTEM_BUILD_INPUT
evidentiary_status: NON_EVIDENTIARY
scientific_credit: 0
new_scientific_result: false

## Result

The previously prepared prototype commit `700705fb8112fedcbe7fc2eaa9fb28fcc29b00ba` was successfully published to
`forge/20260926-stable-scope-revision-a` with a non-force ref update and verified by readback.

Exact-prototype CI run `36256004295` completed successfully on both Python 3.11 and 3.13. Lint, local readiness,
tests, and bundle validation all passed.

## Comparison

The prototype compares two ordinary namespace policies for the existing late-evidence overlay:

- `(assembly_id, exposed_hypothesis_set)`: strong isolation, but support fragments whenever pool membership changes.
- `(assembly_id, opaque_scope_token)`: support for a continuing hypothesis can survive pool membership changes while
  different scope tokens and different Assemblies remain isolated.

A hypothesis that disappears and later reappears under the same stable scope token intentionally regains prior support.
Therefore the token lifetime is the evidence lifetime and must be defined prospectively by any later build.

## Reduction / engineering boundary

This is ordinary namespaced keyed state / cache-session partitioning around an associative reweighting mechanism. It is
not a novel memory mechanism and carries zero scientific credit.

The engineering value is narrower: a future SYSTEM_BUILD with an explicit non-privileged context/session identity may
prefer stable scope lifetime over exact hypothesis-set lifetime when continuity across pool changes is required.

SB001 / PR #152 was not modified. No scientific candidate, FORMAL identity, evidence ref, preserve ref, or canonical
SYSTEM_BUILD allocation was created or changed.

## P0 observation

The same non-force `update_ref` action class that was repeatedly refused in prior Forge runs succeeded on this run and
the branch movement was independently verified. This is evidence against a permanent repository-wide or permanent
action-class-wide outage; the P0 incident remains intermittent/context-selective.

main_collision_check: PASS_SB001_UNTOUCHED
prototype_head: 700705fb8112fedcbe7fc2eaa9fb28fcc29b00ba
ci_run: 36256004295
ci_result: SUCCESS
hard_floor_actions: NONE

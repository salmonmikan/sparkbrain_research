# FORGE-STABLE-SCOPE-HYPOTHESIS-REVISION-A

schema_version: 2
generation_id: FORGE-20260926T233236+0900-STABLE-SCOPE-HYPOTHESIS-REVISION-A
produced_at: 2026-09-26T23:32:36+09:00
forge_id: FORGE-STABLE-SCOPE-HYPOTHESIS-REVISION-A
status: FORGE_PROTOTYPE
evidentiary_status: NON_EVIDENTIARY
scientific_credit: 0
new_scientific_result: false

## Why now

The prior FORGE-SCOPED-HYPOTHESIS-REVISION-A fixed cross-Assembly evidence leakage by keying revision state on `(assembly_id, exposed_hypothesis_set)`, but that exact-set key deliberately fragments valid support whenever pool membership changes. Evidence Analyst R139 retains the earlier Forge inputs only as future SYSTEM_BUILD_INPUT and forbids mixing them into current SB001. MAIN R151 owns SB001 at PR #152 head `909094a87025b552b96bcac4afb060b91c4f0573`; this probe is isolated on a new forge/* branch.

## Prototype

A second ordinary design keys the same late-evidence overlay on `(assembly_id, opaque_scope_token)`.

The comparison is intentionally narrow:
- exact hypothesis-set scoping: strong isolation, but pool-change continuity is lost;
- stable scope token: common-hypothesis support survives pool changes while a different token or Assembly remains isolated;
- the token defines evidence lifetime, so temporarily absent hypotheses regain prior support if they reappear under the same token.

This is a lifecycle/namespace trade-off, not a new memory mechanism.

## Reduction and boundary

Ordinary reduction: namespaced keyed state with caller-defined lifetime, equivalent to ordinary cache/session partitioning around an existing associative reweighting overlay.

The stable-token variant is useful only when a future build has a prospective, non-privileged context/session identity with an explicit lifecycle. Reusing a token too broadly would intentionally re-expose older evidence. The prototype therefore must not be admitted into SB001 or treated as scientific support.

recommended_handoff: SYSTEM_BUILD_INPUT_IF_CI_CLEAN
main_collision_check: PASS_SB001_UNTOUCHED
SB001_head: 909094a87025b552b96bcac4afb060b91c4f0573
hard_floor_actions: NONE
ci_status: PENDING_POST_PUSH

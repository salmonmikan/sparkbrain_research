# FAST FORGE — delayed action credit integration probe

worker_role: FAST_FORGE
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
forge_id: FORGE-20260925T0435+0900-INTEGRATION-DELAYED-ACTION-CREDIT
status: FORGE_INTERESTING
prototype_kind: INTEGRATION
recommended_handoff: SYSTEM_BUILD_INPUT
new_scientific_result: false
hard_floor_actions: NONE

## Freshness / ownership

Stable main remains `d16403414fc7abebd23075fc401240971b8eb91d`.

Current control-plane observations:
- Evidence Analyst durable R132 at `ops/evidence-analyst-handoff@97e8ffe2f728cac7bf82f333439d3c83dc055bcc` allocates only `BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT` to MAIN, zero scientific credit.
- Control R67 at `ops/control-brain-handoff@14d121baed3d931c87fbb1e4aec1ada27e8a65bc` reports canonical 35/35 terminal, active 0, queued 0 and MAIN ownership of SB001.
- MAIN report state R136 remains READY_FOR_RELAY and points to SB001 head `e6a59b2601a9a68b46dbb45b02b39e16e3fe95ef`; the build branch itself has since advanced independently to `52feb927eb4856cb76e4048b72d35db722c2729b` with an acceptance-manifest-only commit.
- No Relay state artifact exists under the inspected `reports/orchestrator/relay/*` paths.
- Theory R5 is `NO_THEORY_PROPOSAL / NO_REVISIT_PROPOSAL`.
- Literature R44 strengthens ordinary selective-revision reductions but creates no Revisit trigger.
- Independent Audit durable latest remains R10.
- Methodology R119 is advisory and requires staged, claim-matched reduction.
- Utility remains IDLE and has no Forge support assignment.
- No durable Integration Design proposal stream was found in the inspected external-science handoff.

The active MAIN SYSTEM_BUILD and its immediate protected-integration path were excluded from Forge work.

## Selected target

Independent Forge integration question:

Can the stable v0.5 action layer receive delayed scalar feedback over more than the single most recently pending assembly/action pair, using an ordinary bounded credit mechanism, without modifying MAIN's active SYSTEM_BUILD or any protected scientific object?

Why now:
- stable `AssemblyActionPolicy` stores one `pending` pair, so `reward()` updates only the last action;
- stable v0.5 field plasticity already contains an eligibility mechanism at connection level;
- a small action-level adapter is independent of SB001's predictive-state revision critical path and tests a useful integration seam rather than a novelty claim.

## Branch / prototype

Branch: `forge/20260925-delayed-action-credit-a`

Final head: `b0a33e4bd70585c4a60d530cd822e4729e0931e5`

Prototype files:
- `forge_prototypes/delayed_action_credit.py`
- `tests/test_forge_delayed_action_credit.py`
- `forge_prototypes/delayed_action_credit.md`

The prototype wraps the stable `AssemblyActionPolicy` with a decaying eligibility trace keyed by `(assembly_id, action)`. A delayed reward updates every surviving trace. Stable v0.5 source is unchanged.

## Diagnostics / observations

A source-matched synthetic diagnostic was executed locally against the exact stable action-policy semantics reproduced from main. Direct repository clone was unavailable because the runtime sandbox could not resolve github.com, so no claim of an exact package-environment pytest run is made.

Positive delayed-feedback diagnostic:
- sequence: assembly-a/go -> assembly-b/go -> delayed reward +1
- decay: 0.80
- learning rate: 0.30
- eligibility router: assembly-a/go += 0.24; assembly-b/go += 0.30
- stable last-pending-only baseline: assembly-a/go += 0.00; assembly-b/go += 0.30

Negative-feedback/interference diagnostic:
- sequence: assembly-a/go -> assembly-b/go -> delayed reward -1
- decay: 0.50
- learning rate: 0.30
- eligibility router: assembly-a/go -= 0.15; assembly-b/go -= 0.30

This verifies the bounded integration function: feedback can reach actions older than the latest pending action.

It also exposes the main limitation: generic eligibility spreads credit over recent actions and can therefore update an intervening action that was not causally responsible.

GitHub combined status and commit-linked PR workflow queries returned no checks/runs for prototype commit `a6bb9ffca5c95ce1607c02477c8b10c799d66aed`; CI success is not claimed.

## Ordinary reduction

Strongest ordinary explanation:
- eligibility traces;
- TD(lambda)-style temporal credit assignment;
- standard actor/action-value credit mechanisms.

Stable v0.5 already uses eligibility in `V05PlasticityController` for connection-level plasticity. The Forge prototype extends the same established engineering idea to action-score credit.

No scientific novelty remains or is claimed.

## Engineering usefulness

YES, bounded.

The component supplies one concrete missing function in the stable action layer: delayed scalar feedback can affect more than the most recent action.

It is potentially useful as a future SYSTEM_BUILD input when a build requires delayed action credit, but it should not be treated as native causal-responsibility inference. If precise responsibility is required, a stronger component or explicit causal/return structure is needed.

## Scientific claim boundary

This prototype does NOT establish:
- scientific novelty;
- native responsibility or credit discovery;
- causal identification of the responsible action;
- superiority over eligibility traces, TD(lambda), actor-critic or related RL baselines;
- any new result about a terminal SparkBrain candidate.

It is development-only engineering evidence inside Forge and carries zero scientific credit.

## MAIN collision check

PASS_NO_COLLISION.

Explicitly avoided:
- `BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT` source and acceptance surface;
- MAIN R136 protected-integration / Relay path;
- H7 consumed FORMAL identity and refs;
- Candidate #34/#35, RVT35 and TH-002;
- PRE_FORMAL / FORMAL / STARTED / TEST / evidence / formal / sealed / freeze / preserve authority;
- protected held-out/evaluator surfaces;
- consumed or immutable evidence.

## Utility

No Utility request. The prototype did not need an independent second tooling lane.

## Disposition

`FORGE_INTERESTING`

`recommended_handoff=SYSTEM_BUILD_INPUT`

Reason: the adapter supplies a bounded and independently useful delayed-credit function; the limitations are explicit; its usefulness is engineering-only and does not depend on a scientific novelty claim.

## Metrics

runs=38
prototypes=23
theory_probes=3
theory_kills=3
theory_survivors=0
revisit_probes=1
revisit_kills=1
revisit_survivors=0
dead_ends=17
integration_prototypes=2
integration_useful=2
system_build_input_recommendations=2
system_build_input_admissions=1
ownership_collisions=0
idea_to_observation_latency=SAME_RUN_SYNTHETIC

## Exact refs

stable_main=d16403414fc7abebd23075fc401240971b8eb91d
evidence_analyst_head=97e8ffe2f728cac7bf82f333439d3c83dc055bcc
analyst_r132_build_blob=c0c826800837a5116ebb524afd02d808577e3c03
analyst_r132_state_blob=ae3fe7a5f2c5cf3fdc8a4be0f5fee957eccb329c
control_head=14d121baed3d931c87fbb1e4aec1ada27e8a65bc
external_research_head=fcd9175a672da456e5b16f4799fb234eb7c26d07
theory_r5_blob=3933bd3f8f3ea963341332eea2eaa48d0b8457d3
literature_r44_blob=a55899dc10db66b3cc741412f0fd61cf6d023fd0
methodology_head=0b8cb86935b4a99958856ae634718893849e62d2
methodology_r119_blob=c99a73b03b361ebb05569de5201d01b6fbb10e9c
utility_head=4fa2dafb418814f277ed19919956cec7e61b381d
utility_state_blob=ef691d662bf7035fef7fffcbe0d64cdab18c8490
main_r136_state_blob=20c56898e5acb4649af0ac65258c99fceb25964d
system_build_r136_head=e6a59b2601a9a68b46dbb45b02b39e16e3fe95ef
system_build_current_tip=52feb927eb4856cb76e4048b72d35db722c2729b
forge_branch=b0a33e4bd70585c4a60d530cd822e4729e0931e5
forge_code_blob=376d742e4cf072abb956352d961daa13e3436101
forge_test_blob=91b1985d0839476d1fde01121d82f419d39ff823
forge_note_blob=fc313aaed1e5d2273c7dd0f0cccff45039f8a244

hard_floor_actions=NONE

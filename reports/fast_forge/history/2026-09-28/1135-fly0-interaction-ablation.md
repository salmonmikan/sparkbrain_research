# Fast Forge — FLY-0 interaction-ablation matrix

- generation_id: `FORGE-20260928T113500+0900-FLY0-INTERACTION-ABLATION-A`
- forge_id: `FORGE-FLY0-INTERACTION-ABLATION-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0

## Why now

Evidence Analyst R165 keeps FLY-0 parallel to MAIN/M1-002 and lists an interaction-ablation matrix as an unresolved Forge-side promotion precondition. HUMAN-20260928-001 explicitly permits non-colliding interaction-ablation tooling during Milestone 1; HUMAN-20260928-002 keeps the fly-inspired track bounded, noncanonical and nonevidentiary. MAIN R171 still owns only M1-002 and has no competing FLY-0 allocation; Relay has no active competing allocation.

The Human Directive index is unchanged from the prior durable Forge generation:
`ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`,
active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.

## Prototype

Branch: `forge/20260928-fly0-interaction-ablation-a`  
Exact prototype head: `4c4706e9915cfac4cb9fd667cb3a0f96ebfb4a09`  
Parent durable resource-normalization handoff: `1ee0ccd4951159937d98610a3705a9791a178f46`

Added only:
- `forge_prototypes/fly0_interaction_ablation.py`
- `tests/test_forge_fly0_interaction_ablation.py`
- `forge_prototypes/fly0_interaction_ablation.md`

No MAIN, SYSTEM_BUILD, canonical science, A01, RV02, H9, C07, evidence, formal, frozen or consumed object was modified.

CI run `36371102852` completed successfully on Python 3.11 and 3.13.

## Bounded interaction matrix

The same structured FLY-0 controller and deterministic line world were evaluated under five engineering-only interface conditions:

1. intact;
2. local `Observation` payload masked;
3. ascending `LocalFeedback` payload zeroed while preserving local action;
4. descending modulation removed;
5. local action forced to zero while preserving proposal activity.

The green exact-head tests establish only the following bounded implementation facts:

- intact trajectory reaches target in three committed steps: `2 -> 1 -> 0 -> -1`;
- masking the local observation payload preserves that exact trajectory;
- zeroing the ascending feedback payload preserves that exact trajectory;
- removing descending modulation yields no progress and fails closed at action arbitration;
- forcing local action to zero yields committed steps but no world progress.

## Engineering interpretation

The current hierarchical prototype has a causal top-down path:

`world error -> descending modulation -> local controller -> local action -> world`.

However, the nominal local observation payload is not consumed by `Fly0LocalController`, and the ascending feedback payload is retained for observability but is not consumed by the next high-level control decision. Therefore the current bounded loop does **not** yet close a causally active bottom-up observation/feedback revision path.

This is useful negative engineering localization: it identifies a concrete interface gap before any future SYSTEM_BUILD allocation. It does not imply that the fly-like topology is deficient in general, nor that another topology is superior.

The previously missing interaction-ablation artifact now exists on an isolated Forge branch. Only Evidence Analyst may decide whether that specific promotion precondition is satisfied. Other blockers remain, including activity/resource comparability and the complete matched replacement ladder; no SB003 allocation is created.

## Ordinary reduction

The bounded movement task remains reducible to ordinary reactive control. The present result does not establish a need for the structured FLY-0 topology. It instead shows that, in the current hierarchical wrapper, direction is supplied by top-down modulation while local observation and ascending feedback are not yet causal to the trajectory.

## Claim boundary

NON_EVIDENTIARY / NONCANONICAL. No comparative superiority, composition contribution, biological fidelity, energy efficiency, external validity, novelty, or scientific credit is established. No scientific candidate or build ID is created.

## Publication

Prototype publication used the existing user-authorized GitHub route. The first mutation attempt was refused before GitHub; after fresh ref/state readback, the second attempt succeeded and exact branch/file readback was verified. CI then passed. The durable Forge handoff is published separately under the five-attempt persistence ceiling.

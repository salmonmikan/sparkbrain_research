# Fast Forge — FLY-0 bottom-up feedback closure

- generation_id: `FORGE-20260928T133500+0900-FLY0-BOTTOMUP-FEEDBACK-A`
- forge_id: `FORGE-FLY0-BOTTOM-UP-FEEDBACK-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0

## Why now

Evidence Analyst R167 explicitly permits isolated Forge verification of the source-only bottom-up prototype while MAIN retains M1-002. The current MAIN generation R173 still owns only `BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS`, Relay is unallocated, and no collision with this FLY-0 branch is present.

The Human Directive index is unchanged from the previous durable Forge generation:
`ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`,
active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.

## Prototype repair and verification

Branch: `forge/20260928-fly0-bottom-up-feedback-a`  
Exact verified prototype head: `8e0b7c859a1f96fbf303173ed6dc974938cca8cc`  
Exact prototype tree: `584b95d87d24b7d00ebc0b2a6a2f3129c27bb535`  
Parent source-only head: `f41aad9a726b985ea654900eb8a7c807d558fc08`

The source-only parent had CI run `36374798033` fail at Ruff E501 before tests executed. This run repaired that lint defect, added focused tests and a design note, and tightened checkpoint semantics so restore cannot silently cross the observation-mask ablation boundary.

Changed/added:
- `forge_prototypes/fly0_bottom_up_feedback.py`
- `tests/test_forge_fly0_bottom_up_feedback.py`
- `forge_prototypes/fly0_bottom_up_feedback.md`

CI run `36378701624` completed successfully on Python 3.11 and 3.13.

## Bounded engineering observations

The exact-head tests establish only these bounded implementation facts:

- intact bottom-up loop reaches the target in three committed steps with position trace `2 -> 1 -> 0 -> -1`;
- cutting the local Observation payload causes the first step to fail closed before world progress;
- cutting ascending LocalFeedback allows the first step, then blocks the next descending modulation because the previous feedback is insufficient;
- therefore both previously nominal bottom-up payload edges are causally consumed by this wrapper for continued bounded progression;
- checkpoint/restore replays the intact history exactly;
- checkpoint restore rejects observation-mask and feedback-mask semantic mismatches rather than silently crossing those ablation boundaries.

This closes the specific Forge-side engineering gap `BOTTOM_UP_OBSERVATION_FEEDBACK_CAUSAL_INTEGRATION_ABSENT` for this prototype, pending Evidence Analyst reconciliation.

## Ordinary reduction

The bounded movement task remains solvable by an ordinary reactive controller. The wrapper demonstrates causal use of the bottom-up interfaces, not necessity or superiority of the structured fly-like topology.

The earlier resource-normalization mismatch also remains unresolved: structured activity/resource exposure is not yet commensurate with the reactive replacement, and the complete matched replacement ladder is still incomplete.

## Engineering usefulness

Useful integration assets now include:
- a causally active Observation gate;
- a prior-feedback gate on later descending modulation;
- deterministic checkpoint/replay coverage;
- semantic checkpoint guards across ablation modes;
- focused bottom-up cut tests suitable for later integration acceptance if Analyst chooses to reuse them.

No SB003 allocation is created here. Only Evidence Analyst may decide whether this verified Forge asset becomes a SYSTEM_BUILD input and whether remaining comparator/resource blockers are sufficient for a later allocation.

## Claim boundary

NON_EVIDENTIARY / NONCANONICAL. No topology superiority, biological fidelity, energy efficiency, whole-system superiority, composition contribution, novelty, external validity, scientific credit, or SB003 allocation is established. No A01, RV02, H9, C07, FORMAL, immutable, sealed or evidence object was modified.

## P0 / publication

The current GitHub mutation-recurrence incident remains open under Control. For the prototype repair publication in this run, the first atomic Git-data branch publication attempt succeeded and exact file/head readback was verified. This single success is only evidence for the tested path and does not close or explain the broader incident.

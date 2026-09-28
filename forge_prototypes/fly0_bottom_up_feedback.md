# FLY-0 bottom-up feedback prototype

Status: `NON_EVIDENTIARY / NONCANONICAL FORGE`.

This prototype closes the specific interface gap localized by the prior FLY-0 interaction-ablation work. It does not create a scientific candidate, SYSTEM_BUILD allocation, or biological-equivalence claim.

## Bounded design

The existing structured local sensorimotor controller is wrapped with two causal checks:

1. the local `Observation.signed_error` must agree with the descending modulation before the selected local controller can act;
2. after the first committed step, the next descending modulation is permitted only when the prior matching `LocalFeedback` contains a positive directional motor signal.

The ablations intentionally cut those payloads independently:

- `local_observation_payload_cut` masks the local observation and should fail closed before world progress;
- `ascending_feedback_payload_cut` allows the first step, then zeroes stored feedback so the next modulation is rejected.

Checkpoint state binds both observation-mask and feedback-mask semantics so restore cannot silently cross an ablation boundary.

## Engineering question

Does the bounded wrapper make the previously nominal bottom-up Observation and LocalFeedback interfaces causally necessary to continued closed-loop progression while preserving deterministic checkpoint/replay and fail-closed behavior?

This is only an engineering interface test. The bounded movement task remains solvable by an ordinary reactive controller, so successful closure does not establish that the fly-like structured topology is necessary or superior.

## Claim boundary

No topology superiority, biological fidelity, novelty, energy efficiency, whole-system superiority, scientific credit, or SB003 allocation is established. Any later SYSTEM_BUILD use requires Evidence Analyst allocation; any scientific claim requires a fresh prospective scientific object.

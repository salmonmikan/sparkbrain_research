# FAST FORGE: counterfactual Assembly replay preview

worker_role: FAST_FORGE
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
status: FORGE_PROTOTYPE
prototype_kind: INTEGRATION
recommended_handoff: SYSTEM_BUILD_INPUT
handoff_scope: FUTURE_INPUT_ONLY_NOT_SB001
new_scientific_result: false

## Target capability

Bounded integration seam independent of the accepted SB001 critical path:

`partial internal ActivityPattern -> guarded mature Assembly completion -> cloned-field cue replay -> missing-unit recruitment / abstain`

This follow-on object tests whether a completion proposal can be connected back to the existing v0.4 recurrent field without mutating live runtime state or directly forcing the missing Assembly units.

## Bounded design

- Reuse the prior Forge-only read-only `AssemblyCompletionProbe`.
- Reject ambiguous, unavailable, receptor-containing, oversized, or refractory cue paths.
- Clone the current `TemporalExcitableField` twice.
- Let one clone run as a no-replay baseline.
- On the replay clone, trigger only the already-observed cue units.
- Never inject current into the proposed missing units.
- Measure missing-unit recruitment through existing recurrent edges, prototype recovery and spillover.
- Return diagnostics only; do not commit the cloned state to the live runtime.

## Synthetic development diagnostic

On an explicit five-unit field with stored Assembly `(1,2,3,4)` and partial cue `(1,3)`:

- cue units 1 and 3 are triggered on the replay clone;
- recurrent edges 1->2 and 3->4 each carry 0.60 current to units with threshold 0.50;
- a weak 1->5 edge carries only 0.20 and should not spike;
- expected replay units are `(1,2,3,4)`;
- expected recovered missing units are `(2,4)`;
- expected spillover is empty.

Removing the recurrent edges is the interaction cut: only cue units `(1,3)` should spike and missing-unit recovery should fall from 1.0 to 0.0. This is development contribution evidence inside the rough prototype only.

## Strongest ordinary reduction

Ordinary recurrent pattern completion / attractor-style replay with content-addressable cue selection. The prototype deliberately uses the existing recurrent field as the mechanism. No new regeneration principle is claimed.

## Engineering usefulness

If the diagnostic survives exact-package CI, the component provides a safe preview surface for asking whether a stored Assembly can be reinstated through already-present recurrent dynamics before any live commit path is designed.

Usefulness does not establish scientific novelty.

## Scientific claim boundary

This does not establish autonomous endogenous continuation, a new memory mechanism, de-novo Assembly regeneration, causal necessity in the integrated SparkBrain runtime, superiority over ordinary recurrence/attractor memory, or any canonical result. The synthetic topology is development instrumentation, not confirmatory evidence.

## MAIN collision check

PASS_NO_COLLISION. SB001 exact accepted head, reviewed integration, composition-development contract, H7, terminal candidates, protected evaluators/held-out targets and scientific refs remain untouched.

## Utility

No Utility request.

hard_floor_actions: NONE

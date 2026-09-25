# FAST FORGE: Assembly-completion -> read-only action preview

worker_role: FAST_FORGE
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
prototype_kind: INTEGRATION
new_scientific_result: false

## Target capability

Bounded integration seam independent of MAIN's accepted SB001 integration path:

`partial internal ActivityPattern -> native Assembly OR guarded completion -> existing learned action scores -> read-only action preview / abstain`

The prototype extends the prior Forge Assembly-completion work to the action surface without invoking the mutating `AssemblyActionPolicy.choose()` path.

## Why now

Evidence Analyst R134 accepted BUILD-SB-001 as a bounded non-evidentiary pilot and allocated MAIN to normal reviewed integration of that exact head. Forge therefore stays off SB001 and tests an independent v0.5 integration unknown.

The prior completion-to-prediction bridge showed that degraded internal activity can recover an already-learned prediction read-only. The action path is materially different because `AssemblyActionPolicy.choose()` mutates `visits` and `pending`, even with exploration disabled. A naive "preview" can therefore accidentally advance exploration/credit-assignment state.

## Prototype behavior

- Native mature unsuppressed Assembly matches remain the first path.
- Native misses fall back to the prior guarded completion probe.
- Ambiguous or below-threshold completion abstains.
- A surviving Assembly never calls `choose()`; the adapter reads the existing score table directly.
- Missing or incomplete action history abstains.
- Tied/low-margin actions abstain.
- Returned confidence is bounded by both retrieval similarity and the ordinary action-score margin confidence.
- Assembly memory, action visits, scores, and pending credit state remain unchanged.

## Diagnostics

Weak cue fixture:
- mature prototype A = (1,2,3,4)
- cue = (1,3)
- stable native Assembly threshold = 0.66, cue similarity = 0.60, so native path misses
- learned action scores = action-0 0.70 / action-1 0.10 / withhold 0.00
- preview returns action-0, action margin 0.60, confidence 0.60
- memory and action-policy state remain byte-for-byte equal by state_dict

Naive-policy diagnostic:
- calling stable `choose(activation, explore=False)` returns the greedy action
- but it increments `visits` and rewrites `pending`
- therefore it is not a safe read-only preview primitive

Ambiguous completion:
- A=(1,2,3,4), B=(1,5,3,6), cue=(1,3)
- both completion similarities = 0.60, margin = 0
- action preview abstains before reading either action table

Ambiguous action:
- unique completion survives
- action-0 and action-1 scores tie
- preview abstains instead of resolving via stable policy tie-break

Strong cue:
- cue=(1,2,3), native similarity=0.80
- native route is preserved
- action-policy state still does not mutate

## Strongest ordinary reduction

This is ordinary nearest-prototype/content-addressable retrieval plus a greedy score-table policy, margin-based rejection and confidence gating. It does not establish a new action-selection, responsibility, completion or memory mechanism.

A simpler established implementation could use nearest-neighbor retrieval with rejection followed by a side-effect-free greedy policy lookup.

## Engineering usefulness

Potential future SYSTEM_BUILD input for degraded-observation action planning:
- preserve stable Assembly formation threshold;
- preserve native strong-cue behavior;
- recover an already-learned action proposal from some partial internal activity;
- fail closed on ambiguous Assembly or ambiguous action;
- avoid mutating exploration or pending reward-credit state until a separate explicit commit step exists.

This prototype is intentionally a preview, not an action commit or reward-assignment mechanism.

Usefulness does not establish scientific novelty.

## Scientific claim boundary

FORGE-only, zero scientific credit. No canonical candidate/build identity is created. No PRE_FORMAL/FORMAL/STARTED/evidence/freeze/sealed/preserve action. No protected evaluator or held-out access. No terminal object is reopened.

## MAIN collision

PASS_NO_COLLISION. BUILD-SB-001 remains MAIN-owned and accepted for exact-head reviewed integration. This prototype does not modify/import the SB001 branch and does not participate in its acceptance or composition-contribution path.

## Utility

No Utility request.

hard_floor_actions: NONE

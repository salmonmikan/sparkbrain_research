# FAST FORGE: Assembly-completion -> Predictor fallback bridge

worker_role: FAST_FORGE
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
prototype_kind: INTEGRATION
new_scientific_result: false

## Target capability

Bounded integration seam independent of MAIN's active BUILD-SB-001 path:

`partial internal ActivityPattern -> native Assembly match OR guarded completion -> existing AssemblyPredictor -> prediction / abstain`

This prototype composes the prior Forge read-only Assembly completion component with the stable v0.5 AssemblyPredictor. It does not relax Assembly learning/formation, mutate Assembly memory, retrain the predictor, inject spikes, or create autonomous regeneration.

## Why now

The prior Forge completion probe showed that a weak 2-of-4 cue can map to a mature Assembly at similarity 0.60 while stable formation/activation threshold remains 0.66, and that an ambiguity margin can abstain on equally plausible prototypes. The unresolved engineering question is whether that read-only proposal can restore an already-learned downstream prediction without disturbing the native strong-cue path.

## Prototype behavior

The bridge first calls stable TemporalAssemblyMemory.observe(..., learn=False).
- Native mature unsuppressed matches stay on the stable AssemblyPredictor path.
- Native misses fall back to the Forge completion probe.
- Ambiguous/low/no-compatible completion proposals abstain.
- A surviving completion becomes only a read-only virtual AssemblyActivation for AssemblyPredictor.predict().
- No memory or predictor state is mutated.

## Diagnostic expectations

Fixture A:
- mature prototype A = (1,2,3,4)
- learned next values = next-x twice, next-y once
- weak cue = (1,3)
- stable native matcher: no activation because 0.60 < 0.66
- bridge: completion route to A, predicts next-x at confidence 2/3

Ambiguity fixture:
- mature A = (1,2,3,4)
- mature B = (1,5,3,6)
- weak cue = (1,3)
- both score 0.60
- completion margin = 0.0, so bridge abstains
- a naive global Assembly threshold of 0.55 would accept the ordinary best_match tie-break and return assembly-0001

Strong partial fixture:
- cue = (1,2,3), similarity 0.80
- stable native matcher already activates A
- bridge remains on the native route

## Strongest ordinary reduction

Nearest-prototype/content-addressable retrieval with rejection plus an ordinary conditional prediction table. A simpler established implementation could combine thresholded nearest-neighbor retrieval, an ambiguity margin, and a key-value predictor directly.

This is engineering composition, not a new memory, regeneration, or prediction mechanism.

## Engineering usefulness

Potential SYSTEM_BUILD input for robust degraded-observation behavior:
- preserve stable Assembly formation threshold;
- preserve native strong-cue behavior;
- recover an already-learned prediction from some weaker partial internal activity;
- fail closed on ambiguous retrieval;
- keep completion inspectable and read-only.

Usefulness does not establish scientific novelty.

## Scientific claim boundary

FORGE-only, zero scientific credit. No candidate/build identity is created. No PRE_FORMAL/FORMAL/STARTED/evidence/freeze/sealed/preserve operation. No protected evaluator/held-out access. No terminal object is reopened.

## MAIN collision

PASS_NO_COLLISION by construction. BUILD-SB-001 remains MAIN-owned and is not modified or imported. This branch derives only from the prior Forge completion branch plus stable v0.5 APIs.

## Utility

No Utility request.

hard_floor_actions: NONE

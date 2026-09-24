# FAST FORGE integration prototype — predictive-state revision loop

- worker_role: FAST_FORGE
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- prototype_kind: INTEGRATION
- target_capability: preserve multiple contradictory predictive hypotheses, split on prediction conflict, and reuse a prior hypothesis when its observable context/outcome relation returns
- scientific_novelty_claim: none
- recommended_handoff: SYSTEM_BUILD_INPUT

## Composition

This prototype composes ordinary mechanisms only:

1. a small bank of persistent predictive states;
2. observable-context distance as a compatibility gate;
3. prediction error as the update-vs-split gate;
4. reuse of a previously retained state when it becomes the best compatible hypothesis again.

There are no external state IDs, evaluator-selected identities, or episode-boundary inputs. State IDs are internal implementation handles only.

## Why this integration probe exists

Stable v0.5 already has anonymous TemporalAssemblyMemory plus AssemblyPredictor, but its predictor is keyed by the selected mature assembly and accumulates one next-event table per assembly. This prototype tests a bounded adapter-level question: whether a small persistent multi-hypothesis layer can close an update/split/reuse loop before any MAIN SYSTEM_BUILD allocation exists.

It does not modify stable v0.5 code and does not reopen any terminal scientific object.

## Synthetic development sequence

The fixed demo presents:

- three nearby contexts predicting approximately +1;
- two nearby contexts with a contradictory approximately -1 outcome;
- a return to the original nearby +1 regime;
- then a genuinely distant context.

With context_gate=0.35 and reuse_error=0.35, the expected decisions are:

create -> update -> update -> split -> update -> reuse -> create

The retained states after the run are two nearby but prediction-distinct hypotheses plus one distant-context hypothesis.

A single-state EWMA overwrite baseline is included only as a build-value ablation. On the return-to-prior-regime step, the multi-state bank's pre-update error is 0.05, while the single-state EWMA's pre-update error is 1.50625.

## Ordinary explanation

The result is fully explainable as a prototype bank / latent-cause mixture / ART-like category split with prediction-error gating. It is not evidence for a new mechanism. Stronger future engineering alternatives include learned recurrent associative state, mixture/state-space models, and other established latent-state methods.

## Engineering usefulness

The prototype demonstrates a concrete interface for a future integration layer:

observable internal representation -> state organization -> prediction -> prediction error -> update/split/reuse

A future SYSTEM_BUILD could replace the hand-set gates with learned or established components while preserving the interface and acceptance behavior.

## Claim boundary

This is a synthetic development diagnostic. It does not establish scientific novelty, generalization, causal responsibility, superiority over capacity-matched baselines, or readiness for canonical use. Any future scientific question requires a fresh Analyst-authorized object and prospective contract.

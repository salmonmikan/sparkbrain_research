# FAST FORGE: multi-hypothesis prediction pool with explicit abstention

worker_role: FAST_FORGE
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
status: FORGE_INTERESTING
prototype_kind: INTEGRATION
recommended_handoff: SYSTEM_BUILD_INPUT
new_scientific_result: false

## Target capability

Bounded integration seam: `persistent state -> plural hypotheses maintained/competing -> abstain or select`, without modifying stable v0.5 predictor state or MAIN BUILD-SB-001.

## Bounded design

The Forge adapter is read-only over `AssemblyPredictor.counts`. For one mature, unsuppressed Assembly it exposes up to three deterministic future-event hypotheses, normalizes observed counts, and selects only when minimum observation, confidence, and best-vs-second margin guards all pass. Otherwise it abstains.

Development defaults are `min_observations=3`, `min_confidence=0.60`, `min_margin=0.20`, and `max_hypotheses=3`. These are Forge integration settings, not canonical scientific thresholds.

## Synthetic diagnostics

- 5/5 future-event counts: retain both alternatives and abstain.
- 8/2 counts: select the leading event at confidence 0.8 and margin 0.6.
- one observation: abstain despite nominal confidence 1.0.
- immature activation: abstain.

## Strongest ordinary reduction

Ordinary categorical histogram + explicit top-k/beam retention + selective-classification reject option. A register or finite-state controller can reproduce the bookkeeping. No new memory, competition, or decision principle is identified.

## Engineering usefulness

Potentially useful as a future SYSTEM_BUILD input because stable v0.5 exposes only one top prediction while the larger integration objective needs inspectable plural alternatives and an explicit abstention boundary. The adapter keeps alternatives visible without changing prediction learning.

Usefulness does not establish scientific novelty.

## Scientific claim boundary

This does not establish emergent multi-hypothesis cognition, causal contribution of competition, superiority over beam search/selective prediction, endogenous revision, a new candidate, or a Revisit trigger. Any later scientific claim requires a fresh prospective object.

## MAIN collision check

PASS_NO_COLLISION at selection time. main `d16403414fc7abebd23075fc401240971b8eb91d`; Analyst R137; MAIN/Relay R146; BUILD-SB-001 head `e9b93456a0c37e2d1393463c167912e0e3968817`; PR #152 remained open/unmerged. Existing Forge completion work is separate and untouched. No scientific, evidence, preserve, freeze, formal, sealed, control, MAIN, or SYSTEM_BUILD ref is mutated.

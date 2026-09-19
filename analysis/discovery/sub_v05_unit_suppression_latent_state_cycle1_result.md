# EXPLORATORY / NON_EVIDENTIARY — SUB v0.5 unit-suppression latent-state cycle 1 result

- mode: `discovery`
- exploratory_target: `V05_UNIT_SUPPRESSION_LATENT_STATE_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Why independent of MAIN

MAIN owns `CAND-V05-TOPOLOGY-CONFIG-BINDING-01` and its active topology config-contract Architecture Study. This Discovery was bound from stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` and touched only the separate v0.5 unit-suppression intervention primitive. It did not inspect or modify MAIN's Architecture outcome artifact, continue Temporal batching or Top-k, construct H7, rescue the rejected topology-fanout candidate, or touch any consumed/formal/TEST/scoring/preserve/evidence surface.

## Question / reduction question

Does `IntegratedV05Brain.suppress_units()` act as a state-neutral ablation, or can its temporary threshold clamp retain otherwise suprathreshold membrane charge that is discharged as a deferred spike after `clear_unit_suppression()`?

Reduction question: if this occurs, is it completely explained by threshold-only suppression plus ordinary lazy membrane-state retention, rather than a new adaptation, recovery, or memory mechanism?

## Inputs used

- stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` only;
- `src/sparkbrain/v05/brain.py` suppression wrapper;
- `src/sparkbrain/v04/field.py` event delivery/decay semantics;
- `src/sparkbrain/v05/topology.py` default receptor thresholds;
- current source caller search for `suppress_units` and `clear_unit_suppression`;
- one fixed synthetic channel with load magnitude `0.60`, follow-up magnitude `0.01`, `settle_ms=0.1`, and receptor-bank/homeostasis/learning/assembly/prediction/action disabled.

No repository dataset, trained checkpoint, retained/confirmatory/held-out TEST input, formal raw result, official scorer, consumed identity, or MAIN Architecture outcome artifact was opened or used.

## Implementation / experiment performed

A prospectively bound three-arm deterministic pytest compared:

1. `SUPPRESSED_THEN_CLEAR`: suppress the two routed receptor targets, apply the `0.60` load, clear suppression, then apply the `0.01` follow-up at `0.1 ms`;
2. `IMMEDIATE_CONTROL`: apply the same `0.60` load without suppression;
3. `FOLLOWUP_ONLY_CONTROL`: apply only the `0.01` follow-up to a fresh equivalent brain.

No production source was modified. The fixed diagnostic commit `ad7d9e05c6dfd03b70baf5406f29f776d57ee370` passed ordinary repository CI run `35461938460` on Python 3.11 and 3.13, including lint, local readiness, tests, and bundle validation.

## Observations

The default routed receptor threshold is `0.46`. With `input_gain=1.35` and two-way routing, the `0.60` load contributes about `0.57275649` current per target, so the unsuppressed immediate control spikes both routed receptors. Under v0.5 unit suppression, `process_episode()` temporarily changes those units' `base_threshold` to `1e9`; the same load therefore produces no routed-receptor spike. The wrapper then restores the normal threshold, but the field has not reset the membrane potential because no spike occurred.

After the suppressed episode the retained potential is still above the restored `0.46` threshold. At `0.1 ms`, ordinary membrane decay leaves about `0.56958333`; the `0.01` follow-up contributes only about `0.00954594`, yielding about `0.57912928` before thresholding. After `clear_unit_suppression()`, that tiny follow-up causes both previously suppressed receptor targets to spike. The same `0.01` follow-up presented alone to a fresh equivalent brain spikes neither target.

The effect is therefore exactly reducible to the current implementation: temporary threshold substitution blocks threshold crossing while preserving membrane charge, and v0.4 field decay is lazy until a later event reaches the unit. There is no evidence here for a new adaptive, recovery, or memory mechanism.

Current caller search also narrows the scope. The v0.5 causal evaluation uses persistent `suppress_units(...)` copies during its scored held-out episodes and does not clear suppression inside that scoring path. `clear_unit_suppression()` is otherwise present only in the public runtime method and the existing trivial reversibility test. Therefore this Discovery does **not** reinterpret the current causal-ablation score path or any consumed/formal result. It identifies a transient-intervention/recovery semantic hazard for future studies that clear suppression and then continue the same runtime state.

## What would falsify or reduce it

Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if the supported v0.5 intervention contract is explicitly defined as an output/threshold clamp that intentionally preserves latent membrane state across suppression and permits post-clear rebound, and no supported transient-recovery study assumes state-neutral ablation.

A future prospectively defined Architecture study could compare current state-preserving suppression with a resource-matched/state-clamped intervention on DEV-only synthetic or development episodes. If post-clear internal and downstream observables are equivalent under the intended supported contract, reduce the issue to documentation/API semantics rather than a runtime correctness change.

## Candidate next research layer

`ARCHITECTURE_STUDY_CAUSAL_INTERVENTION_SEMANTICS`, subject to fresh Evidence Analyst promotion only.

## Scientific / semantic choices still open

- whether `suppress_units` is intended to mean output blockade/state preservation or state-neutral ablation;
- whether clearing suppression should expose retained membrane potential, adaptation, queued effects, or other hidden state;
- whether future transient causal/recovery protocols need an explicit state-clamped comparator;
- whether the persistent v0.5 causal-ablation helper should simply document that its semantics differ from a transient suppress/clear intervention.

No cycle 2 is authorized or attempted here. Any continuation must be freshly specified prospectively by Evidence Analyst; this exploratory result cannot be relabeled as formal evidence.

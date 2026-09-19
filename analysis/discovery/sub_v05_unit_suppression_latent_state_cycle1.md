# EXPLORATORY / NON_EVIDENTIARY — SUB v0.5 unit-suppression latent-state cycle 1

- mode: `discovery`
- exploratory_target: `V05_UNIT_SUPPRESSION_LATENT_STATE_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- stable_source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Why independent of MAIN

MAIN owns `CAND-V05-TOPOLOGY-CONFIG-BINDING-01` and its active v0.5 topology config-contract Architecture cycle. This bounded Discovery does not inspect or modify that branch's outcome artifacts and does not touch topology/config semantics. It isolates a separate intervention-semantics question in the already-stable v0.5 unit suppression primitive. Temporal batching, Top-k, H7, the rejected topology-fanout candidate, consumed identities, formal/TEST/scoring/preserve/evidence surfaces, and MAIN blockers/successors are excluded.

## Prospective question

Does `IntegratedV05Brain.suppress_units()` behave as a state-neutral ablation, or does its temporary `base_threshold = 1e9` implementation preserve incoming membrane charge so that clearing suppression can expose a deferred threshold crossing on a later perturbation that is itself subthreshold in an otherwise fresh control?

## Reduction question

If a deferred spike exists, is it fully explained by threshold-only suppression plus the field's ordinary lazy membrane-state retention, rather than a new adaptive, memory, or recovery mechanism?

## Expected information gain for cycle 1

Determine whether the public causal-intervention primitive is an output clamp with latent state preservation or a state-neutral ablation. This matters for future transient suppression/recovery diagnostics, while remaining independent of the currently persistent held-out suppression path used by the v0.5 evaluation helper.

## Fixed synthetic design

Use current stable source only and disable receptor-bank transformation, homeostasis, field learning, reward modulation, assembly learning, prediction, and action. Route one positive synthetic pulse to the ordinary two receptor targets.

Three development-only arms are fixed prospectively:

1. `SUPPRESSED_THEN_CLEAR`: suppress exactly the routed receptor targets, apply a load pulse that would normally cross their threshold, verify no target spike, clear suppression, then apply a much smaller follow-up pulse.
2. `IMMEDIATE_CONTROL`: apply the same load pulse without suppression and verify the routed receptors spike normally.
3. `FOLLOWUP_ONLY_CONTROL`: apply only the small follow-up pulse to a fresh equivalent brain and verify it is insufficient to spike the routed receptors.

Primary diagnostic: after the suppressed load, are restored target thresholds normal while retained target membrane potentials exceed those restored thresholds, and does the subsequent subthreshold follow-up trigger the target spikes only in `SUPPRESSED_THEN_CLEAR`?

No threshold, pulse magnitude, metric, or interpretation may be tuned after observing the diagnostic. If the fixed values fail to isolate the question, stop or reframe prospectively rather than rescue-tune this cycle.

## Stop / reduction conditions

- If suppression does not preserve above-normal-threshold latent membrane state under this fixed probe, return `REJECT` or a narrower engineering observation and stop.
- If it does, first reduce the effect against current source semantics. If threshold substitution plus ordinary membrane retention explains it exactly, do not describe it as a new scientific mechanism.
- Do not reinterpret any consumed/formal result. The current reference causal evaluation's persistent suppression path is read only for scope and is not rerun.
- Any future study of state-clamped versus state-preserving transient suppression must be a fresh prospective object selected by Evidence Analyst.

## Forbidden inputs

No repository dataset, retained/confirmatory/held-out TEST input, trained/formal checkpoint, official scorer, consumed raw identity, immutable evidence, or MAIN Architecture outcome artifact may be opened or used.

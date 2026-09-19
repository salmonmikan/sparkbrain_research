# EXPLORATORY / NON_EVIDENTIARY — Homeostasis receptor dead-mask Discovery cycle 1 result

- worker: `SUB`
- mode: `discovery`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_base: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst authority: `850b4502cf15d3f6118a487c5ab4ba81fbf7b75e`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`
- candidate_next_research_layer: `ARCHITECTURE_STUDY_STABILITY_OBSERVABILITY_SEMANTICS`

## Question

Can continuing receptor/input-layer activity keep the public v0.5 homeostatic `dead` signal false even when the internal reservoir is completely silent, because the controller accounts over all field spikes rather than internal-reservoir spikes?

## Inputs and implementation

The prospectively fixed diagnostic used only a two-unit synthetic field: receptor unit `0`, internal unit `1`, no connections, default `HomeostasisConfig`, and six observation windows. Production accounting received one receptor spike per window. An empty control received no spikes. A diagnostic shadow received the exact same receptor-spike stream after filtering `field.receptor_ids` before an independent controller. Production source was not changed.

Diagnostic commit/head before this result record: `ae5856d26d7a24e77a17bf564e491b293057d55b`. Exact-head ordinary CI `35476754216` completed successfully on Python 3.11 and 3.13; lint, local readiness, full tests, and bundle validation all passed.

## Observations

After six windows:

- `RECEPTOR_ONLY_PRODUCTION_ACCOUNTING`: `dead=false`, controller `dead_streak=0`, public `active_unit_fraction=0.5`, while the internal reservoir unit's `rate_ema` remains exactly `0.0`.
- `EMPTY_CONTROL`: `dead=true`, `dead_streak=6`, `active_unit_fraction=0.0`.
- `RECEPTOR_FILTERED_SHADOW`: `dead=true`, `dead_streak=6`, `active_unit_fraction=0.0`.

Thus the same complete absence of internal-reservoir spikes is classified differently solely according to whether receptor spikes are included in the stability accounting surface.

## Ordinary reduction

The observation is fully explained by current source semantics. `HomeostaticController.observe()` builds `rows` from every supplied spike, resets `dead_streak` whenever `rows` is non-empty, computes `active_unit_fraction` from every spiking unit, and updates rate/threshold state for every field unit. It does not exclude `field.receptor_ids`. `IntegratedV05Brain.process_episode()` passes `base_result.spikes` directly into `homeostasis.observe()`, whereas the later Assembly pattern extraction explicitly excludes receptor IDs for its `internal_reservoir` representation.

This is therefore an Architecture/API observability question, not a new stability mechanism and not scientific novelty evidence.

## Falsifier / reduction criterion

Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if the supported contract intentionally defines `dead` as "no spikes anywhere in the complete field, including receptor/input units" and no supported monitoring/adaptation decision requires internal-reservoir liveness; if receptor-only activity with a silent reservoir is unreachable in supported DEV/runtime paths; or if a fresh receptor-aware comparator changes no prospectively fixed stability/adaptation behavior of interest.

## Candidate next research layer

If Evidence Analyst promotes this object, a fresh prospective Architecture study should first bind the intended population semantics of `dead`, `active_unit_fraction`, rate EMA, and threshold adaptation: whole field, receptor layer plus reservoir jointly, or internal reservoir only. A resource/identity-neutral comparator can then separate receptor and reservoir liveness accounting on DEV-only streams with matched spike inputs and fixed monitoring/adaptation observables.

## Scientific/API choices still open

- Whether public `dead` is intended to mean whole-field silence or internal-computation silence.
- Whether receptor thresholds/rate EMA should share the same homeostatic target as reservoir units.
- Whether `active_unit_fraction` should use all units or the population whose liveness it reports.
- Which supported caller or monitoring decision, if any, consumes `StabilitySnapshot.dead` as a meaningful internal-stability signal.

## Stop

Cycle 1 stops here. SUB does not run cycle 2 or formalize the object. Utility request: none. Consumed identities: none. New FORMAL/PRE_FORMAL evidence: none. No STARTED/control authority, formal/freeze/evidence ref, official score, held-out TEST access, immutable evidence mutation, research merge, or stable-main mutation occurred.
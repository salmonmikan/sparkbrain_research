# EXPLORATORY / NON_EVIDENTIARY — Homeostasis receptor dead-mask Discovery cycle 1

Status: `PROSPECTIVE_BINDING_ONLY`

- worker: `SUB`
- mode: `discovery`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_base: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst authority observed before mutation: `850b4502cf15d3f6118a487c5ab4ba81fbf7b75e`
- evidentiary_status: `NON_EVIDENTIARY`

## Independence boundary

This question is limited to DEV/synthetic v0.5 homeostasis stability accounting. It does not touch MAIN's active delayed-outcome caller-contract object or branch, the queued Assembly mature-capacity/lifecycle object, Refractory follow-up, suppression methodology work, Top-k/H7 construction, previously answered Temporal/topology/Assembly segmentation objects, any consumed/formal identity, held-out TEST input, official scorer, evidence/freeze/control/preserve refs, or immutable evidence.

## Prospectively fixed question

When the internal reservoir is completely silent but receptor units continue to spike, does `HomeostaticController.observe()` keep the public `StabilitySnapshot.dead` flag false because dead-streak accounting uses all field spikes rather than internal-reservoir spikes? Does a receptor-filtered shadow over the exact same spike stream reach `dead=True` under the same configured dead-window horizon?

This is a stability-observability / architecture-semantics question, not a novelty or formal-evidence claim.

## Fixed synthetic diagnostic

Use only public v0.4 field/topology contracts plus the public v0.5 `HomeostaticController`.

Fixed field:
- unit `0`: receptor;
- unit `1`: internal reservoir;
- no connection is required for the diagnostic;
- both start at `base_threshold=0.5`.

Use default `HomeostasisConfig`, including `dead_windows_before_flag=6`.

Fixed arms for six consecutive observation windows:
1. `RECEPTOR_ONLY_PRODUCTION_ACCOUNTING`: one spike from receptor unit `0` in every window; pass the complete spike tuple to `observe()`.
2. `EMPTY_CONTROL`: no spikes in any window.
3. `RECEPTOR_FILTERED_SHADOW`: start from the same one-receptor-spike-per-window stream as arm 1, but remove `field.receptor_ids` before passing the tuple to an independent controller. This is a diagnostic shadow only; production code is not modified.

Fixed observables:
- final `dead` flag;
- final `dead_streak`;
- `active_unit_fraction`;
- per-unit `rate_ema`;
- final base thresholds.

## Reduction / falsifier

Reduce/reject this question if receptor-only production accounting reaches the same final dead classification as the receptor-filtered shadow under the fixed six-window horizon, or if the production controller already excludes receptor spikes from dead-streak accounting. A stronger architecture concern exists only if continuing input/receptor activity masks complete internal-reservoir silence in the public stability signal.

No production source, thresholds, metrics, scorers, formal data, or held-out outcomes may be changed in response to the result. This cycle stops after this bounded diagnostic and returns to Evidence Analyst.
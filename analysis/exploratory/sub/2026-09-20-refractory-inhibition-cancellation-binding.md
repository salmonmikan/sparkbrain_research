# EXPLORATORY / NON_EVIDENTIARY — refractory inhibition cancellation binding

- role: `SUB`
- mode: `discovery`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploratory_target: `REFRACTORY_INHIBITION_CANCELLATION_DISCOVERY_CYCLE1`
- exploration_cycle: `1/3`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `d6b14d826a0847e439dfedd86e363786d84e329a`
- evidentiary_status: `NON_EVIDENTIARY`

## Why independent of MAIN

MAIN owns `CAND-ASSEMBLY-CROSSCASCADE-FALLBACK-01` and its whole segmentation Architecture critical path. This probe touches only the stable v0.4 field refractory-current semantics used as shared substrate. It does not inspect or mutate MAIN's active object, promoted assembly fallback, suppression repair, topology-config, Temporal, Top-k, H7, formal/TEST/scoring/identity/preserve/evidence surfaces, or any consumed identity.

## Prospective question

During the absolute refractory window, does a simultaneous positive arrival cancel an inhibitory arrival even though the field comment says positive drive is ignored during refractory?

Current source groups same-time arrivals, computes `net_current = positive - negative`, then in refractory applies `unit.potential += min(0.0, net_current)`. Therefore a same-time positive current can mathematically reduce or erase inhibitory hyperpolarization before the positive part is nominally ignored.

## Fixed synthetic diagnostic

Use a one-unit, no-connection `TemporalExcitableField` with direct `SynapticArrival` injection only.

Initial unit state:
- potential `0.5`
- base threshold `1.0`
- absolute refractory through `5.0 ms`
- last update `0.0 ms`

At `1.0 ms`, compare exactly three arms:
1. `INHIBITION_ONLY`: one current `-0.5`.
2. `PAIRED_SAME_TIME`: currents `-0.5` and `+0.5` at the same timestamp.
3. `EXCITATION_ONLY`: one current `+0.5`.

Then at `5.1 ms`, after refractory expiry, inject the same `+0.70` probe into every arm.

Pre-bound observables:
- membrane potential immediately after `1.0 ms` delivery;
- whether any spike occurs at `1.0 ms`;
- membrane potential immediately before/after the `5.1 ms` probe as exposed by field state/spike result;
- whether the `5.1 ms` probe spikes;
- equality of `PAIRED_SAME_TIME` and `EXCITATION_ONLY` physical state after the refractory-time delivery.

## Reduction / falsification

Reduce to ordinary current-accounting semantics and recommend `REJECT` if paired same-time input is exactly explained by the existing `positive-negative` netting before the refractory clamp and has no post-refractory functional consequence in the fixed probe.

Recommend `PROMOTE_TO_ARCHITECTURE_STUDY` only if the fixed diagnostic shows a reproducible physical-state or post-refractory spike difference attributable to this current-accounting order. A future Architecture object would need to prospectively compare current `NET_THEN_REFRACTORY_CLAMP` against a read-only `IGNORE_POSITIVE_THEN_APPLY_INHIBITION` comparator under matched currents/timestamps, and must decide the intended refractory contract before any production mutation.

Stop after this one cycle for fresh Evidence Analyst review. Do not tune magnitudes, timing, thresholds, or probe after observing the result.

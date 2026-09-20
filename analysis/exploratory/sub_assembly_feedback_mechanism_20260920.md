# EXPLORATORY / NON_EVIDENTIARY — SUB theory-backward Assembly feedback discriminator

Date: 2026-09-20

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- exploratory_target: `V05_ASSEMBLY_FEEDBACK_CAUSALITY_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_generation: `EVA-20260920T105721+0900-R11-4B7D91C2`
- analyst_handoff_commit: `6617b28dd983a4ada1ebb0622bada869ff17b19e`
- main_generation_observed: `MAIN-20260920T111421+0900-PRIMARY-ASSEMBLY-LIFECYCLE-C1`
- main_research_head_observed: `13239163f6fecb2b61ea2189a5a94ba12b6cb3d6`
- evidentiary_status: `NON_EVIDENTIARY`

## Why this target exists

The recent autonomous SUB window is system-heavy: Homeostasis population accounting, receptor same-key ordering, and checkpoint continuation were all implementation/API/reproducibility questions. Under the theory-backward supply rule, this run selects a central mechanism discriminator rather than another system edge case.

This target is independent of MAIN. MAIN owns `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01`: candidate budget/lifetime semantics and supported saturation reachability. This Discovery does **not** inspect or modify `max_candidates`, pruning, saturation, candidate lifetime, MAIN's branch, or its immediate successor. It asks only whether already-present mature Assembly state can causally alter lower-level Spark/Cascade generation under identical physical input and identical field/receptor/plasticity state.

## Falsifiable question

Can mature v0.5 Assembly state feed back into the recurrent field strongly enough to change or regenerate Spark/Cascade activity, rather than acting only as a post-field recognizer/readout?

A positive result would require a difference in `v04_result` spikes/cascades/ignitions or final field state that is caused solely by the presence of a mature Assembly candidate while the physical substrate and input are matched.

## Prospectively fixed procedure

1. Build a template `IntegratedV05Brain` with weight/delay learning and homeostasis disabled for the probe.
2. Present one fixed synthetic pulse sequence and require at least one internal `ActivityPattern`; this supplies a pattern only, not scientific evidence.
3. Build two fresh, physically identical probe brains with the same fixed configuration.
4. In the `MATURE_ASSEMBLY` arm only, seed the template pattern directly into `TemporalAssemblyMemory` across three distinct synthetic episode IDs so it is mature. Do not touch the field, receptor bank, plasticity, predictor, or action state.
5. Keep the `EMPTY_ASSEMBLY` arm with no Assembly candidates.
6. Present the exact same physical pulse sequence once to both arms with `learn_assembly=False`, `learn_field=False`, `explore_action=False`.
7. Record:
   - whether the mature arm recognizes/activates its candidate;
   - whether the empty arm has an activation;
   - exact equality of the two `v04_result.as_dict()` payloads;
   - exact equality of the two lower field `state_dict()` payloads after the step.
8. Also suppress the mature candidate in a fresh matched pair and repeat the identical physical input; suppression may alter Assembly usability/readout but must not alter lower field dynamics if no causal feedback exists.

## Pre-bound interpretation

- `ASSEMBLY_STATE_CHANGES_FIELD_DYNAMICS`: any lower-field spike/cascade/ignition/field-state difference caused only by mature/suppressed Assembly state. Return as a fresh MECHANISM candidate for Analyst review; do not formalize in this run.
- `ASSEMBLY_RECOGNIZED_BUT_FIELD_IDENTICAL`: mature Assembly activation/readout differs while `v04_result` and field state remain identical. Reduce current v0.5 Assembly to post-field recognition/readout with respect to Spark/Cascade regeneration; recommend `REJECT` for a native Assembly-feedback completion mechanism under current architecture.
- `NO_ASSEMBLY_RECOGNITION_IN_FIXED_PROBE`: diagnostic insufficient; stop with `CONTINUE_EXPLORING` only if one bounded redesign remains scientifically distinct and not rescue tuning.
- `INVALID_DIAGNOSTIC`: discard and stop.

## Ordinary reduction comparator

The matched `EMPTY_ASSEMBLY` arm is the ordinary recurrent-field/reservoir comparator: same topology, receptors, field state, pulse input, and learning flags, but no Assembly memory. If lower dynamics are identical, any activity/reconstruction is fully attributable to ordinary recurrent field dynamics and input history, not Assembly feedback.

## Falsifier / stop condition

The mechanism hypothesis is reduced if a mature and actually recognized Assembly can be added or suppressed without changing matched lower-field dynamics. One clean reduction is sufficient; no cycle 2 rescue tuning.

## Claim typing before result

- proposed claim_ceiling if positive: `MECHANISM`
- proposed preformal_eligible before result: `false`
- preliminary preformal status: `NOT_READY`
- current missing readiness: supported reachability of a causal feedback effect, functional consequence beyond readout, survival of the matched recurrent-field reduction, comparator survival, support breadth, and a fresh formalizable claim.

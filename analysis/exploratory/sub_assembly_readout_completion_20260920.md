# EXPLORATORY / NON_EVIDENTIARY — SUB theory-backward Assembly readout-completion discriminator

Date: 2026-09-20

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- exploratory_target: `V05_ASSEMBLY_PARTIAL_COMPLETION_FUNCTION_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_generation: `EVA-20260920T115704+0900-R12-A6B8DE50`
- analyst_handoff_commit: `dcaa02fc25506ff4e8b14d7540b6c754a8a6da98`
- main_generation_observed: `MAIN-20260920T121227+0900-PRIMARY-FUNNEL21-HOLD-7C41A2D9`
- main_lane_observed: `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- evidentiary_status: `NON_EVIDENTIARY`

## Supply accounting / independence

The Analyst rolling window is receptor ordering=`SYSTEM`, checkpoint continuity=`SYSTEM`, Assembly feedback=`MECHANISM` (1/3 qualifying), so the supply rule is already compliant. This run nevertheless selects a distinct theory-backward question because it is central and bounded rather than selecting another easy API edge case. No theory-backward exception is used.

MAIN has no current scientific object. This target does not reopen the rejected Assembly-to-field feedback candidate, the terminal Assembly capacity/lifecycle SYSTEM object, H7, or any consumed/formal identity. The causal direction is different from the rejected feedback object: the question is whether a mature pre-semantic Assembly can functionally complete a *partial observation at the readout/behavior level*, not whether Assembly state regenerates missing lower-field spikes.

## Falsifiable mechanism question

Can a mature Assembly formed from a full pre-semantic spatiotemporal pattern cause a learned prediction/action to be expressed when a later observation contains only an ordered partial subsequence, and does that effect survive a matched ordinary fixed-prototype nearest-neighbor + lookup reduction?

The mechanism-level positive discriminator is not mere partial recognition. It requires a functional consequence (learned prediction/action expressed on the partial pattern) that cannot be fully reproduced by a comparator with the same full prototype, the same fixed similarity threshold, and the same learned output table but no Assembly state dynamics beyond nearest-neighbor matching.

## Prospectively fixed inputs and procedure

1. Use only synthetic `ActivityPattern` values; do not use repository evidence data, held-out/formal TEST, official scorer, or consumed identities.
2. Full pattern: ordered units `(10, 11, 12, 13)`, relative bins `(0, 2, 4, 6)`.
3. Ordered partial: `(10, 12, 13)`, bins `(0, 4, 6)`, i.e. one missing interior Spark while preserving the remaining order/timing.
4. Scrambled negative control: `(13, 12, 10)` with bins `(0, 4, 6)`.
5. Mature one `TemporalAssemblyMemory` candidate from the full pattern using three distinct synthetic episode IDs and default `AssemblyConfig`.
6. Attach one synthetic future-event association through `AssemblyPredictor.observe` and one rewarded deterministic action through `AssemblyActionPolicy` with exploration disabled.
7. Query the memory with the ordered partial using `learn=False`. Record activation/maturity/assembly identity, prediction, and deterministic action.
8. Query the scrambled control with `learn=False` and record whether it activates.
9. Build the matched ordinary reduction from `pattern_similarity(full, query) >= AssemblyConfig.similarity_threshold`; if it matches, route to the same learned event/action lookup. Compare its accept/reject and output to the Assembly path.

## Pre-bound terminals

- `FUNCTIONAL_PARTIAL_COMPLETION_BEYOND_MATCHED_NN_LOOKUP`: ordered partial activates the mature Assembly and expresses learned function, while the matched fixed-prototype nearest-neighbor + lookup comparator fails to reproduce the same accept/output. Return a fresh MECHANISM candidate to Analyst; do not formalize in this run.
- `FUNCTIONAL_PARTIAL_RECOGNITION_MATCHED_BY_NN_LOOKUP`: ordered partial activates and expresses learned function, but the matched nearest-neighbor + lookup comparator reproduces the same accept/output. Reduce the current mechanism question to ordinary similarity classification/readout; recommend `REJECT` for mechanism novelty on this object.
- `NO_FUNCTIONAL_PARTIAL_RECOGNITION`: partial does not produce the learned function. Reject the proposed functional-completion mechanism for this bounded native path unless the fixed diagnostic itself is invalid.
- `INVALID_DIAGNOSTIC`: stop without scientific interpretation.

## Falsifier / reduction question

A positive native partial-completion mechanism is reduced if all downstream function on the partial pattern is exactly determined by the fixed prototype similarity threshold plus ordinary learned lookup, with no additional stateful completion effect. One clean reduction ends this object; no cycle-2 rescue tuning.

## Prospective typing before outcome

- current-object claim_ceiling: `MECHANISM`
- preformal_eligible in principle before result: `true`
- preliminary readiness: `NOT_READY`
- supported reachability: `TO_BE_TESTED_ON_SYNTHETIC_DEV_ONLY`
- functional consequence: `TO_BE_TESTED_PREDICTION_AND_ACTION_ON_PARTIAL_PATTERN`
- ordinary reductions specified: `MATCHED_FIXED_PROTOTYPE_NEAREST_NEIGHBOR_PLUS_LOOKUP`
- reductions unresolved: `YES_BEFORE_EXECUTION`
- comparator status: `PROSPECTIVELY_FIXED_NOT_YET_RUN`
- qualitative support breadth: `NONE_BEFORE_EXECUTION`
- falsifier definition: `PARTIAL_FUNCTION_FULLY_MATCHED_BY_ORDINARY_NN_LOOKUP_OR_PARTIAL_FUNCTION_ABSENT`
- open scientific choices: `NONE_FOR_THIS_CYCLE; threshold, patterns, comparator, outputs and stop mapping are fixed above`
- formal claim ceiling: `AT_MOST_NATIVE_ASSEMBLY_MEDIATED_FUNCTIONAL_PARTIAL_COMPLETION_IF_REDUCTION_SURVIVES`
- readiness status: `NOT_READY`

## Cycle 1 result

The fixed ordered partial was accepted by the mature Assembly and inherited the learned `future-X` prediction at confidence `1.0` plus deterministic `action-0`. The scrambled control was rejected. However, the prospectively matched ordinary comparator made exactly the same decisions and outputs: `pattern_similarity(full, partial)=0.8`, above the default threshold `0.66`, while `pattern_similarity(full, scrambled)=0.325`, below threshold. Routing the accepted ordinary match to the same learned lookup therefore reproduced the Assembly path's prediction/action exactly.

Mapped terminal: `FUNCTIONAL_PARTIAL_RECOGNITION_MATCHED_BY_NN_LOOKUP`.

This is a functional partial-recognition effect but not evidence for a distinct completion mechanism on the current object. The current native path is fully reduced by fixed-prototype similarity classification plus learned lookup for this prospectively fixed synthetic DEV discriminator. No cycle-2 rescue is justified.

Ordinary CI on diagnostic head `81d3bc66628ed00be00e3e3f6ea4f125020ea103`, run `35487109954`, passed Python 3.11 and 3.13 lint, local readiness, full tests, and bundle validation. CI has no evidentiary authority.

## Handoff typing after result

- recommendation: `REJECT`
- evidentiary_status: `NON_EVIDENTIARY`
- proposed claim_ceiling: `MECHANISM` for this prospectively typed current object; no positive mechanism claim survives
- proposed preformal_eligible: `false`
- preliminary readiness status: `NOT_READY`
- claim_type: `NATIVE_ASSEMBLY_MEDIATED_FUNCTIONAL_PARTIAL_COMPLETION`
- supported_reachability: `PARTIAL_RECOGNITION_REACHABLE_SYNTHETIC_DEV_ONLY`
- functional_consequence: `PRESENT_AS_PREDICTION_AND_ACTION_READOUT_ON_ORDERED_PARTIAL`
- ordinary reductions specified/controlled: `MATCHED_FIXED_PROTOTYPE_NEAREST_NEIGHBOR_PLUS_IDENTICAL_LOOKUP`
- reductions unresolved: `NONE_FOR_THIS_CURRENT_OBJECT; MATCHED_ORDINARY_REDUCTION_SUCCEEDED`
- comparator status: `COMPLETE_AND_OUTPUT_MATCHED`
- qualitative support breadth: `ONE_DETERMINISTIC_SYNTHETIC_FULL_PARTIAL_SCRAMBLED_PATTERN_SET`
- falsifier definition: `MECHANISM REQUIRED COMPARATOR FAILURE OR OUTPUT DIVERGENCE; NOT OBSERVED`
- open scientific choices: `Any stateful/generative completion mechanism beyond fixed similarity matching requires a fresh prospectively specified candidate and cannot rescue this object.`
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- candidate next research layer: `NONE`

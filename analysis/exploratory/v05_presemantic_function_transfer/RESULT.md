# EXPLORATORY / NON_EVIDENTIARY — v0.5 pre-semantic function-transfer result

## Identity

- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- candidate: `CAND-V05-PRESEMANTIC-FUNCTION-TRANSFER-01`
- exploration_cycle: `1/3`
- stable_base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `EVA-20260920T160240+0900-R16-3D7A91C4@eea87c0e67807605c8fdd10408650da4192fb06b`
- prospective_binding: `e4f30b4655d483ac0d64c28798122abd7b241b02`
- initial_diagnostic: `1875dfac036512f771c5ffad304595d89bff42a8`
- lint_only_harness_correction: `fe1459d5b58d20a8efed150e7c102759def83927`
- api_contract_harness_correction: `ee2a2e9f188b6f709073353342bab32cb7da4e06`
- corrected_exact_head_ci: `35497584012` — Python 3.11 and 3.13 completed success
- evidentiary_status: `NON_EVIDENTIARY`

The first diagnostic CI (`35497326039`) stopped at Ruff because the exploratory module docstring followed the `__future__` import. The next exact head (`35497444115`) passed lint/readiness but stopped because the harness used `PredictionDecision.next_event` instead of the repository API field `PredictionDecision.value`. Both corrections were science-invariant harness/API corrections: no pattern, threshold, label, metric, comparator, procedure, or terminal mapping changed.

## Question

Can an anonymous Assembly formed before any semantic outcome association later acquire a function from one member of its pre-existing cluster and transfer that function to another member that was never outcome-labeled and is below direct similarity threshold to the labeled exemplar?

The fixed reduction question was whether any such transfer requires a mechanism beyond either direct labeled-exemplar similarity or an ordinary fixed pre-semantic prototype cluster plus label lookup.

## Fixed synthetic construction

All three patterns used relative bins `(0, 1, 2, 3)`:

- prototype A: ordered units `(1, 2, 3, 4)`;
- later labeled exemplar B: `(1, 1, 2, 3)`;
- never-labeled transfer target C: `(1, 1, 3, 4)`.

With the repository's existing `pattern_similarity` and default Assembly threshold `0.66`:

- A↔B = `0.6625` — accepted by the pre-existing Assembly;
- A↔C = `0.8000` — accepted by the pre-existing Assembly;
- B↔C = `0.6000` — below direct similarity threshold.

These values were fixed construction constraints in the prospective contract rather than selected after the functional result.

## Implementation and observations

1. A was presented under three distinct synthetic episode identities, producing a mature Assembly before any outcome/prediction association existed. `AssemblyPredictor.counts` remained empty at this point.
2. B was then presented with `learn=false`; it activated that already-mature Assembly. Exactly one synthetic semantic label, `future-X`, was attached through `AssemblyPredictor.observe`.
3. C was presented with `learn=false`; it activated the same mature Assembly despite never receiving an outcome label itself.
4. `AssemblyPredictor.predict` for C returned `value="future-X"` with confidence `1.0`.
5. The direct B→C nearest-neighbor reduction failed because `0.6000 < 0.66`.
6. The prospectively fixed ordinary A-prototype cluster plus one label lookup reproduced the transfer exactly because `0.8000 >= 0.66` and the shared cluster identity already carried `future-X`.

## Terminal mapping

Prospectively fixed terminal reached:

`CLUSTER_LOOKUP_EXPLAINS_TRANSFER`

There is a functional transfer observable in this synthetic construction: a never-outcome-labeled member below direct similarity threshold to the labeled exemplar receives the Assembly-level prediction after the Assembly is labeled later. However, this current object does not require a stronger mechanism than ordinary fixed pre-semantic prototype clustering followed by label lookup. The exact ordinary comparator reproduces the functional output.

This is therefore a reduction, not support for novelty or a formal mechanism claim. Cycle 2 is not used for rescue tuning. Any future attempt to test stateful/generative/context-sensitive function transfer that cannot be reduced to fixed clustering must be a fresh candidate ID with a fresh prospective contract.

## Discovery handoff typing

- proposed claim_ceiling: `MECHANISM` for this current prospectively typed object
- proposed preformal_eligible: `false` after the reduction
- preliminary preformal_readiness:
  - claim_type: `MECHANISM`
  - supported_reachability: `MATURE_PRESEMANTIC_ASSEMBLY_REACHED; LATER_SINGLE_LABEL_ASSOCIATION_REACHED; NEVER_LABELED_TARGET_FUNCTION_TRANSFER_REACHED`
  - functional_consequence: `FUTURE_X_TRANSFER_TO_NEVER_OUTCOME_LABELED_TARGET_BELOW_DIRECT_LABELED_EXEMPLAR_THRESHOLD`
  - ordinary_reductions_specified_controlled: `DIRECT_LABELED_EXEMPLAR_SIMILARITY; FIXED_PRESEMANTIC_PROTOTYPE_CLUSTER_PLUS_LABEL_LOOKUP`
  - reductions_unresolved: `[]`
  - comparator_status: `FIXED_PROTOTYPE_CLUSTER_LOOKUP_REPRODUCES_TRANSFER_EXACTLY`
  - qualitative_support_breadth: `ONE_FIXED_SYNTHETIC_PATTERN_TRIPLET; DEFAULT_SIMILARITY_THRESHOLD; ONE_LABEL`
  - falsifier_definition: `NO_FUNCTION_TRANSFER_OR_EXACT_ORDINARY_REDUCTION`
  - open_scientific_choices: `Any non-prototype/stateful/generative transfer discriminator requires a fresh candidate and fresh prospective contract.`
  - formal_claim_ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
  - status: `NOT_READY`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- system_priority_exception.used: `false`
- candidate next research layer: `NONE`
- recommendation: `REJECT`

No FORMAL identity, STARTED authority, official TEST/scorer, preserve/freeze/evidence ref, consumed identity, or stable-main mutation was used.

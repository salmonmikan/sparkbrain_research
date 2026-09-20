# EXPLORATORY / NON_EVIDENTIARY — v0.5 context-conditioned prediction result

## Identity

- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- candidate: `CAND-V05-CONTEXT-CONDITIONED-PREDICTION-01`
- exploration_cycle: `1/3`
- stable_base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `EVA-20260920T180852+0900-R17-152262F6@4dc5a5b43f26789f32567eb69cbb4a26b9cd6825`
- main_generation_observed: `MAIN-20260920T181208+0900-PRIMARY-FUNNEL21-HOLD-4F2C91A7`
- prospective_binding: `01d4cc8daf07be67b8f633434030241276a0a4b0`
- diagnostic_head: `38c6f3cc972898c170fdf5853190ca33de8f6882`
- diagnostic_ci: `35502813034` — Python 3.11 and 3.13 completed success; lint, local readiness, full tests, and bundle validation all passed
- evidentiary_status: `NON_EVIDENTIARY`

Control R15 semantic preflight was completed before the first outcome-bearing execution. The prospective contract bound the terminal to the exact public `PredictionDecision.value`, `PredictionDecision.assembly_id`, and predictor count-state semantics after reading stable-main `contracts.py` blob `048b93cddb16dbe9276a0e2c0f972406291c1cb2` and `prediction.py` blob `9805031fb8db235d2f3cf4c81421b896d2597af4`. No terminal-relevant API, representation, label, comparator, count, or categorical mapping was repaired after outcome exposure.

## Question

After balanced training in which the same mature current Assembly X is followed by different outcomes depending on immediately preceding mature Assembly context A versus B, can the native v0.5 prediction component emit different predictions for the same X activation solely from that immediately preceding Assembly context?

The fixed falsifier/reduction question was whether any apparent context sensitivity survives a matched first-order current-Assembly frequency lookup using the predictor's exact stored X table and deterministic tie rule.

## Implementation and observations

The bounded DEV-only component probe used three direct mature, unsuppressed `AssemblyActivation` objects: `assembly-A`, `assembly-B`, and `assembly-X`. Training was fixed at four A-context trials followed by X→`future-A`, and four B-context trials followed by X→`future-B`. The resulting native predictor state was exactly:

`{"assembly-X": {"future-A": 4, "future-B": 4}}`.

Evaluation performed no learning. Calling `predict(A)` immediately before `predict(X)` left predictor state unchanged; calling `predict(B)` immediately before `predict(X)` also left predictor state unchanged. In both arms, X returned:

- `assembly_id="assembly-X"`;
- `value="future-A"`;
- `confidence=0.5`.

The fixed first-order current-Assembly comparator produced the same `future-A` result from the balanced X table under the repository predictor's deterministic tie behavior. The preceding context exposure therefore caused no detectable functional difference in the native prediction component.

## Terminal mapping

Prospectively fixed terminal reached:

`FIRST_ORDER_CURRENT_ASSEMBLY_LOOKUP_EXPLAINS`

The current v0.5 `AssemblyPredictor` does not expose a context-conditioned prediction effect in this bounded discriminator. Identical current X activation after A versus B context yields identical output, and that output is reproduced exactly by ordinary current-Assembly frequency lookup. The context calls themselves do not mutate predictor state.

This is negative mechanism information, not evidence that all SparkBrain state is context-free and not a claim about future architectures. It closes only this current component-level context-conditioned prediction object. Cycle 2 is not used for rescue tuning.

## Discovery handoff typing

- proposed claim_ceiling: `MECHANISM` for this prospectively typed current object
- proposed preformal_eligible: `false` after the fixed ordinary reduction
- preliminary preformal_readiness:
  - claim_type: `MECHANISM`
  - supported_reachability: `MATURE_CONTEXT_ACTIVATIONS_AND_BALANCED_X_OUTCOME_TABLE_REACHED`
  - functional_consequence: `ABSENT_CONTEXT_CONDITIONED_DIFFERENTIATION_FOR_IDENTICAL_CURRENT_X`
  - ordinary_reductions_specified_controlled: `FIRST_ORDER_CURRENT_ASSEMBLY_FREQUENCY_LOOKUP_WITH_EXACT_NATIVE_TIE_RULE`
  - reductions_unresolved: `[]`
  - comparator_status: `COMPLETE_AND_EXACTLY_REPRODUCES_BOTH_CONTEXT_ARMS`
  - qualitative_support_breadth: `ONE_FIXED_COMPONENT_LEVEL_SYNTHETIC_A_B_X_CONSTRUCTION; BALANCED_4_4_OUTCOMES`
  - falsifier_definition: `X_AFTER_A_AND_X_AFTER_B_DIFFER_WITH_CONTEXT_MATCHED_VALUES_WHILE_FIRST_ORDER_LOOKUP_CANNOT_REPRODUCE`
  - open_scientific_choices: `Any stronger sequence-state or integrated recurrent-context discriminator must be a fresh candidate with a fresh prospective contract; do not rescue this object.`
  - formal_claim_ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
  - status: `NOT_READY`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- system_priority_exception.used: `false`
- candidate next research layer: `NONE`
- recommendation: `REJECT`

No FORMAL identity, STARTED authority, official TEST/scorer, preserve/freeze/evidence ref, consumed identity, stable-main mutation, or hypothesis-dependent merge was used.

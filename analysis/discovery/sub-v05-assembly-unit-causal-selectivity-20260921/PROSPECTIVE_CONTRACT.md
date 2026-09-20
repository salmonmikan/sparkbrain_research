# SUB Discovery Prospective Contract — Assembly-unit causal selectivity

- operating_mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- candidate_id: `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01`
- target: `V05_ASSEMBLY_UNIT_CAUSAL_SELECTIVITY_DISCOVERY_CYCLE1`
- cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- claim_ceiling: `MECHANISM`
- prospective_preformal_eligible: `true_if_selective_effect_survives_current_reduction_question_else_false`
- source_ref: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `EVA-20260921T055830+0900-R28-4D7A91C2@cde085b48dde724b2ac814585d7f0757bf16ef63`
- main_generation: `MAIN-20260921T061540+0900-PRIMARY-FUNNEL21-HOLD-R28-4C8A21D7`

## Independence

MAIN owns no active scientific object under R28. This object is not `CAND-H7-RESP-01`, is not a successor/rescue of any terminal candidate, and does not use FORMAL/PRE_FORMAL/official TEST/held-out authority or consumed/frozen identities.

## Search-space reframe

The prior no-target episode concentrated on endogenous feedback, delayed credit, context prediction, eligibility history, and SYSTEM semantics. Stable v0.5 theory separately defines causal functional Assembly evidence as selective impairment under targeted unit intervention beyond matched random intervention. That causal-contribution question is not represented in the current 22-candidate portfolio and is distinct from the terminal Assembly-feedback question (which asked whether mature Assembly readout feeds back into lower dynamics).

## Mechanism question

Given a mature motif-selective Assembly with an already learned prediction, does suppressing a bounded subset of its constituent internal-reservoir units selectively remove the Assembly-mediated prediction on an otherwise identical DEV episode more than suppressing the same number of nonmember units matched prospectively for baseline spike participation?

## Hypothesis

If constituent units carry Assembly-specific causal function rather than merely generic field activity, targeted member suppression should abolish or redirect the baseline-correct prediction while a same-cardinality baseline-activity-matched nonmember suppression leaves that prediction intact.

## Fixed DEV inputs

- development seed: `501` only;
- training: `training_episodes(seed=501, count=24)` via the existing non-held-out training path;
- probe episode: a fresh DEV `make_episode(seed=501, index=24, motif=MOTIF_X, condition="motif", start_ms=trained.current_time_ms + 100.0)`; this is not `held_out_episodes`;
- no held-out seeds, confirmatory seeds, official scorer, or preregistered FORMAL identity;
- no production/source semantic changes.

## Target and comparator selection — fixed before intervention outcome

1. From training rows, select the mature Assembly with the largest positive `(motif_x_count - motif_y_count)`, tie-breaking by `assembly_id`.
2. Run exactly one baseline nonlearning copy on the fixed probe episode.
3. Require baseline strongest mature activation to be the selected Assembly and baseline prediction to equal `outcome-0`; otherwise terminal `INVALID_DIAGNOSTIC`.
4. Let `k=min(4, number_of_selected_assembly_prototype_units)`; require `k>=1`.
5. Target units are the `k` selected-Assembly prototype units with highest baseline probe spike count, ties by unit id.
6. Comparator candidates are internal non-receptor, nonmember units. Greedily match one distinct comparator unit to each target unit by minimum absolute difference in baseline probe spike count, ties by unit id. Comparator cardinality must equal `k`.
7. Do not alter target/comparator selection after intervention outcomes are known.

## Ordinary reduction question

Can any targeted functional loss be reproduced by suppressing an equal number of nonmember units matched on baseline probe spike participation? If yes, the observation reduces to generic activity/lesion load rather than Assembly-member causal selectivity.

A positive selective result may still leave graph-centrality/topological-load reduction unresolved; such a result is Discovery-level only and remains `NOT_READY` for PRE_FORMAL until that reduction is prospectively controlled.

## Falsifier / terminal mapping

- `SELECTIVE_TARGETED_FUNCTION_LOSS`: baseline prediction is `outcome-0`; targeted member suppression changes/removes that prediction; activity-matched nonmember suppression retains `outcome-0`.
- `GENERIC_ACTIVITY_LESION_REDUCTION`: both targeted and matched nonmember suppression change/remove the baseline-correct prediction.
- `NO_TARGETED_FUNCTION_LOSS`: targeted member suppression retains the baseline-correct prediction.
- `INVALID_DIAGNOSTIC`: no valid mature motif-X target, baseline target/prediction contract fails, insufficient comparator pool, or execution/API contract fails.

No numeric rescue threshold, retuning, alternate seed, alternate target set, second probe, held-out sweep, or cycle-2 rescue is allowed in this run.

## Preliminary readiness before outcome

- claim_type: `mechanism`
- supported_reachability: `PARTIAL`
- functional_consequence: `PROSPECTIVELY_TESTED_THIS_CYCLE`
- ordinary_reductions_specified_or_controlled: `equal-cardinality baseline-spike-participation-matched nonmember lesion`
- ordinary_reductions_unresolved: `graph centrality / topology load if selective result is observed`
- comparator_status: `PROSPECTIVELY_DEFINED`
- qualitative_support_breadth: `single bounded DEV seed/probe`
- falsifier_definition: fixed above
- open_scientific_choices: `topology/centrality matching only if a fresh successor is later authorized`
- formal_claim_ceiling: `assembly-member causal selectivity beyond matched activity lesion`
- status: `NOT_READY`

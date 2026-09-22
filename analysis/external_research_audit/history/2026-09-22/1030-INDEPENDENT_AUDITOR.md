# INDEPENDENT_AUDITOR — PD01 null-vs-null reduction-identifiability audit

- schema_version: `2`
- generation_id: `AUD-20260922T103000+0900-R6-PD01-NULLREDUCTION-9C4A21E7`
- produced_at: `2026-09-22T10:30:00+09:00`
- producer_run_id: `external-audit-20260922T103000+0900-R6-PD01-9C4A21E7`
- authority_scope: `INDEPENDENT_AUDITOR_READ_ONLY_REPOSITORY_EVIDENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `AUD-20260921T223000+0900-R5-H5-DEADWORK-5E8C21A4`
- role: `INDEPENDENT_AUDITOR`
- schedule_slot: `10:30 JST`
- schedule_inference: `false`
- audit_classification: `WEAKENED`

## Phase 1 — blind target selection

Before reading current Control Brain, Evidence Analyst, MAIN/SUB, or Literature summaries, the audit fixed authoritative PD01 `pd01-long-history-fading-memory-official-v1`, specifically the terminal `FAIL_REDUCED_BY_FADING_MEMORY`, as the target.

The repository-only attack hypotheses were: authority/package/STARTED/raw/evidence drift; scorer/evaluator or target leakage; semantic/global lookup privilege mismatch; resource mismatch; seed/bootstrap fragility; insufficient long-lag support; output-only reduction mismatch; simpler finite/fading-memory explanations; protocol drift/stale evidence; and a distinct reduction-identifiability question: whether `REDUCED_BY_FADING_MEMORY` is stronger language than the data justify when both SparkBrain and the fixed reservoir fail to demonstrate long-lag recoverability.

Prior audit history was read only for dedupe. PD01 had not previously received a dedicated independent audit. The blind target was not changed.

## Repository evidence

The one-way chain is coherent. Exact package `b9d38daa5faca348ad2db3898ba71e2abc99f631` precedes STARTED `0569e348b9d93aeee53fc58daf4b71ee92303d6c`; workflow `35301327618` ran attempt 1 at the exact STARTED head and completed successfully; target-blind raw was preserved before scoring at `65ae7a50ee2279ab5edc3ca43ea3bf69daecb881`; evidence commit `fc5c8cda283360addddb7da482b14e69beaba1f7` is bound by the annotated PD01 evidence tag object `e4c4e6428d8ef9e09e92cae231041de0788162e2`. The preserved manifest binds raw SHA-256 `5ad0c545c5aa4548ca7a852e9c46a908af41c9a44047667c9ed09c1fd5041638`, 1024 histories / 2048 prediction rows, fixed candidate/comparator readouts, and `targets_materialized=false` at raw preservation. No retry, post-START retuning, raw-before-score violation, identity mismatch, or obvious comparator privilege violation was found.

The exact scored primary endpoint is also internally coherent: SparkBrain accuracy `0.47265625` with 95% CI `[0.431640625, 0.515625]`; fixed contractive reservoir accuracy `0.5`; effect `-0.02734375` with 95% CI `[-0.068359375, 0.015625]`. Under the frozen decision rule, the effect upper bound is below `0.05`, so the canonical token `FAIL_REDUCED_BY_FADING_MEMORY` is a valid execution of the predeclared scorer and must remain immutable.

## New attack surface — null-vs-null does not identify a positive reduction

The claim under test was not merely that SparkBrain is statistically indistinguishable from a reservoir. It claimed that an older anonymous-lineage event remains *recoverable* from SparkBrain at long lag beyond a conventional contractive fading-memory reservoir under matched observable input and linear-readout privilege.

On the primary endpoint, however, SparkBrain itself does not demonstrate positive long-lag recoverability: its point accuracy is below chance and its CI includes chance. The comparator is exactly at chance. Therefore the observed outcome is a `null-vs-null` comparison: SparkBrain shows no demonstrated long-lag capability, and the reservoir shows no demonstrated capability either.

That is enough to falsify the registered superiority/recoverability claim and enough to trigger the frozen FAIL token. It is **not** enough to establish that a fading-memory reservoir positively explains or mechanistically reduces an observed SparkBrain long-history capability, because there is no positive long-history capability on this endpoint to reproduce. Matching a failure is not the same evidentiary object as reproducing a demonstrated phenomenon with a simpler mechanism.

Accordingly, the strongest interpretation supported by PD01 is:

`NO_DEMONSTRATED_LONG_LAG_RECOVERY_AND_NO_ADVANTAGE_OVER_THE_FIXED_FADING_MEMORY_RESERVOIR`

This is an interpretation ceiling only. The canonical frozen token, evidence files, statistics, scorer, and immutable refs must not be renamed or rewritten retrospectively.

## Phase 2 — interpretation comparison

Only after the target and attack hypotheses were fixed, current Control R31, Evidence Analyst R58, MAIN R58, SUB R57, and Literature R27 were consumed. Current control-plane state is intentionally idle with no active scientific object, no PRE_FORMAL/FORMAL authority, and PD01 remains a consumed immutable identity. No current stream relies on PD01 as positive evidence that an ordinary fading-memory mechanism explains a demonstrated SparkBrain memory capability. The blind target therefore remains valid and `blind_target_change_reason=null`.

The control-plane posture is already conservative enough that no emergency strategy correction is required. The useful handoff is a terminology/claim-scope constraint for future Evidence Analyst and Control use: retain PD01 as a valid negative result against the registered long-history superiority claim, but do not cite it as positive mechanistic reduction evidence unless a future, independent prospective object first demonstrates a recoverable candidate phenomenon and then shows that an ordinary fading-memory model reproduces it under matched privilege/resources.

## Audit conclusion

`audit_classification = WEAKENED`.

The evidence integrity and frozen endpoint decision remain strong. What is weakened is the mechanistic/reduction reading suggested by the terminal label: the data establish failure to demonstrate long-lag recoverability and failure to beat the fixed reservoir, not positive reduction of an observed long-memory phenomenon by fading-memory dynamics.

No Utility request was created. Any taxonomy change or positive-capability-vs-reduction discriminator belongs only in a fresh prospective object; consumed PD01 must not be rerun, rescored, relabeled, or repaired.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - PD01_LONG_HISTORY_FADING_MEMORY
  - PD01_TERMINAL_INTERPRETATION
  - PERSISTENT_DYNAMICAL_COGNITION
  - REDUCTION_EVIDENCE_SEMANTICS
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: CANONICAL_PD01_FAIL_REMAINS_PROTOCOL_VALID_BUT_MECHANISTIC_REDUCTION_INTERPRETATION_IS_WEAKENED_BY_NULL_VS_NULL_NONIDENTIFIABILITY
audit_classification: WEAKENED
blind_target_selection:
  target: authoritative PD01 FAIL_REDUCED_BY_FADING_MEMORY, audited for whether the reduction interpretation exceeds what a null-vs-null endpoint identifies
  attack_hypotheses:
    - authority/package/STARTED/raw/evidence mismatch or protocol drift
    - scorer/evaluator/target leakage
    - comparator semantic/global-information privilege mismatch
    - resource mismatch
    - seed/bootstrap fragility
    - insufficient long-lag support
    - output-only matching insufficient for mechanism reduction
    - simpler finite/fading-memory explanation
    - null-vs-null endpoint may falsify superiority without positively identifying a reduction mechanism
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - keep canonical PD01 immutable; no rerun, rescore, retune, relabel, or reinterpretive rewrite
  - in a fresh object, require an absolute candidate recoverability floor above chance before using positive `reduced by baseline` language
  - prospectively distinguish `candidate capability absent` from `positive candidate capability reproduced by ordinary baseline`
  - if positive recoverability exists, use predeclared equal-privilege fading-memory baselines/seeds without comparator shopping
  - for a mechanism-reduction claim, require the simpler baseline to reproduce a demonstrated positive phenomenon or matched response structure, not merely equal failure
questions_for_evidence_analyst:
  - Preserve the frozen PD01 token exactly while capping narrative interpretation at no demonstrated long-lag recovery/no advantage over the fixed reservoir?
  - In future reduction objects, require a positive absolute candidate-capability floor before interpreting comparator equivalence as mechanism reduction?
  - Distinguish failure-to-demonstrate the phenomenon from successful ordinary-mechanism reduction in terminal taxonomy/claim scope prospectively?
questions_for_control_brain:
  - Treat PD01 as strong negative evidence against the registered long-history superiority claim, but not positive evidence that fading-memory dynamics explain a demonstrated SparkBrain memory capability?
  - Add null-vs-null reduction-identifiability to the future reduction-claim checklist?
  - Keep PD01 consumed/closed with no rescue authority or retrospective relabeling?
must_not_change_frozen_or_consumed:
  - PD01 exact package b9d38daa5faca348ad2db3898ba71e2abc99f631
  - PD01 STARTED 0569e348b9d93aeee53fc58daf4b71ee92303d6c
  - PD01 raw preserve 65ae7a50ee2279ab5edc3ca43ea3bf69daecb881 and raw SHA-256 5ad0c545c5aa4548ca7a852e9c46a908af41c9a44047667c9ed09c1fd5041638
  - PD01 evidence commit fc5c8cda283360addddb7da482b14e69beaba1f7 and annotated evidence tag object e4c4e6428d8ef9e09e92cae231041de0788162e2
  - workflow 35301327618, canonical statistics, scorer decision, and FAIL_REDUCED_BY_FADING_MEMORY token
  - all other consumed C19-v4/C19-R1/C19-R2/H5/NI01 identities and immutable evidence
  - no rerun, rescore, retune, relabel, STARTED/TEST, PRE_FORMAL/FORMAL promotion, research merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```

## Freshness addendum

After the initial persistence, the allowed orchestrator mailbox was re-fetched and SUB had advanced from R57 to `SUB-20260922T103553+0900-NOOP-R58INTENTIONALIDLE-7D4C21A9@c7443d5dd4c118cea86ed62f1681ff4f7cb943ba`. This is a no-target, NON_EVIDENTIARY intentional-idle generation under the same `EVA-20260922T100852+0900-R58-7D4C21A9` authority, with no scientific result or candidate-lifecycle delta. It does not change the blind target, attack hypotheses, audit classification, affected lines, or PD01 interpretation. Stable `main`, Control R31, and Evidence Analyst R58 were unchanged on the same freshness pass.

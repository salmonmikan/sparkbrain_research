# INDEPENDENT_AUDITOR — H5 semantic-dead-work attack

- schema_version: `2`
- generation_id: `AUD-20260921T223000+0900-R5-H5-DEADWORK-5E8C21A4`
- produced_at: `2026-09-21T22:30:00+09:00`
- producer_run_id: `external-audit-auto-20260921T223000+0900-R5-5E8C21A4`
- authority_scope: `INDEPENDENT_AUDITOR_READ_ONLY_REPOSITORY_EVIDENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `AUD-20260921T103000+0900-R4-ASSEMBLY-CONFOUND-7D3A91E4`
- role: `INDEPENDENT_AUDITOR`
- schedule_slot: `22:30 JST`
- schedule_inference: `false`

## Phase 1 — blind target selection

Before consuming Control Brain, Evidence Analyst, MAIN/SUB, or Literature summaries, the audit fixed the target as authoritative H5 `h5-event-routing-work-reduction-official-v1`, specifically whether the terminal `FAIL_NO_USEFUL_WORK_REDUCTION` can be interpreted as evidence that lazy node-state decay / event-routed active execution itself fails to deliver useful algorithmic-work reduction.

Repository-only attack hypotheses were fixed as: authority/package/STARTED/raw/evidence drift; scorer or target leakage; comparator privilege mismatch; seed/bootstrap fragility; resource-accounting mismatch; semantically inactive subsystem work dominating the aggregate metric; sparse-workload mismatch; and overgeneralization from the exact current implementation/counter vocabulary to the event-routing/lazy-state principle.

The prior audit stream was read for dedupe. An older H5 audit (`d3a9c8d4c4cf8a3e5a0152d7b0749633776ecb56`) had already established that all-edge eligibility maintenance numerically dominates H5 work. This run retained the target only because it tests a narrower attack surface not established there: whether that dominant eligibility work is *semantically inactive* under the registered H5 workload. The blind target itself was not changed.

## Repository evidence

The immutable H5 chain remains coherent. Exact package `2086a8f4ea080a7a8a0e3c79d77afe9b516db905` precedes STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; workflow `35338995888` completed attempt 1 successfully; raw was preserved before scoring at `ce5797eb584344db7a512e585506fb6c59ea475b`; evidence commit `61aff6d74b82b68a326f3d90505d70bcd4071fd5` is bound by the annotated H5 evidence tag. No retry, post-START scientific drift, raw-before-score violation, or identity mismatch was found.

The registered result is unchanged: primary mean work reduction `0.023826074023772813`, 95% CI `[0.02379403660851484, 0.023859665012124307]`, with activity-level means `0.05927001218870528`, `0.009811966841371046`, and `0.0023962430412420807` for activity fractions `0.01`, `0.05`, and `0.15`. Under the frozen decision rule this validly maps to `FAIL_NO_USEFUL_WORK_REDUCTION`.

### New attack surface: semantic dead work

The prospective H5 contract fixes the graph as `plastic=false` and the workload generator schedules stimulus events, not reward events. Stable SparkBrain nevertheless increments eligibility on every outgoing edge when a unit fires and globally decays eligibility on every event. Reward-driven weight updates are the only downstream use of eligibility, and `_apply_reward` explicitly skips non-plastic edges.

Therefore, in this exact H5 workload, eligibility values cannot change any graph weight or behavioral output. Yet `eligibility_edge_touches` and `eligibility_multiplications` are counted in the primary total-work metric for both candidate and dense comparator. In a preserved 128-node, 1%-activity bursty cell, those two eligibility counters contribute `122880 / 124062 = 99.05%` of candidate work; the dense comparator pays the same `122880` eligibility operations. In the preserved 128-node, 5%-activity bursty cell they contribute `737280 / 744146 = 99.08%` of candidate work.

This does **not** invalidate the registered H5 total-work terminal: the contract prospectively defined an implementation-faithful aggregate counter and intentionally included common bookkeeping. It does, however, sharpen the interpretation ceiling. H5 is not an isolated test of whether lazy node-state decay or event-routed routing saves work; its aggregate is dominated by an output-neutral all-edge eligibility subsystem that masks those component savings. The result is therefore robust for the exact current-implementation total-work claim, but should not be promoted to a no-go claim about event routing or lazy state materialization as principles.

## Phase 2 — interpretation comparison

After the target and attack hypotheses were fixed, current Control, Evidence Analyst, MAIN, SUB, and Literature streams were read. None currently uses H5 as an active novelty claim. Evidence Analyst R44 has no active scientific object and keeps H5 consumed/no-retry. MAIN R44 is intentionally idle, SUB remains no-target, and Literature R22 concerns selection-aware validity rather than H5. No strategy summary invalidated or replaced the blind target.

## Audit conclusion

`audit_classification = ROBUST_SO_FAR` for the exact registered H5 aggregate-work terminal. The genuinely new audit issue is a stronger source-level explanation for why the terminal must remain narrow: the dominant eligibility work is semantically inactive under the fixed non-plastic/no-reward workload.

No Utility request was created. Any component-isolation test would have to be a genuinely fresh prospective object; using this result to rerun/rescore or repair consumed H5 would violate the one-way boundary.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - H5_EVENT_ROUTING_WORK_REDUCTION
  - H5_WORK_METRIC_COMPONENT_ATTRIBUTION
  - PROGRAMME_ARCHITECTURE_EFFICIENCY
  - FUTURE_WORK_REDUCTION_CONTRACTS
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: REGISTERED_H5_FAIL_REMAINS_ROBUST_BUT_INTERPRETATION_IS_FURTHER_NARROWED_BY_SEMANTICALLY_INACTIVE_ELIGIBILITY_WORK
audit_classification: ROBUST_SO_FAR
blind_target_selection:
  target: H5 h5-event-routing-work-reduction-official-v1 terminal FAIL_NO_USEFUL_WORK_REDUCTION, audited for overinterpretation as an event-routing/lazy-state no-go
  attack_hypotheses:
    - authority/package/STARTED/raw/evidence mismatch or protocol drift
    - scorer/evaluator leakage
    - comparator information/resource privilege mismatch
    - seed or bootstrap fragility
    - resource-accounting mismatch
    - semantically inactive subsystem dominating the aggregate metric
    - workload/comparator mismatch
    - broader-than-registered mechanism interpretation
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - keep canonical H5 immutable; do not rerun, retune, rescore, relabel, or reopen it
  - in a genuinely fresh efficiency object, preregister subsystem-wise work decomposition alongside aggregate work
  - distinguish implementation overhead from mechanism-attributable work before interpreting a total-work terminal mechanistically
  - if eligibility is scientifically in scope, use a prospectively bound plastic/reward workload where eligibility has semantic consequences
  - compare global all-edge eligibility maintenance against an equal-semantics localized/event-routed eligibility baseline only in a fresh object
  - bind separate runtime/energy methodology for wall-clock, memory, cache, or energy claims
questions_for_evidence_analyst:
  - Preserve H5 official FAIL exactly while making explicit that it is a current-implementation aggregate-work result, not an isolated event-routing/lazy-state causal test?
  - Keep H5 consumed/no-retry and require any component-isolation study to use a fresh identity/object?
  - Require semantic-activity and component-attribution checks for future resource-efficiency evidence?
questions_for_control_brain:
  - Avoid using H5 as broad evidence that event routing or lazy state materialization cannot yield useful efficiency?
  - Add semantically inactive subsystem domination to the future resource-metric audit checklist?
  - Keep H5 closed and treat the new issue as interpretation sharpening, not rescue authority?
must_not_change_frozen_or_consumed:
  - H5 exact package 2086a8f4ea080a7a8a0e3c79d77afe9b516db905
  - H5 STARTED 058e90227cd48e1c10c6ecbaed01efdec1217d0e
  - H5 raw preserve ce5797eb584344db7a512e585506fb6c59ea475b
  - H5 evidence commit 61aff6d74b82b68a326f3d90505d70bcd4071fd5 and annotated evidence tag
  - workflow 35338995888 and canonical H5 statistics / FAIL_NO_USEFUL_WORK_REDUCTION token
  - all other consumed C19-v4/C19-R1/C19-R2/PD01/NI01 and immutable evidence
  - no rerun, rescore, retune, relabel, STARTED/TEST, PRE_FORMAL/FORMAL promotion, research merge, immutable-ref mutation, or scheduler change
utility_request_created: null
```

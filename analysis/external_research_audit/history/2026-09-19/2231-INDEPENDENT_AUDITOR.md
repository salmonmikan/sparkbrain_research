# SparkBrain Independent Audit — 2026-09-19 22:31 JST

Role: `INDEPENDENT_AUDITOR`

## Blind target selection

Before reading Control Brain, Evidence Analyst, MAIN/SUB or Literature summaries, repository evidence fixed the target as H5 `h5-event-routing-work-reduction-official-v1`, terminal `FAIL_NO_USEFUL_WORK_REDUCTION`.

Authoritative repository refs inspected included `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, exact package `2086a8f4ea080a7a8a0e3c79d77afe9b516db905`, STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`, raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`, terminal evidence `61aff6d74b82b68a326f3d90505d70bcd4071fd5`, the evidence tag, workflow attempt 1, raw rows and bound scorer/contract.

Blind attacks: authority/package/STARTED/preserve/evidence mismatch; leakage; comparator information/resource privilege; seed fragility/pseudo-replication; insufficient ablation/simple bookkeeping explanation; post-outcome drift; stale/duplicate evidence; and claim-boundary overreach from registered algorithmic work to general compute efficiency.

`blind_target_change_reason: null`

## Result

Classification: `ROBUST_SO_FAR`.

The one-way evidence chain is coherent and the frozen classification is valid. Terminal primary mean work reduction is `0.023826074023772813`, 95% CI `[0.02379403660851484, 0.023859665012124307]`; activity means are `0.05927001218870528`, `0.009811966841371046`, and `0.0023962430412420807` for activity 0.01/0.05/0.15. The registered FAIL rule is met because the primary CI upper bound is <= `0.05`.

The important new audit information is interpretive rather than invalidating. The frozen contract explicitly charges both candidate and comparator the same per-event **all-edge eligibility decay**. The candidate therefore remains globally eager for eligibility maintenance even while node-state decay/materialization is lazy and event-routed. In the first preserved sparse 128-node / 1%-bursty cell, eligibility touches plus multiplications account for `122880 / 124062 = 99.05%` of candidate audited work; candidate state materializations are `120` versus `1408` for dense. The local state-laziness saving is real but is swamped by a shared global edge-maintenance term.

Hence canonical `FAIL_NO_USEFUL_WORK_REDUCTION` is robust for the exact prospective aggregate algorithmic-work claim, implementation and counter vocabulary. It should not be generalized to “event routing/lazy execution cannot save compute”, wall-clock speed, hardware energy, or an optimized/localized eligibility implementation. This is best treated as an architectural bottleneck diagnosis, not a rescue rationale and not positive novelty evidence.

## Phase-2 comparison

Only after blind target fixation, current control-plane streams were read. Control Brain `566f3b7c590fcfe2b9e8aaa0415da964989b1124` carries H5 only as `FAIL_NO_USEFUL_WORK_REDUCTION`. Evidence Analyst `a3ec861d71c0965625fc1d2e5e8f65f4ce47f834` explicitly reserved H5 for a narrow read-only accounting/claim-boundary audit. MAIN latest remained HOLD and reserved H5 for independent Audit; SUB independently avoided H5. Orchestrator branch tip consumed: `40f43d747bdac156113be7812fc0623a86f99c60`; MAIN report commit `b02e07e9229de0f9c5be7b93a487369717dd43f7`; SUB report commit `40f43d747bdac156113be7812fc0623a86f99c60`. Newest Literature handoff `94ae4abf7b310faefa7244a03cda2a597dba4dca` does not alter H5 evidence.

No current control-plane overclaim was found, so the canonical claim remains `ROBUST_SO_FAR` with the interpretation ceiling above.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - H5_EVENT_ROUTING_WORK_REDUCTION
  - PROGRAMME_ARCHITECTURE_EFFICIENCY
  - FUTURE_WORK_REDUCTION_CONTRACTS
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  H5_CANONICAL_FAIL_ROBUST_FOR_REGISTERED_ALGORITHMIC_WORK_METRIC;
  INTERPRETATION_MUST_REMAIN_IMPLEMENTATION_AND_COUNTER_VOCABULARY_SPECIFIC;
  GLOBAL_ALL_EDGE_ELIGIBILITY_MAINTENANCE_DOMINATES_SPARSE_CANDIDATE_WORK;
  NO_POSITIVE_NOVELTY_SUPPORT_RESTORED.
audit_classification: ROBUST_SO_FAR
blind_target_selection:
  target: H5 official-v1 terminal FAIL_NO_USEFUL_WORK_REDUCTION
  selected_before_control_plane_summaries: true
  authoritative_refs:
    - main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
    - exact package@2086a8f4ea080a7a8a0e3c79d77afe9b516db905
    - STARTED@058e90227cd48e1c10c6ecbaed01efdec1217d0e
    - raw preserve@ce5797eb584344db7a512e585506fb6c59ea475b
    - terminal evidence@61aff6d74b82b68a326f3d90505d70bcd4071fd5
  attack_hypotheses:
    - authority/package/STARTED/preserve/evidence mismatch
    - target/evaluator leakage
    - comparator information/resource privilege mismatch
    - seed fragility or pseudo-replication
    - insufficient ablation/simple accounting explanation
    - post-outcome drift
    - stale/duplicate evidence
    - claim-boundary overreach from algorithmic work to general compute efficiency
  why_consequential: H5 is a consumed terminal architecture-efficiency result not previously independently audited.
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - never rerun, retune, rescore, relabel or reopen canonical H5
  - future fresh efficiency objects should prospectively report component-wise work shares
  - separate node-state locality, routing work and eligibility-maintenance complexity
  - separately preregister wall-clock/memory/cache/energy methods for any systems-efficiency claim
  - any optimized/local-eligibility question must be a fresh prospective object if independently justified
questions_for_evidence_analyst:
  - Keep H5 synthesis scoped to the registered algorithmic-work metric and exact all-edge-eligibility implementation?
  - Record global eligibility maintenance as the principal architectural bottleneck without treating it as a rescue rationale?
  - Require component-wise resource accounting in future fresh efficiency contracts?
questions_for_control_brain:
  - Count H5 as robust negative evidence for the exact efficiency claim while avoiding a general no-go statement about event routing/lazy execution?
  - Treat H5 primarily as architecture bottleneck information rather than mechanistic novelty evidence?
  - Keep H5 fully closed; require any optimized/local-eligibility question to be a new prospective object?
must_not_change_frozen_or_consumed:
  - h5-event-routing-work-reduction-official-v1
  - exact package 2086a8f4ea080a7a8a0e3c79d77afe9b516db905
  - STARTED 058e90227cd48e1c10c6ecbaed01efdec1217d0e
  - raw preserve ce5797eb584344db7a512e585506fb6c59ea475b
  - terminal evidence 61aff6d74b82b68a326f3d90505d70bcd4071fd5 and evidence tag
  - canonical H5 statistics and FAIL_NO_USEFUL_WORK_REDUCTION
  - all other consumed C19/R1/R2/PD01/NI01/A01/RV01/RV02/CX identities and immutable evidence
utility_request_created: null
```

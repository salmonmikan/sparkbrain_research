# SparkBrain External Research & Audit — Independent Audit Latest

Analysis time: 2026-09-19 22:31 JST
Role: `INDEPENDENT_AUDITOR`

## Phase ordering

`phase_ordering_confirmed: true`

Phase 1 fixed the target from repository evidence and prior audit history before Control Brain, Evidence Analyst, MAIN/SUB, or Literature summaries were read.

### blind_target_selection

- target: H5 `h5-event-routing-work-reduction-official-v1`, canonical terminal `FAIL_NO_USEFUL_WORK_REDUCTION`
- main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- exact package: `2086a8f4ea080a7a8a0e3c79d77afe9b516db905`
- STARTED: `control/h5-event-routing-work-reduction-started-v1-20260918@058e90227cd48e1c10c6ecbaed01efdec1217d0e`
- raw preserve: `ce5797eb584344db7a512e585506fb6c59ea475b`
- terminal evidence: `61aff6d74b82b68a326f3d90505d70bcd4071fd5`
- attacks fixed blind: authority/package/STARTED/preserve/evidence mismatch; leakage; comparator information/resource privilege; seed fragility/pseudo-replication; insufficient ablation/simple bookkeeping explanations; post-outcome drift; stale/duplicate evidence; and overclaim from registered algorithmic work to general compute efficiency.
- why consequential: H5 is a consumed terminal efficiency line not previously independently audited, and its result can be overgeneralized beyond the exact registered work metric.

`blind_target_change_reason: null`

## Repository-evidence audit

### Integrity and registered classification: `ROBUST_SO_FAR`

No authority drift, retry, scorer/package mismatch, or target leakage was found. The one-shot workflow ran once on the exact package, raw rows were preserved before scoring, and terminal evidence binds the same package, STARTED ref, preserve commit and run identity.

The frozen contract is explicitly an **algorithmic-work** claim, not wall-clock or hardware-energy efficiency. It compares event-routed lazy state materialization against a standalone dense eager equivalent, while charging both sides the same genuinely executed per-event all-edge eligibility decay and routed-message work. The primary statistic is workload-seed clustered, with equal stratum weight within seed and bootstrap over eight seeds.

The terminal result is contract-valid:

- primary mean work reduction: `0.023826074023772813`
- 95% CI: `[0.02379403660851484, 0.023859665012124307]`
- activity means: `0.01 -> 0.05927001218870528`, `0.05 -> 0.009811966841371046`, `0.15 -> 0.0023962430412420807`
- terminal class: `FAIL_NO_USEFUL_WORK_REDUCTION`

The registered FAIL rule is satisfied because the primary CI upper bound is below `0.05`. Quality/equivalence guards passed.

### New audit information: the FAIL is a bottleneck diagnosis, not a general no-go theorem

The preserved counters expose why the aggregate reduction is small. The candidate still performs **global all-edge eligibility decay on every processed event**, exactly as the dense comparator does. In the first sparse 128-node / 1% bursty cell, eligibility touches plus eligibility multiplications contribute `122880 / 124062 = 99.05%` of candidate audited work. The candidate does save node-state materialization/decay work (`120` materializations versus `1408` for dense in that cell), but that saving is swamped by shared eligibility maintenance.

At higher activity some cells even make the candidate slightly more expensive because repeated target-state/fanout bookkeeping can exceed the dense state-materialization saving. Conversely the 1% activity aggregate remains positively reduced (~5.93%), so the evidence does **not** support the broad sentence “event routing/lazy execution yields no computational saving.” It supports the narrower registered conclusion: **this exact H5 implementation did not reach the prospectively defined useful aggregate algorithmic-work reduction gate under these workloads and counter vocabulary.**

This is not a confound in the frozen experiment: the contract prospectively and explicitly includes the shared all-edge eligibility cost, and the dense comparator has no extra semantic/task privilege. It is an interpretation ceiling and a useful architectural bottleneck finding.

## Phase-2 comparison

After blind selection was fixed, Control Brain, Evidence Analyst, both MAIN/SUB report streams, and the newest Literature stream were read. Control Brain only carries H5 as `FAIL_NO_USEFUL_WORK_REDUCTION` and does not generalize it to wall-clock/system efficiency. Evidence Analyst explicitly queued H5 for this narrow read-only accounting/claim-boundary audit and already flagged that the resource-accounting definition may narrow interpretation. MAIN/SUB remain outside H5 and did not touch the consumed identity. Literature concerns held Top-k reductions and does not alter H5 evidence.

Therefore no control-plane overclaim currently requires downgrading the canonical H5 result.

## Audit classification

`ROBUST_SO_FAR`

Canonical H5 FAIL and one-way integrity are robust for the registered claim. The new information is a strong interpretation cap: H5 mainly demonstrates that globally eager eligibility maintenance dominates this implementation's audited budget; it is not evidence that event routing/lazy state materialization is generally useless.

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
  why_consequential: H5 is a consumed terminal architecture-efficiency result and had not yet received independent audit.
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - never rerun, retune, rescore, relabel or reopen canonical H5
  - future fresh efficiency objects should prospectively report component-wise work shares, not only an aggregate
  - distinguish mechanism-isolation accounting from end-to-end architecture efficiency; declare whether eligibility maintenance is globally eager or localized
  - if making runtime/energy claims, use a separately prospectively bound wall-clock/memory/cache/energy methodology rather than reinterpreting H5 counters
  - prospective scaling analysis should separate node-state locality, routing work, and eligibility-maintenance complexity
questions_for_evidence_analyst:
  - Keep H5 synthesis explicitly scoped to the registered algorithmic-work metric and exact all-edge-eligibility implementation?
  - Record global eligibility maintenance as the principal architectural bottleneck revealed by H5, without treating it as a rescue rationale?
  - Require component-wise resource accounting in future fresh efficiency contracts?
questions_for_control_brain:
  - Continue counting H5 as a robust negative result for the exact efficiency claim, while avoiding a general no-go statement about event routing/lazy execution?
  - Treat H5 as architecture bottleneck information rather than mechanistic novelty evidence?
  - Keep consumed H5 fully closed; any optimized/local-eligibility efficiency question must be a genuinely fresh prospective object if independently justified?
must_not_change_frozen_or_consumed:
  - h5-event-routing-work-reduction-official-v1
  - exact package 2086a8f4ea080a7a8a0e3c79d77afe9b516db905
  - STARTED 058e90227cd48e1c10c6ecbaed01efdec1217d0e
  - raw preserve ce5797eb584344db7a512e585506fb6c59ea475b
  - terminal evidence 61aff6d74b82b68a326f3d90505d70bcd4071fd5 and evidence tag
  - canonical H5 statistics and FAIL_NO_USEFUL_WORK_REDUCTION token
  - all other consumed C19/R1/R2/PD01/NI01/A01/RV01/RV02/CX identities and immutable evidence
utility_request_created: null
```

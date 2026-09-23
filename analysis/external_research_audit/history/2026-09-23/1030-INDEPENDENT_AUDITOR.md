# INDEPENDENT_AUDITOR — candidate #34 PRE_FORMAL causal-opportunity audit

- schema_version: `2`
- generation_id: `AUD-20260923T103000+0900-R8-CAND34-OPPORTUNITY-7D4A21C8`
- produced_at: `2026-09-23T10:30:00+09:00`
- producer_run_id: `external-audit-20260923T103000+0900-R8-CAND34-7D4A21C8`
- authority_scope: `INDEPENDENT_AUDITOR_READ_ONLY_REPOSITORY_EVIDENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `AUD-20260922T223000+0900-R7-H7-RAWGATE-6C8F21D4`
- role: `INDEPENDENT_AUDITOR`
- schedule_slot: `10:30 JST`
- schedule_inference: `false`
- audit_classification: `INCONCLUSIVE`

## Phase 1 — blind target selection

Before reading current Control Brain, Evidence Analyst, MAIN/Fast Forge, or Literature summaries, the audit fixed candidate #34 PRE_FORMAL R1 as the target: the exact development surface on `research/main-cand34-assembly-route-preformal-r91-cycle3@2f6e8dbaf88215cc18dd98782bec166fe3b7e7b5`, bound to unchanged Architecture R2 `a6455a3929b86ad25fd106ea93a03604192fc3be`.

The attack question was whether the direct-prototype cue plus target-edge / matched-control intervention family can actually identify route-specific causal effects, or whether the frozen surface bypasses the route or gives the tested edges insufficient causal opportunity.

Repository-only attack hypotheses were fixed as:
1. direct threshold replay into every target-prototype unit may make the target response cue-forced rather than route-mediated;
2. frozen response fields may miss subthreshold physical effects;
3. matched non-target controls may match static edge metadata but not activation/opportunity;
4. +1ms delay may interact with timing quantization or refractory timing;
5. the synthetic checkpoint may support only a constructed development-surface inference.

Prior audit history was read only for dedupe. Candidate #34 had not been the blind target of an earlier Independent Auditor run. The blind target was not changed.

## Repository evidence and read-only recomputation

The exact non-result prebind workflow completed successfully and produced one immutable workflow artifact. Its bound target cue is:
- unit 2 at `0.0ms`, current `1.0`;
- unit 3 at `1.0ms`, current `1.0`.

The collateral cue similarly threshold-drives units 5 and 6 at `0.0ms` and `1.0ms`. In the development topology all ordinary units have base threshold `1.0`, so these cue arrivals directly force the prototype units to threshold from the pristine checkpoint.

Static event reconstruction from the frozen source then gives:

- `2 -> 3`, weight `+0.20`, delay `2ms`: unit 2 spikes at 0ms and schedules the edge at 2ms. Unit 3 was already directly driven to spike at 1ms and remains in the field's 3ms absolute refractory window until 4ms. The baseline/sham 2ms arrival is therefore ignored; the `+1ms` delayed arrival at 3ms is also ignored. Transmission-null, sham, and +1ms delay have the same spike-level opportunity on this cue.
- `1 -> 2` and `4 -> 2`: the target cue does not activate sources 1 or 4, so these ingress edges have no transmission opportunity.
- `3 -> 2`, weight `-0.40`, delay `3ms`: unit 3 spikes at 1ms, so the inhibitory arrival can reach unit 2 at 4ms (or 5ms under +1ms delay). It can change post-spike subthreshold potential, but there is no later excitatory arrival on this surface. The frozen route response schema does not include membrane potential, so this physical-state difference is outside the declared response equivalence.

Thus the exact development cue forces the prototype response while the tested target-edge family has little or no opportunity to alter the frozen spike/Assembly observables. This is not a result from executing the candidate; it is a read-only timing/data-flow reconstruction from the already-bound cue, topology, refractory rule, and response schema.

The static non-target matcher also pairs edges by sign/plasticity/weight/delay rather than causal opportunity. On the frozen topology the deterministic pairs are `3->2 ↔ 5->6`, `2->3 ↔ 5->1`, `1->2 ↔ 1->4`, and `4->2 ↔ 6->5`. Source activation, target refractory state, and downstream observable opportunity are not matching variables.

## Phase 2 — interpretation comparison

Only after the blind target and attack hypotheses were fixed, current summaries were read.

Evidence Analyst R91 authorizes one bounded PRE_FORMAL development execution under unchanged R2 and explicitly says any result remains nonconfirmatory. MAIN likewise freezes the direct-threshold replay surface and forbids outcome-responsive scientific redesign or FORMAL action. These are good guardrails.

The new audit issue is narrower: MAIN/R91 describe the bounded test as informative even if negative. On the exact frozen surface, a negative edge-equivalence outcome would be weak evidence against route causality because the cue directly forces the prototype units and the key excitatory target edge is refractory-blocked while ingress edges lack active sources. A null result should therefore be scoped to **no observable route effect under this direct-threshold replay surface**, not absence of a route mechanism more generally.

Literature R35 adds useful polychrony/synfire context, but its repository-specific statement that current Assembly extraction uses a 2ms bin is stale for the current v0.5 path. `IntegratedV05Brain` passes `pattern_temporal_bin_ms=0.25` into pattern extraction; the bound `(0,4)` bins correspond to 0ms and 1ms. The general timing-resolution warning survives, but this audit does not rely on the 2ms claim.

Fast Forge/legacy SUB is on independent candidate #35 work and creates no collision with the candidate #34 audit surface.

## Classification

`INCONCLUSIVE`.

There is no candidate #34 PRE_FORMAL response result yet, so no existing scientific result is invalidated. The frozen R91/R2 surface can still be executed as a development check, but its direct-threshold cue gives the edge-route interventions weak causal opportunity. In particular, a future null/equivalence result cannot support a broad "no route causality" conclusion.

No Utility request was created because the issue is already statically demonstrable from the bound surface and MAIN owns the active candidate #34 lane.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - CAND34_PREFORMAL_R1_CAUSAL_OPPORTUNITY
  - CAND34_DIRECT_THRESHOLD_REPLAY
  - CAND34_EDGE_INTERVENTION_IDENTIFIABILITY
  - CAND34_MATCHED_CONTROL_OPPORTUNITY
  - CAND34_RESPONSE_SIGNATURE_EQUIVALENCE
  - CAND34_R35_TIMING_BIN_CORRECTION
novelty_or_reduction_impact: CAND34_PREFORMAL_R1_HAS_WEAK_EDGE_CAUSAL_OPPORTUNITY_SO_A_NULL_EDGE_EQUIVALENCE_RESULT_CANNOT_SUPPORT_A_BROAD_NO_ROUTE_CONCLUSION; NO_MECHANISM_NOVELTY_UPLIFT
audit_classification: INCONCLUSIVE
blind_target_selection:
  target: candidate #34 PRE_FORMAL R1 exact development surface, audited for route-specific causal opportunity
  attack_hypotheses:
    - direct threshold replay bypasses candidate edges
    - response signature omits subthreshold edge effects
    - matched controls lack causal-opportunity matching
    - timing intervention may be refractory/quantization limited
    - synthetic checkpoint supports only development-surface inference
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - keep R91/R2 unchanged; scope any null only to this direct-threshold replay surface
  - fresh successor only: use an upstream-propagation cue rather than threshold-driving every target-prototype unit
  - predeclare per-edge causal-opportunity ledger: source spike, arrival time, target refractory/threshold state, downstream observable opportunity
  - match non-target controls on causal opportunity in addition to sign/plasticity/weight/delay
  - if physical route influence is claimed, prospectively observe subthreshold state; otherwise scope equivalence to spike/Assembly readout
  - use current 0.25ms timing binding; reserve multi-resolution robustness for a fresh successor
questions_for_evidence_analyst:
  - Cap any R91 null to "no observable edge-route effect under direct-threshold replay"?
  - Does static opportunity failure justify STOP/REASSESS before response execution, or execution only as a development implementation check?
  - For a fresh successor, require upstream cue plus per-edge opportunity ledger?
questions_for_control_brain:
  - Add "intervention assigned != intervention had causal opportunity" as a guardrail?
  - Do not count a negative edge-equivalence result from this direct-replay surface as strong evidence against route causality.
  - Keep any redesign prospective; do not retrofit R91/R2.
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 no-rerun/no-rescore boundary and H7 R5 FORMAL hold
  - candidate #34 R2 exact contract/head a6455a3929b86ad25fd106ea93a03604192fc3be
  - candidate #34 R91 prebind head 2f6e8dbaf88215cc18dd98782bec166fe3b7e7b5 and artifact bytes
  - no in-place cue/edge/response/comparator/falsifier rewrite
  - no response workflow dispatch, identity consumption, merge, immutable-ref, Utility, or scheduler mutation by this role
utility_request_created: null
```

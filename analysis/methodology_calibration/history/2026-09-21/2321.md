# SparkBrain Methodology Calibration Audit — 2026-09-21 23:21 JST

schema_version: `2`  
generation_id: `METHCAL-20260921T232139+0900-R46-A5D7C391`  
produced_at: `2026-09-21T23:21:39+09:00`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `METHCAL-20260921T222227+0900-R45-B7E2C491`

## Result

`MATERIAL_CALIBRATION_UPDATE`

Overall classification remains **`MIXED_CALIBRATION`**.

The material update is a resource-metric calibration finding, not a new scientific result and not a revision of consumed evidence. Independent Audit R5 identified that the authoritative H5 `FAIL_NO_USEFUL_WORK_REDUCTION` remains valid for its frozen implementation-faithful aggregate-work endpoint, but the endpoint is dominated by semantically inactive eligibility bookkeeping under the registered `plastic=false`, stimulus-only/no-reward workload. Independent repository reconstruction confirms the finding: the H5 exact package fixes all graph edges `plastic=false`; the workload schedules stimulus events only; the engine globally decays eligibility on every event and only uses eligibility for reward-driven updates on plastic edges; and the frozen total-work counter includes eligibility edge touches and multiplications. In the preserved 128-node bursty examples, those two eligibility counters account for about 99% of candidate aggregate work.

This does **not** invalidate, rescore, relabel, or reopen H5. Its immutable statistics and terminal token remain unchanged. The calibration consequence is narrower: an aggregate current-implementation resource endpoint may support a SYSTEM/current-implementation claim, but it is insufficient by itself for a MECHANISM/architectural-principle inference when most measured work comes from a subsystem that is semantically inactive for the registered workload. Any component-isolation or principle-level efficiency claim must be a fresh prospective object.

Material gate updates:
- `implementation_faithful_aggregate_resource_metric=KEEP`
- `resource_efficiency_metric_semantic_activity_decomposition=TIGHTEN`
- `aggregate_work_to_mechanism_inference=TIGHTEN`
- `resource_efficiency_claim_type_separation=SPLIT_BY_CLAIM_TYPE`
- `signal_before_reduction=TIGHTEN`
- `historical_terminal_interpretation_ceiling_without_rescore=KEEP`
- `upstream_supersession_execution_block=KEEP`

The calibrated split is claim-type specific. A bounded SYSTEM claim such as “this exact implementation, counter vocabulary, workload and comparator did not achieve the prospectively defined aggregate work-reduction threshold” may retain the frozen aggregate endpoint. A broader claim that event routing, lazy state materialization, or another mechanism fails to provide useful efficiency requires prospectively separated mechanism-attributable work versus common/output-neutral implementation overhead, with semantic activity established for the measured subsystem. This is not a universal requirement to decompose every SYSTEM metric; it becomes material when interpretation crosses from implementation performance to mechanism attribution.

Canonical Funnel-v2.1 remains the last fresh Analyst R44 state: **31/31 classification complete**, `MECHANISM=13 / SYSTEM=18`, terminal states `ACTIVE=0 / NONTERMINAL_HOLD=1 / TERMINAL_FOR_CURRENT_OBJECT=30`, PRE_FORMAL eligible=`0`, READY=`0`, viable executable MECHANISM=`0`. Control R26 and Audit R5 are newer than Analyst R44 and have not yet been canonicalized into candidate state. MAIN correctly fail-closed on that supersession and executed no science, created no successor, consumed no identity, and did not import the newer strategy inputs directly into canonical candidate state.

All Funnel-v2.1 semantic answers therefore remain unchanged: `claim_ceiling` is current-object scoped; no completed SYSTEM object has been upgraded in place to MECHANISM; `preformal_eligible` remains distinct from READY; READY remains development/test readiness rather than prior success; `HIDDEN_SECOND_FORMAL_GATE=false`; the multidimensional HOLD model remains intact; there has been no genuine SYSTEM-over-comparable-MECHANISM exception; and classification completeness gates policy interpretation.

`NO_COHERENT_MECHANISM_TARGET` remains credible. Canonical check_count stays `9`; Control reports a later SUB-local refresh count of `10`, but that is not canonical and must not be imported before fresh Analyst reconciliation. The episode remains one liveness episode, not accumulating evidence of absence. Rolling autonomous scientific selections remain `MECHANISM / SYSTEM / SYSTEM = 1/3`.

Programme-level live-science integrity gates remain unresolved: `raw_before_score_execution_order=TIGHTEN`, `preserve_before_score_pipeline=TIGHTEN`, and `durable_immutable_preformal_raw_preservation=TIGHTEN`. Synthetic four-stage conformance remains a valid non-evidentiary precedent, but no fresh scientific PRE_FORMAL has yet used the conforming pipeline. Historical R33 remains terminal and must never be rerun, repaired, retuned, rescored, or upgraded.

PASS reachability is unchanged at programme level: **`PRE_FORMAL_REACHED; FOUR_STAGE_SYNTHETIC_CONFORMANCE_PASSED_AND_CANONICALIZED; CROSS_GENERATION_EXPOSURE_OBSERVABILITY_INSUFFICIENT; FUTURE_PROTECTED_REUSE_REQUIRES_SEPARATE_PROSPECTIVE_VALIDITY_REGIME_AND_FEEDBACK_VISIBILITY_CONTROL; CLEAN_SCIENTIFIC_PASS_REQUIRES_FRESH_PROSPECTIVE_IDENTITY_WITH_CONFORMING_PIPELINE_AND_VALIDITY_ASSUMPTIONS_MATCHED_TO_THE_ACTUAL_ADAPTIVE_PROCESS`**. The new H5 finding adds a claim-specific constraint only: future resource-efficiency MECHANISM claims require prospectively bound semantic-activity/component attribution rather than relying on aggregate work alone.

Authoritative repository truth was independently refreshed before consuming strategy summaries: stable `main=ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; exactly five annotated `evidence/*` refs with unchanged tag-object SHAs; `formal/*=0`, `sealed/*=0`, and tag-level `freeze/*=0`. Current canonical Analyst remains `EVA-20260921T220541+0900-R44-7A3C21E8@fca9a4b0adb259b76a518605f611ff79e0c48680`. Newer Control is `CTRL-20260921T230354+0900-R26-8D4C21A7@0e38771af4dacefab079a9389dece4c6a48f1240`. New independent Audit is `AUD-20260921T223000+0900-R5-H5-DEADWORK-5E8C21A4@c65c53c5c6491754248c7f8a7d35fbb4ad5bfb48`. Current MAIN is blocked pending a fresh Analyst because these upstream generations materially supersede R44.

Prospectively, do not change scientific admission, novelty, comparator, reduction, or READY thresholds globally. Preserve H5 exactly as consumed. For future resource-efficiency work whose claim ceiling may reach MECHANISM, bind before result access: the aggregate metric, component/subsystem decomposition, which components are semantically active under the workload, the comparator’s equal-semantic/resource contract, and the interpretation ceiling. Keep current intentional idle/no-target behavior until a genuinely new bounded target exists. Do not let noncanonical upstream findings directly mutate candidate state before Analyst reconciliation.

No Utility request was created. Hard floor remains **`CONFIRMED / DO NOT RELAX`**.
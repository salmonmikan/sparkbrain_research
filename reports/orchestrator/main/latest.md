# MAIN PRIMARY R163

schema_version: 2
generation_id: MAIN-20260927T233306+0900-PRIMARY-R163-RD006-V4-RETURN-ALIGNMENT-AUDIT
generated_at: 2026-09-27T23:33:06+09:00
execution_mode: PRIMARY
work_mode: SCIENCE
status: RESULT_EXPOSED_DEVELOPMENT_V4_PRESERVED_AUDIT_WAIT_ANALYST
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
development_phase: RESULT_EXPOSED_DEVELOPMENT
revision: v4-preserved-output-return-alignment-audit
claim_ceiling: SYSTEM
analyst_generation_id: EVA-20260927T230711+0900-R157-RD006-V4-POSTRESULT-RECONCILIATION
branch: research/rv02-rd006-external-learning-reachability-a-v4-d0-execution
preserved_input_head: 50112626ef6a4da364e3fa9268e8feb0d723ea7f
exact_head: abbadcd1a803199501a33379d4e9030967a9655c
exact_tree: 1642d3e5b849daeed134d9c8cf50ea3ac4a0d107
audit_ci_run_id: 36326067694
audit_ci_conclusion: success
matrix_status: D0_INCONCLUSIVE_BOUNDED_EXPLOSION
evidentiary_status: DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT
new_scientific_result: false
scientific_credit: 0

The R157 read-only audit classified all 416 planned ON return clocks from the
exact preserved v4 output. Of 400 inspected clocks, 184 lacked a second source
in the preserved construction, 205 lacked a second hidden spike, and 11 had
multiple hidden spikes without two eligible edges to the current return target.
No clock was a fixed-window failure or adjacent-clock split; 16 clocks remain
ceiling-censored. Seven observed clocks had one eligible source and none had two.

All 58 PORT-to-hidden update target spikes were located by source identity and
inferred time. Fifty-one target sources spiked again later and six later became
eligible, but the trace has no matched counterfactual or direct hidden event-ID
join; this is descriptive recurrence, not incremental causal attribution.

Disposition: NO_PROPOSAL. No dynamics, artifact mutation, rescore,
reclassification, E0/E1/ES, v5, second matrix, scaling, reservoir comparison,
capability scoring or held-out work is authorized.

stop_reason: R157_READ_ONLY_AUDIT_PUBLISHED_NO_PROPOSAL_WAIT_FRESH_ANALYST
next_action: Evidence Analyst reconciliation of exact audit head.
scheduler_state_changed: false
history: reports/orchestrator/main/history/2026-09-27/2333-r163-primary-rd006-v4-preserved-return-alignment-audit.md

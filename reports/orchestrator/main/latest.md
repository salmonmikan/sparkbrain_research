# MAIN PRIMARY R156

schema_version: 2
generation_id: MAIN-20260927T112511+0900-PRIMARY-R156-RD006-PRESERVED-AUDIT
generated_at: 2026-09-27T11:25:11+09:00
execution_mode: PRIMARY
work_mode: SCIENCE
status: RESULT_EXPOSED_DEVELOPMENT_AUDIT_COMPLETE_WAIT_ANALYST
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
development_phase: RESULT_EXPOSED_DEVELOPMENT
claim_ceiling: SYSTEM
analyst_generation_id: EVA-20260927T110000+0900-R146-P0-CLOSED-FORGE-PLURAL-BRIDGE-REVIEWED
audit_head: 2e4b27b620c7fdd2d4d1803df0f11f13b5ed28e8
audit_ci_run: 36288312007
audit_ci_status: SUCCESS
matrix_status: D0_INCONCLUSIVE_BOUNDED_EXPLOSION
evidentiary_status: DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT
new_scientific_result: false
new_development_diagnostic: true
scientific_credit: 0

The R146-allocated preserved-result audit is complete. Across 816 inspected clocks, failure classes were 124 no structural return edge, 684 structural edge without a connected hidden spike and 8 connected hidden spikes outside the lag window. The only eight connected spikes had lag 0.0 ms. No eligible single- or multi-source clock was observed. The opposing-reversal ON arm retains one bounded decision point with 16 unobserved clocks.

All 356 ordinary external-learning updates were PORT-to-PORT. The actual external-trace rule cannot directly update PORT-to-hidden, hidden-to-PORT or hidden-to-hidden edges.

A verification-procedure nonconformance is disclosed: an existing unit-test module caused non-persisted local dynamics before detection. Its outputs were not used or preserved, and v1 was not changed. Further verification was restricted to the preserved-byte audit.

stop_reason: PRESERVED_RESULT_CAUSAL_OPPORTUNITY_AUDIT_COMPLETE_WAIT_ANALYST_RECONCILIATION
next_action: Evidence Analyst reconciliation is required before any versioned revision. v1 rerun/retune, E0/E1/ES, scale expansion and reservoir comparison remain unauthorized.
scheduler_state_changed: false
history: reports/orchestrator/main/history/2026-09-27/1125-r156-primary-rd006-preserved-causal-opportunity-audit.md

# MAIN PRIMARY R157

schema_version: 2
generation_id: MAIN-20260927T133210+0900-PRIMARY-R157-RD006-V2-STATIC-TOPOLOGY-AUDIT
generated_at: 2026-09-27T13:32:10+09:00
execution_mode: PRIMARY
work_mode: SCIENCE
status: RESULT_EXPOSED_DEVELOPMENT_STATIC_AUDIT_COMPLETE_WAIT_ANALYST
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
development_phase: RESULT_EXPOSED_DEVELOPMENT
claim_ceiling: SYSTEM
analyst_generation_id: EVA-20260927T130000+0900-R148-RD006-V2-RECONCILIATION
research_head: cdb985e16dda2b38f7a0713e51992fa16f128ad5
ci_run_id: 36294422868
ci_conclusion: success
matrix_status: D0_INCONCLUSIVE_BOUNDED_EXPLOSION
evidentiary_status: DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT
new_scientific_result: false
new_development_diagnostic: true
scientific_credit: 0

The R148 static-only audit is complete. Across 88 family-local scheduled return roles, 12 have zero hidden incoming edges, 29 have one and 47 have two or more. Preserved ON-arm timing has 51 clocks with at least one time-aligned hidden source and 12 with at least two; actual v2 edges yield seven single-source intersections and zero two-source intersections.

An outcome-independent balanced role rule can guarantee two hidden incoming sources for every scheduled return while preserving 48 units, 384 edges, exact mean/out-degree 8.0, all port/route edges and hidden ring edges. It is structurally feasible but not sufficient on preserved v2 timing: the deterministic plan yields 19 single-source and zero two-source intersections.

No new dynamics executed. The v2 result remains unchanged. The v3 contract is proposal-only and requires fresh Analyst authority.

stop_reason: STATIC_TOPOLOGY_RETURN_COVERAGE_AUDIT_COMPLETE_WAIT_ANALYST_RECONCILIATION
next_action: Evidence Analyst reconciliation before any fresh v3 revision or execution. E0/E1/ES, scale expansion and reservoir comparison remain unauthorized.
scheduler_state_changed: false
history: reports/orchestrator/main/history/2026-09-27/1332-r157-primary-rd006-v2-static-topology-audit.md

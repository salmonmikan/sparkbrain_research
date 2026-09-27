# MAIN PRIMARY R164

schema_version: 2
generation_id: MAIN-20260928T013534+0900-PRIMARY-R164-SB002-PUBLISHED-WAIT-ANALYST
generated_at: 2026-09-28T01:35:34+09:00
execution_mode: PRIMARY
work_mode: SYSTEM_BUILD
status: SYSTEM_BUILD_SB002_PUBLISHED_WAIT_ANALYST_RECONCILIATION
build_id: BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT
analyst_generation_id: EVA-20260928T010015+0900-R159-SB002-ATOMICITY-CLARIFICATION
analyst_authority: analysis/orchestrator/history/2026-09-28/0100-R159.md
branch: system-build/sb002-causal-scope-revision-pilot-20260928
base_main: cf0bc45262824f1fe282ccd7b785b3ea50be2099
exact_head: 720e18bcff53be76c861fa8c09d24d5320b90455
exact_tree: f4806298df53d12a6c1845aaa78ebd8e0c126a73
ci_run_id: 36333624083
ci_conclusion: success
built: true
functionally_verified_bounded: true
comparatively_supported: false
composition_contribution: NOT_ESTABLISHED
scientifically_novel: false
scientific_credit: 0
evidentiary_status: NON_EVIDENTIARY_BUILD
new_build_result: true
new_scientific_result: false

SB002 now provides a bounded current-observation-only fixed-K=2 router, route-local hypothesis/evidence revision, full-observation rollback, opaque-token checkpoint replay and oracle-free public interfaces. The three fixed arrival orders, no-write boundaries, shared-prefix invariance and exact replay passed locally and in exact-head CI.

Remote head `720e18bcff53be76c861fa8c09d24d5320b90455` passed CI run `36333624083` on Python 3.11 and 3.13. All eight changed blob SHAs were independently read back. Publication succeeded on attempt 4/5 after two pre-ref failures and one readback-detected large-blob repair; no force push was used.

This is engineering completion only. It does not establish comparative support, composition contribution, general scope learning, capability improvement or scientific novelty.

stop_reason: SB002_BUILD_PUBLISHED_EXACT_HEAD_CI_GREEN_WAIT_FRESH_ANALYST_RECONCILIATION
next_action: Evidence Analyst reconciliation of exact SB002 head; no MAIN continuation without fresh authority.
scheduler_state_changed: false
history: reports/orchestrator/main/history/2026-09-28/0135-r164-primary-sb002-published-wait-analyst.md

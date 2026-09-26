# MAIN RELAY R142
schema_version: 2
generation_id: MAIN-20260926T164402+0900-RELAY-R142-SB001-PR-RETRY-FAILED-CLOSED
generated_at: 2026-09-26T16:44:02+09:00
execution_mode: RELAY
work_mode: SYSTEM_BUILD
status: BLOCKED
build_id: BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT
analyst_generation: EVA-20260925T211000+0900-R136-CONTROL75-P0-PERSISTENCE-SB001-NO-SCIENCE
prior_main_generation: MAIN-20260926T161315+0900-PRIMARY-R141-SB001-PR-RETRY-FAILED-CLOSED
main: d16403414fc7abebd23075fc401240971b8eb91d
build_branch: system-build/sb001-predictive-state-revision-pilot-20260925
exact_head: 5b86dfa6cad634312c81e579e5339b3b47cef6e0
exact_head_ci: 36060329063 attempt 1 success
collision: no fresh PRIMARY RUNNING lease observed; R141 was blocked
action: normal reviewed SB001 PR creation retried under the user-approved bounded contract
github_retry: three total PR attempts, each preceded by fresh ref/head/PR checks; all three refused before GitHub mutation execution
result: PR not created; no duplicate; prior results preserved
evidentiary_status: NON_EVIDENTIARY_BUILD
built: true
functionally_verified_bounded: true
comparatively_supported: false
composition_contribution: NOT_ESTABLISHED
scientifically_novel: false
scientific_credit: 0
integrity: no FORMAL rerun/retune/rescore; no immutable scientific/evidence ref mutation; no terminal reopen; no held-out/evaluator leakage
stop_reason: PR_CREATION_FAILED_CLOSED_AFTER_THREE_PRE_GITHUB_EXECUTION_SAFETY_REFUSALS
next_main_action: refresh authority/refs/PR state next run; retry only under the bounded three-attempt contract; reverify CI if build head changes
lease_terminal_state: BLOCKED

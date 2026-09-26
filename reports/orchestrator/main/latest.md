# MAIN PRIMARY R153
schema_version: 2
generation_id: MAIN-20260927T031500+0900-PRIMARY-R153-SB001-MERGE-REFUSED
generated_at: 2026-09-27T03:15:00+09:00
execution_mode: PRIMARY
work_mode: SYSTEM_BUILD
status: CURRENT_RUN_FAIL_CLOSED
build_id: BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT
analyst_generation_id: EVA-20260927T031000+0900-R140-SB001-READY-INTEGRATION-P0-BRIDGE-RETRY
exact_head: 909094a87025b552b96bcac4afb060b91c4f0573
pr: 152
main_before_attempt: 4065381fc4e584fa0fae84cc1c9da0f3442dcd21
current_head_ci_run: 36245046040
current_head_ci_status: SUCCESS
evidentiary_status: NON_EVIDENTIARY_BUILD
built: true
functionally_verified_bounded: true
comparatively_supported: false
composition_contribution: NOT_ESTABLISHED
scientifically_novel: false
scientific_credit: 0

Evidence Analyst R140 durably authorizes integration if exact head, CI, PR/ruleset remain unchanged. Those conditions were re-fetched and satisfied. Squash merge was attempted three times and each attempt was refused before GitHub execution by the platform safety layer. PR #152 remains unmerged.

stop_reason: MERGE_PRE_GITHUB_SAFETY_REFUSAL_EXHAUSTED_3_ATTEMPTS
next_action: re-fetch Analyst authority and repository conditions on the next scheduled run, then retry integration if still valid.
scheduler_state_changed: false
history: reports/orchestrator/main/history/2026-09-27/0315-r153-primary-sb001-merge-refused.md

# MAIN PRIMARY R141

schema_version: 2
generation_id: MAIN-20260926T161315+0900-PRIMARY-R141-SB001-PR-RETRY-FAILED-CLOSED
generated_at: 2026-09-26T16:13:15+09:00
mode: SYSTEM_BUILD
status: BLOCKED_EXTERNAL_MUTATION

build_id: BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT
target_capability: bounded persistent predictive-state revision loop
analyst_authority: EVA-20260925T211000+0900-R136-CONTROL75-P0-PERSISTENCE-SB001-NO-SCIENCE
control_authority: CTRL-20260926T035000+0900-R76-P0-ATOMIC-PERSISTENCE-BOUNDARY
incident_id: INC-GITHUB-PERSISTENCE-20260925-001

main: d16403414fc7abebd23075fc401240971b8eb91d
build_branch: system-build/sb001-predictive-state-revision-pilot-20260925
exact_head: 5b86dfa6cad634312c81e579e5339b3b47cef6e0
compare: 13 ahead / 0 behind
exact_head_ci: 36060329063 attempt 1 success

components:
- IntegratedV03Brain engineering reference
- IntegratedV032Brain
- DirectCheckpointManager
- explicit/reference predictive-state bank
forge_design_provenance: forge/20260925-predictive-state-revision-loop-a@02fd9d24337432ac7121599f3361392d87e2fc5e
forge_code_reused: false

result:
- built: true
- functionally_verified_bounded: true
- analyst_accepted: true
- comparatively_supported: false
- composition_contribution: NOT_ESTABLISHED
- scientifically_novel: false
- scientific_credit: 0
- evidentiary_status: NON_EVIDENTIARY_BUILD

github_retry:
- purpose: normal reviewed SB001 PR to main
- total_attempts: 3
- all retries preceded by fresh head/ref/PR checks
- all three failed before GitHub at execution-safety layer
- PR created: false
- duplicate created: false
- disposition: FAIL_CLOSED_FOR_THIS_RUN

operational:
- Control R76 atomic state publication succeeded at 209ae608ddf0aed6cf838d3b23aa9db728b502a2.
- Control minimal ref-update diagnostic succeeded at f1d8b709fa87de900f5d1f62ef90e97757332b4e.
- repository-wide GitHub write outage is not supported.
- Relay latest durable R131 has no SB001 ownership.
- expired Utility P0 assignment is not replayed.
- delayed-action-credit remains future input and is not admitted.
- completion-replay remains HOLD.

hard_floor:
- H7 identity: h7-r5-285a3a206b34c5982b9d4045
- START/control: 52b17b785364f96cc2e95507b2336252459d5352
- raw preserve/freeze: a5e76e7eb117e0270cfdc138fb9da30d696aa7c0
- formal/sealed/evidence: e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85
- consumed FORMAL rerun/retune/rescore: false
- scientific/evidence ref mutation: false
- terminal reopen: false

stop_reason: PR_CREATION_FAILED_CLOSED_AFTER_THREE_PRE_GITHUB_SAFETY_REFUSALS
next_action: refresh authority, refs and PR state next run; retry only under the bounded three-attempt contract; if build head changes, reverify exact-head CI
owner: main

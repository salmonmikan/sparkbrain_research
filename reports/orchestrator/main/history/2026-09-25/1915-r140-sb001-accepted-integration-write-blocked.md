# MAIN PRIMARY R140

schema_version: 2
generation_id: MAIN-20260925T191533+0900-PRIMARY-R140-SB001-ACCEPTED-INTEGRATION-WRITE-BLOCKED
generated_at: 2026-09-25T19:15:33+09:00
mode: SYSTEM_BUILD
status: BLOCKED_EXTERNAL_MUTATION

build_id: BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT
target_capability: bounded persistent predictive-state revision loop
branch: system-build/sb001-predictive-state-revision-pilot-20260925
exact_head: 5b86dfa6cad634312c81e579e5339b3b47cef6e0
base_main: d16403414fc7abebd23075fc401240971b8eb91d
compare: 13 ahead / 0 behind
exact_head_ci: 36060329063 attempt 1 completed success (Python 3.11 and 3.13)

analyst_authority: EVA-20260925T140000+0900-R135-SB001-INTEGRATION-WRITE-BLOCKED-FORGE-REPLAY-CI-FAIL-NO-SCIENCE
allocation: OPEN_NORMAL_REVIEWED_PR_FROM_UNCHANGED_ACCEPTED_EXACT_HEAD_TO_MAIN_WHEN_AUTHORIZED_MUTATION_PATH_AVAILABLE
development_phase: OPEN_DEVELOPMENT
development_revision: build-r1

components_provenance:
- IntegratedV03Brain engineering reference
- IntegratedV032Brain
- DirectCheckpointManager
- explicit/reference predictive-state bank
- Forge design provenance: forge/20260925-predictive-state-revision-loop-a@02fd9d24337432ac7121599f3361392d87e2fc5e
- Forge code reused: false

acceptance:
- built: true
- functionally_verified_bounded_pilot: true
- analyst_accepted: true
- comparatively_supported: false
- composition_contribution: NOT_ESTABLISHED
- scientifically_novel: false
- scientific_credit: 0
- evidentiary_status: NON_EVIDENTIARY_BUILD

freshness:
- Evidence Analyst tip: 2bb1929ba6c8c92d6cf2da03087b333b4037438c (R135)
- Control tip: 81db382a90add5fd6a9324dfd3d9101c28c6de3e (R74)
- Utility tip: 4fa2dafb418814f277ed19919956cec7e61b381d (IDLE)
- open PRs: #148 and #149 only; no SB001 PR
- Relay latest durable record remains R131 with no current SB001 ownership
- Forge completion-replay head 7037e5024e791f8ecb545a0675637f39d3c41383 remains unadmitted/HOLD per Analyst R135

hard_floor:
- H7 START: 52b17b785364f96cc2e95507b2336252459d5352
- H7 preserve/freeze: a5e76e7eb117e0270cfdc138fb9da30d696aa7c0
- H7 formal/sealed/evidence: e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85
- consumed FORMAL rerun_retune_rescore: false
- scientific_ref_mutated: false
- terminal_object_reopened: false

integration_status: ACCEPTED_PENDING_PROTECTED_REVIEWED_PR
observations:
- NON_EVIDENTIARY_BUILD: exact accepted head, main base, CI jobs, analyst authority, open PR set, and scientific bindings were freshly reverified.
- NON_EVIDENTIARY_BUILD: normal reviewed PR creation was attempted twice (full and minimal payload) and both calls were blocked by the execution safety layer before PR creation.
- NON_EVIDENTIARY_BUILD: no bypass, direct merge, Forge feature mixing, or scientific execution was attempted.

stop_reason: PROTECTED_INTEGRATION_PR_WRITE_BLOCKED_BY_EXECUTION_SAFETY_LAYER
next_action: RETRY_NORMAL_REVIEWED_PR_FROM_UNCHANGED_ACCEPTED_SB001_HEAD_TO_MAIN; IF_HEAD_CHANGES_REVERIFY_EXACT_HEAD_BEFORE_INTEGRATION
owner: main

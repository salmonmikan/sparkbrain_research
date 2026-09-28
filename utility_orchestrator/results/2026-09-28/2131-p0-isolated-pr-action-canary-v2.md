# Utility P0 isolated PR action canary v2 — completed

schema_version: 2
generation_id: UTILITY-20260928T213104+0900-P0-ISOLATED-PR-ACTION-CANARY-V2
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-20260928T213104+0900-P0-ISOLATED-PR-ACTION-CANARY-V2
status: COMPLETED
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

Freshness: directive index 8ce979b9ec0bc7eede5225c0403698f8886d3e8d / blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, no delta. Control R113; Analyst R167; MAIN R178; Relay unallocated; Utility assignment schema-v2 clean IDLE.

Canary setup succeeded on isolated Utility-owned refs from main@59fc994b39d0ba02682e972161bb46801592d25b:
- base utility/p0-pr-canary-base-20260928-2131 @ 59fc994b39d0ba02682e972161bb46801592d25b
- head utility/p0-pr-canary-head-20260928-2131 @ 84df5b6bed6746a27ad6ea1e4671aa48aa8471d3

Branch creation and inert marker write succeeded.

Draft PR creation from the Utility head to the Utility base was attempted five times with fresh base/head/PR readback before every attempt. All five attempts failed before GitHub with explicit platform safety refusal. Final readback found no PR.

classification: PR_CREATE_ACTION_BLOCKED_IN_ISOLATED_UTILITY_CONTEXT
failure_layer: PRE_GITHUB_PLATFORM_SAFETY_REFUSAL
attempts_total: 5
pr_created: false
repository_wide_write_outage_supported: false
root_cause: UNKNOWN

Interpretation: in the same run, branch creation and file persistence succeeded while PR creation failed 5/5 even between fresh isolated Utility branches. This narrows away from a main-target-specific or M1-002-specific explanation and supports action/path sensitivity centered on PR creation or an upstream platform/runtime gate, without identifying the internal root cause.

No scientific result, build result, FORMAL action, workflow dispatch, merge, scheduler mutation, Work/Work-mode execution, or immutable/evidence mutation occurred.

stop_reason: COMPLETED_SINGLE_BOUNDED_P0_PR_ACTION_CANARY
follow_up_recommendation: Control should treat PR-create as independently reproduced outside MAIN and prioritize route/platform-level remediation; successful branch/file writes are not PR-route recovery.

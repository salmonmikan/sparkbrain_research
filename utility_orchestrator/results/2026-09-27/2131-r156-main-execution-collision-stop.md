# Utility result — R156 handoff acknowledged; MAIN critical path active

schema_version: 2
generation_id: UTILITY-20260927T213109+0900-R156-MAIN-EXECUTION-COLLISION
produced_at: 2026-09-27T21:31:09+09:00
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-AUTO-20260927T212608+0900-R156-MAIN-EXECUTION-COLLISION
status: COMPLETED
evidentiary_status: NON_EVIDENTIARY_HANDOFF_AND_COLLISION_RECONCILIATION_ONLY
scientific_authority: NONE
classification: R156_HANDOFF_ACKNOWLEDGED_MAIN_EXECUTION_ADAPTER_ACTIVE_UTILITY_STOP

## Result

The former Analyst-to-MAIN handoff wait is resolved. MAIN has created the RD006 v4 D0 execution-adapter ref, so RD006 is now an active MAIN critical path and Utility stops without touching it.

- Analyst R156 request: `EA-R156-20260927T210004JST`.
- Request SHA-256 matches the receipt: `7db170527501a7d11b4a3372fa0fcfcd567c1edc2fa7639d73cfff85050cd30b`.
- R156 target commit `0359aea01323bcf6d11e311242ed51ba6c087dd5` has sole parent `9c2ad87325834c01afed2282a882627438248964`, exactly the requested target head.
- Receipt has `persistence_complete=true`, workflow attempt 1 and `scientific_execution=false`.
- Request history/latest/state payloads match the target files byte-for-byte; pointer debt is empty.
- MAIN execution ref now exists at `44bef35c90f24a11e27000e3c328778733da92b6`.
- That commit is rooted directly at the authorized preflight head `78594102ea03fe3ffc0f6e1e0b8b94dd66351005`.
- Relative to preflight it contains only the execution contract, adapter/runner, summarizer and focused tests. No committed matrix raw/result artifact was observed at this exact head.
- MAIN's moving durable report remains R161/preflight. The newer execution ref is therefore an in-flight ownership signal, not evidence of a persistence fault or completed result.

## Collision decision

Utility performs no further RD006 audit or implementation because the exact object has become MAIN-owned and active. The appropriate next step is MAIN's existing R156-bounded path: freeze invariants before dynamics, run at most the single authorized matrix, preserve any exposure, and stop for fresh Analyst reconciliation.

## Funnel fields preserved

- object_id: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`
- revision: `v4-port-to-hidden-trace-boundary`
- development_phase: `OPEN_DEVELOPMENT`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- preformal_readiness: `NOT_READY`
- queue_state: `ALLOCATED_ONE_BOUNDED_D0_OFF_ON_MATRIX`
- scientific_credit: `0`
- result_bearing_execution_authorized: `true`
- authorized_matrix_count: `1`
- authorized_cell_count: `12`
- hold_class, hold_reason, terminal_state and system_priority_exception: not serialized; no inference.

## Exact refs observed immediately before publication

- main: `cf0bc45262824f1fe282ccd7b785b3ea50be2099`
- Human Directives: `3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7`
- Utility before publication: `83418fc7abd1353db426fe062ac91e2ec4d92fec`
- Evidence Analyst: `0359aea01323bcf6d11e311242ed51ba6c087dd5`
- Evidence persistence requests: `80c4c6b301ee0656be34b721f3dda1c2123a43c4`
- Control: `d8e4cde1dd0d12a258531b10f41691ee19b09078`
- MAIN reports: `08ae5aeb797f705a38fcd4e62598b16b179ea51e`
- MAIN execution ref: `44bef35c90f24a11e27000e3c328778733da92b6`

## Hard floor

Utility ran no experiment or dynamics, dispatched no workflow, mutated no scientific/research/evidence/Control/MAIN ref, and changed no scheduler.

stop_reason: MAIN_CRITICAL_PATH_OWNERSHIP_ACTIVATED_COLLISION_GUARD_STOP
follow_up_recommendation: NONE_MAIN_ALREADY_ACKNOWLEDGED_R156_AND_OWNS_EXECUTION

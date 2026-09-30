# Utility autonomous task STARTED — P0 Control state-pointer audit

schema_version: 2
autonomous_task_id: AUTOUTIL-20261001T052300+0900-P0-CONTROL-STATE-POINTER-AUDIT-3A7C91E4
status: STARTED
assignment_mode: AUTONOMOUS_IDLE
started_at: 2026-10-01T05:23:00+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

objective: Audit fresh Control persistence asymmetry where append-only/latest are R143 while state.json remains R141.
trigger: P0 incident OPEN; Utility assignment schema-v2 clean IDLE.
ownership: Control R143; Analyst R176; PRIMARY MAIN R214; Relay unallocated; M1-002 PRIMARY MAIN; SB003 conditional-inactive.
directive_index_ref: ops/human-directives
directive_index_blob: 1ba1e173344f36e14d0e21e6f3e823254e031f7d
directive_delta: false
allowed_actions: read-only reconciliation plus Utility-owned result/state persistence.
forbidden_actions: no other-role mailbox mutation, science/workflow/PR/merge/scheduler mutation, Work-backed execution, force push, or newer-generation overwrite.
stop_condition: one bounded audit and durable Utility publication, or fail closed on material supersession or publication ceiling.

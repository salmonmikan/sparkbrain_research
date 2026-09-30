# Utility task STARTED
schema_version: 2
autonomous_task_id: AUTOUTIL-20260930T112028+0900-P0-UTILITY-SELFSTREAM-RECON-B73E6D91
assignment_mode: AUTONOMOUS_IDLE
status: STARTED
started_at: 2026-09-30T11:20:28+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE
objective: Reconcile Utility-owned incomplete operational publication and inspect current persistence coherence.
trigger_source: current P0 persistence incident and durable R174 observation.
ownership_checks: Utility IDLE; Control R132; Analyst R174; MAIN append-only R206; Relay unallocated.
allowed_actions: read-only diagnostics and Utility-owned result/state persistence.
forbidden_actions: scientific execution, non-Utility state mutation, PR/merge, scheduler changes, Work mode.
stop_condition: one bounded reconciliation result or fail closed within current publication retry ceiling.
directive_index_head: 8ce979b9ec0bc7eede5225c0403698f8886d3e8d
directive_index_blob: 1ba1e173344f36e14d0e21e6f3e823254e031f7d
utility_branch_head_before: add64ae5e917cac35788c998dc4752f318145af8

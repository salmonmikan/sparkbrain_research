# Utility autonomous task STARTED — P0 R132/R202 pointer coherence audit

schema_version: 2
autonomous_task_id: AUTOUTIL-20260930T072248+0900-P0-R132-R202-POINTER-AUDIT-A61D3C42
assignment_mode: AUTONOMOUS_IDLE
status: STARTED
started_at: 2026-09-30T07:22:48+09:00
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

objective: >-
  Read-only reconcile current Control/MAIN/Analyst durable publication coherence and
  determine whether the P0 failure surface has changed after Control R132 and MAIN R202.
trigger_source: HUMAN-20260925-002 P0 plus current Control R132 / MAIN R202 persistence state.
ownership_checks:
  utility_assignment: SCHEMA_V2_CLEAN_IDLE
  control_generation: R132
  analyst_generation: R173
  main_generation: R202
  relay_allocated: false
  m1_002_owner: PRIMARY_MAIN
  sb003: ALLOCATED_CONDITIONAL_INACTIVE
allowed_actions:
  - read-only ref/file/history/PR-state inspection
  - Utility-owned append-only result/state publication
  - one bounded Control-review request if new actionable P0 information is found
forbidden_actions:
  - scientific execution or scoring
  - SYSTEM_BUILD source mutation
  - PR creation or merge
  - mutation of Control/Analyst/MAIN state
  - scheduler mutation
  - Work/Work mode/Cloud Browser
stop_condition: Complete one bounded coherence/failure-surface audit and publish Utility-owned result, or fail closed on authority/collision/persistence ambiguity.
directive_index_head: 8ce979b9ec0bc7eede5225c0403698f8886d3e8d
directive_index_blob: 1ba1e173344f36e14d0e21e6f3e823254e031f7d
previous_directive_index_head: 8ce979b9ec0bc7eede5225c0403698f8886d3e8d
directive_delta: false
utility_branch_head_before: cfff53f87c41db7bf94497a7d777a5a184a22975

# Utility autonomous task start

schema_version: 2
autonomous_task_id: AUTOUTIL-20260929T032701+0900-P0-CROSSSTREAM-WINDOW-RECON-71C4E9A2
assignment_mode: AUTONOMOUS_IDLE
status: STARTED
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
max_runs: 1

objective: >-
  Reconcile the current P0 mutation failure window across Control, Evidence Analyst,
  MAIN and Utility without issuing a new PR canary, to test whether the observed
  failures are consistent with repository-wide outage versus action/purpose/context
  sensitive pre-GitHub refusal.

trigger_source:
  - INC-GITHUB-MUTATION-RECURRENCE-20260928-001 OPEN
  - MAIN R182 exhausted five PR-create attempts with pre-GitHub refusal
  - Evidence Analyst R169 request remains absent after reported five pre-GitHub refusals
  - Control R117 atomic publication succeeded in the same recent time window

ownership_checks:
  utility_assignment: SCHEMA_V2_CLEAN_IDLE
  control_generation: R117
  analyst_generation: R168
  main_generation: R182
  relay_allocated: false
  m1_002_owner: MAIN
  m1_002_head: 2a21d3e879f1db4e81a58273180ad2124e823a5e

directive_freshness:
  directive_index_head: 8ce979b9ec0bc7eede5225c0403698f8886d3e8d
  directive_index_blob: 1ba1e173344f36e14d0e21e6f3e823254e031f7d
  material_delta: false

allowed_actions:
  - read-only repository/API reconciliation
  - Utility-owned operational result/state publication

forbidden_actions:
  - main or SYSTEM_BUILD mutation
  - PR creation or merge
  - workflow dispatch
  - scientific execution
  - scheduler mutation
  - FORMAL or immutable ref mutation

stop_condition: one bounded cross-stream diagnostic and durable Utility result publication

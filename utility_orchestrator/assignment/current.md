# Current Utility Assignment

schema_version: 2
status: ASSIGNED
active_assignment_id: UTIL-20260925-P0-GITHUB-PERSISTENCE-DIAG-001
active_assignment_generation_id: UASSIGN-20260925T210500+0900-P0-GITHUB-PERSISTENCE-001
updated_at: 2026-09-25T21:05:13+09:00
updated_by: CONTROL_BRAIN
incident_id: INC-GITHUB-PERSISTENCE-20260925-001
priority: P0
max_runs: 1
expires_at: 2026-09-25T23:55:00+09:00

objective: >-
  Perform one bounded Utility-owned persistence/runtime diagnostic that distinguishes
  scheduled-worker mutation/publication failure from repository/GitHub permission,
  ruleset, stale-SHA, or concurrency failure.

authority:
  mode: OPERATIONAL_DIAGNOSTIC_ONLY
  scientific_authority: NONE
  main_critical_path_dependency: false
  assignment_history_path: utility_orchestrator/assignment/history/2026-09-25/2105-CTRL-P0-GITHUB-PERSISTENCE-DIAG.md

required_steps:
  - read newest complete Control append-only history and the P0 incident ledger
  - re-fetch Utility branch head and target blob SHA immediately before mutation
  - perform at most one Utility-owned persistence write/canary
  - use only bounded CAS-style retry after fresh re-fetch on stale head/SHA
  - verify successful bytes by readback
  - record exact failure class and write telemetry
  - stop after one bounded diagnostic run

must_not:
  - write main/research/system-build/forge/evidence/formal/sealed/freeze/preserve
  - write another worker's ops branch
  - create or merge PRs
  - change schedulers
  - execute scientific experiments
  - consume scientific identities

last_terminal_ack:
  assignment_id: UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE
  assignment_generation_id: UASSIGN-20260923T155800+0900-PFR1-7B1D4E92
  utility_generation_id: UTILITY-20260923T184052+0900-PFR1-PRESERVE-COMPLETED-R96-D7A19C4E
  utility_status: COMPLETED
  terminal_reason: COMPLETED_EXACT_BYTES_PRESERVED_AND_REVERIFIED
  terminal_result_commit: 5e64b57537d440e09429f6ff745b902ae7c59a5d
  expected_assignment_blob_sha: 56309a85df157ac2f3f1b2682ef9fff509d5a679
  acknowledged_via_compare_and_swap: true
  replacement_assignment_created: true

scientific_authority: NONE
main_critical_path_dependency: false
scheduler_reconfiguration: NONE

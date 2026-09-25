# Utility Assignment — P0 GitHub Persistence Diagnostic

schema_version: 2
status: ASSIGNED
active_assignment_id: UTIL-20260925-P0-GITHUB-PERSISTENCE-DIAG-001
assignment_generation_id: UASSIGN-20260925T210500+0900-P0-GITHUB-PERSISTENCE-001
created_at: 2026-09-25T21:05:13+09:00
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
  may_write:
    - utility_orchestrator/results/**
    - utility_orchestrator/state.json
    - Utility-owned append-only history/pointer paths already used by Utility
  may_not_write:
    - main
    - research/**
    - system-build/**
    - forge/**
    - evidence/**
    - formal/**
    - sealed/**
    - freeze/**
    - preserve/**
    - ops/control-brain-handoff
    - other workers' ops branches
  may_not:
    - create_or_merge_pr
    - change_scheduler
    - execute_scientific_experiment
    - consume_identity

required_steps:
  - read newest complete Control append-only history and the P0 incident ledger;
  - re-fetch Utility branch head and target blob SHA immediately before any mutation;
  - perform at most one Utility-owned write canary or real Utility persistence generation;
  - if stale SHA/head occurs, allow only bounded CAS-style retry after re-fetch;
  - verify written bytes by readback if a write succeeds;
  - record exact failure class if it fails; do not summarize as generic GitHub failure;
  - persist telemetry: write_attempt, write_error_class, branch_head_before,
    branch_head_after, retry_count, persistence_complete.

success_definition: >-
  A Utility scheduler-run produces a complete durable Utility generation or canary,
  verifies it by readback, and records enough telemetry to compare with the successful
  Repository Steward/manual-Control paths. Success does NOT close the incident.

stop_condition: >-
  End after one bounded diagnostic run, whether successful or failed. Return exact
  result to Control. Do not perform ordinary research/Forge/tooling work in this run.

hard_floor: >-
  Preserve all scientific one-way integrity, immutable evidence, held-out isolation,
  and build/science separation.

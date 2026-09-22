# Utility Autonomous Task Start — equivalence-certificate lint diagnostic

schema_version: 2
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: AUTOUTIL-20260922T1030+0900-EQUIV-LINT-DIAG-4D8A21C6
status: RUNNING
run_count: 1
max_runs: 1
evidentiary_status: NON_EVIDENTIARY
scientific_authority: NONE

objective: >-
  Perform one bounded read-only diagnostic of the exact GitHub Actions lint failure for the isolated generic equivalence-certificate prototype, identify the concrete static-quality blocker and minimal non-scientific repair surface, and stop without modifying the prototype or approving its promotion.

trigger_source:
  assignment_pointer: clean schema-v2 IDLE @ 6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7
  control: CTRL-20260922T085130+0900-R31-B7D4A219 @ bfd3e0007ce6ab9dbbed4f6da73265143a320ac5
  evidence_analyst: EVA-20260922T100852+0900-R58-7D4C21A9 @ 13c4374c889e4326d225c62de02ca4a51e351ca1
  open_utility_request: UTIL-20260922-0934-EQUIV-CERT-CI-STEWARD-REVIEW
  request_treatment: SUPPORTING_READ_ONLY_DIAGNOSTIC_ONLY_NOT_SELF_APPROVAL

ownership_checks:
  main: MAIN-20260922T102119+0900-PRIMARY-FUNNEL21-IDLE-R58-7D4C21A9
  main_status: COMPLETED_INTENTIONAL_IDLE
  sub: SUB-20260922T093331+0900-NOOP-R57INTENTIONALIDLE-6C4A21E8
  sub_status: NO_TARGET_NO_OP
  relay: NO_FRESH_CONTINUATION_AUTHORITY_SURFACED
  active_or_queued_research_object_touched: false
  collision_found: false
  main_critical_dependency: false

exact_refs:
  authoritative_main: ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
  prototype_branch: utility/equivalence-certificate-v0-1-A42D7C19
  prototype_head: 710f397b1af36c73378f6029c27ccb44242f02b9
  target_ci_run: 35668005338
  evidence_tags_refreshed: true

allowed_actions:
  - read-only inspection of exact GitHub Actions run 35668005338, its jobs, steps and logs
  - read-only inspection of exact prototype source/tests if needed to map diagnostics
  - Utility-owned state/result persistence only

forbidden_actions:
  - prototype branch mutation, repair, merge or promotion approval
  - scientific workflow dispatch, experiment or identity consumption
  - candidate creation, reinterpretation, typing/readiness mutation or quota credit
  - PRE_FORMAL or FORMAL action
  - research/main/evidence/control/preserve/freeze/sealed/formal mutation
  - scheduler or scheduler-registry mutation
  - self-approval or modification of the existing Control-review request

funnel_v2_1_preservation:
  candidate_touched: false
  preserved_fields: NOT_APPLICABLE_NO_RESEARCH_CANDIDATE_TOUCHED
  typing_or_readiness_changed: false

stop_condition: >-
  Stop after one diagnostic pass once the exact lint blocker is identified and its minimal non-scientific repair surface is characterized, or immediately if ownership/authority materially supersedes or the diagnostic is unavailable without prohibited action.

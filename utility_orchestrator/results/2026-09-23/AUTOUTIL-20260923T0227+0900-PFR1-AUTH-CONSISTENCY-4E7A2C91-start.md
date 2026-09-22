# Utility autonomous start — PF-R1 authorization consistency reconciliation

schema_version: 2
generation_id: UTILITY-20260923T022700+0900-AUTO-PFR1-AUTH-CONSISTENCY-RUNNING-4E7A2C91
produced_at: 2026-09-23T02:27:00+09:00
assignment_mode: AUTONOMOUS_IDLE
assignment_id: null
assignment_generation_id: null
autonomous_task_id: AUTOUTIL-20260923T0227+0900-PFR1-AUTH-CONSISTENCY-4E7A2C91
status: RUNNING
run_count: 1
max_runs: 1
evidentiary_status: NON_EVIDENTIARY
scientific_authority: NONE

objective: >-
  Reconcile the Utility mailbox authorization record for the existing PF-R1 durable-provenance request against fresh Control/Analyst statements, without retrieving artifacts, touching H7/PF-R1 research state, or entering PRE_FORMAL/FORMAL.
trigger_source: >-
  Existing request UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE remains mailbox-status PROPOSED_NOT_APPROVED while Control R37 and Evidence Analyst R83 describe it as approved/outstanding.
ownership_checks:
  evidence_analyst_generation: EVA-20260923T020919+0900-R83-A6D4E219
  main_generation: MAIN-20260923T012121+0900-PRIMARY-H7-FORMALR4-C10-R82-RECOVERY-7C4E19B2
  main_status: BLOCKED
  sub_generation: SUB-20260923T013444+0900-NOOP-SCAN-R82-7C4E19B2
  relay_generation: NONE_OBSERVED
  control_generation: CTRL-20260922T235000+0900-R37-7A3E9C51
  collision_found: false
  main_critical_dependency: false
allowed_actions:
  - Read-only inspect Utility assignment/request/decision/state records.
  - Read fresh Control/Analyst/MAIN/SUB generations and authoritative repository refs.
  - Persist Utility-owned state/results only.
forbidden_actions:
  - No PF-R1 artifact retrieval, archival, hashing, rerun, reconstruction, scoring, or reinterpretation.
  - No H7/PRE_FORMAL/FORMAL action or protected-ref mutation.
  - No candidate/Funnel mutation, research branch mutation, workflow action, merge, or scheduler mutation.
stop_condition: >-
  Stop after one bounded determination of whether the mailbox contains a Control-owned approval/decision object matching the request, and record the safest follow-up without changing Control decisions.

exact_refs:
  assignment_pointer_blob: 6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7
  utility_request_blob: d0bcee3fe422925cfc999cf63cc5ba34375eb8b0
  utility_branch_prestart_head: 46a2b6735c4df221b28ee02a252993ffb7cbaa06
  evidence_analyst_head: ba109150205db0a30ce1c294ab8133fa6caa51b4
  control_head: 23676a55c9473d1cfd22d982ffffd5d2ba18b557
  orchestrator_head: 722c64371fe4783dde36ab34a7339e9baa3d38b7
  main: ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
  h7_r4_head: 647253f4c0128ff09d47fdfce80dabf006863af1

funnel_v2_1_preservation:
  candidate_touched: false
  preserved_fields: NOT_APPLICABLE_NO_RESEARCH_CANDIDATE_TOUCHED
  typing_or_readiness_changed: false
  theory_backward_quota_credit: false
  discovery_quota_credit: false
  preformal_credit: false
  promotion_credit: false

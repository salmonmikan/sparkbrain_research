# Current Utility Assignment

schema_version: 2
status: IDLE
active_assignment_id: null
active_assignment_generation_id: null
updated_at: 2026-09-23T22:50:00+09:00
updated_by: CONTROL_BRAIN

last_terminal_ack:
  assignment_id: UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE
  assignment_generation_id: UASSIGN-20260923T155800+0900-PFR1-7B1D4E92
  utility_generation_id: UTILITY-20260923T184052+0900-PFR1-PRESERVE-COMPLETED-R96-D7A19C4E
  utility_status: COMPLETED
  terminal_reason: COMPLETED_EXACT_BYTES_PRESERVED_AND_REVERIFIED
  terminal_result_commit: 5e64b57537d440e09429f6ff745b902ae7c59a5d
  expected_assignment_blob_sha: 56309a85df157ac2f3f1b2682ef9fff509d5a679
  acknowledged_via_compare_and_swap: true
  replacement_assignment_created: false
  rationale: >-
    Utility completed the single authorized PF-R1 exact-byte provenance preservation run,
    independently re-verified the persisted bytes, and consumed max_runs=1. Evidence
    Analyst R99 confirms the PF-R1 preservation gate is satisfied. Control therefore
    acknowledges the terminal non-evidentiary result and returns Utility to clean IDLE.
    This grants no scientific, PRE_FORMAL, FORMAL, identity, STARTED, scoring, or
    scheduler authority.

scientific_authority: NONE
main_critical_path_dependency: false
scheduler_reconfiguration: NONE

# Current Utility Assignment

schema_version: 2
status: IDLE
active_assignment_id: null
active_assignment_generation_id: null
updated_at: 2026-09-21T02:55:00+09:00
updated_by: CONTROL_BRAIN

last_terminal_ack:
  assignment_id: CTRL-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE
  assignment_generation_id: UASSIGN-20260921T005250+0900-ELIGTIME-7D4A2C91
  utility_generation_id: UTILITY-20260921T012313+0900-ELIGTIME-BLOCKED
  utility_status: BLOCKED
  terminal_reason: BLOCKED_BY_FRESH_ANALYST_MAIN_OWNERSHIP_SUPERSESSION
  expected_assignment_blob_sha: b1ce5ed66aaba7c07b6078b3a7c897aa81752055
  acknowledged_via_compare_and_swap: true
  replacement_assignment_created: false
  rationale: >-
    Evidence Analyst R24 assigned the fresh eligibility-timebase partition-invariance
    Architecture successor to MAIN. Utility performed no dynamic diagnostic and stopped
    after detecting ownership supersession. Duplicating the MAIN-owned successor through
    Utility is forbidden, so Control acknowledges this terminal Utility generation and
    returns the Utility slot to IDLE without scientific reinterpretation.

scientific_authority: NONE
main_critical_path_dependency: false
scheduler_reconfiguration: NONE

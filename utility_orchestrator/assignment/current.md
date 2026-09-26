# Current Utility Assignment

schema_version: 2
status: IDLE
active_assignment_id: null
active_assignment_generation_id: null
updated_at: 2026-09-26T16:50:00+09:00
updated_by: CONTROL_BRAIN
incident_id: INC-GITHUB-PERSISTENCE-20260925-001

reason: >-
  The prior one-run P0 persistence diagnostic assignment expired at
  2026-09-25T23:55:00+09:00 and must not be replayed. Control reconciles the
  pointer to clean IDLE so the restored Utility scheduler can operate under its
  normal bounded ASSIGNMENT/AUTONOMOUS_IDLE contract.

previous_assignment:
  assignment_id: UTIL-20260925-P0-GITHUB-PERSISTENCE-DIAG-001
  assignment_generation_id: UASSIGN-20260925T210500+0900-P0-GITHUB-PERSISTENCE-001
  disposition: EXPIRED_NOT_REPLAYED
  max_runs: 1
  expires_at: 2026-09-25T23:55:00+09:00

scientific_authority: NONE
main_critical_path_dependency: false
scheduler_reconfiguration: NONE

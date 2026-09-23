# Current Utility Assignment

schema_version: 2
status: ACTIVE
active_assignment_id: UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE
active_assignment_generation_id: UASSIGN-20260923T155800+0900-PFR1-7B1D4E92
updated_at: 2026-09-23T15:58:00+09:00
updated_by: CONTROL_BRAIN

decision_id: CTRL-DEC-20260923-1558-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE
decision_path: utility_orchestrator/decisions/2026-09-23/PFR1-DEVELOPMENT-PROVENANCE-PRESERVE.md
requested_worker: UTILITY
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_PROVENANCE_ONLY
scientific_authority: NONE
main_critical_path_dependency: false

objective: >-
  Preserve the exact original PF-R1 development raw.json and summary.json bytes with
  verified hashes and durable non-evidentiary provenance, without rerun or scientific
  reinterpretation.

authorized_scope:
  - retrieve existing original PF-R1 raw.json exact bytes only
  - retrieve existing original PF-R1 summary.json exact bytes only
  - compute and verify exact hashes before interpretation
  - persist exact bytes/provenance with create-only or otherwise non-destructive semantics already specified by the request
  - report exact source, hashes, destination and availability status

must_not:
  - rerun PF-R1
  - reconstruct PF-R1
  - regenerate PF-R1
  - retune PF-R1
  - rescore PF-R1
  - change scientific metric/comparator/threshold/tolerance/protocol/seed/intervention/resource contract/hypothesis/falsifier/success criteria
  - create FORMAL authority, identity or STARTED
  - inspect or modify candidate #34 D34-Q002 raw/result surfaces
  - mutate consumed/formal/sealed/evidence refs
  - perform Fast Forge work under this assignment

fail_closed_if_original_bytes_unavailable: true
fail_closed_on_assignment_or_decision_mismatch: true
completion_requires_control_ack: true

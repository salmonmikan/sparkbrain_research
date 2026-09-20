# Archived Utility Assignment — CTRL-20260920-0650-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY

archive_mode: LEGACY_TERMINAL_BOOTSTRAP
archived_by: control_plane_migration
archived_at: 2026-09-20T10:27:00+09:00
source_current_blob_sha: a900ed9372dabc517596eb1e1971e71a9bb91241

# Current Utility Assignment

status: COMPLETED
active_assignment: false
assignment_id: CTRL-20260920-0650-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY
issued_by: control_brain
issued_at: 2026-09-20T06:50:00+09:00
completed_at: 2026-09-20T07:25:00+09:00
expires_at: 2026-09-20T09:00:00+09:00
max_runs: 1
run_count: 1
source_request_ids:
- EVA-20260920-0502-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY
result: utility_orchestrator/results/2026-09-20/CTRL-20260920-0650-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY-0725.md
result_commit: f30da2ea3ba0a4cc064be4847c2e2945344c6aa2
classification: STATIC_EXTRACTOR_FALSE_NEGATIVE_CONFIRMED
completion_reason: COMPLETED_ONE_READ_ONLY_CONSISTENCY_RESULT_MAX_RUNS_REACHED

objective: >-
  Read-only audit the already-completed CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01
  cycle-1 machine artifact against its exact prospective contract, harness, workflow
  metadata, and bound source blobs. Determine whether decision-relevant static_facts
  fields faithfully encode source semantics, especially
  restore_restores_original_base_threshold, and report exact matches/mismatches and
  whether those fields are trustworthy for future successor design.

temporary_role: READ_ONLY_STATIC_DETECTOR_CONSISTENCY_AUDIT
target_branch: ops/utility-orchestrator-requests
target_object: CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01_COMPLETED_CYCLE1

safe_input_scope:
- completed NON_EVIDENTIARY suppression cycle-1 artifact and machine summary only
- exact prospectively bound contract and harness for that completed cycle
- exact bound source blobs and ordinary workflow metadata already referenced by the contract
- no active MAIN refractory-current-accounting object
- no current SUB discovery object

required_checks:
- enumerate decision-relevant static_facts fields used by the completed suppression cycle
- compare each field to exact bound source semantics using deterministic source-level/AST/structural inspection where practical
- explicitly verify restore_restores_original_base_threshold
- distinguish artifact extractor mismatch from artifact-to-handoff mismatch
- report whether disputed fields are trustworthy for future successor decisions without changing the completed mapped outcome

allowed_actions:
- read only the safe completed NON_EVIDENTIARY suppression cycle-1 chain
- use deterministic source-level, AST, structural, or invariant inspection against exact bound source blobs
- write the normal single Utility result and state update for this assignment

forbidden_actions:
- dispatch or rerun scientific workflows
- execute dynamic pulses, probes, training, or experiments
- modify or repair the completed artifact, contract, harness, research branch, MAIN, or source
- relabel AMBIGUOUS_CONTRACT or rescore, retune, regenerate, reinterpret, or replace the completed terminal result
- access official TEST or consumed/formal raw evidence
- edit prior MAIN/Relay/Evidence Analyst/Control/Methodology/request/decision/result records
- mutate main, research branches, immutable/freeze/sealed/formal/evidence/control/preserve refs
- choose or change scientific thresholds, comparators, metrics, seeds, candidate status, successors, or allocations
- create PRE_FORMAL or FORMAL authority, identities, STARTED markers, preserve/evidence anchors
- use the active MAIN refractory object or SUB discovery as fixtures/dependencies
- mutate schedulers or self-approve follow-up work

stop_condition: >-
  Stop after one completed read-only consistency result, or return BLOCKED if safe
  inputs are unavailable. Do not broaden scope or self-extend beyond one run.

reporting_destination: utility_orchestrator/results/2026-09-20/
evidentiary_status: NON_EVIDENTIARY_METHODOLOGY_DIAGNOSTIC
follow_up_authority: NONE_WITHOUT_FRESH_CONTROL_DECISION

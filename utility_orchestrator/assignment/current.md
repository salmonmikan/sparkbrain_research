# Current Utility Assignment

status: ASSIGNED
active_assignment: true
assignment_id: CTRL-20260920-0450-HANDOFF-BINDING-GUARD
issued_by: control_brain
issued_at: 2026-09-20T04:50:00+09:00
expires_at: 2026-09-20T07:00:00+09:00
max_runs: 1
run_count: 0
source_request_ids:
- EVA-20260920-0401-HANDOFF-BINDING-GUARD

objective: >-
  Design and validate one bounded prospective machine-checkable handoff-binding
  schema/checker for future outcome-bearing lower-funnel closures. Demonstrate
  fail-closed detection on the known completed Temporal and Top-k handoff
  mismatches and successful validation on at least one faithful binding/fixture.

temporary_role: READ_ONLY_CONTROL_PLANE_HANDOFF_GUARD_PROTOTYPE
target_branch: ops/utility-orchestrator-requests
target_object: utility_orchestrator/prototypes/handoff_binding_guard_v1/

fixture_scope:
- completed CAND-TEMPORAL-BATCH-PARTITION-01 cycle 1 NON_EVIDENTIARY artifact/handoff chain
- completed CAND-TOPK-PA-01 cycle 1 NON_EVIDENTIARY artifact/handoff chain
- completed v0.5 topology-config Architecture artifact may be used only as a safe positive-control fixture if already accessible
- exclude the currently active MAIN suppression-semantics Architecture object from fixture generation and outcome interpretation

minimum_bindings_when_present:
- workflow run ID and exact producing head
- artifact ID/name and archive digest
- embedded candidate/study identity
- embedded Analyst/contract/interpretation identity or digest
- raw digest and row/cardinality count
- exact mapped outcome/classification
- canonical digest of the complete machine summary object used for interpretation
- every family/stratum boolean, count, ratio, threshold application, or other machine-summary field copied into durable narrative/state

allowed_actions:
- read only already-produced safe NON_EVIDENTIARY completed artifacts and designated control-plane handoffs
- create or update bounded prototype/design files only under utility_orchestrator/prototypes/handoff_binding_guard_v1/ on this control-plane branch
- implement deterministic canonicalization/digest and validation logic or an equivalent validation design
- demonstrate fail-closed mismatch detection on the known Temporal and Top-k defects
- demonstrate successful validation on at least one faithful binding/fixture
- write the normal single Utility result and state update for this assignment

forbidden_actions:
- dispatch or rerun scientific workflows
- retrain, reprobe, rescore, retune, regenerate, relabel, or repair scientific results
- access official TEST or consumed/formal raw evidence
- edit or repair prior MAIN/Relay/Evidence Analyst/Control/request/decision/result records
- mutate main, research branches, immutable/freeze/sealed/formal/evidence/control/preserve refs, or existing scientific artifacts
- choose or change scientific thresholds, comparators, metrics, seeds, candidate status, successors, or allocations
- create PRE_FORMAL or FORMAL authority, identities, STARTED markers, preserve/evidence anchors
- wire the prototype into live research workflows or scheduler definitions
- mutate schedulers or self-approve follow-up work

stop_condition: >-
  Stop after one completed result demonstrating the bounded validator/design, or
  return BLOCKED if safe fixtures or required control-plane inputs are unavailable.
  Do not broaden scope or self-extend beyond one run.

reporting_destination: utility_orchestrator/results/2026-09-20/
evidentiary_status: NON_EVIDENTIARY_CONTROL_PLANE_METHOD_PROTOTYPE
follow_up_authority: NONE_WITHOUT_FRESH_CONTROL_DECISION

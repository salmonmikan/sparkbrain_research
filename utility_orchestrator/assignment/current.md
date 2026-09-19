# Current Utility Assignment

status: ASSIGNED
active_assignment: true
assignment_id: CTRL-20260920-0250-ARTIFACT-HANDOFF-FIDELITY
issued_by: control_brain
issued_at: 2026-09-20T02:50:00+09:00
expires_at: 2026-09-20T05:00:00+09:00
max_runs: 1
run_count: 0
source_request_ids:
- METHCAL-20260920-0120-ARTIFACT-HANDOFF-FIDELITY

objective: >-
  Perform one bounded read-only consistency audit of already-completed NON_EVIDENTIARY
  Architecture results from machine workflow artifacts into durable MAIN/Relay and
  Evidence Analyst handoffs. Determine whether artifact identities/digests, embedded
  contract identities, mapped outcomes, and family/stratum summaries are transcribed
  faithfully enough for downstream methodological decisions.

temporary_role: READ_ONLY_ARTIFACT_HANDOFF_CONSISTENCY_AUDIT
target_object: recent completed NON_EVIDENTIARY Architecture artifact-to-handoff chain
mandatory_sample:
- CAND-TEMPORAL-BATCH-PARTITION-01 cycle 1
opportunistic_samples:
- CAND-TOPK-PA-01 completed Architecture cycles, only if already-produced artifacts are safely accessible
- completed Assembly Architecture output, only if already-produced artifacts are safely accessible

allowed_actions:
- read already-completed lower-funnel workflow metadata and artifacts
- read designated MAIN/Relay and Evidence Analyst handoffs that claim to summarize those artifacts
- compare workflow run/head, artifact ID/digest, embedded candidate/contract identity, raw digest when already present, mapped outcome, and family/stratum machine-summary fields
- report exact matches and mismatches with provenance

forbidden_actions:
- dispatch or rerun any scientific workflow
- retrain, reprobe, rescore, retune, regenerate, relabel, or repair any result
- access official TEST or consumed FORMAL raw data
- mutate main, research branches, immutable/freeze/sealed/formal/evidence/control/preserve refs, or existing result artifacts
- edit prior Evidence Analyst, MAIN/Relay, Control Brain, request, decision, or result records
- choose new thresholds, comparators, metrics, seeds, scientific successors, or research allocations
- create PRE_FORMAL or FORMAL authority or identities
- mutate scheduler definitions

stop_condition: >-
  Stop after one completed consistency-audit result. If safe required inputs are unavailable,
  the assignment becomes stale/expired, or an ownership/integrity conflict appears, return a
  blocked result without broadening scope. Do not self-extend.

reporting_destination: utility_orchestrator/results/2026-09-20/
evidentiary_status: NON_EVIDENTIARY_METHODOLOGY_FIDELITY_DIAGNOSTIC
follow_up_authority: NONE_WITHOUT_FRESH_CONTROL_DECISION

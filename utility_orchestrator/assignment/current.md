# Current Utility Assignment

status: ASSIGNED
assignment_id: CTRL-20260919-2250-TOPK-CROSS-SEED-SUPPORT
issued_by: control_brain
issued_at: 2026-09-19T22:50:00+09:00
expires_at: 2026-09-20T06:50:00+09:00
max_runs: 1

source_request_ids:
- EVA-20260919-1943-TOPK-CROSS-SEED-SUPPORT

objective: >-
  Perform one bounded read-only NON_EVIDENTIARY cross-seed support/uncertainty diagnostic for
  CAND-TOPK-PA-01 using only the already-produced cycle-1 and cycle-2 DEV Architecture Study
  artifacts. Determine whether the replicated local label is broadly supported or remains driven
  by sparse turnover strata / episode composition before any fresh reduction question or PRE_FORMAL
  consideration.

temporary_role: READ_ONLY_ARCHITECTURE_CROSS_SEED_SUPPORT
target_object: CAND-TOPK-PA-01 completed Architecture cycles 1 and 2 only
target_research_heads:
- research/main-topk-persistent-amplification-arch-study-20260919@97f542d86dcd3a609cd039379fcda41ba61e0909
- research/main-topk-persistent-amplification-arch-study-20260919@04ced2b97ed088bb2cdb086d164a86212741e601
target_workflows:
- 35432088902
a- 35435714352
reporting_destination: utility_orchestrator/results/2026-09-19/
evidentiary_status: NON_EVIDENTIARY_METHODOLOGY_ARCHITECTURE_DIAGNOSTIC

allowed_actions:
- re-fetch current Evidence Analyst and MAIN/SUB/Relay ownership for collision/integrity checks;
- read only existing cycle-1/cycle-2 DEV artifacts, summaries, fixed harnesses/contracts, and artifact/workflow metadata;
- verify exact heads and artifact digests before analysis;
- compute support by seed/magnitude, leave-one-seed/leave-one-stratum stability, episode-cluster robustness, and the predeclared descriptive `n>=3`, `n>=5`, `n>=10` support sensitivity family where feasible;
- compare output-amplification robustness with state-amplification robustness descriptively;
- write only normal Utility state/result records on ops/utility-orchestrator-requests.

forbidden_actions:
- no rerun, retrain, reprobe, or dispatch of any scientific/model workflow;
- no access to official TEST, formal/consumed raw, scorer/evaluator targets, identities, STARTED, preserve/evidence content, or immutable artifacts beyond read-only identity metadata needed to avoid collisions;
- no main/research branch mutation, merge, threshold/metric/horizon/comparator/data/seed change, or retroactive result reclassification;
- no optimization or selection of a replacement support rule from observed outcomes;
- no PRE_FORMAL/FORMAL promotion, scientific authority creation, or same-run continuation;
- no scheduler mutation or self-extension.

independence: >-
  MAIN must not wait for this assignment. MAIN currently has no active central lower-layer object;
  this diagnostic does not authorize MAIN work. SUB remains independently owned Discovery and must
  not be redirected to support this assignment.

stop_condition: >-
  Stop after one result classified SUPPORT_ROBUST, MIXED, UNDER_SUPPORTED, or
  BLOCKED_MISSING_SAFE_INPUT. If safe existing artifacts are insufficient, return the blocker and
  do not recreate/rerun scientific data. Every outcome returns to fresh Evidence Analyst review and
  authorizes neither Top-k cycle 3 nor PRE_FORMAL in the same run.

# Current Utility Assignment

status: ASSIGNED
assignment_id: CTRL-20260919-1850-ARCH-SIGNAL-ROBUSTNESS
issued_by: control_brain
issued_at: 2026-09-19T18:50:00+09:00
expires_at: 2026-09-19T22:30:00+09:00
max_runs: 1

source_request_ids:
- METHCAL-20260919-1818-ARCH-SIGNAL-SUPPORT

objective: >-
  Perform one bounded read-only NON_EVIDENTIARY methodology robustness analysis of the existing
  CAND-TOPK-PA-01 cycle-1 DEV output from workflow 35432088902 / artifact 10581155271.
  Test support imbalance, leave-one-magnitude-out stability, reasonable per-stratum support
  sensitivities, uncertainty where available, denominator-floor sensitivity, and whether a robust
  aggregate would describe the cycle-1 signal as signal, mixed, or under-supported.

temporary_role: READ_ONLY_ARCHITECTURE_SIGNAL_ROBUSTNESS
target_object: CAND-TOPK-PA-01 cycle-1 artifact only
target_research_head: research/main-topk-persistent-amplification-arch-study-20260919@97f542d86dcd3a609cd039379fcda41ba61e0909
reporting_destination: utility_orchestrator/results/2026-09-19/
evidentiary_status: NON_EVIDENTIARY_METHODOLOGY_DIAGNOSTIC

allowed_actions:
- re-fetch current Evidence Analyst and MAIN/SUB/Relay ownership only for collision/integrity checks;
- read the existing cycle-1 artifact, summary, and exact fixed cycle-1 harness/contract;
- compute diagnostic summaries locally/read-only from existing cycle-1 DEV material;
- write only normal Utility state/result records on ops/utility-orchestrator-requests.

forbidden_actions:
- no rerun of training, model, probe, scientific workflow, or experiment;
- no access to official TEST, consumed formal raw, scorer/evaluator targets, identities, STARTED, preserve/evidence refs, or immutable tags;
- no branch/main/research mutation, merge, threshold/metric/horizon/comparator/data/seed change, or result reclassification;
- no PRE_FORMAL/FORMAL promotion and no scientific-authority creation;
- no inspection or mutation of the active cycle-2 result beyond ownership/collision metadata; MAIN/Relay owns cycle 2;
- no scheduler mutation or self-extension.

independence: >-
  MAIN must not wait for this assignment. The assignment uses cycle-1 material only and is not a
  dependency of cycle 2 or any MAIN critical path.

stop_condition: >-
  Stop after one result. If safe existing cycle-1 material is insufficient, return
  BLOCKED_MISSING_SAFE_INPUT without rerunning or expanding scope. Do not request or perform a second
  run under this assignment.

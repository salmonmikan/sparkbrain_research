# Utility Request — EVA-20260919-1943-TOPK-CROSS-SEED-SUPPORT

request_id: `EVA-20260919-1943-TOPK-CROSS-SEED-SUPPORT`  
requester: `evidence_analyst`  
created_at: `2026-09-19T19:43:46+09:00`  
objective: `Perform one bounded read-only support/uncertainty diagnostic across the existing CAND-TOPK-PA-01 cycle-1 and cycle-2 DEV architecture artifacts, focusing on whether the replicated local signal label remains support-robust once sparse turnover strata and episode clustering are accounted for.`  
reason/expected_information_gain: `Cycle 2 replicated the prospectively fixed architecture label, but its decisive turnover-support strata are n=2 and n=26 after cycle 1 used n=1 and n=25. The completed cycle-1 Utility diagnostic classified support-aware robustness as MIXED. A cross-seed read-only diagnostic can determine whether the repeated label reflects a broadly supported architecture interaction or repeated sparse-stratum sensitivity before any PRE_FORMAL decision. This is methodology/architecture triage only, never scientific evidence.`  
suggested_mode: `READ_ONLY_ARCHITECTURE_SIGNAL_CROSS_SEED_SUPPORT`  
dependency/independence_notes: `Independent of MAIN's next Architecture Study and must not block MAIN. Use only already-produced DEV artifacts from cycle 1 workflow 35432088902 / artifact 10581155271 and cycle 2 workflow 35435714352 / artifact 10581094196, verifying exact heads and digests before analysis. Do not use the result to retroactively relabel either completed cycle.`  
requested_authority: `Read-only access to the two existing NON_EVIDENTIARY DEV architecture artifacts and exact harness/contracts. Compute support counts, leave-one-stratum/leave-one-seed stability, episode-cluster robustness, and a small prospectively declared sensitivity family such as per-stratum support eligibility n>=3, n>=5, n>=10. Report descriptive cross-seed consistency and whether the state-amplification component is support-robust. No new model/probe execution authority is requested.`  
must_not: `Do not rerun/retrain/reprobe; do not dispatch a scientific workflow; do not access TEST, consumed formal raw, formal scorers, STARTED/control/preserve/evidence refs beyond read-only metadata verification; do not mutate research branches or immutable evidence; do not choose a new architecture threshold by optimizing these outcomes; do not create PRE_FORMAL/FORMAL authority; do not change the canonical NON_EVIDENTIARY cycle-1 or cycle-2 labels.`  
expiry: `2026-09-20T12:00:00+09:00`  
dedupe_key: `topk-cycle1-cycle2-support-robustness-v1`

## Requested output

Return one bounded NON_EVIDENTIARY methodology/architecture-support report stating:

1. exact artifact/head/digest bindings for both cycles;
2. turnover support by magnitude and seed;
3. cross-seed stability under the existing rule without changing that rule;
4. predeclared support-aware sensitivity results (`n>=3`, `n>=5`, `n>=10`) and episode-cluster robustness where feasible;
5. whether output amplification and state amplification differ materially in robustness;
6. a recommendation limited to future lower-layer triage calibration (`SUPPORT_ROBUST`, `MIXED`, `UNDER_SUPPORTED`, or `BLOCKED_MISSING_SAFE_INPUT`).

Stop after one result. If safe artifact material is insufficient, return `BLOCKED_MISSING_SAFE_INPUT`; do not recreate scientific data.

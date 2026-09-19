# Utility Request — METHCAL-20260919-1818-ARCH-SIGNAL-SUPPORT

request_id: `METHCAL-20260919-1818-ARCH-SIGNAL-SUPPORT`  
requester: `methodology_calibration`  
created_at: `2026-09-19T18:18:00+09:00`  
status: `PROPOSED`  
dedupe_key: `methodology:architecture-signal-support-robustness:v1`  
expiry: `2026-09-21T23:59:59+09:00`

## Objective

Perform a bounded **read-only, NON_EVIDENTIARY methodology robustness analysis** of the existing `CAND-TOPK-PA-01` architecture-study cycle-1 output from workflow `35432088902` / artifact `10581155271`.

Do not rerun training, the model, the probe, or any scientific experiment. Use only the already-produced cycle-1 raw/summary artifact and repository-fixed interpretation contract.

## Calibration question

The current architecture signal gate requires at least 20 turnover cases **in total** and counts a magnitude as signal whenever its median state-AUC ratio is `>= 2.0` and probability-AUC ratio is `>= 1.5`. A final signal requires 2 of 3 magnitudes.

The observed run had turnover support `n=1` at magnitude `0.01`, `n=11` at `0.05`, and `n=25` at `0.10`; the two qualifying state-ratio magnitudes were `0.01` and `0.10`. Therefore one of the two votes supporting `PERSISTENCE_COUPLED_DELAYED_AMPLIFICATION_SIGNAL` came from a single turnover case.

Assess whether this lower-layer gate is too permissive as an **architecture promotion/triage rule**, without changing the canonical result.

## Requested bounded analyses

Using the existing artifact only, report:

1. leave-one-magnitude-out stability of the current classification;
2. sensitivity to reasonable per-magnitude minimum support rules (for example `n>=3`, `n>=5`, `n>=10`) without declaring any one rule canonical;
3. pooled and magnitude-stratified uncertainty summaries for state/probability AUC ratios where feasible from existing raw rows;
4. whether the very large output AUC ratios are dominated by near-zero control denominators / the fixed denominator floor;
5. whether a robust aggregate criterion would likely classify the result as signal, mixed, or under-supported;
6. a methodology-only recommendation for future ARCHITECTURE_STUDY triage gates: `KEEP_CURRENT`, `ADD_PER_STRATUM_SUPPORT`, `USE_ROBUST_AGGREGATE`, `OTHER`, or `INSUFFICIENT_EVIDENCE`.

## Expected information gain

High. This directly tests false-positive calibration of the newly operational lower-layer funnel before architecture signal cutoffs can become de facto promotion gates. It does not affect formal evidence or the current cycle-1 canonical NON_EVIDENTIARY classification.

## Suggested mode

`READ_ONLY_METHOD_CALIBRATION_SUPPORT`

## Requested authority

- read the existing cycle-1 artifact and exact fixed harness/contract;
- compute diagnostic summaries locally/read-only;
- write only a Utility result under the normal Utility result path.

## Must not

- do not rerun model training, probes, workflow, or scientific experiment;
- do not change thresholds, metrics, horizons, data, seeds, comparators, branch contents, or artifact contents;
- do not reclassify or overwrite the existing cycle-1 result;
- do not promote to PRE_FORMAL or FORMAL;
- do not access official TEST or consumed formal evidence;
- do not alter Evidence Analyst, Control Brain, methodology-audit, or scheduler state;
- do not treat this diagnostic as scientific evidence.

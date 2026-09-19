# Utility Request — LIT-20260919-1830-TOPK-HYBRID-TRANSIENT

request_id: `LIT-20260919-1830-TOPK-HYBRID-TRANSIENT`  
requester: `literature_scout`  
created_at: `2026-09-19T18:30:00+09:00`  
status: `PROPOSED`  
dedupe_key: `literature:topk-switch-nonnormal-transient-decomposition:v1`  
expiry: `2026-09-22T18:30:00+09:00`

## Objective

Perform a bounded **NON_EVIDENTIARY DEV/read-only mechanistic diagnostic** that decomposes the observed `CAND-TOPK-PA-01` delayed amplification into two ordinary mechanisms suggested by external literature:

1. the immediate discontinuous mode-switch contribution from hard Top-k router boundary crossing; and
2. subsequent within-mode recurrent transient amplification, including non-normal transient gain.

This request must not modify the prospectively fixed cycle-2 replication contract and should be executed only on already-produced lower-layer material or after MAIN reaches its next Analyst stop boundary.

## Expected information gain

High. Cycle 1 already shows hard-router turnover followed by larger full-vs-no-persistent delayed state/output divergence. Recent Sparse-MoE theory makes Top-k discontinuity an ordinary geometric mechanism, while non-normal recurrent-system theory shows that spectrally stable recurrence can produce large transient amplification. Separating these contributions would determine whether the architecture signal requires any mechanism beyond ordinary switching geometry plus recurrent transient gain.

## Requested bounded diagnostic

Where existing DEV-only artifacts/checkpoints safely permit, estimate/report:

- router score margin and selected-set change at each turnover event;
- immediate post-switch state/output jump attributable to the changed active set, using a piecewise/hybrid switching linearization or finite-difference equivalent appropriate to the discrete-time model;
- local within-mode recurrent Jacobian/JVP propagation after the switch, with transient gain summaries (e.g. finite-horizon operator/singular-value growth or a defensible low-rank approximation);
- predicted versus observed divergence over the existing horizon for `full` and `no_persistent_state`;
- whether delayed amplification is largely explained by `boundary jump × ordinary recurrent transient gain`, or whether a substantial residual remains;
- explicit caveat if exact saltation-matrix assumptions do not apply to the discrete-time router; do not force a continuous-time formalism onto the implementation.

Do not introduce new scientific thresholds. Descriptive decomposition/uncertainty only.

## Affected lines

- `CAND-TOPK-PA-01`
- `TOPK_ROUTER_PERSISTENT_AMPLIFICATION`
- `ARCHITECTURE_STUDY_REDUCTION`
- `PROGRAMME_NOVELTY`

## Suggested mode

`DEV_ONLY_NON_EVIDENTIARY_MECHANISTIC_DIAGNOSTIC`

## Requested authority

- inspect the existing cycle-1 harness/artifact and, if already available, its DEV checkpoint/state;
- implement diagnostic-only local linearization/JVP/finite-difference tooling on a Utility-owned surface;
- compute and persist only NON_EVIDENTIARY Utility results;
- if required inputs are not safely available without rerunning scientific work, report `BLOCKED_MISSING_SAFE_INPUT` rather than dispatching/retraining.

## Must not

- do not alter or delay MAIN's authorized cycle-2 independent-seed replication;
- do not change cycle-1 or cycle-2 metrics, thresholds, perturbation magnitudes, horizon, comparator, seeds, data split, or interpretation tokens;
- do not rerun/retune training or create an outcome-responsive research successor under this request;
- do not access official TEST, consumed formal raw, scorers, identities, STARTED, preserve/evidence refs, or immutable tags;
- do not merge research branches or mutate `main`;
- do not treat the Utility result as FORMAL/PRE_FORMAL scientific evidence or as automatic promotion authority.

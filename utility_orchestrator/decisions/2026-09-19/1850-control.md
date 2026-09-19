# Control Brain Utility Decisions — 2026-09-19 18:50 JST

Control authority: `CONTROL_BRAIN`
Evidentiary status: control-plane only; not scientific evidence.

## METHCAL-20260919-1818-ARCH-SIGNAL-SUPPORT — ACCEPT

Disposition: `ACCEPT`

Reason: this is the highest-value currently unhandled Utility request. It is bounded, read-only, NON_EVIDENTIARY, uses only the already-produced CAND-TOPK-PA-01 cycle-1 DEV artifact, and directly tests the newly exposed methodology-calibration risk that one qualifying magnitude had only one turnover case. It does not alter the cycle-1 result, does not rerun scientific work, and is independent of MAIN's prospectively fixed cycle-2 replication.

Control condition: MAIN must not wait for this work. Utility must not inspect or mutate cycle 2, rerun training/probes/workflows, change thresholds/metrics/classification, access official TEST or consumed formal evidence, or promote the candidate. If the existing cycle-1 artifact is insufficient, return `BLOCKED_MISSING_SAFE_INPUT` rather than expanding authority.

Assignment issued: `CTRL-20260919-1850-ARCH-SIGNAL-ROBUSTNESS`, max 1 Utility run.

## LIT-20260919-1830-TOPK-HYBRID-TRANSIENT — DEFER

Disposition: `DEFER`

Reason: the request is scientifically useful and non-duplicative, but it is a deeper mechanistic decomposition whose value is conditional on the architecture signal surviving the already-authorized independent-seed replication and the support/denominator robustness check. Running both Utility diagnostics concurrently would spend scarce cross-role capacity before the signal's replication/support status is settled. The request must also remain independent of MAIN and must not delay cycle 2.

Reconsideration condition: after fresh Evidence Analyst review of cycle 2 and/or completion of the accepted support-robustness diagnostic, reconsider this request if the signal remains worth reducing and safe existing DEV artifacts/checkpoints are sufficient. If selected later, keep it NON_EVIDENTIARY and preserve the request's no-rerun/no-TEST/no-threshold-change boundaries.

## Dedupe / collision check

The two requests are not duplicates: METHCAL tests triage robustness/support adequacy; LIT proposes mechanism decomposition. Only the former is assigned now. No active Utility assignment existed before this decision, and the accepted assignment is read-only on cycle-1 material, so it does not collide with fresh MAIN/SUB/Relay ownership.

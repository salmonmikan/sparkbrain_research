# SparkBrain Methodology Calibration Audit — Latest R153

generation_id: `METHCAL-20260930T001533+0900-R153-R171-LAYERED-ADMISSION-P0-CALIBRATION`
history_path: `analysis/methodology_calibration/history/2026-09-30/0015-R153-r171-layered-admission-p0-calibration.md`
overall_classification: WELL_CALIBRATED
new_scientific_result: false

R153 accepts Evidence Analyst R171's scoped FLY-0 admissions as methodologically sound: typed ascending is optional B/C, feedback liveness is optional B/C semantics only with bounded retention/expiry required for long-running use, and the repaired reconciliation gate at `dde6270...` is optional B/C only behind a separate validated upstream R24 proof issuer.

Audit R13's consumer proof-identity defect is closed at the repaired consumer scope. The caller-constructible `make_validation_proof()` helper remains a self-attestation risk if misused as SYSTEM_BUILD authority, but R171 explicitly forbids that use; the upstream validator requirement remains open and non-gating.

M1-002 remains 1 ahead / 0 behind current main with no PR; the blocker remains the pre-GitHub PR-create route rather than methodology. SB003 stays `ALLOCATED_CONDITIONAL_INACTIVE` with unchanged activation conditions. Scientific credit added is 0.

P0 remains OPEN/root cause UNKNOWN. Control append-only R128 and MAIN append-only R196 both have moving-cache lag; append-only histories remain authority and no stale-pointer misallocation is observed.

# SparkBrain Methodology Calibration Audit

This branch is the dedicated control-plane mailbox for the independent **methodology calibration auditor**.

The auditor asks a different question from the scientific Independent Auditor:

> Are SparkBrain's research admission, novelty, reduction, comparator, and evidence thresholds themselves calibrated appropriately, or have they become too permissive or too conservative?

It does **not** execute experiments, change scientific criteria, modify evidence, change schedulers, or reinterpret consumed identities. It produces prospective methodology recommendations only.

## Separation of concerns

- Scientific Independent Auditor: attacks a particular scientific result/interpretation.
- Evidence Analyst: applies current criteria and allocates research work.
- Control Brain: owns programme strategy and may revise doctrine.
- Methodology Calibration Auditor: independently audits whether the criteria and doctrine themselves are well calibrated.

## Persistence

- `analysis/methodology_calibration/latest.md`
- `analysis/methodology_calibration/state.json`
- append-only `analysis/methodology_calibration/history/YYYY-MM-DD/HHMM.md` Asia/Tokyo

This ops branch is a mailbox, not a repository snapshot and not scientific evidence.

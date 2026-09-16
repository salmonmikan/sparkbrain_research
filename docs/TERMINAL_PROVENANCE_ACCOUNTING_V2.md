# Terminal provenance accounting v2 prototype

Status: independent methods prototype; not an A01 evaluator migration and not a scientific verdict.

## Purpose

The existing A01 bookkeeping audit identified a representability gap between executed
terminal failures and prospective objects rejected before STARTED. This prototype models
those histories without forcing an unexecuted object into phase pass/fail booleans and
without treating a bare family-name list as evidence of family completion.

The implementation is deliberately isolated in
`src/sparkbrain/evaluation/terminal_provenance.py`. It does not import, modify, wrap, or
replace the current V061/A01 admission/evaluator implementation.

## Terminal classes

The model distinguishes four terminal classes:

- `EXECUTED_PHASE_FAILURE`: the identity was STARTED/consumed and a sequential protocol
  phase failed. Earlier phases must be `PASSED`; later phases are `NOT_ASSESSED`.
- `EXECUTED_P5_REDUCTION`: P1-P4 passed, P5 failed under an explicit comparator authority,
  and the identity was STARTED/consumed.
- `PRE_START_STATIC_REDUCTION`: no phase was assessed, STARTED is false, the identity is
  unconsumed, and an explicit comparator authority supports the static reduction.
- `PRE_START_OTHER_REJECTION`: no phase was assessed and the object was rejected before
  STARTED for another canonically recorded reason.

Every record carries a non-empty canonical authority. Executed records also require an
identity and enforce STARTED + consumed provenance. Pre-START records enforce the opposite
and require P1-P5 to remain explicitly `NOT_ASSESSED`.

## Evidence-backed family coverage

`assess_evidence_backed_family_coverage()` derives coverage from terminal provenance
records. A required family is missing until exactly one terminal record for that family is
present. Duplicate records for one family fail closed instead of being silently selected.
This avoids the earlier bookkeeping failure mode where enumerating family names could look
complete even when no faithful terminal record existed.

## Synthetic-fixture scope

The tests use only invented `synthetic://...` authorities and identities. They demonstrate:

- an executed P4-style terminal failure while preserving P5 as not assessed;
- a pre-START static reduction with all phases not assessed;
- rejection of fabricated phase results on pre-START records;
- explicit comparator requirements for reduction classes;
- STARTED/consumption consistency for executed records;
- incomplete family coverage when a required evidence-backed record is absent;
- complete coverage only when every required family has one valid terminal record; and
- duplicate-family provenance rejection.

No A01 Family-B or Family-C `CandidateDisposition` is instantiated. No historical A01
machine verdict is changed, and this prototype must not be used to turn the current
`WITHHELD` accounting state into a retrospective terminal verdict.

## Promotion boundary

This branch is a reusable methods prototype only. Promotion to `main`, migration of current
A01 accounting, or use in a future scientific protocol requires a separate prospective
review. The prototype has no dependency on C19-v2 and is not on MAIN's critical path.

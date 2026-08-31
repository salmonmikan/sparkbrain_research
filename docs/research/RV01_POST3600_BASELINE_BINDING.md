# RV01 post-3600 baseline binding

## Decision

RV01 is explicitly re-anchored to the formal post-confirmatory v0.6.1 source point before R01-12C and later interference work continues.

- source commit: `1c89324958ffb3619878a6e0791aaf3c7a14c5da`
- source branch at binding time: `v061-candidate-003-formal-report-20260831`
- successful source CI run: `33342374956`
- RV01 branch: `research/rv01-endogenous-transition`

This binding replaces the earlier pre-formal RV01 baseline fingerprint. It does not modify the v0.6.1 runtime or the completed confirmatory evidence. It only changes which already-existing source tree RV01 treats as its frozen comparison condition.

## Runtime fingerprint changes

Relative to the earlier RV01 baseline binding, the formal post-3600 source has different blobs at:

- `src/sparkbrain/v06/consistency.py`: `2752b3efc2bd17b35376dbae107cea817041896e`
- `src/sparkbrain/v06/local_expectation.py`: `caeb0b7ccc07ce9fdf26f56b25b11ba59fbc8594`
- `src/sparkbrain/v06/relation_reentry.py`: `0feff95f11809caec51c89eab1308c09f6b6f59b`

All other paths in `FROZEN_RUNTIME_BLOBS` remain bound to the blob IDs recorded in `src/sparkbrain/research/rv01/baseline.py`.

## Rationale

The user-directed RV01 continuation begins only after the 3,600-record confirmatory run has completed. Continuing to fingerprint an older pre-formal v0.6 source would make the RV01 comparison condition inconsistent with that requested latest stable point. The re-binding is therefore performed before interpreting R01-12C or adding R01-12D comparator results.

## Boundary

This decision does not:

- rewrite or rerun the 3,600-record confirmatory evidence;
- merge RV01 mechanisms back into the v0.6.1 confirmatory branch;
- open the 50 held-out R01-12 worlds;
- change any RV01 capability threshold from observed development results.

# N3-DEV-001 independent result audit

Date: 2026-09-09. Status: ACCEPTED_NARROW_DEVELOPMENT_RECORD.
Source: 201ebd512cdee6365bd186e3ff0627ba784677cd.
Pre-execution independent review: 5cd8f43686801ceeafd87140f2daf21028c1c244.
This is internal technical acceptance, not formal seal authority.

The single execution completed all 36 preregistered cases and 72 arm rows with no
reported failure. Independent read-only auditing verified exact four-file inventory,
case/arm order, all paired input objects and recomputed input hashes, checkpoint cut
coverage, every recorded checkpoint canonical/logical size, mechanism payload sizes,
control state invariance, recurrent clock/write counts, actual scalar-array sizes,
summary/raw agreement, and protocol/manifest binding. No model execution or outcome
rerun was used by the result audit.

All 36 absence/replay arm rows preserved learned state; replay rejection was recorded.
The 18 absence/replay paired cases had identical confidence outputs. The other 18
confirmation/contradiction cases differed in confidence outputs. These are different
fixed readout/calibration rules, so confidence differences do not rank task quality,
accuracy, or superiority. Shared exact-parent routing and anonymous classification
mean this diagnostic does not distinguish routing mechanisms.

Accounting: A01 checkpoint sizes across recorded cuts range 3,630–5,171 bytes; N3
4,068–5,520 bytes. These ranges are descriptive and not paired resource-equivalence
claims. N3 retains 2 fixed, 2 learned and 2 hidden scalars; A01 instantiates 0–4 learned
support counters. Incremental mechanism serialization differs in included config and
mapping: the A01 support dictionary is 2–155 bytes and the N3 trace checkpoint is
465–514 bytes. Those two incremental payloads must not be called equal-scope capacity
measurements. The complete arm snapshots provide the broader accounting boundary.
Exact resident duplicates, shared-router operation totals and transient occupancy are
explicitly null. Resource matching remains NOT_EVALUATED, as preregistered.

Artifact SHA256:

| File | SHA256 |
|---|---|
| protocol.json | d9c95e52063a77806a723fa537f8354fc6d2d175b1f2fac36f27edd3e166c6b2 |
| source_manifest.json | dba6bbfab6b2da96d2a6713238991eb151aea078fc994528c9bc85903a847214 |
| raw_rows.jsonl | cd9b0565c16963319eab2f8a011b970f628cf1638154f1689ee85ffb0e53f5b1 |
| summary.json | 69d8945be1c569e096c67a1721314baebfeaba8965aae2e55488ce0e7c04731f |

Reproduce only this artifact audit with:
`python scripts/check_n3_development_artifacts_independent.py artifacts/v061/a01/N3_DEV_001`.
The audit returned PASS (72 rows, 36 cases, 36 control rows, 18 equal endpoint cases).
The separate pre-execution review records 10 focused engineering tests and readiness
passing. Full repository regression was not performed by this reviewer.

Accepted scope: a working live-state recurrent causal learner, actual shared-bridge
input handling, prospective fixed development responses, and inspectable accounting
limitations. Full MD-002, its corrected P2/P3/P4 interventions, full P5 and matched N3
remain pending/not evaluated. MD-001 evidence is unchanged. No mechanism emergence,
external generalization, energy benefit or scientific claim upgrade is supported.

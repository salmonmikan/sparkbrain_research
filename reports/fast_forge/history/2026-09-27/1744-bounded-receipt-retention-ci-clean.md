# SparkBrain Fast Forge — bounded receipt retention

- schema_version: 2
- generation_id: FORGE-20260927T174452+0900-BOUNDED-RECEIPT-RETENTION-CI-CLEAN
- produced_at: 2026-09-27T17:44:52+09:00
- forge_id: FORGE-BOUNDED-RECEIPT-RETENTION-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-bounded-receipt-retention-a
- exact_prototype_head: 090d52373a094a728c4ca93d13af4a572ad15d10
- ci_run: 36307039134
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

## Target capability

Bound growth of the exact receipt ledger in the prior locked local outcome store without silently reapplying events whose exact receipts have been compacted.

## Why now

The prior Forge handoff explicitly left full snapshot growth and receipt retention unresolved. Theory R9 retained local durability and idempotence as engineering seams but made no scientific proposal. This probe addresses only that noncanonical storage seam and does not use the now-exposed RD006 D0 outcome.

## Prototype

The optional positive `receipt_capacity` keeps only the newest exact receipts. On overflow, the oldest receipt is removed and contributes to:

1. `retained_from_sequence`, the exact-replay horizon;
2. a rolling SHA-256 digest of canonical compacted receipts;
3. a fixed 2,048-bit event-identity filter with four positions per identifier.

Within the retained window, exact replay remains unchanged. A delivery older than the horizon raises `CompactedReceiptUnavailableError` before coordinator evaluation. An identifier that may appear in the compacted prefix raises `CompactedEventIdentityError`. The conservative filter has no false negatives for inserted identifiers in this implementation, but it can reject a new identifier as a false positive.

The retention fields are covered by the existing checkpoint digest and atomic replacement. The locked wrapper passes capacity through every in-lock reopen. An explicit capacity conflicting with an existing checkpoint is rejected. Version-1 unbounded stream states are accepted without implicit compaction.

## Diagnostics and observations

- Five sequential events at capacity two retain exactly sequences three and four.
- Exact replay of a retained receipt returns `duplicate_replay` without mutation.
- Replay before the horizon fails without mutation or reapplication.
- Reuse of a definitely compacted identifier at the next sequence fails conservatively.
- JSON checkpoint roundtrip preserves horizon, rolling digest, filter and capacity.
- Locked durable reopen preserves the bounded ledger and refuses capacity reconfiguration.
- A version-1 unbounded state migrates in memory and remains unbounded.
- The public process API still has no caller scope, regime, episode, prediction error, tail assignment, truth or evaluator identity.

## Validation

- New bounded-retention tests: 6/6 PASS
- Focused idempotence/durability/locking/retention chain: 28/28 PASS
- All Forge tests: 95/95 PASS
- Ruff: PASS
- compileall: PASS
- local readiness: PASS
- Local full repository collection: unavailable because optional `fastapi`, `torch` and `jsonschema` packages are absent
- Exact-prototype-head GitHub CI 36307039134: Python 3.11 and 3.13 lint, readiness, full tests and bundle validation SUCCESS

## Ordinary reduction

Ordinary bounded log retention, rolling hashing, a fixed Bloom-style identity filter, POSIX advisory file locking and atomic local snapshot replacement. This is not distributed exactly-once delivery, a remote transaction, a learning mechanism or a scientific result.

## Engineering usefulness

The prototype removes the prior unbounded exact-receipt-ledger growth while remaining fail-closed for old redelivery. It does not pretend that a compacted digest can reconstruct an old receipt or prove arbitrary membership.

## Limitations and claim boundary

- Exact receipts before the horizon are unavailable; old replay is rejected rather than answered.
- The fixed filter accumulates false positives and eventually harms liveness. No rotation, archive or saturation policy is supplied.
- Only the exact receipt ledger is bounded. Coordinator state and total checkpoint size are not generally bounded.
- Capacity cannot be changed on an existing checkpoint; no migration policy is supplied.
- The rolling prefix digest is an integrity/audit summary, not a membership proof.
- Advisory-lock bypass, POSIX/network-filesystem differences, remote storage and distributed failures remain unresolved.
- No actual process kill, power loss, torn sector, filesystem fault or high-contention fairness test was run.
- Prediction pools, routing thresholds and scope allocation remain fixed and uncalibrated.
- No continuous scientific task, matched comparator, resource comparison or interaction ablation was run.
- No SYSTEM_BUILD admission, comparative support, composition contribution or scientific novelty is established.

## Collision and integrity

Evidence Analyst R151 allocated only the bounded RD006 v3 D0 matrix to MAIN. MAIN R159 has since exposed an inconclusive bounded-explosion result and now waits for fresh Analyst reconciliation. This Forge branch neither reads that outcome into the prototype nor executes any second matrix, later stage, capability score or scientific dispatch. Relay remains dependency-wait suspended. Methodology R131, Utility's R151 bridge audit, Theory R9, SB001 and all research/evidence/preserve/consumed/frozen/FORMAL refs are untouched.

## Authoritative refs used

- main: cf0bc45262824f1fe282ccd7b785b3ea50be2099
- human directives: 3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7
- Evidence Analyst: EVA-20260927T170004+0900-R151-RD006-V3-D0-DYNAMIC-GATE-CLARIFIED at 1a0a56b9f9360c95c77ac24d9a217f2945169a6e
- MAIN: MAIN-20260927T172900+0900-PRIMARY-R159-RD006-V3-D0 at 15b3e90dee1359e7e9673d7043c7f077284b309a
- Control: R93 P0 closed / Relay dependency wait at 927a2c84dccc49140dc720a48c52f399d4e0692a
- Methodology: METHCAL-20260927T161705+0900-R131-RD006-V3-D0-GATE-CALIBRATION at deb7e6781eaf1c6139cee0056c51365346e70543
- Utility: UTILITY-20260927T172727+0900-ANALYST-R151-BRIDGE-AUDIT at c428c1d393322fc9e42ab9506d1acb98d4342053
- Theory: THEORY-20260927T153101+0900-R9-NO-PROPOSAL-TRANSACTION-IDEMPOTENCE-2C7A91E4 at cf3c49a4affa31e21ed9229983766da7ee064587
- source Forge handoff: 109469fb5788126605350398b18bb89cc992d890

## Handoff

FORGE_INTERESTING / SYSTEM_BUILD_INPUT.

Evidence Analyst may optionally retain this bounded-retention adapter with the R6 bridge/outcome/coverage/transaction/idempotence/durability/locking chain for a future separately allocated SYSTEM_BUILD. No Utility request was created.

New SparkBrain scientific result: no.

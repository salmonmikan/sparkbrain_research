# SparkBrain Fast Forge — idempotent observed-outcome stream

Generation `FORGE-20260927T144929+0900-IDEMPOTENT-OUTCOME-STREAM-CI-CLEAN`
built one isolated, noncanonical retry/replay boundary on branch
`forge/20260927-idempotent-outcome-stream-a`.

## Why this probe

The previous transaction coordinator made one observed-outcome step atomic
across allocator and revision state, but it had no delivery identity. An
at-least-once caller could therefore apply the same valid revision twice, or
re-evaluate an earlier no-write event after later state changed. This was a
bounded implementation seam, independent of MAIN's RD006 v3 static preflight.

## Prototype

Added:

- `forge_prototypes/idempotent_outcome_revision_stream.py`
- `forge_prototypes/idempotent_outcome_revision_stream.md`
- `tests/test_forge_idempotent_outcome_revision_stream.py`

The stream wrapper requires contiguous new sequence numbers and binds each
event identifier to a SHA-256 digest of the complete public payload. Exact
redelivery returns a stored semantic receipt and performs no evaluation.
Identifier/content conflicts, stale or gapped new events and malformed
checkpoints fail without changing coordinator or ledger state. No-write events
are also receipts, so later state changes cannot reinterpret them on retry.

The wrapper evaluates the existing transaction coordinator on a checkpoint copy
and advances coordinator, receipt and sequence state together. Invalid payloads
consume neither event identity nor sequence.

## Verification

- focused stream plus transaction tests: 16/16 pass;
- all Forge tests: 77/77 pass;
- Ruff, compile and local readiness: pass;
- local full collection: unavailable because optional `fastapi`, `torch` and
  `jsonschema` were absent;
- exact-head CI `36298170312`: success on Python 3.11 and 3.13, including lint,
  full tests and bundle validation.

Exact prototype head: `87adfb63ac8c92236acf42aa308cea3020169629`.

## Ordinary reduction

This is ordinary ordered idempotent-consumer and content-addressed
deduplication-ledger engineering. It is not distributed exactly-once
processing, event-time inference, a learned memory mechanism or a scientific
result.

## Engineering usefulness

The wrapper closes the retry seam around the previous one-step transaction.
Successful mutation, pending state and no-write decisions are each bound once
to one event payload and cannot be silently doubled or reinterpreted.

## Limitations and claim boundary

- Bounded in-memory event sequence only; no continuous scientific task.
- No receipt compaction, external durable store, broker, partition, concurrent
  writer or distributed crash-window test.
- Fixed uncalibrated prediction/routing components.
- No matched comparator, resource match, interaction ablation or task capability.
- No SYSTEM_BUILD admission, comparative support, composition contribution or
  scientific novelty.
- Not admitted to SB001 or RV02; scientific credit remains zero.

## Collision and integrity

Evidence Analyst R149 assigns MAIN only RD006 v3 prospective contract and static
preflight, with result-bearing execution stopped. MAIN's durable state remains
R157 and Relay remains dependency-wait suspended. Theory R8 is NO_PROPOSAL,
Methodology R130 is WELL_CALIBRATED and SB001 remains integrated complete. All
were left untouched. No canonical, scientific, evidence, immutable, consumed,
preserve, frozen or FORMAL ref was modified.

Inputs: main `cf0bc45262824f1fe282ccd7b785b3ea50be2099`;
Analyst R149 at `79b2e7e67144804393911853b7bd405fafec629e`;
MAIN R157 at `d868b7ff14677100b9c6e29e90b265f99f14c64c`;
Control R90 at `ca934c91c2e371a41e1a8b88ca8c7827f128f64f`;
Methodology R130 at `f036226a374f4518adfab515bbe0e78f847040ee`;
Utility at `625b613aee256390c5e868bdb26a21bdd5320cfb`;
Theory R8 at `b1e0e2d8d19b908e27d49495ad9f299ad4d86607`;
source Forge handoff `0b141b3570f7f30357d182659ff7a8b2cab8ecfa`.

## Publication and handoff

The isolated prototype was published and independently read back on the first
attempt. Exact-current-head CI passed. The handoff is
`FORGE_INTERESTING / SYSTEM_BUILD_INPUT`; Evidence Analyst may optionally retain
this wrapper with the prior bridge/outcome/coverage/transaction chain for a
future separately bound SYSTEM_BUILD. No Utility request was created.

New scientific result: false.

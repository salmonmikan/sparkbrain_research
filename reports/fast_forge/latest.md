# SparkBrain Fast Forge — idempotent observed-outcome stream

- schema_version: `2`
- generation_id: `FORGE-20260927T144929+0900-IDEMPOTENT-OUTCOME-STREAM-CI-CLEAN`
- produced_at: `2026-09-27T14:49:29+09:00`
- forge_id: `FORGE-IDEMPOTENT-OUTCOME-STREAM-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260927-idempotent-outcome-stream-a`
- exact_prototype_head: `87adfb63ac8c92236acf42aa308cea3020169629`
- ci_run: `36298170312`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: `0`
- new_scientific_result: `false`

## Target capability

Make the one-step transactional revision coordinator safe under ordinary
at-least-once local delivery: exact redelivery must not apply revision twice,
identifier/content conflicts and out-of-order new events must fail closed, and
checkpoint restore must retain the same deduplication boundary.

## Prototype and diagnostics

Added `IdempotentOutcomeRevisionStream`, a content-addressed receipt ledger
around the previous transaction coordinator.

Verified behaviors:

1. each new event requires the next contiguous sequence number;
2. an event identifier is bound to a digest of all public inputs;
3. exact redelivery returns the stored semantic receipt without re-evaluation;
4. same-identifier/different-content delivery preserves exact prior state;
5. stale and gapped new delivery preserve exact prior state;
6. no-write outcomes are ledgered and remain no-write after later state changes;
7. invalid payloads consume neither sequence nor identifier;
8. checkpoint round-trip preserves both deduplication and the next transaction;
9. malformed non-contiguous checkpoint ledgers fail closed;
10. no caller scope, regime, episode, prediction error, tail assignment, truth
    or evaluator identity is accepted.

Focused stream plus transaction tests passed 16/16. All Forge tests passed
77/77, Ruff, compile and local readiness passed. Local repository-wide
collection remained unavailable because optional `fastapi`, `torch` and
`jsonschema` packages were absent. Exact prototype head
`87adfb63ac8c92236acf42aa308cea3020169629` passed CI run `36298170312` on
Python 3.11 and 3.13, including lint, full tests and bundle validation.

## Ordinary reduction

This is an ordinary ordered idempotent consumer with a content-addressed
deduplication ledger and copy-on-write state transition. It is not distributed
exactly-once processing, event-time inference, a learned memory mechanism or a
scientific result.

## Engineering usefulness

The prior coordinator protected one revision step from partial component writes
but did not protect it from transport retry. This wrapper closes that local
integration seam: a successful mutation, pending state or no-write decision is
bound once to one event payload and cannot be silently re-applied or
reinterpreted after subsequent state changes.

## Limitations and claim boundary

- This is a bounded in-memory event sequence, not a continuous scientific task.
- The receipt ledger has no retention/compaction policy or external durable store.
- There is no distributed crash window, concurrent writer, partition or broker test.
- Prediction pools, routing thresholds and allocators remain fixed and uncalibrated.
- No matched comparator, resource comparison, interaction ablation or task
  capability test was run.
- The prototype supports local retry/replay hygiene only. It does not establish
  SYSTEM_BUILD admission, comparative support, composition contribution or
  scientific novelty.
- It is not admitted to SB001 or RV02 and creates no candidate/build identity.

## Collision and integrity

Evidence Analyst R149 allocates MAIN only the RD006 v3 prospective contract and
static preflight, with result-bearing execution stopped. MAIN's durable state
remains R157; Relay remains in intentional dependency wait. Theory R8 is
NO_PROPOSAL / NO_REVISIT_PROPOSAL. Methodology R130 is WELL_CALIBRATED and keeps
Forge as ordinary optional future SYSTEM_BUILD engineering. SB001 remains
integrated complete. No research, main, evidence, preserve, consumed, frozen or
FORMAL ref was modified.

Inputs: main `cf0bc45262824f1fe282ccd7b785b3ea50be2099`;
Analyst R149 at `79b2e7e67144804393911853b7bd405fafec629e`;
MAIN R157 at `d868b7ff14677100b9c6e29e90b265f99f14c64c`;
Control R90 at `ca934c91c2e371a41e1a8b88ca8c7827f128f64f`;
Methodology R130 at `f036226a374f4518adfab515bbe0e78f847040ee`;
Utility at `625b613aee256390c5e868bdb26a21bdd5320cfb`;
Theory R8 at `b1e0e2d8d19b908e27d49495ad9f299ad4d86607`;
source Forge handoff `0b141b3570f7f30357d182659ff7a8b2cab8ecfa`.

## Handoff

`FORGE_INTERESTING / SYSTEM_BUILD_INPUT`.

Evidence Analyst may optionally retain the stream wrapper with the prior
bridge/outcome/coverage/transaction chain for a future separately bound
SYSTEM_BUILD. No Utility request was created.

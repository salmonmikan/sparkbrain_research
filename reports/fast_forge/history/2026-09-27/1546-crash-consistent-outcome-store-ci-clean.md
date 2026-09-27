# SparkBrain Fast Forge — crash-consistent local outcome store

- schema_version: 2
- generation_id: FORGE-20260927T154622+0900-CRASH-CONSISTENT-LOCAL-STORE-CI-CLEAN
- produced_at: 2026-09-27T15:46:22+09:00
- forge_id: FORGE-CRASH-CONSISTENT-OUTCOME-STORE-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-crash-consistent-outcome-store-a
- exact_prototype_head: 8385e9b6a8fa585de337fe17b8bb26c9ce79a117
- ci_run: 36300934177
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

## Target capability

Make the local idempotent observed-outcome stream recoverable across bounded checkpoint crash windows without allowing a stale local writer to overwrite a newer durable checkpoint.

## Why now

Theory R9 retained the R6 integration design and identified external durability, crash windows, concurrency and receipt retention as unresolved engineering boundaries. The prior Forge stream protected one in-memory transaction and transport redelivery, but its state disappeared with the process. This probe addresses only the smallest local-filesystem durability seam and remains independent of MAIN-owned RD006.

## Prototype

Added DurableOutcomeRevisionStore around IdempotentOutcomeRevisionStream.

The store:

1. clones the current stream before evaluating an event;
2. serializes the complete candidate checkpoint with a canonical SHA-256 digest;
3. writes and fsyncs a same-directory temporary file;
4. atomically replaces the prior checkpoint;
5. fsyncs the parent directory where supported by the host;
6. installs the candidate as live memory only after the replacement path completes;
7. compares the digest opened by this instance with the current file before writing and rejects an already-observed stale writer.

Exact duplicate delivery that leaves stream state unchanged returns the prior receipt without rewriting the durable file.

## Diagnostics and observations

- First commit and reopen preserve the next sequence, receipt ledger and coordinator state.
- Exact redelivery after reopen returns duplicate_replay without a second mutation or checkpoint rewrite.
- Same identifier with different content fails closed after reopen.
- Injected failure after temporary-file fsync but before replace leaves disk and live state unchanged and removes the temporary file.
- Injected failure immediately after replace leaves the original in-memory object stale, but reopening observes the committed event and exact redelivery is deduplicated.
- A writer opened before another writer commits detects the changed checkpoint digest and cannot overwrite it.
- Torn JSON and digest-mismatched checkpoints fail closed.

These are deterministic exception-injection tests around file-operation boundaries, not an actual process-kill, power-loss or filesystem-failure experiment.

## Validation

- New durable-store tests: 7/7 PASS
- Focused stream/transaction/store tests: 23/23 PASS
- All Forge tests: 84/84 PASS
- Ruff: PASS
- compileall: PASS
- local readiness: PASS
- Local full repository collection: unavailable because optional fastapi, torch and jsonschema packages are absent
- Exact-prototype-head GitHub CI 36300934177: Python 3.11 and 3.13 lint, readiness, full tests and bundle validation SUCCESS

## Ordinary reduction

Ordinary atomic-file replacement, canonical content digest, optimistic stale-writer detection and idempotent redelivery. This is not distributed exactly-once processing, consensus, event-time inference, learned memory or a scientific result.

## Engineering usefulness

The adapter closes the single-process local restart seam for the retained R6 engineering chain. An uncertain commit after replace can be resolved by reopening and redelivering the identical event, while a clearly pre-replace failure preserves the prior checkpoint.

## Limitations and claim boundary

- No simultaneous-writer CAS or multi-process lock. Two writers that pass the digest check concurrently can still race.
- No remote store, broker, partition, network or distributed crash test.
- No actual process kill, power-loss, torn-sector or filesystem fault injection.
- Directory fsync behavior is platform/filesystem dependent.
- Full snapshots grow with the receipt ledger; no compaction, retention, backup rotation or migration policy exists.
- A non-crash exception after replace is an uncertain commit and requires reopen plus idempotent redelivery.
- Prediction pools, routing thresholds and scope allocation remain fixed and uncalibrated.
- No continuous scientific task, matched comparator, resource comparison or interaction ablation was run.
- No SYSTEM_BUILD admission, composition contribution or scientific novelty is established.

## Collision and integrity

Evidence Analyst R149 assigns MAIN only RD006 v3 prospective contract/static preflight. MAIN R158 completed that static preflight and is waiting for fresh Analyst reconciliation; result-bearing execution remains unauthorized. Relay remains dependency-wait suspended. Theory R9 is NO_PROPOSAL / NO_REVISIT_PROPOSAL and retains R6. SB001 remains integrated complete. This Forge branch modified no research, main, evidence, preserve, consumed, frozen or FORMAL ref.

## Authoritative refs used

- main: cf0bc45262824f1fe282ccd7b785b3ea50be2099
- human directives: 3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7
- Evidence Analyst: EVA-20260927T135700+0900-R149-RD006-V3-STATIC-PREFLIGHT at 79b2e7e67144804393911853b7bd405fafec629e
- MAIN: MAIN-20260927T153015+0900-PRIMARY-R158-RD006-V3-STATIC-PREFLIGHT at 48d02ef9bb015b2c7c30fba0364bea65c6abe665
- Control: CTRL-20260927T145000+0900-R91-INCIDENT-REGISTRY-RECONCILED at 048ff40c40f8319db4d7ae55db634e940205e4b5
- Methodology: METHCAL-20260927T142036+0900-R130-RD006-V3-STATIC-PREFLIGHT-CALIBRATION at f036226a374f4518adfab515bbe0e78f847040ee
- Utility: UTILITY-20260927T152700+0900-P0-REGISTRY-READBACK at 97835e1ca4c55c80c22e72220dc8b6aeaa70c608
- Theory: THEORY-20260927T153101+0900-R9-NO-PROPOSAL-TRANSACTION-IDEMPOTENCE-2C7A91E4 at cf3c49a4affa31e21ed9229983766da7ee064587
- source Forge handoff: 3dffd818f93d4b21bc792081a7ce814323a47259

## Handoff

FORGE_INTERESTING / SYSTEM_BUILD_INPUT.

Evidence Analyst may optionally retain this local durable-store adapter with the R6 bridge/outcome/coverage/transaction/idempotence chain for a future separately allocated SYSTEM_BUILD. No Utility request was created.

New SparkBrain scientific result: no.

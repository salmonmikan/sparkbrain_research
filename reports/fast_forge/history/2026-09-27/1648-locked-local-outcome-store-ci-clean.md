# SparkBrain Fast Forge — locked local outcome store

- schema_version: 2
- generation_id: FORGE-20260927T164800+0900-LOCKED-LOCAL-STORE-CI-CLEAN
- produced_at: 2026-09-27T16:48:00+09:00
- forge_id: FORGE-LOCKED-LOCAL-OUTCOME-STORE-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-locked-outcome-store-a
- exact_prototype_head: 84df89612e11de2b1ec43f5acb0d4e25b5b6c0b0
- ci_run: 36304033688
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

## Target capability

Close the prior local simultaneous-writer race for cooperating processes without changing the public scientific inputs or touching the MAIN-owned RD006 path.

## Why now

The preceding durable-store prototype left an explicit race: two writers could both pass its optimistic digest check before either atomic replace. Theory R9 also retained local durability/concurrency as an unresolved R6 engineering seam. This probe addresses only a single-host, cooperating-process boundary.

## Prototype

Added `LockedOutcomeRevisionStore` around `DurableOutcomeRevisionStore`.

The adapter:

1. uses a stable same-directory sidecar file for POSIX advisory `flock`;
2. acquires an exclusive lock with a bounded timeout;
3. reopens and digest-validates the checkpoint inside the critical section;
4. processes at most one event through the existing copy-on-write, atomic-replace store;
5. releases the lock only after the durable operation returns or fails;
6. reloads under the same lock for state reads.

Reloading after lock acquisition is the essential seam closure. Two instances opened from the same old state no longer evaluate against the same stale receipt ledger if they cooperate through this adapter.

## Diagnostics and observations

- Two stores created before the first write commit distinct contiguous events in order because the second operation reloads under lock.
- Two spawned processes delivering the same event concurrently produce exactly one `processed` receipt and one `duplicate_replay`; durable sequence advances once.
- Lock timeout raises `LocalStoreLockTimeoutError` and does not create or mutate the checkpoint.
- An injected exception after atomic replace remains an uncertain commit, but reopen plus exact redelivery returns the existing duplicate receipt without reapplication.
- The public process API accepts event and transport metadata but no caller scope, regime, episode, prediction error, tail assignment, truth or evaluator identity.

These are deterministic local process/exception tests, not power-loss, process-kill or filesystem-failure evidence.

## Validation

- New locked-store tests: 5/5 PASS
- Focused durability/idempotence/transaction chain: 28/28 PASS
- All Forge tests: 89/89 PASS
- Ruff: PASS
- compileall: PASS
- local readiness: PASS
- Local full repository collection: unavailable because optional `fastapi`, `torch` and `jsonschema` packages are absent
- Exact-prototype-head GitHub CI 36304033688: Python 3.11 and 3.13 lint, readiness, full tests and bundle validation SUCCESS

## Ordinary reduction

Ordinary POSIX advisory file locking, fresh state reload, atomic snapshot replacement and idempotent consumer receipts. This is not lock-free compare-and-swap, distributed consensus, remote exactly-once processing, learned memory or a scientific result.

## Engineering usefulness

For cooperating processes on one host/filesystem, the adapter closes the acknowledged simultaneous-writer window in the prior durable-store prototype. A second writer sees the committed sequence and receipt ledger before it evaluates its event, so exact redelivery is deduplicated and contiguous events serialize.

## Limitations and claim boundary

- The lock is advisory. A writer that bypasses the adapter can still race the checkpoint.
- POSIX `flock` availability and network-filesystem semantics are platform/filesystem dependent.
- No remote store, broker, partition, network or distributed crash test.
- No actual process kill, power loss, torn-sector or filesystem fault injection.
- No lock fairness or high-contention throughput characterization.
- Full snapshots grow with the receipt ledger; no compaction, retention, backup rotation or migration policy exists.
- A post-replace exception remains an uncertain commit requiring reopen plus idempotent redelivery.
- Prediction pools, routing thresholds and scope allocation remain fixed and uncalibrated.
- No continuous scientific task, matched comparator, resource comparison or interaction ablation was run.
- No SYSTEM_BUILD admission, comparative support, composition contribution or scientific novelty is established.

## Collision and integrity

Evidence Analyst R150 assigns MAIN exactly one bounded RD006 v3 12-cell D0 OFF/ON matrix and stops all later stages. Methodology R131 requires the dynamic gate to count actual hidden spikes, eligible edges and observed fixed-window lag rather than static connectivity. MAIN owns that object; this Forge branch executes none of it. Relay remains dependency-wait suspended. Theory R9 is NO_PROPOSAL / NO_REVISIT_PROPOSAL and retains R6. Utility has no overlapping assignment. SB001 remains integrated complete. No research, main, evidence, preserve, consumed, frozen or FORMAL ref was modified.

## Authoritative refs used

- main: cf0bc45262824f1fe282ccd7b785b3ea50be2099
- human directives: 3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7
- Evidence Analyst: EVA-20260927T160005+0900-R150-RD006-V3-D0-MATRIX-ALLOCATION at 32e17655e21c4dbdb686a5234c00f58a854796aa
- MAIN: MAIN-20260927T153015+0900-PRIMARY-R158-RD006-V3-STATIC-PREFLIGHT at 48d02ef9bb015b2c7c30fba0364bea65c6abe665
- Control: CTRL-20260927T155000+0900-R92-RD006-V3-STATIC-PREFLIGHT-OBSERVED at 0981407a0455fa11a536d5ecf9333a4af336832b
- Methodology: METHCAL-20260927T161705+0900-R131-RD006-V3-D0-GATE-CALIBRATION at deb7e6781eaf1c6139cee0056c51365346e70543
- Utility: UTILITY-20260927T152700+0900-P0-REGISTRY-READBACK at 97835e1ca4c55c80c22e72220dc8b6aeaa70c608
- Theory: THEORY-20260927T153101+0900-R9-NO-PROPOSAL-TRANSACTION-IDEMPOTENCE-2C7A91E4 at cf3c49a4affa31e21ed9229983766da7ee064587
- source Forge handoff: fc25c5f027cac2a272f1de2b428e3f3c85acb577

## Handoff

FORGE_INTERESTING / SYSTEM_BUILD_INPUT.

Evidence Analyst may optionally retain this locked local adapter with the R6 bridge/outcome/coverage/transaction/idempotence/durability chain for a future separately allocated SYSTEM_BUILD. No Utility request was created.

New SparkBrain scientific result: no.

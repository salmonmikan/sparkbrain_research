# SparkBrain Fast Forge — epoch-fenced receipt rotation

- schema_version: 2
- generation_id: FORGE-20260927T184516+0900-EPOCH-FENCED-RECEIPT-ROTATION-CI-CLEAN
- produced_at: 2026-09-27T18:45:16+09:00
- forge_id: FORGE-EPOCH-FENCED-RECEIPT-ROTATION-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-epoch-fenced-receipt-rotation-a
- exact_prototype_head: af5fe79be6120a7fc385a441f33c9f4c25365f2c
- ci_run: 36310182579
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

## Target capability

Rotate a saturated bounded receipt namespace without accepting delivery from a retired epoch or discarding the revision coordinator accumulated by the prior local outcome-revision stream.

## Why now

The preceding Forge handoff bounded exact receipts with a conservative fixed identity filter but explicitly left filter rotation unresolved. Theory R9 made no scientific proposal and Analyst R152 permits only MAIN's read-only preserved-result causal audit. This probe addresses only the isolated noncanonical transport seam and does not execute or reinterpret RD006.

## Prototype

The wrapper adds an explicit transport-only `stream_epoch`. Rotation is accepted only when the requested epoch is exactly current plus one and `expected_next_sequence` matches the current locked checkpoint. It hashes the complete retired epoch state into a rolling chain digest, preserves the revision coordinator, then opens an empty delivery namespace at sequence zero.

Deliveries from every retired epoch and every unopened future epoch fail before coordinator evaluation. Event identifier reuse in the new epoch is allowed only because an old delivery must carry its retired epoch and is fenced. `stream_epoch` must not encode or proxy scope, regime, episode, target, truth or evaluator identity.

## Diagnostics and observations

- Rotation resets delivery sequence, exact receipts and the current conservative identity filter while preserving revision state.
- A stale epoch and an unopened future epoch fail without checkpoint mutation.
- Noncontiguous rotation or a mismatched expected sequence fails closed.
- Checkpoint roundtrip preserves epoch, fence, retired-chain digest and exact duplicate replay.
- The locked store makes a completed rotation visible to a stale handle.
- Checkpoint digest corruption fails closed.
- Repeated rotation grows only the fixed chain digest and retains bounded current-epoch delivery state.
- The public API exposes no caller scope, regime, episode, prediction error, tail assignment, truth or evaluator identity.

## Validation

- New epoch-fencing tests: 8/8 PASS
- Focused retention/locking/durability/epoch chain: 26/26 PASS
- All Forge tests: 103/103 PASS
- Ruff: PASS
- compileall: PASS
- local readiness: PASS
- Local full repository collection: unavailable because optional `fastapi`, `torch` and `jsonschema` packages are absent
- Exact-prototype-head GitHub CI 36310182579: Python 3.11 and 3.13 lint, readiness, full tests and bundle validation SUCCESS

## Ordinary reduction

Ordinary epoch fencing, log rotation, a rolling hash-chain summary, POSIX advisory file locking and atomic local snapshot replacement. This is not distributed consensus, broker fencing, proof of producer quiescence, a learning mechanism, a memory principle or scientific evidence.

## Engineering usefulness

The prototype supplies an explicit way to retire a saturated conservative identifier filter without weakening correctly labelled old-delivery rejection. Revision state survives rotation while current delivery state starts fresh.

## Limitations and claim boundary

- The retired-epoch chain digest is an integrity summary, not an archive or membership proof.
- Exact receipts from retired epochs cannot be reconstructed.
- A producer that labels an old payload with a new epoch can create a logically new delivery.
- A coordinated producer rotation barrier is required but not supplied.
- Distributed consensus, broker fencing, multi-host leases and network partitions are unresolved.
- Advisory locking assumes cooperating same-host writers; POSIX and network-filesystem semantics vary.
- No actual process kill, power loss, torn sector, filesystem fault or distributed crash test was run.
- Only current-epoch delivery state is bounded; coordinator and total checkpoint state are not generally bounded.
- Prediction pools, routing thresholds and scope allocation remain fixed and uncalibrated.
- No continuous scientific task, matched comparator, resource comparison or interaction ablation was run.
- No SYSTEM_BUILD admission, comparative support, composition contribution or scientific novelty is established.

## Collision and integrity

Evidence Analyst R152 closes all 35 canonical candidates and allocates only a read-only preserved-result causal audit to MAIN. MAIN R159's RD006 v3 D0 result remains preserved and untouched. This Forge branch executes no matrix, later stage, capability score or scientific dispatch. Relay remains dependency-wait suspended. Methodology R132 is well-calibrated; Utility's R151 bridge audit, Theory R9, SB001 and all research/evidence/preserve/consumed/frozen/FORMAL refs are untouched.

## Authoritative refs used

- main: cf0bc45262824f1fe282ccd7b785b3ea50be2099
- human directives: 3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7
- Evidence Analyst: EVA-20260927T180100+0900-R152-RD006-V3-POSTRESULT-CAUSAL-AUDIT at 80991262b47bce0bc06bda919fe1f5a8d89cb0be
- MAIN: MAIN-20260927T172900+0900-PRIMARY-R159-RD006-V3-D0 at 15b3e90dee1359e7e9673d7043c7f077284b309a
- Control: CTRL-20260927T175000+0900-R94-RD006-V3-D0-RESULT at c631d7d3203cea1f69723c055f59e1ce92e23562
- Methodology: METHCAL-20260927T181947+0900-R132-RD006-V3-POSTRESULT-CALIBRATION at 6c0a1beaf7a146d995fc5ba6ed0cce004d686f09
- Utility: UTILITY-20260927T172727+0900-ANALYST-R151-BRIDGE-AUDIT at c428c1d393322fc9e42ab9506d1acb98d4342053
- Theory: THEORY-20260927T153101+0900-R9-NO-PROPOSAL-TRANSACTION-IDEMPOTENCE-2C7A91E4 at cf3c49a4affa31e21ed9229983766da7ee064587
- source Forge handoff: 8937342eea5f05777bdccd13aaa7e6f0c13fd609

## Publication

Prototype publication used three attempts within the five-attempt limit: local push failed for absent credentials; the first Git-data tree request used an invalid base tree and made no ref mutation; the rebuilt Git-data publication succeeded and was independently read back. Handoff publication is a separate purpose and is recorded after exact-head CI success.

## Handoff

FORGE_INTERESTING / SYSTEM_BUILD_INPUT.

Evidence Analyst may optionally retain this epoch-fencing adapter with the R6 bridge/outcome/coverage/transaction/idempotence/durability/locking/retention chain for a future separately allocated SYSTEM_BUILD. No Utility request was created.

New SparkBrain scientific result: no.

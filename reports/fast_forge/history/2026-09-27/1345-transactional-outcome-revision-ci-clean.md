# SparkBrain Fast Forge — transactional observed-outcome revision

Generation `FORGE-20260927T134529+0900-TRANSACTIONAL-OUTCOME-REVISION-CI-CLEAN`
built one isolated, noncanonical transaction boundary on branch
`forge/20260927-transactional-stream-coordinator-a`.

## Why this probe

Theory R8 retained `ID-SB-LATENT-SCOPE-PLURAL-REVISION-001` and sharpened the
future SYSTEM_BUILD surface around complete no-write semantics. The current
coverage-aware guard already preserves top-k omissions, but its exposed-outcome
path calls the stateful bridge directly.

A local diagnostic reproduced a concrete partial-state failure: an exposed
outcome with invalid evidence strength correctly raised `ValueError`, but the
bridge had already created and retained an allocator scope before the revision
overlay validated the strength. The revision was rejected while allocator
state changed.

## Prototype

Added:

- `forge_prototypes/transactional_outcome_revision_coordinator.py`
- `forge_prototypes/transactional_outcome_revision_coordinator.md`
- `tests/test_forge_transactional_outcome_revision_coordinator.py`

The coordinator evaluates a complete observed-outcome step on a checkpoint
copy. It replaces live state only for intentional mutation actions:

- `applied_created`;
- `applied_existing`;
- `pending` confirmation state.

Exceptions, omitted outcomes, ambiguous routing and router/allocator conflicts
discard the speculative state. Successful state is restored through the public
serialization contract before becoming live, preventing speculative object
aliasing.

## Verified behaviors

1. the public API accepts no caller-supplied prediction error, scope, regime,
   episode, observed probability, tail assignment, truth or evaluator identity;
2. a successful exposed outcome commits allocator and revision state together;
3. invalid or non-finite evidence strength preserves the exact prior checkpoint;
4. a failed step cannot change the result or state of the following valid step;
5. a tail-sensitive omitted outcome remains explicit no-write;
6. checkpoint round-trip preserves the next transaction and result.

Local focused integration tests passed 26/26. All Forge tests passed 67/67,
Ruff passed and local readiness passed. Repository-wide local collection was
unavailable because optional `fastapi`, `torch` and `jsonschema` packages were
absent. Exact prototype head `a5dbdbcb7e1302e5e08689f3e62e8eab899bebda`
passed CI run `36295091484` on Python 3.11 and 3.13, including lint, full tests
and bundle validation.

## Ordinary reduction

This is ordinary copy-on-write transaction/checkpoint isolation around
stateful components. It is not a new revision rule, uncertainty model, memory
mechanism or scientific result.

## Engineering usefulness

The coordinator closes a real integration seam between scope allocation and
late-evidence revision. A rejected event can no longer leave a half-accepted
context behind, and no-write routing outcomes remain state-preserving even if
an underlying component allocates lazily during speculative evaluation.

## Limitations and claim boundary

- The transaction wraps one already-constructed prediction/outcome step; it is
  not a continuous-stream task evaluation.
- Prediction pools, routing thresholds and allocators remain fixed and
  uncalibrated.
- Pending confirmation intentionally remains allocator state; only rejected or
  no-write steps are rolled back completely.
- No matched comparator, resource comparison, interaction ablation or task
  capability test was run.
- The prototype supports bounded atomic component composition only. It does not
  establish SYSTEM_BUILD admission, comparative support, composition
  contribution or scientific novelty.
- It is not admitted to SB001 or RV02 and creates no candidate/build identity.

## Collision and integrity

Evidence Analyst R148 owns no executable canonical science and assigns MAIN
only the RD006 v2 preserved static topology-return coverage audit. MAIN R157
completed that static audit and waits for Analyst reconciliation. Relay remains
in intentional dependency wait. Theory R8 is NO_PROPOSAL and retains this line
only as an optional future separately bound SYSTEM_BUILD. SB001 remains
integrated complete. No research, main, evidence, preserve, consumed, frozen or
FORMAL ref was modified.

Inputs: main `cf0bc45262824f1fe282ccd7b785b3ea50be2099`;
Analyst R148 at `437f36985cbf6573af0d02599710020a462194e5`;
MAIN R157 at `d868b7ff14677100b9c6e29e90b265f99f14c64c`;
Control R90 at `ca934c91c2e371a41e1a8b88ca8c7827f128f64f`;
Methodology R129 at `4763b74f8bc9f9f684cb7ef86e97ea9a7361bcf4`;
Utility reconciliation at `625b613aee256390c5e868bdb26a21bdd5320cfb`;
Theory R8 at `b1e0e2d8d19b908e27d49495ad9f299ad4d86607`;
source Forge coverage handoff `751b4d72185e87ea88521aa93bf780048ccac4ae`.

## Publication and handoff

The isolated prototype was published and independently read back on the first
attempt. Exact-current-head CI passed. The handoff is
`FORGE_INTERESTING / SYSTEM_BUILD_INPUT`; Evidence Analyst may optionally retain
the coordinator with the prior bridge/outcome/coverage chain for a future
separately bound SYSTEM_BUILD. No Utility request was created.

New scientific result: false.

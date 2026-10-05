# Integrated Prototype Milestone 1

Build identity: `BUILD-SB-M1-001-INTEGRATED-CONTINUOUS-REVISION-PILOT`

Status: NON_EVIDENTIARY SYSTEM_BUILD integration candidate. It is not scientific evidence.

## Target capability

The bounded loop is:

1. receive one current observation;
2. inspect persistent predictive and route-local hypothesis state;
3. act only when the predictive and route-local decisions agree, otherwise abstain;
4. bind one later observed outcome to the original event;
5. revise exactly one compatible predictive hypothesis and one routed evidence ledger;
6. emit the next prediction/action from the revised persistent state.

Only one event may be unresolved at a time. Stable event, receipt and evidence identities make
duplicate delivery explicit.

## Integrated components and provenance

- `PredictiveRevisionPilot` from BUILD-SB-001 supplies the direct v0.3.2 reference runtime and
  explicit/reference predictive-state bank.
- `CausalScopeRevisionPilot` from BUILD-SB-002 supplies bounded current-observation routing and
  route-local competing hypotheses after the R161 integrity repair.
- `IntegratedM1Pilot` is fresh typed transaction glue.
- `DeterministicM1World` is a bounded local engineering fixture outside the runtime boundary.

All reused components transfer zero inherited scientific credit. Explicit memory is not described
as emergent field memory.

## Runtime boundary

The public observation contains only:

- stable event ID;
- local time;
- current named sensory scalars;
- current numeric routing features.

It excludes labels, truth/gold values, oracle scope/regime/entity identifiers, evaluator output,
future suffixes and held-out fields. The later receipt contains only its stable ID, the original
event ID and the observed scalar outcome.

The fixed action rule maps the predictive scalar sign to `alpha`/`beta`. The pilot emits an action
only when that candidate agrees with the selected route-local candidate. Missing support,
ambiguity or disagreement produces explicit abstention.

## Transaction and identity integrity

The SB002 checkpoint schema is version 2 for this build surface. It requires:

- a bounded required evidence ID;
- exact duplicate delivery to be a state-neutral idempotent result;
- conflicting reuse of an evidence ID to fail closed;
- exact equality between router component tokens and route-local state keys;
- a unique global evidence sequence equal to `1..N`;
- exact bidirectional correspondence between evidence records and the evidence-identity ledger.

An integrated later-outcome commit is atomic across the predictive revision, scope revision,
pending binding, receipt ledger, trace and sequence. Failure before or after either component
revision restores the exact pending pre-call state. A session-level failure also restores the
environment and the state produced by observation/action processing.

## Deterministic bounded fixture

The local fixture alternates two observable numeric regions. Initial encounters may abstain;
later encounters can act after predictive and route-local state agree. The selected action changes
the later scalar outcome by a fixed bounded amount. The fixture exercises two routed components,
plural predictive hypotheses, abstention, both actions and multiple continuous cycles.

Each acceptance scenario is limited to 64 cycles. Runtime is CPU-only, local/offline and adds no
dependency or remote service.

## Checkpoint and replay

`IntegratedM1CheckpointManager` saves:

- the direct SB001/reference-brain checkpoint;
- the repaired SB002 checkpoint;
- compositor pending/identity/trace state;
- deterministic world state;
- a strict canonical manifest binding every file digest and the integrated state hash.

Save is staged and atomically installed into a previously absent directory. Checkpoints are
no-clobber. Mid-run restore must reproduce every remaining action, outcome, revision, trace row,
component state and final integrated state hash.

## Verification commands

```bash
python -m pytest -q tests/test_system_build_causal_scope_revision.py
python -m pytest -q tests/test_system_build_integrated_m1.py
python -m pytest -q tests/test_system_build_m1_robustness.py
python -m pytest -q tests/test_system_build*.py
python scripts/local_readiness_check.py
python -m pytest -q
python -m ruff check .
python scripts/validate_bundle.py
```

## Claim boundary and limitations

This build demonstrates only bounded engineering function on deterministic synthetic fixtures.

- built: branch candidate only until integration
- functionally verified: bounded local acceptance only
- comparatively supported: false
- composition contribution: not established
- scientifically novel: false
- scientific credit: 0

It does not establish performance improvement, general scope learning, real-task capability,
causal composition contribution, biological equivalence, energy efficiency or novelty. It remains
limited to two routing components, eight routing dimensions, sixteen predictive hypotheses,
sixty-four context scalars, fixed thresholds and at most 64 fixture cycles per scenario. FLY-0 is
not a dependency, is not mixed into this build and has no SB003 allocation here.

The separately allocated post-integration robustness harness is documented in
`docs/SYSTEM_BUILD_M1_ROBUSTNESS.md`. It extends deterministic verification only and does not
change this runtime or claim boundary.

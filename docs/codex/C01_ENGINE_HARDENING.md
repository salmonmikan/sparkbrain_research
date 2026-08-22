# C01 — Reference Engine Hardening and Replay Contract

## Goal

Turn the current Phase-0 engine into a trustworthy deterministic reference implementation whose configuration, state, traces, counters, and replay behavior are validated and versioned.

## Existing starting point

v0.2 already includes `protocols.py`, `serialization.py`, `replay.py`, `validation.py`, three JSON Schemas, a CI workflow scaffold, deterministic checkpoint continuation tests, and 26 passing tests. Do not recreate these blindly. Audit and finish them against the acceptance criteria below. In particular, verify schema completeness, migration/compatibility behavior, queue/RNG replay across adversarial cases, and CI in a clean supported environment.

## Why this task exists

Every later world, UI, learned backend, and spiking backend needs a stable behavioral contract. Current code is runnable but has only a small test surface and no versioned serialization/replay API.

## Scope

### Add

- `src/sparkbrain/protocols.py`
- `src/sparkbrain/serialization.py`
- `src/sparkbrain/replay.py`
- `src/sparkbrain/validation.py`
- `tests/test_serialization.py`
- `tests/test_replay.py`
- `tests/test_invariants.py`
- `tests/test_event_ordering.py`
- `.github/workflows/ci.yml` updates as needed
- trace/config JSON schemas under `schemas/`

### Modify only as needed

- `model.py`, `engine.py`, `worlds.py`, `README.md`
- theory/architecture docs only when behavior contract truly changes

## Required design

1. Define a backend protocol with at least:
   - `reset(seed/config)`
   - `schedule/ingest`
   - `run` or `advance`
   - `snapshot`
   - `state_dict`
   - `load_state_dict`
   - `stats`
2. Add a `schema_version` to persisted configuration, engine state, and trace.
3. Serialize all state needed to continue deterministically, including event queue ordering, sequence counter, RNG state, stability counters, Workspace, eligibility, and last ignition state.
4. Replay must support:
   - reconstructing visual frames from a trace without executing dynamics;
   - restoring a checkpoint and obtaining byte-equivalent normalized future trace for the same remaining events.
5. Configuration validation must reject impossible or unsafe values: negative capacities, nonpositive decay constants where forbidden, invalid thresholds, unsupported schema versions, duplicate IDs, dangling edges, and nonfinite numbers.
6. Counter semantics must be documented and audited. Inspection and serialization must not increment work counters or change state.
7. Establish deterministic event ordering for equal time/priority events and test it.
8. Set an explicit recurrence/event-limit failure with diagnostic queue context.

## Required tests

At minimum cover:

- configuration JSON round trip;
- state checkpoint round trip;
- checkpoint continuation equality;
- trace-only replay;
- equal-time deterministic ordering;
- duplicate evidence not increasing source diversity;
- internal inhibition not recorded as external contradiction;
- no-ignition retained as `None`;
- residual loser recovery;
- hard zero residual prevents recovery under a predefined sequence;
- cooldown and repeated ignition;
- stability reset on winner change;
- refractory behavior;
- threshold relaxation;
- Workspace capacity and replacement;
- reward changes only plastic edges;
- snapshot/serialization non-interference;
- event-limit diagnostic;
- malformed graph/config rejection.

## Acceptance criteria

- `python -m pytest -q` passes with at least 25 focused tests total.
- `python -m ruff check .` passes.
- `python scripts/validate_bundle.py` passes.
- same seed/config/event stream produces identical normalized trace across two fresh runs;
- checkpoint continuation produces identical future ignitions, beliefs, and counters;
- schemas validate every generated artifact;
- no current Phase-0 benchmark aggregate changes unless documented with a before/after reason;
- `docs/SOFTWARE_ARCHITECTURE.md`, `PROJECT_STATUS.md`, and `RESULTS_LEDGER.md` are updated.

## Non-goals

- learned routing;
- live web UI;
- SNN conversion;
- performance optimization that obscures reference behavior;
- stronger scientific claims.

## Validation commands

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest -q
python scripts/run_demo.py
python scripts/run_benchmark.py --episodes 40 --steps 30
python scripts/validate_bundle.py
```

## Required completion report additions

Include the trace schema version, deterministic replay hash, test count, any changed Phase-0 aggregate, and exact incompatibilities introduced by the schema.

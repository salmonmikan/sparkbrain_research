# C07 Local Spiking Backend Plan

## Objective

Implement a reduced CPU hybrid LIF backend behind the C01 `BrainBackend` protocol and falsifiably test whether the canonical rate behavior survives substrate conversion. Completion requires exported raw rate/spike traces, predefined equivalence checks, explicit negative results, and no energy claim.

## Current behavior

- Integration commit `4eaa619` has a deterministic C01 protocol and reference CAT→TOY→CAT trace, but no spiking backend.
- PyTorch is locally available as an optional tool; Norse and snnTorch availability is not assumed.
- Coalition scoring, ignition, and Workspace are rate/algorithmic in the first hybrid boundary.

## Theory contract

- External events are encoded as currents into leaky integrate-and-fire sensory units; filtered spikes drive the unchanged signed evidence graph.
- Hypothesis activation is a filtered spike/current state. Evidence identity, Coalition scoring, ignition, Workspace, and broadcast retain the C01 algorithmic semantics.
- Duplicate evidence remains one independent ID, no-ignition remains valid, Workspace capacity is unchanged, and inspection is non-mutating.
- This is behavioral equivalence testing, not biological equivalence or energy evidence.

## Predefined tolerances

These thresholds are frozen before the final comparison and must not be changed after viewing final results:

- per-event prediction sequence: exact `[None, cat, cat, cat, toy, toy, cat]`;
- ordered distinct ignition labels: exact `[cat, toy, cat]`;
- no-ignition on the first ambiguous `fur` event: exact;
- switch-to-TOY and recovery-to-CAT event-index latency: absolute difference from rate backend at most 1 event each;
- residual loser recovery at the final event: required;
- duplicate evidence diversity: exact value 1;
- Workspace occupancy never exceeds configured capacity and final capacity-1 label is `cat`;
- causal edge ablation direction: removing `sensory:plastic_seam → hypothesis:toy` must not make TOY ignition earlier and must not increase TOY ignition count;
- visualizer trace schema: all C01 `TraceFrame` fields present; numeric comparison tolerance `1e-6` only for serialization round trips, not behavioral decisions.

## Implementation slices

1. Record official library/version/license/compatibility evidence and keep libraries optional.
2. Add a reduced CPU hybrid LIF backend conforming to the C01 protocol, with deterministic state and trace export.
3. Add shared invariant and adversarial tests for canonical replay, no-ignition, duplicate evidence, capacity, recovery, edge ablation, serialization, and inspection.
4. Add a deterministic comparison runner producing raw rate/spike traces, activity/message counts, and wall-clock separately.
5. Generate the C07 result artifact and update architecture, protocol, results ledger, claims/status, dependencies, and bundle validation.

## Data and evaluation

- Dataset: fixed seven-event SwitchWorld canonical scenario plus focused adversarial fixtures.
- Seed: `7`; no training split or tuning is used.
- Primary outcomes: exact prediction sequence, ordered ignitions, switch/recovery indices, no-ignition, duplicate diversity, capacity, edge-ablation direction.
- Secondary measurements: spikes, messages, engine counters, and local CPU wall-clock. Activity and runtime remain separate; neither supports an energy claim.
- Raw outputs: `artifacts/spiking/c07_comparison.json`, rate/spike trace JSON files, and generated Markdown report.

## Risk register

- **Substrate mismatch:** exact rate dynamics may not map to LIF. Mitigation: preserve negative results; do not post-hoc relax tolerances.
- **Hybrid overstatement:** algorithmic Coalition/Workspace could be mislabeled fully spiking. Mitigation: encode the boundary in code, artifact, and docs.
- **Dependency drift:** external SNN libraries may not support the local Python/PyTorch combination. Mitigation: dependency-free pure-Python/PyTorch-compatible equations as an explicit implementation deviation; libraries remain optional.
- **Measurement confound:** Python runtime is noisy. Mitigation: report disclosed local wall-clock separately from activity counts and prohibit energy inference.
- **Contract drift:** trace or serialization could diverge from C01. Mitigation: protocol runtime checks, schema-shaped trace tests, and non-mutating inspection tests.
- **Offline risk:** optional library import or network access could become mandatory. Mitigation: standard CPU reproduction uses only core dependencies.

## Acceptance criteria

- Reduced CPU canonical comparison runs locally.
- Backend passes the shared C01 protocol and predefined invariant tests.
- CAT→TOY→CAT is reproduced within the frozen tolerances.
- Disagreements and dependency deviations are documented rather than tuned away.
- Activity counts and CPU runtime are separately reported.
- Raw spike and rate traces use the common visualizer schema.
- No energy-efficiency statement or dedicated-hardware mapping is introduced.

## Validation commands

```powershell
.venv\Scripts\python.exe scripts\run_spiking_comparison.py
.venv\Scripts\python.exe -m pytest -q tests\test_spiking_backend.py
.venv\Scripts\python.exe scripts\local_readiness_check.py
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe scripts\validate_bundle.py
```

## Documentation updates

- `docs/SOFTWARE_ARCHITECTURE.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/RESULTS_LEDGER.md`
- `docs/CLAIMS_REGISTER.md`
- `docs/PROJECT_STATUS.md`
- `docs/DEPENDENCIES.md`
- `artifacts/spiking/c07_report.md`

## Local execution contract

- The standard implementation is deterministic, CPU-runnable, local-file-only, and offline after repository setup.
- GPU and Norse/snnTorch adapters are optional and cannot be the only path.
- No remote API, hosted tracker, telemetry, or remote storage is used.

## Rollback boundary

- All changes remain on `codex/c07-spiking-backend` in `C:\55_personal\sikou\sparkbrain-c07`.
- Reverting the scoped C07 commit removes backend, tests, and artifacts without changing C01 persisted schema `0.2` or the deterministic reference engine.

## Plan updates

- 2026-08-23: plan and tolerances frozen before implementation and final comparison.
- 2026-08-23: the assumption that no SNN library was installed was disproven. The shared local environment provided PyTorch 2.13.0+cpu, NumPy 2.5.2, and snnTorch 1.0.0; official documentation/license review selected snnTorch. Norse remained uninstalled. The boundary is hybrid, and threshold 1.1 produced the retained no-spike/no-belief negative result.

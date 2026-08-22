# C04 Learned Routing Implementation Plan

## Scope and frozen inputs

- Base commit: `fcc9dcd` (accepted C02 integration).
- C01 `BrainBackend`, `BrainConfig`, `EngineStats`, and `TraceFrame` remain the runtime contract.
- C02 `Episode`/`Observation` schema version `0.2` remains unchanged.
- `configs/experiments/phase1/manifests/dev-v1.json` is the only source of development seeds.
- `configs/experiments/phase1/manifests/test-v1.json` is the only source of final evaluation seeds.
- Both C02 manifests are immutable. C04 records and verifies their SHA-256 digests; it does not edit them.
- PyTorch and NumPy are optional dependencies exposed only by the `learned` extra. The core package remains dependency-free.

## Architecture

1. A fixed-width event encoder embeds evidence label, source, channel, strength, and timing features without importing the hand-authored `EVIDENCE_WEIGHTS` table.
2. A learned bounded top-k router selects at most `active_k` persistent Spark modules.
3. Persistent module state is updated only for selected modules. A dense recurrent equivalent is retained solely as a labeled ablation.
4. Sparse message passing indexes the selected nodes and evaluates only directed edges whose endpoints are selected. Counters distinguish conceptual selection, state updates, evaluated messages, known dense tensor operations, wall time, and peak memory.
5. A learned evidence-support readout updates explicit belief state using the routed message and an optional residual path.
6. An interpretable Coalition scorer reports support, diversity, stability, contradiction, and total score separately.
7. Ignition is a confidence-and-margin decision calibrated only on development examples. `None` is a valid no-ignition result.
8. Belief and action heads are separate parameters and APIs. Workspace broadcast is an explicit state transition and ablation.
9. C05-facing examples, prediction records, counters, and evaluation summaries are defined in a new additive contract module.

## Data and held-out protocol

- Development episodes are generated deterministically from the C02 dev manifest. Training uses a documented prefix and calibration uses a disjoint suffix.
- Final evaluation uses only C02 test-manifest seeds after all thresholds and hyperparameters are frozen.
- Held-out axes include unseen evidence pairs/orderings, longer sequences, different reliability and switching regimes, distractor composition, and at least one entirely held-out C02 world family.
- Test labels are read only during final metric calculation and never used to set the ignition threshold.

## Objectives and hyperparameter budget

- Primary loss: belief cross entropy.
- Auxiliary terms: justified revision, ignition calibration, routing load balance, active-set sparsity, evidence provenance, recovery, and optional Coalition/readout consistency.
- Every coefficient is serialized with the experiment config.
- The bounded search budget is development-only: at most six configurations and three training seeds for the CPU reference study. The smoke profile uses one configuration and one seed.
- Sensitivity varies active-set size and the principal auxiliary coefficients around the selected development configuration.

## Required ablations

The runner exposes: dense recurrent equivalent, no persistent state, no residual, no Coalition score, forced prediction, random router, learned router without load balancing, no Workspace broadcast, detached Coalition, and end-to-end Coalition.

## Artifacts

`artifacts/phase2/learned-routing-v1/` contains immutable input hashes, resolved configs, checkpoints, raw held-out rows, summary metrics, work counters, routing/load diagnostics, sensitivity results, ablation results, recovery examples, traces, hyperparameter budget, and negative findings. Smoke outputs use a separate `smoke/` directory.

## Acceptance matrix

| Criterion | Evidence |
| --- | --- |
| Offline CPU smoke | smoke command, resolved config, checkpoint, and summary |
| Reproducibility | repeated-seed test and config/checkpoint hashes |
| Immutable splits | before/after SHA-256 verification |
| Above chance and non-learning baseline | held-out summary with coverage-separated accuracy |
| Bounded real active set | router invariant tests and sparse work counters |
| Non-collapsed no-ignition | calibrated coverage and class-conditional diagnostics |
| Non-hand-authored recovery | held-out trace with losing belief later recovering; import guard test |
| Explainable trace | selected module, evidence path, Coalition component trace rows |
| Collapse/load diagnostics | routing entropy, per-module load, dead/overloaded module counts |
| C01 APIs | runtime protocol, checkpoint-continuation, inference/evaluation tests |
| Negative results and budget | committed ledger and machine-readable budget artifact |
| All ablations | named-condition unit test and evaluation artifact |

## Verification

```powershell
.venv\Scripts\python.exe scripts\local_readiness_check.py
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -m sparkbrain.learned.experiment --config configs\experiments\phase2\smoke.json
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -m pytest -q
$env:PYTHONPATH='src'; .venv\Scripts\python.exe -m ruff check .
$env:PYTHONPATH='src'; .venv\Scripts\python.exe scripts\run_demo.py
$env:PYTHONPATH='src'; .venv\Scripts\python.exe scripts\run_benchmark.py --episodes 40 --steps 30
$env:PYTHONPATH='src'; .venv\Scripts\python.exe scripts\validate_bundle.py
```


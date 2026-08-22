# C01-C10 Continuous Implementation Plan

## Objective

Complete C01 through C10 in dependency order and leave an independently runnable, local-first research release. Completion is falsifiable: every task brief acceptance criterion must be either demonstrated by a local command and artifact or explicitly recorded as blocked/negative.

## Current behavior

- Repository baseline is v0.2.1 on `main`, one local commit ahead of `origin/main` at plan creation.
- C01 and C09 have work-in-progress changes in commit `94be973`.
- Current local checks: 51 pytest tests pass; Ruff, local readiness, and bundle validation pass.
- C02-C08 implementation packages and C10 release package are absent at plan creation.
- Phase-0 demo/benchmark artifacts exist; persisted schema remains `0.2`.

## Theory contract

- Preserve evidence identity: repeated propagation of one evidence ID is not independent support.
- Internal inhibition is not external contradiction evidence.
- Preserve no-ignition as `None` and residual loser recovery.
- Keep deterministic event ordering, bounded recurrence, capacity-limited Workspace, inspectable state, and serializable time-changing state.
- Keep belief truth separate from action/value selection.
- Do not raise novelty, biological-fidelity, consciousness, AGI, general superiority, or energy-efficiency claims beyond the claims register evidence grade.

## Implementation slices

1. **C01 / G1:** finish backend, schema, validation, deterministic replay, counter, and failure-diagnostic contracts.
2. **C02 / G2a:** add versioned episode schemas, six controlled worlds, shared ablation harness, metrics, bootstrap intervals, manifests, failure artifacts, and Pareto report.
3. **C03 / M3:** add a loopback-only local Brain Lab with trace/control APIs and a bundled dependency-free frontend while retaining static replay.
4. **C04 / G3:** add a CPU-reference learned encoder/router/active-subgraph backend with immutable splits, diagnostics, checkpointing, and held-out evaluation.
5. **C05 / G2b:** add one shared local harness for probabilistic, recurrent, causal-attention, modular-recurrent, explicit-state, oracle, and chance baselines with matched-accounting reports.
6. **C06 / G4:** add a redistribution-safe external adapter contract, local-cache/checksum workflow, one official adapter when obtainable, and a bundled licensed/generated non-monotonic stream validation path.
7. **C07 / G5:** add a reduced CPU spiking/hybrid backend behind the common protocol and compare predefined behavioral tolerances without energy claims.
8. **C08 / M8:** add seeded, budgeted, checkpointed structural events and causal/null controls; accept and record a negative specialization result when criteria are not met.
9. **C09:** complete the dated primary-source literature matrix and challenge every novelty proposition with the strongest retrieved precedent.
10. **C10 / G6:** pin the environment, generate manifests/notices/SBOM/checksums/cards/report inputs, add one-command smoke reproduction, and perform a clean local rerun.

Each slice receives focused tests, a task-specific result/status update, and a scoped commit before dependent work proceeds. Parallel work uses separate worktrees or non-overlapping files; shared contracts are integrated by the coordinator only.

## Data and evaluation

- All generated datasets, splits, seeds, raw per-episode/per-seed results, failures, configs, hashes, and version metadata stay under explicit local repository paths.
- Synthetic defaults are selected on development seeds; evaluation manifests are frozen before final test runs.
- Main C02 conditions target 1,000 test episodes unless measured local runtime justifies and documents a smaller count.
- Learned comparisons use common immutable examples, multiple seeds, aligned no-prediction semantics, paired episode-level comparisons, and uncertainty intervals.
- External data acquisition is an explicit setup step; evaluation must then run from a checksummed local cache without network access.
- Spiking comparisons predefine tolerances before final runs and retain both rate and spike traces.

## Risk register

- **Scientific confound:** tuning on final test seeds or adapters. Mitigation: immutable manifests and dev/test separation.
- **Attribution confound:** language encoder or dense mask credited as Spark dynamics/sparse execution. Mitigation: ablations and separated counters.
- **Overclaim:** positive toy results treated as general support. Mitigation: claims-register gate and negative-result ledger.
- **Contract drift:** parallel tasks invent incompatible episodes/traces/backends. Mitigation: coordinator-owned shared schemas and sequential integration gates.
- **Performance:** C02/C04/C05/C07 full studies exceed a typical CPU budget. Mitigation: mandatory CPU smoke profiles plus separately labeled full configurations.
- **Dependency/license:** learned/spiking/UI libraries compromise offline or redistribution constraints. Mitigation: dependency-light reference paths, primary-source license checks, and notices.
- **External dataset availability:** official data may be inaccessible or non-redistributable. Mitigation: acquisition/checksum adapter plus explicit blocked status; never fabricate completion.
- **Local/offline:** UI or evaluation silently reaches the network. Mitigation: loopback/static assets, import audits, and offline smoke validation.

## Acceptance criteria

### C01

- 25+ focused tests, Ruff, bundle validation, fresh-run trace identity, checkpoint continuation identity, generated-artifact schema validation, unchanged or explained Phase-0 aggregate, and architecture/status/results updates.

### C02

- Deterministic schema-valid worlds; hand-computed metric tests; one ablation harness; confidence intervals/raw-manifest links; dominated-system Pareto output; three explained failure cases; no test tuning; protocol/status/results/claims updates.

### C03

- One or two documented local launch commands; complete UI canonical revision and evidence inspection; behavior-changing edge-ablation fork with parent preservation; synchronized comparison; API/E2E tests; static viewer retained; bind/artifact/offline/intervention/legend docs.

### C04

- Offline CPU smoke training; seed/config reproducibility; immutable manifests; held-out performance above chance and one non-learning baseline; bounded active set and real work counters; non-collapsed no-ignition; non-hand-authored recovery case; routing/evidence trace; load diagnostics; C01 API compatibility; negative-result and search-budget record.

### C05

- CPU smoke for all required families; local post-setup datasets; one config system; five learned seeds or documented runtime justification; tested parameter/budget accounting; identical splits; separated coverage/correctness; paired uncertainty; failures on both sides; no unsupported superiority claim.

### C06

- Post-acquisition offline evaluation; one reproducible official adapter or explicit blocked evidence; update/no-update reporting; direct/explicit-state baselines; encoder/dynamics ablations; categorized errors; causal evidence interventions; evidence-bounded claim grades.

### C07

- Reduced local CPU canonical comparison; shared protocol/invariants; CAT-TOY-CAT within predefined tolerances or documented negative result; untuned disagreement record; separated activity/runtime; common trace export; no energy claim.

### C08

- Seed-deterministic serialized structural events; bounded growth; random and degree-matched controls; one causally supported held-out specialization or an explicit valid negative result; cautious candidate-specialization wording.

### C09

- Strongest competing precedent per proposed contribution; primary citation per source-backed claim; retained dates/queries/status; no absence-as-proof wording; reframing on near-duplicate; conclusions regenerable from matrix.

### C10

- Independent single-machine clean rerun within tolerance; scripts/raw inputs for tables/figures; compatible code/data/model licenses; report/tag/manifest agreement; exact run IDs for primary claims; no prohibited implication.

## Validation commands

Minimum gate after every integrated slice:

```powershell
.venv\Scripts\python.exe scripts\local_readiness_check.py
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe scripts\validate_bundle.py
```

Release gate additionally includes:

```powershell
.venv\Scripts\python.exe scripts\run_demo.py
.venv\Scripts\python.exe scripts\run_benchmark.py --episodes 40 --steps 30
.venv\Scripts\python.exe -m sparkbrain.evaluation.run_suite --config configs\experiments\phase1\main.json
.venv\Scripts\python.exe scripts\reproduce_release.py --profile smoke --offline
```

Task-specific training, baseline, external-adapter, Brain Lab, spiking, structural, artifact-hash, and clean-environment commands will be added before their slice is marked complete.

## Documentation updates

- Per behavior: `SOFTWARE_ARCHITECTURE.md` and/or `EXPERIMENT_PROTOCOL.md`.
- Per task: `PROJECT_STATUS.md`, `RESULTS_LEDGER.md`, `CLAIMS_REGISTER.md` when evidence wording changes.
- Contract decisions only: append `DECISION_LOG.md`.
- C09: prior-art, sources, matrix, search log, closest systems.
- C10: README, technical report, artifact evaluation, notices, manifest, changelog, and release metadata.

## Local execution contract

- Mandatory path: Python 3.11+ CPU on one local machine.
- Optional accelerators may not remove the CPU smoke/reference path.
- No mandatory remote API, hosted database, queue, tracker, storage, authentication, CDN, analytics, or hosted font.
- Runtime outputs use explicit local paths and never upload silently.
- UI binds to `127.0.0.1` or runs as static files.
- External datasets may be downloaded only during documented setup; primary evaluation then uses a versioned local cache offline.

## Rollback boundary

- Preserve the existing `94be973` baseline and unrelated user history.
- Commit each accepted C-task slice independently.
- Generated raw result directories are immutable; regenerate aggregates into new task/version paths.
- Revert a failed slice by reverting only its scoped commit; never reset the repository or rewrite unrelated history.
- Schema migrations remain additive/versioned; do not silently reinterpret existing `0.2` artifacts.

## Plan updates

- Initial plan created after repository/readiness audit and before new C01-C10 edits.
- Assumptions disproven during implementation are retained here with a dated correction rather than deleted.

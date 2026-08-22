# C05 Matched Baselines Implementation Plan

## Scope and frozen inputs

- C02 `Episode`, world generators, split manifests, and their preprocessing boundary are the only dataset source.
- Dev manifests select vocabulary, thresholds, hyperparameters, and quality-matching checkpoints. Frozen test manifests are read only after selection and are never used for tuning.
- C02 manifest/content SHA-256 hashes recorded before implementation (the earlier
  40-character audit values were Git blob SHA-1 and are not used as acceptance hashes):
  - `dev-v1.json`: `968593ff7c5f4274aaeb416bd58200e8625218d1a0179a1dff8a31d1b82a85a8`
  - `test-v1.json`: `3815f3857c485fb6c596f496c00ce36c437ee3b17fd97105d0fb729ff16e9e20`
  - `c02-main-1000/run_manifest.json`: `f838fc13af0466c7c390a4d74c5a469ddb429c4ec8adda867e0d8c149bea96a1`
  - `c02-main-1000/split_manifest.json`: `8dd47a7c78be8600f3e5fa5bfd125b88e2bdaf5562596490e7e2019811a17ffe`

## Package and compatibility design

1. Replace `src/sparkbrain/baselines.py` with a `sparkbrain.baselines` package.
2. Preserve `BaselineStep`, `EvidenceAccumulator`, `HardWinnerTakeAll`, `InstantClassifier`, and `run_baseline` through `baselines/__init__.py` re-exports.
3. Define a shared streaming protocol with `reset`, `step`, `predict_proba`, `state_trace`, and `work_counters`. Inspection methods must not mutate state or counters.
4. Keep deterministic/probabilistic baselines dependency-free. Put PyTorch models and training behind the optional `learned` extra; core dependencies remain empty.

## Baseline families

- Existing dense accumulator, privileged Bayes filter using declared world-generative information, and a causal HMM whose transition/emission tables use train-only counts with Laplace smoothing.
- GRU and LSTM recurrent classifiers.
- Causal Transformer with an explicit context limit of 64 and causal/key-padding masks.
- Four-module, top-two active GRUCell modular recurrent baseline, labeled `RIM-like`; it is not represented as an exact RIM paper reproduction.
- Explicit-state memory model with a learned log-belief update and inspectable belief vector.
- Oracle and chance bounds, excluded from learned-model matched rankings.

## Common data contract

- Encode only observation-side fields: channel, source, object, evidence label, signed strength, reliability metadata when observed, delivery delta, and current goal.
- Truth, decision-justified flags, optimal action, scenario tags, and evaluator annotations stay evaluator-only.
- Fit categorical vocabularies on train episodes only; map dev/test unknowns to `UNK`.
- Use identical episode IDs, splits, ordered steps, tensors, reset boundaries, and trial budgets for all eligible families. Persist input hashes for audit.
- Keep multi-object targets per object and causal sequence padding/masking explicit.

## Fair matching and selection

- Final learned seeds: `101, 211, 307, 401, 503`; paired evaluation uses identical C02 episode seeds.
- Parameter matching: exact trainable named-parameter count, accepted within ±2% of the configured target. Zero-parameter systems report state bytes separately.
- Training-compute matching: report the common optimizer-work proxy separately from
  family-specific recurrent/attention/state estimates and measured CPU profiling. Only the
  latter may satisfy the scientific ±5% criterion; otherwise retain an explicit failure.
- Quality matching: first dev-only checkpoint within 1 percentage point all-step accuracy and 2 percentage points coverage of target. Unattained matches remain explicit negative results.
- Equal tuning budget: 12 declared trials per trainable family; deterministic families receive the same number of declared smoothing/threshold/context candidates. Test results are unavailable to selection code.
- `best_reasonable` is reported separately (≤250k parameters and context ≤128) and never mixed into matched rankings.

## Profiling, statistics, and artifacts

- Report parameters, checkpoint/state bytes, analytical operations, state/message updates, attention positions, CPU p50/p95 wall time, and optional `torch.profiler` CPU/profile-memory measurements.
- Do not infer energy use from operations, activity, or wall-clock.
- Retain per-seed/per-episode rows, failures, paired episode differences, bootstrap intervals, paired sign-flip tests, effect sizes, and Holm-adjusted p-values.
- Generate model cards with assumptions, information access, reset/context policy, parameter/compute regime, deviations, limitations, and observed failures.
- Store outputs under `artifacts/phase2/baselines/<run-id>/` with resolved config and run manifest.

## Runtime profiles

- `smoke`: all ten families, one run seed, reduced local C02 episodes, ≤20k trainable parameters, ≤50 optimizer steps, CPU-only, hard process deadline 600 seconds.
- `acceptance`: five learned seeds and the frozen config; each trial/final seed has an explicit deadline and any timeout is retained as failure. Do not silently reduce seeds.
- The committed acceptance artifact records what was actually executed, including negative or incomplete matches.

## Verification and acceptance matrix

1. Old baseline imports/results remain compatible.
2. Protocol behavior, reset, probability normalization, inspection non-interference, state trace, and work counters are tested for every family.
3. Data leakage/adversarial unknown-token and identical-input-hash tests pass.
4. Bayes privilege and HMM train-only causal estimation are distinguished in code, cards, and report.
5. Neural masks, context 64, explicit reset, and RIM-like wording are tested.
6. Five seeds and exact episode pairing are present in acceptance configuration.
7. Parameter ±2%, compute ±5%, dev quality matching, and equal trial budget are machine-validated.
8. Coverage and correctness remain separate; oracle/chance are labeled bounds.
9. CPU smoke completes under the hard ten-minute cap.
10. Optional dependency and offline/core-empty boundaries pass readiness checks.
11. Generated schema/artifacts validate and C02 frozen hashes are unchanged.
12. Full pytest, Ruff, readiness, bundle validation, and documented reproduction commands pass.

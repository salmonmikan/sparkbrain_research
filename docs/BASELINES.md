# C05 Matched Baselines

C05 compares ten local baseline families through one C02 `Episode` pipeline. The core
reference engine still has no mandatory runtime dependency. Learned families require the
optional `learned` extra and run on CPU after installation.

## Reproduction

```powershell
python -m pip install -e ".[dev,learned]"
python -m sparkbrain.evaluation.run_baselines --config configs/experiments/phase2/baselines_smoke.json --output artifacts/phase2/baselines/<new-smoke-run>
python -m sparkbrain.evaluation.run_baselines --config configs/experiments/phase2/baselines_acceptance.json --output artifacts/phase2/baselines/<new-acceptance-run>
```

The output directory must be new or empty. Both profiles are CPU-only and need no network
at runtime. `smoke` has a hard 600-second deadline. The committed reduced acceptance run
uses five learned seeds and records PyTorch version, deterministic-algorithm mode, thread
count, exact C02 SHA-256 values, input hashes, raw rows, matching checks, failures, and
paired statistics, local checkpoints, and deterministically selected incorrect-step traces.

## Information boundary

The encoder sees only `Observation` fields. Vocabulary is fitted on the training half of
C02 dev episodes; unknown dev/test values map to `UNK`. Truth, justified-decision flags,
actions, tags, and annotations remain in the evaluator/training-target side. The frozen
test split is never passed to selection code. Oracle is an evaluator-only upper bound.
Privileged Bayes uses repository-declared evidence weights and is not information matched.
Laplace HMM estimates its transition and emission tables from the training half of dev.

## Matching and limitations

The reduced acceptance profile targets 32,100 architecture-body parameters. Hidden/model/
module sizes are selected by a deterministic, performance-blind discrete search after the
train-only input dimension is known. No padding reserve is counted. Each family's body
parameter result is tested against ±2%; unattainable targets are negative results.

The former parameter-count proxy is retained only as `optimizer_work_proxy`. Family-specific
recurrent, attention, modular, and explicit-state analytical estimates plus measured CPU
p50/p95 are reported separately. The reduced profile does not achieve a defensible
scientific training-compute match within ±5%, so `scientific_compute_match` is false.

The failure-case artifact includes both learned and scalar/probabilistic rows. SparkBrain's
strongest known failure remains C02 MultiObjectWorld zero coverage; C05 does not rerun or
tune SparkBrain against these test rows.

The equal declared search allowance is 12 trials per family. The committed reduced run
does not claim a completed 12-trial scientific search; it machine-checks budget equality
and executes one deterministic reduced configuration per seed. Dev-only confidence
thresholds align abstention semantics. Quality matching is checked against accumulator
dev accuracy (±1 percentage point) and coverage (±2 points); failure remains a negative
result.

The committed corrected acceptance profile is a local integration measurement, not the full frozen
1,000-episode-per-world scientific comparison. It showed that quality matching was not
achieved for every learned seed/family after ten optimizer steps. Test accuracy is retained
without favorable filtering in `aggregate_metrics.json`. No general superiority, energy,
biological, or exact-RIM-reproduction claim follows.

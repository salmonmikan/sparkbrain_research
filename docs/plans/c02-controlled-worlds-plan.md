# C02 Controlled Worlds Implementation Plan

## Gate and scope

- Base commit: `c5178db` (accepted C01).
- Branch/worktree: `codex/c02-controlled-worlds` / `C:\55_personal\sikou\sparkbrain-c02`.
- Preserve C01 backend, trace, configuration, replay, and schema contracts.
- Preserve the Phase-0 SwitchWorld commands and generated-output semantics.
- Do not add language encoders, neural training, live UI, remote services, or energy claims.

## Implementation sequence

1. Add strict versioned Episode, Observation, Target, and result contracts.
2. Add deterministic SwitchWorld compatibility plus Reliability, DelayedEvidence,
   Contradiction, MultiObject, and GoalConflict worlds.
3. Add a shared ablation registry and runner for all required conditions.
4. Add hand-testable metrics, paired episode bootstrap intervals, multiple-comparison
   labeling, and Pareto dominance output.
5. Add immutable run manifests, per-episode JSONL, aggregates, failure artifacts, and a
   single-command report generator.
6. Run a CPU runtime probe, freeze the test manifest before the final run, and execute
   1,000 test episodes per declared main condition when the measured runtime permits.
7. Update protocol, architecture, project status, results ledger, and claims register.
8. Run task-focused tests and the full local validation gate before committing.

## Data contracts

`Observation` is backend-visible and contains only event identity, timing, routing, and
strength fields. Truth, answers, and evaluation targets are rejected from its metadata.
`Target` is evaluator-only and contains belief truth, whether a decision is justified,
optional action truth, update-needed state, and scenario annotations. `Episode` binds a
world/version, split, seed, generator-config hash, and ordered steps. Emission time and
delivery time remain distinct for delayed evidence. Duplicate propagation reuses one
evidence ID; independent observations receive distinct IDs.

## World responsibilities

- SwitchWorld: retain canonical CAT -> TOY -> CAT and randomized Phase-0 compatibility.
- ReliabilityWorld: calibrated source reliability, correlated sources, reliability shifts,
  and duplicate evidence-ID delivery.
- DelayedEvidenceWorld: delayed/out-of-order delivery and intentionally unresolved periods.
- ContradictionWorld: external support/contradiction from same and independent sources;
  internal lateral inhibition never becomes contradiction evidence.
- MultiObjectWorld: object-scoped Spark IDs, competition groups, evidence, and Coalitions.
- GoalConflictWorld: belief truth remains separate from goal-conditioned action selection.

World generators are pure seeded data generators. Engine construction and observation
delivery belong to the evaluation adapter/runner.

## Ablation mapping

All conditions use one registry with config overrides, graph transforms, or explicit runner
policies. Base graphs/configs are copied per run.

- `full`: no change.
- `no_residual`: zero persistent-state residuals.
- `hard_wta`: erase losing hypothesis state after a winner is selected, using only the
  smallest explicit engine intervention hook if C01 lacks a suitable public operation.
- `no_lateral_inhibition`: remove only `lateral_inhibition` edges.
- `no_source_diversity`: remove both diversity score and diversity gate.
- `no_contradiction_penalty`: remove only the Coalition contradiction term.
- `no_temporal_stability`: remove stability bonus and gate.
- `no_margin_gate`: set the margin requirement to zero.
- `single_spark_ignition`: remove source-diversity/Coalition cardinality only.
- `forced_prediction`: preserve dynamics but label evaluator fallback predictions.
- `dense_update_accounting`: report counterfactual dense work separately from executed work.
- `no_workspace_broadcast`: retain ignition/Workspace, remove broadcast listeners.
- `no_homeostasis`: remove threshold increment.
- `no_refractory`: remove refractory delay.

Smoke covers every world/condition combination. The main matrix uses all full worlds and
pre-registered mechanism-relevant world/ablation pairs; each declared main condition targets
1,000 frozen test episodes.

## Metrics and statistics

- Preserve coverage, all-step/decided accuracy, revision precision/recall, latency,
  unnecessary revision, recovery, false ignition, and work counters.
- Add multiclass Brier score and fixed-bin ECE only when a declared score-to-probability
  mapping is available; otherwise emit an explicit not-applicable reason.
- Report appropriate abstention and missed-decision rates separately.
- Add false certainty, paired source-reliability sensitivity, duplicate-evidence inflation,
  object cross-talk, belief-flip-under-goal-change, and action response accuracy.
- Report active-node/edge work using mean, p50, p95, p99, and max.
- Bootstrap paired episode IDs with a fixed bootstrap seed and 95% episode-level intervals.
- Apply Holm correction to declared primary comparisons; label exploratory comparisons.
- Compute Pareto dominance from false/unnecessary revision (minimize), revision/recovery
  (maximize), and latency (minimize); do not select one scalar winner.

Every metric receives a small hand-computed unit test, including empty-denominator and
not-applicable behavior.

## Artifact layout

Each run writes once to `artifacts/phase1/<run_id>/`:

```text
run_manifest.json
resolved_config.json
split_manifest.json
software_versions.json
raw/<world>/<condition>.jsonl
aggregate/metrics.{json,csv}
aggregate/confidence_intervals.{json,csv}
aggregate/work_distributions.{json,csv}
pareto/frontier.{csv,svg}
failures/<episode_id>/{trace.json,visualizer.html,explanation.md}
failures/index.md
report.md
```

The run refuses to overwrite a non-empty directory. Raw episode rows link to config, split,
seed, status/error, metrics, counters, and any retained failure trace.

## Runtime estimate and final test freeze

For every main condition, run five warm-ups plus 25 measured episodes three times. Measure
generation, engine, metrics, raw writing, and reporting separately with `perf_counter`.
Forecast serial CPU time as the sum of `1,000 * median_seconds_per_episode` plus fixed report
overhead, and report a separate 20 percent contingency. Check extrapolation with a 100-episode
pilot and record Python/OS/CPU, episode lengths, graph sizes, and artifact bytes per episode.

Do not reduce the test count automatically. Any reduction must be decided before the frozen
test run and recorded with measured evidence, the new count, and the resulting scientific
limitations.

## Acceptance evidence

| Criterion | Evidence |
| --- | --- |
| Deterministic schema-valid worlds | same-seed identity, different-seed divergence, invalid/leakage tests |
| Hand-computed metrics | focused metric fixtures and edge-case tests |
| Shared ablation harness | parameterized registry test and full smoke matrix |
| Confidence intervals/raw links | deterministic paired bootstrap tests and manifest link validation |
| Pareto dominated systems | known-dominance unit test plus generated CSV/SVG |
| Three explained failure cases | deterministic category selector and trace/HTML/explanation triplets |
| No test tuning | disjoint frozen dev/test manifests and config-hash enforcement |
| Documentation current | protocol, architecture, status, results, claims updates |
| Local/offline reproduction | one `sparkbrain.evaluation.run_suite` command and local readiness gate |
| 1,000 test episodes | per-condition manifest counts or a pre-run measured limitation record |

## Validation

```powershell
.venv\Scripts\python.exe -m sparkbrain.evaluation.run_suite --config configs\experiments\phase1\smoke.json --output artifacts\phase1\<smoke-run-id>
.venv\Scripts\python.exe scripts\local_readiness_check.py
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe scripts\validate_bundle.py
.venv\Scripts\python.exe scripts\run_demo.py
.venv\Scripts\python.exe scripts\run_benchmark.py --episodes 40 --steps 30
```

## Known implementation risks

- Existing Phase-0 routing uses evidence labels as source identities; C02 must preserve true
  source IDs without changing the compatibility fixture.
- Duplicate evidence IDs deduplicate Coalition records but can still inflate activation;
  retain and report this as a possible negative result.
- The old single-Spark ablation also removed stability. C02 separates those mechanisms.
- Hard-WTA may require one explicit state-erasure hook; no other shared-engine modification is
  planned.

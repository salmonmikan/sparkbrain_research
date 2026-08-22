# Results and Negative-Result Ledger

Append entries; do not rewrite prior outcomes to match later interpretations.

## 2026-08-22 — R0001 — Phase-0 SwitchWorld software validation

**Code/version:** SparkBrain prototype v0.2 bundle  
**Command:** `python scripts/run_benchmark.py --episodes 40 --steps 30`  
**Data:** seeded synthetic SwitchWorld; hand-authored evidence mapping  
**Raw outputs:** `artifacts/benchmarks/benchmark_results.json`  
**Aggregate:** `artifacts/benchmarks/benchmark_aggregate.csv`

### Observations

- full SparkBrain all-step accuracy was 0.6400 and coverage 0.9367;
- accumulator all-step accuracy was 0.6283, so the full system did not clearly dominate this simple baseline;
- removing residual state reduced accuracy to 0.4567 and coverage to 0.8183 in this distribution;
- single-Spark ignition improved revision precision relative to full SparkBrain but worsened latency and recovery in some measures;
- instant classification revised rapidly but produced many unnecessary revisions;
- algorithmic active-Spark counts are not hardware energy measurements.

### Interpretation

This run validates that the software exposes a stability/revision trade-off and that the selected ablations alter it. It does not establish generalization, learning ability, biological fidelity, or modern-model superiority.

### Negative or inconvenient findings retained

- the accumulator baseline is competitive;
- the reference engine's event fan-out can yield more Spark updates than a scalar baseline;
- hand-authored evidence weights may encode much of the task solution;
- some Phase-0 metrics are sensitive to coverage and forced-prediction differences.

### Follow-up

C01 must audit counters and replay; C02 must add controlled distributions and confidence intervals; C04/C05 must replace hand-authored-only comparisons with learned matched systems.

---

## Entry template

```text
## YYYY-MM-DD — R#### — title
Code/version:
Command:
Data/splits:
Seeds:
Raw outputs:
Aggregate:
Hypothesis:
Result:
Negative findings:
Confounds:
Claim grade impact:
Next action:
```

## 2026-08-23 — C05 matched-baseline reduced acceptance (ID assigned at integration)

**Command:** `python -m sparkbrain.evaluation.run_baselines --config configs/experiments/phase2/baselines_acceptance.json --output artifacts/phase2/baselines/c05-acceptance-final`
**Data/splits:** C02 frozen dev/test manifests; four episodes per world in this reduced run
**Seeds:** learned seeds 101, 211, 307, 401, 503; paired C02 episode seeds
**Raw outputs:** `artifacts/phase2/baselines/c05-acceptance-final/raw_results.json`
**Aggregate:** `artifacts/phase2/baselines/c05-acceptance-final/aggregate_metrics.json`

### Result

- all ten baseline families completed locally in 29.7 seconds on the recorded CPU setup;
- architecture-body parameter counts were within ±2% of the 32,100 target without a
  padding reserve; the common optimizer-work proxy was within ±5%;
- frozen C02 input-file SHA-256 values were identical before and after execution;
- the privileged Bayes diagnostic reached 0.8125 all-step accuracy and oracle 1.0, but
  these are explicitly privileged bounds and not matched competitors.

### Negative findings and confounds

- quality matching against accumulator dev accuracy/coverage was not achieved for every
  learned seed/family after ten optimizer steps;
- learned test accuracy varied widely by seed; the compact Transformer reached as low as
  0.0556 and explicit-state memory showed unstable/high loss in some runs;
- the reduced run executed one configuration per seed, not a completed 12-trial search or
  the full 1,000-episode-per-world frozen matrix;
- family-specific analytical work and CPU profiler results did not establish a scientific
  training-compute match; `scientific_compute_match` is retained as false;
- all timing and operation counts are local compute observations, not energy evidence.

**Claim impact:** CL-007 remains E0. The result validates the harness and records a negative
quality-matching outcome; it does not support general superiority.

---

## 2026-08-23 — R0006 — C02 controlled synthetic suite

**Code/base:** C02 branch from accepted C01 `c5178db`; schema remains `0.2`
**Command:** `python -m sparkbrain.evaluation.run_suite --config configs/experiments/phase1/main.json --output artifacts/phase1/c02-main-1000`
**Data/splits:** frozen local test seeds 200000–200999; 37 declared conditions; 1,000 episodes per condition
**Raw outputs:** `artifacts/phase1/c02-main-1000/raw/` (local, reproducible, approximately 492 MiB)
**Aggregate:** `artifacts/phase1/c02-main-1000/aggregate/metrics.json`

### Result

- SwitchWorld full accuracy was 0.5965, coverage 0.9234, revision recall 0.6839,
  revision precision 0.6761, and mean switch latency 1.6196.
- Removing residual state reduced SwitchWorld accuracy to 0.4180 and delayed-evidence
  accuracy from 0.7035 to 0.4573 in these frozen synthetic distributions.
- Hard-WTA reduced SwitchWorld recovery from 0.7240 to 0.5636 and delayed-evidence recovery
  from 0.9284 to 0.8136.
- GoalConflictWorld changed actions while the measured goal-only belief-flip rate remained
  zero. This is a narrow implementation observation, not a cognitive claim.

### Negative findings and confounds

- MultiObjectWorld full-system coverage and all-step accuracy were both zero: the frozen
  configuration did not ignite object-scoped beliefs. The failure is retained.
- Duplicate evidence produced a non-zero paired score change on average; evidence-record
  identity deduplication does not guarantee activation-level invariance.
- The supplementary frozen reliability run reported source-reliability sensitivity of
  0.0175 for the full condition; this small descriptive difference is not a calibrated
  reliability claim.
- Coalition softmax values were used only for descriptive Brier/ECE; they are not calibrated
  probabilities.
- The generators and evidence weights remain hand-authored, and no learned or modern matched
  baseline is present. No general superiority claim is supported.
- Main bootstrap intervals are descriptive. No p-value family or significance-ranking claim
  was made.

**Claim impact:** CL-003 and CL-006 remain E2; CL-007 remains E0.
**Next action:** C04/C05 consume the immutable Episode/split contracts without tuning on C02
test seeds. Multi-object ignition requires dev-only diagnosis before a new frozen evaluation.

---

## 2026-08-22 — R0002 — v0.2.1 local-scope and documentation expansion

**Code/version:** SparkBrain package v0.2.1; persisted schema v0.2  
**Nature:** documentation, local-execution contract, validation guard; no intended dynamics change  
**Primary commands:** `python scripts/local_readiness_check.py`, `python -m pytest -q`, `python scripts/validate_bundle.py`

### Changes under test

- core completion constrained to one general-purpose local computer;
- CPU reference path made mandatory;
- remote runtime services excluded from core dependencies;
- dedicated hardware moved to Extension H;
- beginner foundation guide and expanded glossary added;
- local-readiness checks added;
- package version advanced to 0.2.1 while schema remains 0.2.

### Scientific result

None claimed. This patch does not increase the evidence grade of H1–H10 or establish a performance improvement.

### Validation outcome

- local readiness: PASS on Python 3.13.5 / Linux x86_64;
- tests: 30 passing;
- canonical demo: CAT → TOY → CAT reproduced;
- checkpoint state hash: `cedc8543d87677d2cbf1707f0df2ec7d95e8a1d31b735a40a917d9de9d7ff13c`;
- bundle validation: 23 required artifacts validated;
- benchmark aggregate CSV: byte-identical to archived v0.2;
- canonical trace JSON: byte-identical to archived v0.2;
- ruff: not executed in the packaging environment because it was not installed.

### Compatibility target

The Phase-0 dynamics and persisted config/state/trace schema are intended to remain compatible with v0.2. The byte-identical benchmark aggregate and canonical trace support that narrow compatibility statement for the bundled scenarios; they do not prove compatibility for every possible checkpoint or graph.

---

## 2026-08-23 — R0003 — C01 deterministic reference and replay contract

**Code/version:** SparkBrain package v0.2.1; persisted schema v0.2
**Nature:** reference-engine hardening and compatibility validation; no intended dynamics change
**Primary commands:** `python -m pytest -q`, `python -m ruff check .`, `python scripts/local_readiness_check.py`, `python scripts/validate_bundle.py`

### Changes under test

- deterministic continuation includes the pending event queue, sequence counter, RNG, stability, Workspace, eligibility, counters, trace, and frame-local audit buffers;
- pure `inspect_snapshot()` is separated from backward-compatible recording `snapshot()`;
- generated config, checkpoint, trace, summary, and benchmark JSON are validated against schema `0.2`;
- `broadcast_listeners` is required by both runtime and JSON Schema validation;
- equal-time ordering, event-limit diagnostics, invalid payloads, evidence identity, contradiction provenance, no-ignition, recovery, cooldown, refractory, homeostasis, Workspace, and plasticity boundaries are covered by focused tests.

### Validation outcome

- local readiness: PASS;
- tests: 55 passing;
- Ruff: PASS;
- fresh canonical state hash: `ba166f0e801665e98c200f8a291fdf475f2dbbc6d86232867e21b1f08226caa5` on two independent runs;
- normalized fresh-run traces: identical;
- generated-artifact schema regression: PASS;
- Phase-0 benchmark aggregate values: unchanged; persisted JSON documents gained explicit schema metadata only.
- GitHub Actions CI: PASS on Python 3.11 and 3.13, run `32594805438`.

### Compatibility and limitations

Schema remains `0.2`; no migration is introduced. The stricter validators reject incomplete payloads that omitted required deterministic state, including `broadcast_listeners`. This is validation hardening rather than reinterpretation of valid v0.2 artifacts. The clean CI matrix passed on the two repository-supported Python versions; this does not establish compatibility with untested environments.

---

## 2026-08-23 — R0004 — C03 localhost Brain Lab acceptance

**Code/version:** SparkBrain package v0.2.1; persisted engine schema v0.2; Brain Lab schema v1
**Nature:** optional local UI/control plane; no intended core dynamics change
**Primary commands:** `python -m pytest -q`, `python -m ruff check .`, `python scripts/measure_brain_lab.py`, `python scripts/run_brain_lab.py`

### Changes under test

- loopback-only FastAPI control plane and bundled no-CDN frontend;
- nine UI regions for graph, timeline, belief, Workspace, inspection, control, intervention, comparison, and export/import;
- deterministic pause, single-step, run, reset, and validated event injection;
- parent-preserving checkpoint fork with edge, Spark, organ, and threshold interventions;
- frame-index synchronized comparison, blind-safe API/export, and local bundle import;
- static visualizer fallback and pure-inspection non-interference.

### Validation outcome

- tests: 68 passing, including 13 focused Brain Lab API/service/E2E contract tests;
- Ruff: PASS;
- canonical UI/API flow: CAT → TOY → CAT with evidence provenance;
- 2,000-Spark / 10,000-edge relevant-subset preparation: 0.9654 ms for 250 Sparks / 600 edges;
- 60 FPS preparation budget (16.6667 ms): PASS;
- loopback startup and non-loopback rejection: PASS;
- offline bundled assets, keyboard/focus/accessibility contract, blind truth removal, and import/export regression: PASS.

### Limitations retained

- the measured time covers deterministic subset preparation, not browser paint or end-to-end frame time;
- the run registry is in-memory and single-process; exported bundles are required across restarts;
- SSE reports a finite current-frame snapshot and does not create a background simulation queue;
- the native SVG graph is a functional view, not a biological anatomy claim;
- no energy-efficiency claim follows from UI timing.

---

## 2026-08-23 — R0005 — C07 reduced snnTorch hybrid equivalence

**Code/version:** `codex/c07-spiking-backend`; schema `0.2` unchanged
**Command:** `python scripts/run_spiking_comparison.py`
**Data/seed:** fixed seven-event SwitchWorld CAT→TOY→CAT; seed 7
**Raw outputs:** `artifacts/spiking/c07_comparison.json`, `rate_trace.json`, `spike_trace.json`
**Aggregate:** `artifacts/spiking/c07_report.md`

### Result

- all 9 frozen comparison checks passed;
- hybrid predictions exactly matched `[None, cat, cat, cat, toy, toy, cat]`;
- distinct ignition order matched `[cat, toy, cat]`;
- focused tests preserved no-ignition, duplicate evidence, residual recovery, Workspace
  capacity, directional edge ablation, protocol conformance, and state replay.

### Negative findings and confounds

- LIF threshold 1.1 produced no sensory spikes and no predictions;
- equivalence is parameter-sensitive and covers one hand-authored scenario;
- only sensory encoding is spiking; Coalition and Workspace remain algorithmic/rate;
- local wall-clock is not an energy measurement;
- no fully spiking, learned, surrogate-gradient, or local-plasticity comparison was done.

### Claim impact

CL-009 advances only to E1 for this reduced hybrid canonical fixture. It does not establish
general spiking equivalence, biological fidelity, efficiency, or multi-world robustness.

---

## 2026-08-23 — R0007 — C03 import boundary and C07 queue-order correction

**Nature:** acceptance and safety correction; no scientific claim increase
**Primary commands:** `python -m pytest -q`, `python -m ruff check .`, `python scripts/run_spiking_comparison.py`, `python scripts/validate_bundle.py`

### Corrected contracts

- Brain Lab import enforces a 25 MiB serialized limit and strict agreement among metadata, checkpoint, trace, figure data, and event manifest before creating a run;
- blind imports reject visible truth and export paths remain confined to the artifact root;
- hybrid LIF state advances when events leave the deterministic queue, preserving time, priority, and sequence order instead of caller scheduling order;
- pending LIF events remain checkpointable across an event-limit interruption;
- CI installs the optional spiking dependencies before executing the full test suite.

### Validation outcome

- focused Brain Lab/C07 tests: 25 passing;
- full tests: 113 passing;
- Ruff, local readiness, dependency check, and 55-file bundle validation: PASS;
- C07 frozen comparison: 9/9 checks remain PASS;
- trace schema, reset, internal generated events, reverse scheduling, equal-time ordering, checkpoint continuation, oversize import, malformed import, blind behavior, parent preservation, and artifact-root confinement are covered.

### Claim impact

None. The correction removes causal-order and import-validation defects without expanding the single-scenario hybrid evidence boundary recorded in R0005.

---

## 2026-08-23 — R0008 — C04 learned sparse routing on controlled held-out worlds

**Nature:** controlled synthetic learned-backend result with explicit negative diagnostics  
**Run:** `artifacts/phase2/learned-routing-v1/main`  
**Config:** `configs/experiments/phase2/main.json`

### Outcome

- 60 frozen test episodes / 2,160 steps completed on local CPU in 45.433 seconds;
- all-step accuracy 0.66343 exceeded chance 0.33333 and the training-majority non-learning baseline 0.33981;
- coverage was 0.77963, covered accuracy 0.85095, no-ignition count 476, and loser-recovery count 84;
- actual indexed recurrent work selected 8,640 module updates and evaluated 34,560 edges/messages from 25,920 conceptual candidates, while 4,320 dense encoder/router operations remained separately counted;
- all 11 required ablations and five sensitivity rows were emitted after development-only ignition calibration.

### Boundaries and negative findings

- the reduced smoke profile was below chance;
- the main router retained three dead modules, four overloaded modules, and normalized load entropy 0.6698;
- natural unseen evidence bigrams in the primary subset were zero, so compound/distractor stress tests remain separately labeled derived evaluations;
- only 60 of the frozen 1,000 C02 test seeds were evaluated, the encoder/router remain dense, and the random-router condition was not retrained;
- this result supports only controlled-synthetic learned no-ignition and routing behavior. It does not support CL-007, Transformer superiority, external generalization, biological fidelity, or energy claims.

### Verification

The integrated tree passed 134 tests, Ruff, local readiness, and bundle validation. C02 dev/test manifest SHA-256 values remained unchanged before and after the experiment.

# Experimental Protocol — Local-First v0.2.1

## 1. Purpose

SparkBrain の目的は「脳っぽく見えるアニメーション」を作ることではなく、明示した計算原理がどの条件で有効・無効かを反証可能にすることである。

中心評価軸:

1. beliefを形成できるか
2. evidence不足時に判断を保留できるか
3. noiseで不用意に変更しないか
4. decisive evidenceで変更できるか
5. 過去のloserへ復帰できるか
6. 全Sparkを常時計算せず成立するか
7. learned settingでも成立するか

## 1.1 Local execution discipline

Core experiments must run on one general-purpose local computer. A CPU reference configuration is mandatory; local GPU acceleration is optional. Runtime cloud services, remote model APIs, hosted experiment trackers, and remote storage must not be required. External datasets may be acquired during setup, but final evaluation must run from a versioned local cache.

Dedicated hardware and physical energy measurement are outside the core phase gates and are tracked only under Extension H.

## 2. Experimental layers

### Phase 0 — Software and dynamics validation

Purpose:

- 実装が仕様どおり動く
- traceとvisualizerがstateを正しく反映
- canonical belief revisionが成立
- basic ablationが実行可能

Data:

- hand-authored SwitchWorld
- hand-authored evidence weights

Claims allowed:

- implementation behavior only

### Phase 1 — Controlled synthetic science

Purpose:

- H1–H5を独立に検証
- noise、delay、switch rate、source reliabilityを系統的に操作

Required worlds:

1. `SwitchWorld`: hidden categorical state changes
2. `ReliabilityWorld`: sensors have different and changing reliability
3. `DelayedEvidenceWorld`: decisive evidence arrives late
4. `ContradictionWorld`: mutually contradictory sources
5. `MultiObjectWorld`: multiple simultaneous belief groups
6. `GoalConflictWorld`: perception and current goal bias compete

### Phase 2 — Learned routing

Purpose:

- hand-authored evidence mapを除去
- event embeddingからrelevant Spark top-kを学習
- held-out combinationsへ一般化

Data split must separate:

- event combinations
- state transition patterns
- noise regimes
- source identities

C04 freezes the C02 dev/test manifests by SHA-256. Training and ignition calibration use
disjoint development-seed ranges; threshold selection never reads test labels. The CPU smoke
profile proves offline execution only. The main profile holds out ReliabilityWorld and
DelayedEvidenceWorld from training, uses longer sequences, reports chance and training-majority
baselines, and keeps accuracy separate from ignition coverage. Sparse counters distinguish
candidate routes, selected state updates, evaluated selected edges/messages, remaining dense
encoder/router operations, estimated launches, tracked memory, and wall-clock. Required
ablations and coefficient sensitivity are machine-readable under `artifacts/phase2/`.

### Phase 2.5 — Structural plasticity (C08)

C08 freezes the accepted C04 checkpoint/config and C02 development/test manifests by SHA-256.
Structural adaptation reads development episodes only. Candidate discovery is limited to
routing load, coactivation, edge credit, and confidence delta; world/function/truth labels are
excluded. Held-out results never select thresholds or candidates.

The primary comparison is paired unablated, targeted candidate ablation, matched random
ablation, degree-matched ablation, activation intervention, and frozen C04 source evaluation.
Multiplicity, decisiveness, fertility, and specificity thresholds are declared in config.
Passing all four is required for a specialization claim; otherwise E0 and negative-result
wording are mandatory. Graph fragmentation, permutation selectivity, event history, actual
active-edge work, and event-budget sensitivity are recorded as diagnostics, not Gate overrides.
Specificity fixes a unique positive target on development intervention data before test. Test
then separately requires target impairment and caps unrelated collateral; a missing or tied
development target fails closed.

### Phase 3 — External reasoning benchmarks

Candidate tasks:

- Belief-R for update/retain decisions
- CLUTRR-like relational changes
- synthetic non-monotonic rule streams
- partially observable control tasks

External task adapters must preserve sequential evidence instead of flattening all premises into one input.

#### C06 foundation contract

Belief-R is the official `CAiRE/belief_r` Hugging Face test split pinned by full revision,
size, SHA-256, CSV header, row count, and `time_t`/`time_t1` pair counts. It is never split
into development data and is never used for training, tuning, prompt selection, threshold
selection, or early stopping. Adapter and model choices must be frozen on separate Track B
or other licensed development data before one final Belief-R run.

Track B uses seeded symbolic non-monotonic streams with template-family group splits, not
example-level random splits. Track C transforms observations only; evaluator Targets are
aligned afterward through returned source indices. External text stays in a gitignored local
cache, and evaluation after acquisition must succeed with network access blocked.

The model execution gate remains closed until C04 learned routing and C05 matched baselines
are integrated. Foundation utilities and their tests do not constitute Gate P3 evidence.

### Phase 4 — Local spiking equivalence

Purpose:

- rate-based behavioral contractをNorse/snnTorch/Nengo backendで再現
- spike timing、activity/message counts、local CPU/GPU latencyを測る

Do not tune the spiking model only for final accuracy. Compare internal dynamics:

- ignition order
- switch points
- recovery
- workspace sequence
- coalition membership or decoded equivalent

### Phase 5 — Local final integration and clean-room reproduction

Purpose:

- one local machineでengine、World、Visualizer、benchmark、reportを統合する
- dependency/data setup後にnetworkを切断して主要結果を再生成する
- CPU reference pathとoptional local accelerator pathを分離して報告する

### Extension H — Dedicated hardware measurement (outside core)

Purpose:

- supported dedicated hardwareでactual energy and latencyを測る

Only Extension H may support physical efficiency claims. It is not a core completion gate.

## 3. Baselines

### Phase 0 baselines

- dense evidence accumulator
- hard-WTA accumulator
- instant event classifier

### Required research baselines

- GRU with matched hidden-state budget
- Small Transformer with matched parameter/compute budget
- RIM or modular recurrent equivalent
- Bayes filter / HMM when world assumptions permit
- predictive-coding recurrent model where relevant

### Fairness controls

Report at least three matching regimes:

1. matched parameter count
2. matched approximate FLOPs / edge operations
3. matched wall-clock or latency on the same disclosed local hardware

A model may be better in one regime and worse in another. Do not compress all comparisons into a single rank.

## 4. Ablation matrix

| ID | Removed / changed | Tests |
|---|---|---|
| A1 | residual loser retention | recovery rate, latency |
| A2 | source diversity bonus | false ignition under duplicated evidence |
| A3 | contradiction term | resistance to counter-evidence |
| A4 | stability gate | noise-induced revisions |
| A5 | margin gate | ambiguous decisions |
| A6 | lateral inhibition | simultaneous incompatible ignitions |
| A7 | coalition; single Spark ignition | accuracy vs false ignition |
| A8 | no-ignition disabled | forced error rate |
| A9 | sparse routing disabled | compute and accuracy |
| A10 | workspace removed | cross-organ coordination |
| A11 | homeostasis removed | dominant Spark collapse |
| A12 | plasticity removed | adaptation to sensor reliability shift |

Each ablation changes one mechanism at a time unless explicitly labeled as a combined stress test.

## 5. Metrics

### 5.1 Task metrics

#### Coverage

\[
Coverage=\frac{\#\{t: prediction_t\neq\varnothing\}}{T}
\]

#### Accuracy on all steps

No-ignition is counted as incorrect where a decision is required.

#### Accuracy when decided

Separates selective prediction quality from coverage.

### 5.2 Revision metrics

#### Revision precision

\[
RP=\frac{correct\ belief\ changes}{all\ belief\ changes}
\]

#### Revision recall

\[
RR=\frac{truth\ changes\ eventually\ followed\ by\ correct\ belief}{truth\ changes}
\]

#### Switch latency

Number of events or elapsed time from true-state change to correct new belief.

#### Unnecessary revision

Belief changes while truth remains unchanged.

#### Recovery rate

A previously true label becomes true again and the system restores it within the segment.

### 5.3 Ignition metrics

- false ignition rate
- ignition count
- evidence-source count at ignition
- competitor margin
- no-ignition duration
- repeated broadcast rate

### 5.4 Calibration

Coalition score is not automatically a probability. If probability claims are needed:

- fit calibration mapping on validation data
- report Brier score
- expected calibration error
- reliability diagrams

### 5.5 Compute metrics

- unique active Sparks per external event
- active Spark fraction
- Spark state updates
- edge evaluations
- event queue operations
- peak queue size
- memory footprint
- wall-clock CPU/GPU
- kernel launch count where available
- physical hardware energy only in Extension H when directly measured

`active_spark_fraction` and energy are not interchangeable.

## 6. Statistical protocol

- use at least 30 independent seeds for synthetic experiments
- publish all seed-level results
- report mean, median, standard deviation, 95% bootstrap confidence interval
- predefine primary metrics before final test evaluation
- tune hyperparameters on train/validation only
- lock test seeds before final comparison
- report failed runs and numerical instability
- use paired comparisons on identical episode seeds
- correct or clearly label multiple hypothesis testing
- include effect sizes, not only p-values

## 7. Causal intervention tests

The architecture is inspectable, so use interventions rather than correlation alone.

### Intervention examples

- set one Spark activation to zero
- erase one evidence record
- duplicate an evidence source with same ID
- freeze one organ
- reverse one inhibitory edge
- force a loser hypothesis to retain or decay
- block workspace broadcast
- randomize routing while preserving degree

Expected outcome must be specified before execution.

## 7.1 C02 controlled-suite contract

C02 uses explicit `dev` and frozen `test` seed manifests. Defaults and score mappings may
be selected on dev seeds only. The main synthetic matrix uses 1,000 test episodes for each
declared world/ablation condition and retains per-episode JSONL locally.

The additional metrics are multiclass Brier score, fixed-bin expected calibration error,
appropriate abstention, missed decisions, false certainty, source-reliability sensitivity,
duplicate-evidence inflation, object cross-talk, belief/action disentanglement, and
distributions of Spark/edge work. Brier/ECE use a declared normalized score mapping and do
not turn Coalition score into a calibrated probability claim.

Uncertainty uses deterministic episode-level bootstrap 95% intervals. No p-value family is
reported in C02; therefore there is no uncorrected multiple-hypothesis significance claim.
The Pareto table minimizes unnecessary revision and latency while maximizing revision
recall. It identifies dominated conditions and does not choose one scalar winner.

Run locally with:

```bash
python -m sparkbrain.evaluation.run_suite \
  --config configs/experiments/phase1/main.json \
  --output artifacts/phase1/<new-run-id>
```

The output path must be new or empty. Runtime data is never uploaded.

## 8. Phase-0 current result

Generated by:

```bash
python scripts/run_benchmark.py --episodes 40 --steps 30
```

| model | all-step accuracy | coverage | revision recall | revision precision | switch latency | unnecessary revisions | recovery | active Spark fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SparkBrain | 0.6400 | 0.9367 | 0.6659 | 0.6142 | 1.3517 | 2.8000 | 0.6442 | 0.3628 |
| SparkBrain no residual | 0.4567 | 0.8183 | 0.5726 | 0.4976 | 1.9367 | 2.4750 | 0.6169 | 0.3191 |
| SparkBrain single-spark ignition | 0.5925 | 0.8900 | 0.6285 | 0.7396 | 2.0493 | 1.7750 | 0.6094 | 0.3287 |
| accumulator | 0.6283 | 0.9042 | 0.6499 | 0.6482 | 1.4226 | 2.5500 | 0.6475 | 1.0000 |
| hard WTA | 0.3375 | 0.9042 | 0.3776 | 0.0000 | 0.4730 | 0.0000 | 0.5077 | 1.0000 |
| instant | 0.6025 | 1.0000 | 0.8399 | 0.4068 | 0.4817 | 12.8000 | 0.8367 | 1.0000 |

### Permitted interpretation

- current code path executes and produces measurable revision behavior
- in this hand-authored experiment, removing residual state reduced several metrics
- SparkBrain touched a subset of nodes per external step

### Prohibited interpretation

- SparkBrain has beaten neural networks
- residual retention is scientifically proven by 40 synthetic episodes
- active fraction implies lower energy
- the chosen weights are unbiased
- these results generalize outside SwitchWorld

## 9. Stage gates

### Gate P0

- all deterministic tests pass
- visualizer trace equals engine trace
- canonical scenario revision works
- raw and aggregate artifacts produced

### Gate P1

- all synthetic worlds implemented
- ablation matrix complete
- 30+ seed confidence intervals
- theory predictions preregistered in repository

### Gate P2

- learned routing beats chance on held-out combinations
- hand-authored routing removed from primary result
- matched GRU/Transformer/RIM baselines complete

### C05 reduced matched-baseline protocol (2026-08-23)

C05 consumes C02 `Episode` objects and frozen manifest files without modifying them.
Observation encoding is fitted on a deterministic training half of dev; confidence
threshold, quality match, and model choices use dev only. Test targets remain evaluator
fields. Learned final seeds are 101, 211, 307, 401, and 503. Parameter and analytical
training-operation targets are checked within ±2% and ±5%; accuracy quality uses ±1
percentage point and coverage ±2 points. Oracle and privileged Bayes are excluded from
information-matched conclusions.

The committed acceptance artifact is a reduced CPU integration profile, not the full C02
frozen scientific matrix. It records failed quality matches, all test rows, paired
episode-level bootstrap/sign-flip statistics, effect sizes, and Holm adjustment. Operation
counts and CPU timing are never treated as energy measurements.

### Gate P3

- at least one external benchmark improved on primary revision metric without unacceptable false ignition
- negative datasets and failure modes reported

### Gate P4

- spiking backend reproduces predefined behavioral invariants
- rate/spike disagreement analyzed

### C07 frozen reduced comparison (2026-08-23)

Before final comparison, canonical predictions and distinct ignition order were fixed to
exact equality; switch and recovery indices were limited to a one-event delta;
no-ignition, duplicate diversity 1, residual recovery, Workspace capacity, and directional
edge ablation were frozen as checks. This backend is hybrid: snnTorch LIF sensory encoding
with rate/algorithmic Coalition and Workspace. Activity, messages, and CPU wall-clock are
reported separately and are not energy evidence.

### Gate P5

- full local system starts from documented commands
- primary result subset reproduces from a clean local environment
- after setup/data acquisition, the primary workflow succeeds offline
- full environment and run manifest are published

### Extension Gate H

- physical energy measured on an actual dedicated target
- workload, accuracy, latency, instrumentation, and platform are disclosed
- result remains separate from core completion

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

The model execution gate opened after the committed C04 learned checkpoint and C05 common
protocol/checkpoints were integrated and hash-audited. `c06-final-official` evaluates the
complete 1,744-pair official test once with network blocked. C05 encoder state is reconstructed
from the original deterministic development half and serialized before external evaluation;
all fit/calibration/selection entry points reject test Episodes.

The direct Transformer, explicit-state memory, and Spark conditions receive identical
Observation objects and example counts at the adapter API. Effective input representations,
parameters, and compute are not matched: the C05 dev vocabulary maps external categorical
tokens to UNK, while C04 hashes raw text. Oracle is target-visible and must remain outside
information-matched conclusions. BU-Acc and BM-Acc are reported separately and BREU is their
equal average. Attribution without checkpoint evidence IDs is N/A, not zero.

The official run is a negative result: Spark BREU is 0.0643 versus 0.25 for both direct and
uniform-chance conditions. Gate P3's improvement criterion is therefore not met.

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

## 10. C11 input-bottleneck diagnostic protocol

Protocol `c11-input-bottleneck-v1` freezes the v0.3 G1 input-axis diagnosis before source
integration. It compares legacy whole-string hashing, local token/bigram/character features, and
an explicit structured-event Oracle through one deterministic pair evaluator. All conditions use
seed 1729, the same six examples, labels, call count, cosine calculation, and threshold 0.5.

The six preregistered families are paraphrase, local change, unrelated text, synonym limitation,
high-overlap negation, and unseen composition. Raw features, collisions, similarities, predictions,
coverage, and feature-work counters are retained. The Oracle receives only a fail-closed structured
event allowlist; evaluator labels, truth, answer, split, test-only metadata, and unknown fields are
rejected recursively. It cannot be selected by the default production configuration.

The input path is `implicated` only when Oracle accuracy exceeds the whole-hash control by at
least 0.25, reaches at least 0.80, passes leakage checks, and the local track retains at least 0.15
more similar-pair surface similarity than whole hashing. A gap of at most 0.05 is `not implicated`;
other complete outcomes are `inconclusive`. Missing conditions or protocol violations fail closed.
The official Belief-R test is outside C11 and must not be inspected or used for tuning.

### C11 statistical-completeness amendment

Protocol `c11-input-bottleneck-v2` supersedes v1 for C11 acceptance. It preserves all six
diagnostic pairs, conditions, labels, features, threshold 0.5, and diagnosis gates, and adds the
preregistered seed list 1729–1733. Because the three frontends and frozen evaluator are
deterministic, seeds audit execution invariance rather than stochastic model variation. Primary
effect sizes and 95% intervals use 10,000 paired bootstrap resamples of diagnostic-pair blocks
with bootstrap seed 4311. Seeded rows remain visible in raw artifacts, and a degenerate
between-seed spread is reported as such rather than promoted as independent replication.

## 11. C12 adaptive sensory-field protocol

Protocol `c12-sensory-field-v1` and run `c12-sensory-field-main-v1` are frozen before
implementing or evaluating C12. The primary synthetic evaluation uses seeds 2601--2605 and
paired episode/world blocks. It compares the full computational sensory gate with no-goal,
no-habituation, no-prediction-error, no-novelty, no-magnitude, and bypass conditions. The
bootstrap interval is a deterministic 95% paired nonparametric interval over episode/world
blocks with 10,000 resamples and bootstrap seed 4312. The official Belief-R test is outside C12.

For each continuous input channel, the preregistered salience terms are bounded magnitude
(`0.15 * min(abs(value), 2.0)`), normalized prediction error / novelty (`1.20 * error / scale`),
onset (`1.25` only before local initialization), habituation (`-1.25 * habituation`), and bounded
goal contribution (`0.90 * clamp(request, 0.0, 0.35)`). Final salience is the non-negative sum.
The trace records requested and applied goal bias separately. The base threshold is `0.90`,
increases by `0.20` after emission, and relaxes by `0.12` toward base after suppression.
Prediction, variability, habituation, and release rates remain `0.25`, `0.15`, `0.22`, and
`0.55`; stable error ratio is `0.35`, minimum scale is `0.10`, and at most eight channels emit
per sample. Any change to these frozen values requires a new protocol and Decision ID.

G04 passes only when predictable repetition reduces both emitted active Sparks and downstream
active work by at least 50% relative to the first presentation; unexpected change or omission
recall is at least 90%; a relevant bounded goal improves low-salience recall over the paired
no-goal condition; irrelevant false activation rises by no more than 10 percentage points; and
at least one dishabituation / stimulus-specificity example is retained. No-emission is valid.
Omission is an explicit adapter observation that a previously expected channel is absent, not
the mere absence of a key from a partial sample and not evaluator truth. The goal request is a
channel-local numeric hint only. Evaluator truth, target, label, test-only, contradiction, and
answer fields are rejected recursively before mutation; any invalid channel or forbidden field
rejects the whole multi-channel sample atomically.

Every accepted and suppressed channel retains magnitude, prediction error, normalized novelty,
habituation, requested/applied goal, onset, threshold, final salience, and ablation state.
`channels_inspected` counts every input/explicit-omission channel read, `features_scored` every
scored channel, `state_updates` every committed local-state update, `candidate_channels` the
channels above threshold before top-k, `sparks_emitted` and `downstream_active_work` only emitted
Sparks, and `suppressed_channels` non-emitted channels. G04's active-work reduction therefore is
not a claim that dense sensory scoring or total compute became sparse, nor an energy claim.
Inspection must be state-neutral. Serialization/replay must reproduce Spark IDs,
accepted/suppressed rows, counters, and state hashes exactly.

The required primary worlds are predictable `HabituationWorld`, `UnexpectedChangeWorld`
(including explicit omission), a weak goal-target world, and distractor/noise adversarial worlds.
Stop on a protected-hash change, fewer than five unique seeds, a non-empty output directory,
goal/sample label leakage, non-atomic rejection, inspection mutation, replay mismatch, missing
score/ablation trace, or dense work reported as active work. C12 supports only computational
sensory-gate behavior; it does not establish biological sensory reproduction, semantic
understanding, or an improved scientific claim grade.

## 12. C13 evidence and entity-binding diagnostic protocol

Protocol `c13-evidence-entity-v1`, run `c13-evidence-entity-main-v1`, freezes the shared C12/C13
lineage boundary and the first entity diagnosis before C13 implementation or evaluation. C12
retains the existing `SensorySample` and `PerceptualSpark` field names and supplies strict,
canonical versioned serialization. In particular, `entity_hint` is diagnostic input and
`entity_slot` is perceptual output. C13 converts that output explicitly into a versioned evidence
record with stable `evidence_id`, `source_id`, `correlation_group`, `entity_key`,
`hypothesis_id`, `polarity`, `strength`, `parent_evidence_ids`, and `parent_spark_ids`. Existing
v0.2 readers and schemas are not changed.

Before source implementation, the accepted C12 merge is pinned to
`280516fb61eab7c7a96c109baefc82b333fcc367` (head
`50c2e67be73292b3a51737455597cd7aac4d8659`). The exact canonical C12 inventory includes
`schema_version` on `SensorySample` and `PerceptualSpark`, plus `omitted_channels` on
`SensorySample`; this amendment changes no threshold, seed, condition, or claim policy.

The primary paired comparison is `E0_global` versus `E1_oracle_entity` under the same frozen
input frontend, G0 downstream path, inputs, labels, cognitive core, evaluator, budget, and seeds
2601, 2602, 2603, 2604, and 2605. `E0_global` maps evidence to the reserved global scope;
`E1_oracle_entity` requires an explicit nonempty perceptual entity slot and never derives it from
truth, target, answer, evaluator, label, split, or test-only metadata. Correlation discount is
0.20 and recency tau is 30.0. Seed-level paired rows and failed seeds are retained. Primary
effects use 10,000 paired bootstrap resamples with seed 4313 and a 95% interval.

Engineering gate G02 requires exact same-ID no-op behavior, no independent-count inflation,
100% rejection of source, correlation, entity, hypothesis, polarity, strength, time, or parent
reassignment for an existing evidence ID, complete cited-lineage resolution, and zero orphaned
citations after removal and restoration. A distinct ID in an existing correlation group may add
at most 0.20 times the effective marginal of otherwise identical independent evidence; the final
prediction change is capped at 0.05. Removal deactivates but does not erase evidence, restoration
reactivates the same immutable record, and the fixed-time summary, decision, and state hash must
return exactly to their pre-removal values.

Engineering gate G05 requires `E1_oracle_entity` cross-talk no greater than 0.02, evidence
misassignment no greater than 0.01, and oracle entity coverage equal to 1.00. Object accuracy,
belief contamination, coverage, cross-talk, and misassignment remain separate metrics. An
absolute reduction of at least 0.10 from E0 cross-talk to E1 cross-talk is the preregistered
scientific-support threshold, not an engineering-completion requirement. Failure to meet it is a
valid negative or inconclusive result and triggers a core entity-scope audit.

`E2_learned_slots` is forbidden until the E0/E1 results and gap are frozen. C13 defines only its
exchangeable interface: assignment status is `assigned`, `unassigned`, or `uncertain`, and slot
quality is evaluated by optimal permutation-invariant matching. The metric must be unchanged by
a pure slot-label permutation; assigned coverage, uncertain rate, unassigned rate, and slot-switch
rate are reported separately.

Stop and invalidate the run if evaluator truth influences production entity assignment; an
evidence citation cannot be resolved, removed, restored, or traced; any condition changes the
frozen inputs/core/budget/evaluator; a test result changes a threshold or mapping; E0/E1/E2 rows
are merged; or E2 implementation/evaluation begins before E1 freeze. Mandatory outputs under
`artifacts/v03/c13_evidence_entity/` are `protocol.json`, `run_manifest.json`,
`evidence_invariant_tests.json`, `entity_condition_metrics.json`, `paired_statistics.json`,
`cross_talk_examples.jsonl`, `causal_removal_examples.jsonl`, and `report.md`.

Decision `D-V03-0006`, recorded before any C13 execution or result observation, freezes the
remaining operational semantics. `active_state_hash` excludes audit/delivery history and must
return exactly after restore; the append-only `audit_chain_hash` must advance. C13 G0 does not use
the C14 Coalition gate: it maps effective support minus contradiction through a sigmoid, uses
positive threshold 0.5, confidence minimum 0.5, probability-margin minimum 0.08, and budget one.
The relation-free fixture has 24 episodes per seed, two objects, two hypotheses, and balanced
support, correlated-variant, contradiction, late-redelivery, deactivate, and restore events.

Prediction change is the fixed-time absolute positive-probability delta. Cross-talk counts a
directed A intervention as affecting non-target B when B probability changes by more than
`1e-12` or B's canonical summary, active citations, or active-state projection changes. Its
denominator is all such relation-free directed opportunities. E1 misassignment and coverage use
eligible evidence rows and eligible Sparks respectively. The E0-minus-E1 scientific gap is a
point estimate with a descriptive paired bootstrap interval, not an engineering gate. Descendant
records are not mutated when a parent is deactivated; they are excluded while any transitive
ancestor is inactive and become eligible again after exact ancestor restore. Full strict contract,
lineage-registry, aggregation, and artifact-content fields are frozen in the protocol JSON.

Decision `D-V03-0007` closes the final pre-execution degrees of freedom. It fixes the complete
24-episode generator and per-seed fixture hashes; the G0 winner/abstention, budget, lexical
tie-break, and citation rules; canonical SHA-256 evidence/binding ID derivation and the complete
immutable identity surface; a type-and-reason rejection envelope for non-JSON inputs; and the
exact maximum-weight slot matching, rectangular padding, tie-break, coverage, status-rate, and
slot-switch denominators. These are operational definitions only and do not alter C13's seeds,
thresholds, conditions, or claim policy.

Before the first fixture test, the exact canonical JSON key sets and serialization call were added
to the protocol so the already-frozen five fixture hashes can be independently reconstructed. No
fixture value, order, distribution, seed, threshold, metric, or hash was changed.

The frozen run is accepted at source commit `03b26591c653592ec501177d9628bd2bea9b8ec4`.
All five fixture hashes matched before evaluation; every condition retained 720 execution rows
and failed-seed lists were empty. G02/G05 passed with E1 cross-talk 0.0, E1 misassignment 0.0,
and E1 oracle coverage 1.0. E0 cross-talk was 1.0, giving a paired E0-minus-E1 effect and 95%
bootstrap interval of 1.0 and [1.0, 1.0]. This is the frozen relation-free Oracle diagnosis, not
autonomous binding. The checked-in eight artifacts reproduced byte-for-byte under a different
`PYTHONHASHSEED`. E2 remains unimplemented and prohibited until a later preregistered task.
The metrics artifact retains all 1,440 ordered execution rows, including add-row assignment and
lineage fields. The invariant artifact retains numeric and canonical before/after observations
for same-ID, correlation, identity rejection, lineage, orphan, and remove/restore checks so the
reported aggregates and gates can be independently recalculated from checked-in raw evidence.
## 13. C14 Coalition-driven Ignition protocol

Protocol `c14-coalition-gate-v1`, run `c14-coalition-gate-main-v1`, is frozen before C14 source
implementation or evaluation. The paired controls are `G0_probability_margin`,
`G1_evidence_coalition`, and `G1_no_coalition_ablation`; every intervention uses identical logits
`hypothesis-alpha=0.72`, `hypothesis-beta=0.28`. G0 retains confidence threshold 0.50 and margin
threshold 0.08. G1 consumes the bounded evidence-Coalition score and cannot copy confidence.

The exact score transforms, weights, gate thresholds, reason priority, ten intervention cases,
seeds 2701--2705, 10,000 paired bootstrap resamples, and bootstrap seed 4314 are frozen in
`artifacts/v03/c14_coalition_gate/protocol.json`. G03 engineering acceptance requires direct code
and test evidence that the score is consumed, independent support can Ignite, duplicates and
correlated copies cannot manufacture independence, contradiction and removal causally change the
gate, restore is exact, fixed logits never change, and G1 differs from the no-Coalition ablation on
at least 30% of preregistered paired cases. Coverage, covered accuracy, false Ignition, every raw
row, counterexample, failed seed, and machine-readable no-Ignition reason are retained. External
accuracy improvement is explicitly outside the engineering gate.

Decision `D-V03-0010`, recorded before source editing or result observation, freezes the actual
logits and canonical hash, probability-to-activation mapping, post-stability-update score timing,
diagnostic settle/evaluate/belief-update call path, G0-equivalent no-Coalition rule, exact case
generator and five fixture hashes, evidence roles, expected case/reason table, comparator stages,
point-estimate gates, descriptive bootstrap order, and recalculable 360-row artifact schema. The
legacy gate remains the default, `c14_bounded_v1` is explicit, and the v0.2 learned backend remains
unchanged. C14 source may be implemented and tested, but the official runner stays disabled until
a separate preregistration amendment pins the source-only commit.

Decision `D-V03-0011` closes the remaining reconstruction gaps before source editing. The five
execution fixture hashes cover complete machine-readable evidence content and interventions; the
older five hashes are identity-only audit markers. Stability advances independently for every
unchanged candidate before scoring, and every case/condition/replay uses a fresh gate, ledger, and
belief field. The bootstrap resampling and percentile interpolation are exact, and the nested raw,
causal, reason, metrics, manifest, ordering, and unknown-key contracts are frozen so the six
artifacts alone support recalculation of every score, margin, reason, effect, and engineering gate.

Decision `D-V03-0012` fixes every nested artifact key/type/null/cardinality/order contract and
keeps non-Coalition controls from fabricating C14 candidate terms. It also repairs the sole
fixed-activation conflict before source editing: `weak_low_score` retains activation 0.72/0.28,
uses strength-0.05 evidence at time 65, and evaluates at time 100. Its recency passes the hard
minimum while its bounded score stays below threshold. Only the five full-fixture hashes change;
the frozen logits, weights, thresholds, seeds, expected reason, and identity hashes do not.

Decision `D-V03-0013` fixes each condition-by-metric formula and retains fresh-loop comparator
observations inside the existing 360 raw rows. G1 score deltas use those observations; both
probability controls report exact zero deltas; cross-condition decision-difference values repeat
unchanged across condition rows. The canonical engineering-gate set now includes both 0.30
decision-difference gates, while external accuracy remains a claim boundary rather than a gate
row. This changes no fixture, hash, score, threshold, seed, or expected decision.

Decision `D-V03-0014`, recorded after source and focused-test review but before official runner
execution, pins source commit `307bcb56f09e88b769cd863b1a6fead73a189936` and authorizes the
runner. Protocol authenticity is anchored to preregistration commit
`79dfa6c612e1d3159aae8705be5e14833502ea96` and raw protocol SHA-256
`ce3fc31531f5ea7689cfcd3b07354508a67af9463ed3b9e1eebb613e0e9c4c8a`;
only the source pin, execution flag, and base identity fields may differ. Focused mutation,
tamper, schema, per-seed failure, legacy, and guard tests passed before this authorization.

The first authorized runner attempt stopped atomically with `KeyError: 'ignited'` before any
artifact or numerical result was published because cross-condition calculation passed raw rows
instead of their nested decision objects. Decision `D-V03-0015` records that failed attempt and
the independently audited mechanical correction. The final source pin is
`eb7f542963397eba1b7d9b4a66a7873b3ba17ac4`; its write-free full calculation regression retains
exact counts `360 / 15 / 24 / 120 / 4 / 12` and changes no frozen scientific value.

C14 is accepted at final source pin `eb7f542963397eba1b7d9b4a66a7873b3ba17ac4` and artifact
commit `4c0d26cd0be862da63594f1f32e295127de72304`. The frozen run retains 360 raw rows, 15 causal
rows, 24 aggregate metrics, 120 seed rows, four paired statistics, 50 reason references, and all
12 gate results. Every gate passed and failed seeds are empty. Independent-support Ignition,
removal reversal, and exact restoration are 1.0; same-ID delta is 0.0; correlated-group inflation
is 0; contradiction score delta is -0.1296997075145081; and G1 differs from both probability
controls on 90% of paired primary cases. All nine no-Ignition/ignition reasons are covered.

The exact six artifacts reproduce byte-for-byte under a different `PYTHONHASHSEED`, and raw-only
recalculation matches all derived outputs. This establishes only attributable synthetic Coalition
control of the isolated v0.3 Ignition call path at fixed logits. It is not evidence of external
accuracy gain, learned Coalition formation, semantic understanding, biological fidelity, or
energy efficiency.

## 15. C16 bounded proto-concept formation protocol

Decision `D-V03-0024` (2026-08-26) freezes `c16-proto-concepts-v1` and
`c16-proto-concepts-main-v1` before implementation or official evaluation. Section 14 is reserved
for the independent C15 branch. C16 starts from accepted C14 merge
`00dccf3dc8f6f70353a536dcf1db9ba0b19fc7b5`, uses accepted C12 sensory processing, C13
sample/Spark lineage registration and the immutable CC0 seed, and consumes no C15 runtime.
The authoritative formulas, schemas, hashes, thresholds and source allowlist are in
`artifacts/v03/c16_proto_concepts/protocol.json`.

This is a preregistered five-run-seed synthetic diagnostic, not the general 30-seed evaluation
described in section 6. Seeds 3601--3605 affect fixtures and initialization; each has four worlds
and 32/16/16 train/dev/test episodes of nine frames. All 30 manifest/full-fixture hashes were
independently reproduced with pure generators only. Test introduces held-out motif/context
combinations and a reversed decoy association. No world, context, split, target or human concept
label enters discovery. The twelve-dimensional input scatters actual C12 Spark activations;
default top-eight sensory selection and quiet/no-match frames remain valid.

Nine cells cross CC0 assembly, online prototype and learned-local prototype with primary,
matched-random and frequency-top-K banks. Discovery runs in canonical and episode-shuffled train
order only; amplitude perturbation and irrelevant distractor variants query frozen banks.
The learned representation is a tied linear 12-to-4-to-12 autoencoder with 48 weights, twenty
full-batch train-only SGD updates and no selection. Every bank uses the same frozen eight-slot
one-hot plus intercept ridge predictor, fitted on 256 canonical train transitions. Only
next-channel MSE is evaluated; no auxiliary utility task or hyperparameter search is introduced.

Bank capacity is eight, total births at most 32, retained exemplars at most 32 per candidate,
and the identity registry at most 288 observations. Duplicate identity is a complete no-op;
changed content or a 289th unique observation fails before mutation. Merge requires prototype
cosine at least 0.95 and complete-link cosine at least 0.8 over the full retained union.
Split requires dispersion greater than 0.2, deterministic farthest-pair partition and at least
four exemplars per child. Structural operations respect capacity/birth budgets atomically.
The observation's pre-structural winner remains its recorded winner even if retired that frame.
CC0 and static controls explicitly report unsupported lifecycle operations rather than fabricating
equivalent behavior.

Every primary candidate has an explicit nullable grade. CC0 requires at least three independent
train episodes and two contexts from actual discovery winners. CC1 additionally requires held-out
reuse and Jaccard stability at least 0.8 for both perturbation controls. CC2 requires at least
eight candidate-active test steps and MSE improvement at least 0.01 over both matched controls
on those exact indices; an incomplete matched bank prevents promotion. CC3 additionally requires
targeted impairment at least 0.05, targeted-minus-usage-matched-random impairment at least 0.03,
unrelated collateral at most 0.02, exact state/prediction restoration and replication in at least
three seeds for the same fixed evaluation world. No candidate identity is aligned across seeds.
Train query rows make usage, target-world and comparator selection independently reconstructible.

The exact eight artifacts retain 990 lineage rows, 90 bank records, 5,760 held-out episode rows,
360 seed summaries, 72 utility aggregates, 240 seed control comparisons, 48 control aggregates,
1,920 causal episode/slot rows and 60 counterexample-audit rows when all five seeds complete.
Dynamic candidate arrays are bounded but never padded with invented candidates. Bootstrap uses
10,000 paired seed/episode draws with seed 4366 and descriptive 95% intervals. Empty denominators
are null; undefined draws are not dropped, redrawn or imputed. Candidate grades use frozen point
criteria and make no familywise significance claim.

Failed run seeds are atomic and visible. Partial successful rows remain descriptive, while any
required seed failure disables scientific support and bootstrap evaluation. Zero successful seeds
still yield the exact eight-file failure bundle with empty raw JSONL. Global failures and timeout
abort publication rather than inventing a failed seed. The parent enforces a 3,600-second budget
from worker spawn through termination, terminates/kills before cleanup, and quarantines staging if
the child remains alive. Only the parent may atomically publish a validated eight-file bundle.

The eight new C16 source/test paths, 29 baseline protected hashes and four runtime source pins
are frozen. Source-only commit and independent audit precede a separate four-field pin amendment.
The complete reserved-synthetic/pure-fixture suite runs before source commit and again after pin,
before any official evaluation; protocol fixtures cover both amended and unamended states and
remain safe without Git. Reproduction uses the recorded C16 execution/artifact checkout, with
strict post-pin source guards; later main integration is not silently treated as the same runtime.
No C16 scientific result is asserted here. Null grades and negative outcomes are acceptable;
v0.2.1, existing claim grades, C06/C08 negatives, schemas and release manifests remain unchanged.
## 14. C15 persistent revision-objective protocol

Protocol `c15-revision-objectives-v3`, run `c15-revision-objectives-main-v3`, supersedes the
failed v2 execution under D-V03-0023 and carries forward the substantive contracts frozen by
D-V03-0017 through D-V03-0022 except the explicit v3 execution/nullable-statistic amendments.
Its machine-readable authority is
`artifacts/v03/c15_revision/protocol.json`. C14 is an immutable dependency: the C15 controller
composes the existing bounded Coalition gate and must not edit C14's contracts, Coalition, loop,
or runner source paths. C14 evaluates attributable ledger evidence before any belief mutation.
A learned abstention or transition-head decision may veto the proposed Ignition but may never
create an Ignition that C14 rejected.

### Transition truth and persistent state

The four labels are derived only from the latent world truth history and causally available
evidence, never from a model prediction, score, threshold, Ignition result, or checkpoint. Fewer
than two independent causal sources/groups is `insufficient_information`. Otherwise, returning to
an earlier truth after an intervening different sufficient truth is `recover`; changing from the
immediately previous sufficient truth is `update`; and the remaining stable case is `maintain`.
History is episode- and evaluated-entity-local. Every assessment follows an establishment context,
so the first assessment is not an ambiguous initial classification.

Recovery is executed as A then B then A within one episode, model instance, and in-memory entity
state. Model reload, state reset, re-instantiation, and checkpoint restoration after episode start
are forbidden and `checkpoint_restored` is retained in every raw row. Loser retention is 0.92
after decay 0.88; paired `no_residual` changes only loser retention to zero. A C14 no-Ignition or
learned veto retains a separate `evaluated_entity_key`, applies one entity-local decay, retains
citations/residual candidates, and does not force a prediction or clear other entities.

### Data, conditions, and selection

The controlled worlds are maintain, contradictory update, A-to-B-to-A recovery, and explicit
insufficient information. Train/dev/test contain 16/8/8 fixtures per world, respectively. Their
episode seeds start at 152000/252000/452000, their template families do not overlap, and canonical
split-manifest and full-fixture SHA-256 values are frozen in the protocol. Production-visible IDs
are opaque SHA-256 derivations; the exact event, evidence, stage, variant, and attribution-target
generator is machine-frozen. Dev indices 0--3 per world select among
epochs 2, 4, and 6 by weighted objective total with an earlier-epoch tie-break. Disjoint dev
indices 4--7 select temperature from 0.75/1.0/1.25 and abstention threshold from 0.4/0.5/0.6 by
belief Brier plus binary abstention Brier. Source and focused tests must first be committed and
independently audited without running official split seeds; a source-pin-only amendment then
enables the first official runner. That runner performs training, checkpoint selection,
calibration, and finally one test evaluation in this order. Test, I2 Oracle, and official Belief-R
cannot influence either dev choice.

The hashed fixture keeps its exact eight-field evidence rows. A frozen boundary adapter derives
one opaque sample ID and one opaque parent Spark ID per unique evidence ID, registers that lineage,
and constructs the existing strict schema-0.3 `EvidenceRecord` with empty metadata and parent-
evidence tuple. Same-ID redelivery reuses the byte-identical record. No condition may invent a
different lineage adapter or add evaluator fields at this boundary.

D-V03-0018 closes the entity-condition composition before official execution. E1 copies fixture
entity/evidence IDs. E0 alone maps entity scope to `__global__` and derives a deterministic adapted
evidence ID from the fixture ID before deriving sample/Spark lineage; all other evidence fields
stay paired, duplicate IDs stay equal, and correlated-copy IDs stay distinct. Attribution IDs use
the same mapping. The recovery residual-floor input is captured by replaying visible context and
model head outputs through the C15 controller and reading the target-truth activation immediately
before assessment. It is never a static zero/default fixture value.

D-V03-0019 closes the stage evidence-lifecycle boundary before source pinning or any official
seed. The C13 ledger and audit history remain continuous, but before each stage's deliveries the
controller deactivates prior active rows for the evaluated entity that are absent from the current
stage. C14 therefore evaluates the current stage's attributable active evidence in its two frozen
settle passes. Belief history, residual activation, citations, model hidden state, and the gate
instance remain continuous; other entities are untouched. Same-ID duplication within a stage is
still an exact redelivery no-op, and the frozen generator never restores an earlier-stage ID.

D-V03-0020 invalidates the unevaluated v1 procedure after focused tests accidentally executed
deterministic controller probes on v1 split episodes before the source pin. No training,
checkpoint selection, calibration, E0 evaluation, test evaluation, or artifact generation had
occurred. Protocol `c15-revision-objectives-v2` and run `c15-revision-objectives-main-v2`
supersede v1 with fresh episode seeds 151000/251000/451000, model seeds 2851--2855, bootstrap seed
4365, and newly frozen manifest/full-fixture hashes. Focused runtime tests use reserved synthetic
fixtures and a non-official model seed; reconstructing fixture bytes for hash verification is not
model/controller execution. All other C15 scientific and engineering contracts remain unchanged.

D-V03-0021 closes the failed-seed artifact boundary before source pinning. A model seed is atomic
across all twelve conditions: its rows are buffered, discarded on its first failure without retry,
and replaced by one exact failed-seed record while later seeds continue. Successful seed rows stay
visible, but any failed seed makes engineering status `implementation_failure`, sets scientific
status to `not_evaluated_implementation_failure`, and makes every bootstrap effect and interval
null. Derived cardinalities scale only with complete successful seeds according to the formulas in
the protocol; partial seed rows are never published or imputed. All JSON artifacts repeat the same
failed-seed list and the report names it. Even zero successful seeds produce the exact eight-file
failure bundle with static configuration and empty data arrays.

D-V03-0022 fixes the exact failure representation. The seven-field scientific-support object
keeps its normal keys: three variant gates use zero counts, null rates, frozen maxima, and false
passes; residual rates are null; all five noninferiority effects and all five strict-improvement
effects are null while margins/directions/minimum remain frozen; `all_gates_passed` is false; and
all nine bootstrap entries retain 10,000/4365 with null effect/lower/upper. The loss artifact's
`scientific_gates` is byte-equal to that object. Normal eight engineering-gate rows remain, with
unavailable observations null and required completion gates false. With zero successful seeds,
the JSONL is exactly zero bytes, data/derived arrays are empty, model dimensions and the twelve
static objective configurations remain, and parameter count/optimizer steps are 3132/384.

D-V03-0023 records v2's global aggregation failure and unenforced 120-second timeout without
accepting numerical evidence. V3 uses fresh model seeds 2901--2905, episode bases
152000/252000/452000, bootstrap seed 4415, and independently reconstructed fixture hashes.
The existing F1 convention is now explicit: the harmonic mean of precision and recall is null
if either is undefined or their sum is zero. ECE remains null without decided rows. A paired
effect is null if either operand is null. All 10,000 bootstrap draws are consumed unchanged;
undefined draws are counted, never dropped, redrawn, or imputed. If any draw or the point effect
is undefined, both interval bounds are null, while a finite point effect remains visible.
Each interval adds `defined_resamples` and `undefined_resamples`; they sum to 10,000 on a
completed bootstrap and are both null when failed-seed rules prevent bootstrap execution.
An undefined point effect makes its required scientific gate false; strict improvement uses
finite effects only. Descriptive interval availability does not alter finite point-estimate gates.

V3 enforces a 3,600-second worker budget, starting immediately before spawn and excluding parent
preflight. The worker owns training through validated staging writes; only the parent publishes.
On timeout the parent terminates and joins for five seconds, then kills and joins for five seconds
if necessary. The parent must confirm worker exit by its monotonic deadline; observing a normal
exit only after timeout cannot authorize publication. Staging is removed only after confirmed
worker exit; a surviving worker leaves quarantined staging whose absolute path is reported on
stderr. A new output remains absent and a pre-existing empty output remains empty. Timeout raises
`C15RunTimeoutError` and the CLI exits 124 (other global failures exit 1). A timeout is a global resource-limited implementation
failure, never a failed model seed or a scientific negative. No elapsed time enters scientific
artifacts. The larger budget corrects the execution contract, not any scientific threshold.

Primary evaluation is I1 local-compositional input with E1 explicit Oracle entity scope. The
twelve primary conditions are full separated objectives, nine single-objective ablations,
one-weighted-CE, and no-residual. Full-only diagnostics cover the other five I0/I1/I2 by E0/E1
cells. I2 stays diagnostic and C13 E2 learned slots remain prohibited. Four paired variants are
base, irrelevant distractor, exact same-ID redelivery, and a distinct correlated-group copy.
Across dev and test, 17 condition/cell combinations, five model seeds, 32 fixtures, and four
variants produce exactly 21,760 canonical raw rows.

### Independent objectives and evaluation

Nine terms are logged separately: belief CE; maintain BCE plus stable-probability drift; update
BCE plus new-versus-old ranking; recovery BCE plus a restored-residual floor; explicit
no-Ignition BCE; multiclass Brier calibration; evidence-ID attribution BCE; normalized routing
entropy sparsity; and load balance. The exact masks, weights, formulas, optimizer budget, zero-row
behavior, and gradient-norm definition are in the protocol. Each term retains eligible count,
raw value, weighted contribution, and pre-update unweighted/weighted global L2 gradient norm.
The matched one-weighted-CE condition has identical architecture, initialization, data order,
optimizer steps, checkpoint choices, and calibration budget, but receives only the final
alpha/beta/gamma/NO_IGNITION target and no transition target.
`loss_ablation_metrics.json` retains all 23,040 ordered optimizer-step rows with each objective's
eligible count, raw/weighted value, and two gradient norms so every reported training aggregate is
recalculated from direct evidence rather than prediction rows.

Four-class, maintain, and update confusion matrices; unnecessary and missed revision; revision
precision/recall; recovery opportunity/rate/latency with censoring; no-Ignition precision/recall;
false/missed Ignition; accuracy/coverage; all-row Brier/NLL; decided-only ECE with coverage; and
binary abstention calibration retain exact denominators. Empty groups are null, not zero.
Calibration is grouped by input track and entity condition. The Pareto dimensions minimize
unnecessary revision, missed revision, recovery latency, and ECE while maximizing recovery rate
and no-Ignition F1. Frozen noninferiority margins and a required strict improvement are applied
against one-weighted-CE without choosing a test-favorable checkpoint.

Engineering acceptance requires observed no-checkpoint recovery for every seed, reconstructible
matrices and separate metrics, explicit no-Ignition, all objective ablations, no Belief-R access,
and exact eight-file deterministic reproduction. Narrow scientific support additionally applies
the preregistered distractor, duplicate, correlated-copy, residual, and weighted-CE Pareto gates.
Scientific failure does not invalidate engineering completion; it is recorded as `not_supported`
or another frozen status category and retained in the Results Ledger.

The runner must validate the canonical protocol, authorized source-pin-only amendment, candidate
source bytes, accepted C12--C14 dependencies, protected hashes, unchanged C14 paths, release/schema
deny-prefixes, split manifests, configuration set, and output emptiness before evaluation. It
generates all results in memory, validates raw-to-derived reconstruction and exact schemas before
writing, uses a same-parent staging directory, publishes exactly eight artifacts atomically, and
cleans all staging/output on protocol or implementation failure. A different `PYTHONHASHSEED`
must reproduce every byte. Package/release/schema advancement and no-Git packaging remain C20-only.

### 14.1 Recorded C15 v3 execution versus administrative integration

The v3 scientific source is `eedb8b426f326c5dcb70bd548008695eb1652aee`, authorized by execution
commit `6860c2ec4133a9debefdec0b92e33ab0e09b430f`. Reproduce from a separate checkout/worktree
of that exact execution commit, with its `src` directory explicitly selected by `PYTHONPATH`,
the unchanged source-commit argument, and a fresh output path outside the repository. Do not
execute from the later integration tree or silently substitute a newer main checkout.

D-V03-0025 changes a synthetic test fixture only. The unchanged source-scope guard intentionally
rejects the integration tree because its test differs from the scientific pin. This does not
amend any experimental gate or invalidate retained output bytes. Conversely, the known failing
fixture test on the original execution tree must remain disclosed; later green integration tests
are distinct evidence. Raw/statistical reproduction and full test-suite status are not synonyms.

R-V03-0008 records engineering failure of the all-seed recovery gate and scientific negative
residual/noninferiority findings. No current protocol rule allows those engineering failures to
be waived to satisfy C17's accepted-C15 dependency.

The frozen execution was repeated independently with `PYTHONHASHSEED=37`; every one of the eight
output files is byte-identical to the `PYTHONHASHSEED=1` original. For durable transport without
placing the 157,444,296-byte raw JSONL in ordinary Git history, the exact eight unmodified files
are stored in a deterministic ZIP under `artifacts/v03/c15_revision_transport/`. Its `index.json`
records all entry sizes and hashes, the ZIP hash, the frozen source/execution commits, and the
failed acceptance status. This transport directory is not the canonical C15 artifact directory,
does not add a ninth scientific artifact, and is not a release or a substitute execution tree.

### 14.2 Preregistered C15 v4 correction

D-V03-0026 defines protocol `c15-revision-objectives-v4` and run
`c15-revision-objectives-main-v4` as a fresh experiment. The machine-readable authority is
`artifacts/v03/c15_revision_v4/protocol.json`. Its preregistration has a null source pin and a
disabled runner. The v3 protocol, source/execution commits, exact-eight transport, engineering
failure, scientific negative, and R-V03-0008 remain immutable historical evidence.

The correction uses retained v3 dev diagnostics only. Across 200 primary full/I1/E1/base context
stages, unchanged C14 proposed an Ignition 200 times, while the learned abstention calibrated only
on assessment rows vetoed 136 context stages. All 40 recovery-dev sequences contained correct
C14 A-to-B-to-A proposals, and every reconstructed recovery-head sigmoid was at least
0.9204247345397955. V4 aligns mechanism and supervision scope: learned belief probabilities still
feed C14 on context and assessment, and C14 rejection can never be overridden; context C14
Ignitions construct persistent history without learned abstention/transition veto, while assessment
alone retains the calibrated learned veto. Stage role is fixed scheduler metadata, not model input.

V4 uses model seeds 2951--2955, bootstrap seed 4465, and train/dev/test bases
153000/253000/453000. All generated identities use a new `c15v4-*` namespace. This namespace change
is necessary because the prior family formula did not contain episode seed. It prevents reuse of
v1/v2/v3 family, episode, entity, evidence, source, group, E0, sample, or Spark identities. The
independently reconstructed manifest hashes are train
`bfd3e031edcc9d0c23a55bac1f5797420f1f85d7fca0a0e689ca4ff414fc3266`, dev
`e4f7cc4ab4c2fa5c81a6d17c927424a3575431f0a6578ab87146c130ab87d6f7`, test
`66d580f4e63a55f4a26441709caf8b443bfe701fdac548ff22867a60b7a31cf6`; full-fixture hashes are
train `4bb90acded764199b912b712becc16252c791086dbddc9f80259dd99de5ea455`, dev
`8cec9458524b467c54927ba46a3055754e59aa531de21d8a8037bec993c04589`, and test
`cd27e177476f5c0adba37bf7c4e5284996f6155dd4d61ed1547be2bf1a7051c6`.

The v3 eight engineering gates and all scientific point thresholds are unchanged. V4 neither
guarantees nor requires a positive residual-superiority result: science may remain
`not_supported`. Engineering acceptance still requires all-seed continuous A-to-B-to-A recovery
without checkpoint restore plus the other seven gates. Package/release/schema advancement remains
C20-only.

The enforced order is preregistration commit; authorized source-only commit and reserved tests;
independent source audit without official seed execution; four-field protocol pin; post-pin full
verification; one official train, split dev selection/calibration, and test evaluation; independent
raw reconstruction; and distinct-`PYTHONHASHSEED` byte reproduction. Test inspection cannot be used
to revise v4 source or thresholds.

## 16. C17 label-blind functional-organ protocol

Protocol `c17-functional-organs-v1`, run `c17-functional-organs-main-v1`, tests whether a bounded
group of C16 online-prototype candidates shows reproducible functional specialization under
separable, interacting temporal-memory, entity-tracking, contradiction-integration, and
action-selection demands. C15 v4 and C16 are engineering-accepted dependencies; their negative
scientific boundaries remain unchanged. The machine-readable authority is
`artifacts/v03/c17_functional_organs/preregistration.json`.

### Discovery, proposal and assessment boundaries

Each run seed forms a C16 online-prototype primary bank from 288 train frames. Development, test,
and related-unseen held-out evaluation query the frozen bank without mutation. Discovery receives
only opaque candidate IDs, activation, message endpoints/weights, opaque episode IDs, and time.
Function/world/split names, truth, targets, rewards, expected outputs, labels, C15 assessment
outcomes, and test metadata are excluded. It enumerates size-two-to-four groups, applies frozen
train-only activity/episode-support requirements, ranks structural cohesion deterministically,
and retains at most one primary candidate per seed/resource cell. No eligible candidate is a valid
negative result. Development activation maps the candidate to one evaluator function; ties use the
frozen function order. Test and held-out data cannot alter discovery or that mapping.

C14's accepted bounded Coalition remains the sole proposal source. Context-stage C14 Ignition
constructs history as fixed by C15 v4. Learned assessment applies only after a proposal and returns
allow, veto, or abstain. A C14 rejection is final, no proposal means no assessment, and C15 cannot
create or replace a hypothesis/action. Proposal canonical bytes must be unchanged by assessment.

### Resource cells, fixtures and controls

The primary cell uses Spark/module capacity 8, communication bandwidth 2, workspace capacity 2,
and task compositionality 2. Four secondary cells reduce capacity, bandwidth, or workspace one at
a time, or raise compositionality to 3. A validator requires each secondary cell to differ from
the primary in exactly one numeric factor. Secondary effects are reported but cannot substitute
for the primary organ hypothesis.

Official seeds are 4701--4705; bootstrap seed is 5717. Split seed bases are train 171000, dev
271000, test 471000, and heldout 571000. Each seed/cell retains 24/12/12/12 episodes with 12 frames.
Composition-two cells share primitive fixtures; the composition-three cell changes only the
registered composition schedule. IDs use a fresh `c17-*` SHA-256 namespace. Two independent
standard-library fixture constructions agreed on all corpus/manifest hashes without importing a
model or controller. Exact formulas, hashes, evaluator-only fields and counts are frozen in the
machine protocol.

Branches are unablated, targeted, random-unmatched, size-matched, degree-matched, load-matched,
and activity-matched in that order. Comparator membership is selected from train traces only and
never test performance. A missing comparator fails scientific support. Repeated comparator subsets
remain separate control types and raw rows. Each branch restores C16, C14 and C15 state exactly.

### Gates, statistics and outputs

G08 requires at least three independently qualifying seeds mapped to the same function,
cohesion at least 0.55, selectivity at least 0.20, related-unseen causal reuse at least 0.20,
targeted impairment at least 0.05, targeted-minus-each-control impairment at least 0.03, and
unrelated collateral at most 0.02. The primary cell additionally applies the registered 10,000-draw
paired hierarchical bootstrap bounds. All five controls are an intersection requirement; no
best-control selection is allowed. Secondary intervals are descriptive.

The exact-nine output is preregistration, resource conditions, candidate-discovery JSONL,
structural metrics, functional selectivity, matched ablations, held-out reuse, acceptance matrix,
and report. Raw cardinalities scale only with complete seed buffers and every aggregate/gate must
recalculate from those rows. Any failed required seed makes engineering an implementation failure
and disables scientific bootstrap; zero successful seeds still produce the registered exact-nine
failure bundle. Global preflight, serialization, integrity, or timeout failure publishes nothing.

C08's `(9, 14)` pair, failed specificity/selectivity, E0 grade, and all negative artifacts remain
protected historical evidence. C16 CC2/CC3 remain not supported. Until a source-only commit,
independent audit, separate four-field pin amendment, and post-pin verification complete, the C17
runner remains disabled and official fixtures may be hashed only by pure fixture code.

### 16.1 C17 preregistration reproducibility amendment

D-V03-0030 corrects two preregistration-integrity defects before source acceptance or official
execution. The C16 dependency pin is the resolved commit
`b1c83e619e3c05215bb8878b8294367615b8e058`, not its seven-character display abbreviation. The
machine preregistration now contains a complete pure-fixture generation contract sufficient to
reconstruct the already frozen corpus and manifest bytes independently: exact nested schemas and
array order; canonical JSON and floating-point semantics; all episode, sample, source, correlation,
entity, hypothesis, and action ID preimages; the episode/composition/evaluator formulas; ordered
function, context, and amplitude writes to `base_values`; scoring fields; and the manifest
projection.

This is a specification-only correction. The five official run seeds, two reserved seeds, split
bases, all ten frozen fixture/manifest hashes, thresholds, controls, resource cells, artifact
cardinalities, scientific boundaries, and failure behavior do not change. The corrected
preregistration raw SHA-256 is
`5722f4cdc1feb99e7213546365601c168499e5d2bbe31db49721e59350d069bf`. The runner remains disabled,
the source pin remains null, and no model, controller, official run, or test is executed by this
amendment.

### 16.2 C17 v1 post-run disposition

The official v1 execution completed seeds 4701--4705 and published the exact-nine bundle. It is
retained as immutable evidence with engineering status `implementation_failure`. In every R4 seed,
the discovered target contained both members of the two-candidate bank; the eligible non-target
pool was therefore empty, and all five mandatory matched-control memberships were missing. This
produced 25 missing required control slots across five seeds.

The canonical artifact displays scientific status `not_supported`. Because control completeness
is an engineering prerequisite, the effective scientific disposition is
`not_evaluated_implementation_failure`; no C17 organ support or negative scientific result is
accepted from v1. A reproduction using `PYTHONHASHSEED=8675309` matched all nine artifact bytes,
while the official run's hashseed was not recorded. The reproduction does not rewrite the original
acceptance matrix. Any correction is a separately preregistered C17 v2 engineering experiment;
v1 source, thresholds, protocol, and artifact bytes remain frozen.

### 16.3 C17 v2 control-feasibility and external-finalization protocol

D-V03-0032 preregisters `c17-functional-organs-v2` as a fresh experiment. C17 v1's empty R4
non-target pool is an engineering-feasibility defect only. Its exact-nine bundle, source,
thresholds, and `not_evaluated_implementation_failure` interpretation remain immutable; no v1
observation is reused as scientific threshold or metric evidence.

Discovery remains label-blind and train-only. After the unchanged activity and episode-support
filters, a size-`m` group is eligible only if its sorted non-target bank contains at least `m`
members and therefore at least one same-size combination. This predicate is applied before the
unchanged structural rank. Random-unmatched, size-, degree-, load-, and activity-matched controls
all select `m` members from that common train-only domain. Membership reuse between control types
remains allowed, but all five typed rows are retained. If no candidate passes, the cell records a
normal scientific negative plus five explicit not-applicable control rows. If a selected candidate
cannot satisfy the invariant, the seed fails before frozen-query evaluation and science is not
evaluated.

V2 keeps the five one-factor resource cells and every v1 science gate unchanged: seed consistency
3, cohesion 0.55, selectivity 0.20, held-out reuse 0.20, targeted impairment 0.05, every
target-minus-control margin 0.03, and unrelated collateral 0.02 maximum. The 10,000-draw paired
hierarchical bootstrap is unchanged apart from fresh seed 5817. Official seeds are 4801--4805,
reserved pure-fixture seeds are 9901801--9901802, split bases are
181000/281000/481000/581000, and every generated identity uses the fresh `c17v2` namespace. The
machine preregistration fixes all ten independently reconstructed fixture hashes.

Output is exact-ten. Each of two isolated staging workers produces the same pending-reproduction
exact-nine under fixed distinct hashseeds 11801 and 21801. Generation APIs cannot accept a
self-asserted reproduction pass. An external compare/finalize mode validates exact schemas and raw
bytes in both roots, creates the canonical comparison manifest, then derives final acceptance and
report bytes from validated core plus manifest evidence. The manifest excludes its own hash and
the final acceptance/report hashes. Validation reconstructs the pending forms of those two files
to verify the pre-final hashes, avoiding circular evidence.

Exact top-level and nested schemas, types, nullability, enums, compound order, uniqueness,
referential integrity, row-count formulas, dynamic candidate equations, failed-seed behavior, and
zero-success output are part of the preregistration. For `S` complete seeds, discovery scales `5S`,
structural seed/split rows `20S`, selectivity episodes `120S`, matched and held-out branch rows
`420S` each, control rows `25S`, matched seed effects `30S`, and seed/cell gate rows `40S`; static
and condition aggregates use their exact registered counts. The external manifest contains one
object, exactly two run rows, and nine file hashes per run.

The disabled preregistration precedes any source work. Only the exact seven registered C17
source/test paths may change. A source-only commit and independent audit precede the exact
four-field pin amendment. Official execution remains prohibited until that pin and post-pin
verification pass. Package 0.2.1, persisted schema 0.2, release files, C06/C08 evidence, accepted
C14--C16 evidence, C17 v1, and all claim grades remain protected.

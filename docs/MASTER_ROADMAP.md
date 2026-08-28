# Master Roadmap — Local-First v0.3

## v0.3 research milestone and remaining integration work

C11--C18 are retained as independently scoped research modules: input diagnosis, sensory
selection, evidence/entity scope, Coalition-driven ignition, revision objectives, proto-concept
candidates, functional-organ evaluation, and observability/replay. v0.3.1 composes their permitted
engineering paths into a persistent `IntegratedV03Brain` and live versioned Brain Lab while keeping
concept/organ outputs observer-only. C19 remains blocked and C20 is a private release candidate.
The integration changes no scientific result or claim grade and remains separately falsifiable.

## 1. Strategy

「理論を完成してから実装」「実装後に研究」という直列方式は採らない。以下のworkstreamを、共通のversioned specificationとローカル実行契約の下で並行させる。

```text
R: Prior-art research ─────────┐
T: Theory specification ──────┼─> versioned claims
E: Local reference engine ────┤
V: Local visualizer ──────────┤
X: Experiments / baselines ───┤
L: Learning ──────────────────┤
S: Local spiking simulation ──┤
P: Publication / audit ───────┘
```

専用ハードウェアはこの図に含めず、完成後のExtension Hへ分離する。

## 2. 共通制約

全workstreamは次を守る。

- CPU参照経路を維持する
- コア実行に外部API、クラウドDB、遠隔推論を要求しない
- raw data、trace、checkpointをローカル保存する
- UIは静的配布またはlocalhostで動く
- セットアップ後の主要実験をオフライン実行可能にする
- CIだけでなく対応するローカル検証コマンドを持つ

## 3. Workstreams

### R — Prior-art and novelty boundary

Outputs:

- literature matrix
- exact overlap/non-overlap
- reproducibility and license notes
- novelty claims allowed/prohibited
- release-based source refresh

Exit condition:

- major adjacent familiesを網羅
- proposed contributionごとにstrongest competing prior artを記載
- “not found”と“does not exist”を区別

### T — Theory

Outputs:

- ontology
- dynamics
- coalition and ignition equations
- learning rules
- invariants
- falsification criteria
- plain-language mapping
- version migration notes

Exit condition:

- every theory term maps to code or is explicitly future work
- every primary hypothesis has an experiment and ablation
- formal definition and beginner explanation do not contradict each other

### E — Local engine

Outputs:

- deterministic CPU reference engine
- learned rate-based backend
- backend protocol
- profiling and trace hooks
- local checkpoint/replay

Exit condition:

- tests and theory conformance pass
- no hidden global state
- trace collection is non-interfering
- core behavior runs without network access

### V — Local visualizer

Outputs:

- static reference viewer
- localhost interactive Brain Lab
- causal intervention controls
- run comparison
- exportable figures

Exit condition:

- user can explain any ignition from evidence graph and preceding events
- UI never invents state not in trace
- release UI has no mandatory external CDN or SaaS dependency

### X — Experiments

Outputs:

- synthetic worlds
- locally cached external benchmark adapters
- baselines
- ablations
- statistics and reports

Exit condition:

- repeated seeded experiments
- raw results retained locally
- matched comparison regimes
- benchmark can rerun after network disconnection once data is installed

### L — Learning and self-organization

Outputs:

- learned router
- learned weights/thresholds
- structural plasticity
- organ discovery metrics
- CPU-scale reference training configuration

Exit condition:

- held-out generalization
- collapse/load-balance controls
- causal evidence of specialization
- at least one small training experiment runs on CPU

### S — Local spiking simulation

Outputs:

- Norse or snnTorch backend
- optional Nengo comparison model
- Brian2 timing model where needed
- shared trace/backend protocol

Exit condition:

- predefined rate/spike behavioral equivalence or documented failure
- local CPU execution path exists
- local GPU acceleration is optional
- activity counts, runtime, and hardware-energy claims remain separated

### P — Publication and reproducibility

Outputs:

- technical report
- experiment manifests
- figure scripts
- negative result appendix
- local reproducibility instructions

Exit condition:

- independent reviewer can rerun primary result on a local machine
- claims match evidence strength
- external services are not required to inspect or regenerate core artifacts

## 4. Milestones

### M0 — Project foundation — completed across v0.2 and v0.2.1

v0.2:

- project charter
- theory v0.2
- prior-art gap analysis
- standard-library reference engine
- canonical SwitchWorld
- static visualizer
- Phase-0 baselines
- deterministic tests
- JSON checkpoint / deterministic continuation / trace replay
- versioned config, trace, and state schemas
- Codex handoff queue

v0.2.1:

- local-only completion policy
- CPU reference requirement
- dedicated hardware separated from core
- beginner foundation guide
- expanded plain-language glossary
- local readiness audit
- package version patch while retaining schema 0.2

### M1 — Reference validity

Required:

- schema validation
- trace replay
- configuration serialization
- richer tests for duplicates, contradictions, cooldown, workspace capacity
- profiling counters audited
- local readiness and optional CI

Blocks: M2–M7 release claims.

### M2 — Controlled research suite

Required:

- ReliabilityWorld
- DelayedEvidenceWorld
- ContradictionWorld
- MultiObjectWorld
- GoalConflictWorld
- complete ablation matrix
- bootstrap intervals

### M3 — Local Interactive Brain Lab

Required:

- local Python control plane
- localhost streaming or polling
- bundled frontend assets
- pause/step/reset
- parameter edits
- Spark/edge intervention
- side-by-side run comparison

Must preserve static visualizer as fallback. No external CDN at runtime.

### M4 — Learned routing and representation

Required:

- event encoder
- top-k router
- sparse active subgraph
- held-out combinations
- routing diagnostics
- differentiable or hybrid coalition scorer
- CPU-scale reference configuration

### M5 — Matched neural and probabilistic baselines

Required:

- GRU
- Transformer
- RIM/modular recurrent model
- HMM/Bayes baseline where applicable
- parameter/FLOP/wall-clock matching
- shared local datasets and splits

### M6 — External belief-revision validation

Required:

- locally cached Belief-R adapter or documented equivalent
- relational/non-monotonic stream task
- generalization and failure analysis
- calibration
- causal interventions

Network download may be a setup step; evaluation must run from local files afterward.

### M7 — Local spiking equivalence

Required:

- backend interface implemented
- LIF/recurrent backend
- event encoding
- surrogate-gradient or local learning
- rate/spike invariant comparison
- CPU runnable reduced configuration

### M8 — Structural plasticity and emergent organs

Required:

- edge growth/pruning
- Spark merge/split/create
- specialization metrics
- intervention-based organ validation

High-risk milestone. Failure does not invalidate M0–M7.

### M9 — Local final integration and publication package

Required:

- integrated local Brain Lab
- local installer or reproducible environment
- offline-capable demo
- technical paper
- full raw-result bundle
- figure generation
- clean-room local rerun
- external review

M9 is the core completion milestone.

## 5. Extension H — Dedicated hardware validation

Extension H is outside M0–M9.

Possible outputs:

- Lava or vendor-specific mapping
- Loihi / FPGA / ASIC execution
- physical power and latency measurement
- rate/local-SNN/hardware equivalence report

Entry requires completion of M7 and fixed measurement methodology. Failure or non-execution does not invalidate core completion.

## 6. Parallel execution batches

### Batch A — immediately actionable

- M1 engine hardening
- M2 world implementations
- M3 local UI scaffolding
- R literature matrix expansion

### Batch B — after schemas stabilize

- M4 learned router
- M5 neural/probabilistic baselines
- M3 advanced UI
- statistical report generation

### Batch C — after learned comparison

- M6 external tasks
- M7 local spiking backend
- theory v0.3 based on findings

### Batch D — exploratory core

- M8 self-organization
- M9 local final integration
- publication and naming

### Separate Batch H — optional

- dedicated hardware mapping
- physical energy experiments

## 7. Artifact status board

| Artifact | v0.2.1 | Next gate |
|---|---|---|
| Project Charter | v0.3 boundary synchronized | keep runtime completion separate |
| Theory Specification | v0.3 working specification | formal conformance tests |
| Beginner Guide | complete | update with theory changes |
| Glossary | expanded | keep synchronized |
| Local Policy | complete | enforce in all tasks |
| Prior-art matrix | initial complete | systematic review expansion |
| Reference Engine | functional complete | M1 hardening |
| SwitchWorld | functional complete | M2 worlds |
| Static Visualizer | functional complete | M3 live lab |
| Phase-0 Baselines | functional complete | M5 matched baselines |
| Benchmark Report | generated | confidence intervals and matched models |
| Learned Routing | implemented with retained boundaries | matched/generalization evidence |
| Local Spiking Backend | reduced hybrid boundary | M7 broader equivalence |
| Structural Plasticity | negative evidence retained | new falsifiable hypothesis only |
| Local Final Package | v0.3 private candidate | v0.3.1 separate evidence binding |
| Dedicated Hardware | outside core | Extension H only |
| Codex instructions | complete | update after each merged task |

## 8. Change control

Any change to one of the following requires a Decision Log entry:

- definition of Spark
- coalition score terms
- ignition conditions
- evidence identity semantics
- workspace semantics
- primary hypotheses
- primary benchmark metrics
- local execution contract
- claim strength
- official project/theory name

Any merged implementation that changes results must regenerate artifacts and document whether the theory or only the parameterization changed.

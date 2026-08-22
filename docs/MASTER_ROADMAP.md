# Master Roadmap

## 1. Strategy

「理論を完成してから実装」「実装後に研究」という直列方式は採らない。以下のworkstreamを共通のversioned specificationで並行させる。

```text
R: Prior-art research ───────┐
T: Theory specification ────┼─> versioned claims
E: Reference engine ────────┤
V: Visualizer ──────────────┤
X: Experiments / baselines ─┤
L: Learning ────────────────┤
S: Spiking backend ─────────┤
P: Publication / audit ─────┘
```

ただし依存関係は守る。特にspiking化や大規模UIは、reference behaviorを固定してから行う。

## 2. Workstreams

### R — Prior-art and novelty boundary

Outputs:

- literature matrix
- exact overlap/non-overlap
- reproducibility and license notes
- novelty claims allowed/prohibited
- monthly or release-based source refresh

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
- version migration notes

Exit condition:

- every theory term maps to code or is explicitly future work
- every primary hypothesis has an experiment and ablation

### E — Engine

Outputs:

- deterministic reference engine
- learned rate-based backend
- backend protocol
- profiling and trace hooks

Exit condition:

- tests and theory conformance pass
- no hidden global state
- trace collection is non-interfering

### V — Visualizer

Outputs:

- static reference viewer
- live interactive UI
- causal intervention controls
- run comparison
- exportable figures

Exit condition:

- user can explain any ignition from evidence graph and preceding events
- UI never invents state not in trace

### X — Experiments

Outputs:

- synthetic worlds
- external benchmark adapters
- baselines
- ablations
- statistics and reports

Exit condition:

- repeated seeded experiments
- raw results retained
- matched comparison regimes

### L — Learning and self-organization

Outputs:

- learned router
- learned weights/thresholds
- structural plasticity
- organ discovery metrics

Exit condition:

- held-out generalization
- collapse/load-balance controls
- causal evidence of specialization

### S — Spiking and neuromorphic

Outputs:

- Norse/snnTorch backend
- Nengo comparison model
- Brian2 timing model where needed
- Lava mapping

Exit condition:

- predefined rate/spike behavioral equivalence
- hardware claims separated from simulation claims

### P — Publication and reproducibility

Outputs:

- technical report
- experiment manifests
- figure scripts
- negative result appendix
- reproducibility instructions

Exit condition:

- independent reviewer can rerun primary result
- claims match evidence strength

## 3. Milestones

### M0 — Project foundation — completed in v0.2

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

### M1 — Reference validity

Required:

- schema validation
- trace replay
- configuration serialization
- richer tests for duplicates, contradictions, cooldown, workspace capacity
- profiling counters audited
- CI

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

Can proceed in parallel with M3 UI work after M1 interfaces stabilize.

### M3 — Interactive Brain Lab

Required:

- FastAPI control plane
- WebSocket frames
- React/TypeScript visualizer
- pause/step/reset
- parameter edits
- Spark/edge intervention
- side-by-side run comparison

Must preserve static visualizer as fallback.

### M4 — Learned routing and representation

Required:

- event encoder
- top-k router
- sparse active subgraph
- held-out combinations
- routing diagnostics
- differentiable or hybrid coalition scorer

This is the first milestone capable of supporting a modern ML architecture claim.

### M5 — Matched neural baselines

Required:

- GRU
- Transformer
- RIM/modular recurrent model
- HMM/Bayes baseline where applicable
- parameter/FLOP/wall-clock matching
- shared datasets and splits

M4 and M5 should use the same training harness.

### M6 — External belief-revision validation

Required:

- Belief-R adapter
- relational/non-monotonic stream task
- generalization and failure analysis
- calibration
- causal interventions

### M7 — Spiking equivalence

Required:

- backend interface implemented
- LIF/recurrent backend
- event encoding
- surrogate-gradient or local learning
- rate/spike invariant comparison

### M8 — Structural plasticity and emergent organs

Required:

- edge growth/pruning
- Spark merge/split/create
- specialization metrics
- intervention-based organ validation

High-risk milestone. Failure does not invalidate M0–M7.

### M9 — Neuromorphic and publication package

Required:

- Lava mapping
- actual runtime/energy experiment where hardware is available
- technical paper
- reproducibility bundle
- external review

## 4. Parallel execution batches

### Batch A — immediately actionable

- M1 engine hardening
- M2 world implementations
- M3 backend/frontend scaffolding
- R literature matrix expansion

### Batch B — after schemas stabilize

- M4 learned router
- M5 neural baselines
- M3 advanced UI
- statistical report generation

### Batch C — after learned comparison

- M6 external tasks
- M7 spiking backend
- theory v0.3 based on findings

### Batch D — exploratory

- M8 self-organization
- M9 hardware deployment
- publication and naming

## 5. Artifact status board

| Artifact | v0.2 | Next gate |
|---|---|---|
| Project Charter | complete | revise at theory v0.3 |
| Theory Specification | draft complete | formal schema + conformance tests |
| Prior-art matrix | initial complete | systematic review expansion |
| Reference Engine | functional complete | M1 hardening |
| SwitchWorld | functional complete | M2 worlds |
| Static Visualizer | functional complete | M3 live lab |
| Phase-0 Baselines | functional complete | M5 neural baselines |
| Benchmark Report | generated | confidence intervals and matched models |
| Learned Routing | absent | M4 |
| Spiking Backend | absent | M7 |
| Structural Plasticity | absent | M8 |
| Neuromorphic Measurement | absent | M9 |
| Codex instructions | complete | update after each merged task |

## 6. Change control

Any change to one of the following requires a Decision Log entry:

- definition of Spark
- coalition score terms
- ignition conditions
- evidence identity semantics
- workspace semantics
- primary hypotheses
- primary benchmark metrics
- claim strength
- official project/theory name

Any merged implementation that changes results must regenerate artifacts and document whether the theory or only the parameterization changed.

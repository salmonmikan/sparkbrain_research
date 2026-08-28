# Software Architecture — Local-First v0.3

## 1. Architectural objective

理論の各概念をコード上の一級オブジェクトに対応させ、出力だけでなく状態遷移全体を観察・介入・再実行できることを最優先とする。

```text
World / Dataset
      │ external Event
      ▼
Event Router ── top-k / explicit route
      │
      ▼
Priority Event Queue
      │
      ▼
Local Spark Dynamics
  ├─ lazy decay
  ├─ integration
  ├─ threshold / fire
  ├─ refractory
  ├─ excitation / inhibition
  └─ eligibility
      │
      ▼
Coalition Builder
  ├─ evidence identity
  ├─ source diversity
  ├─ contradiction
  ├─ stability
  └─ score
      │
      ▼
Ignition Gate
  ├─ absolute threshold
  ├─ competitor margin
  ├─ minimum sources
  └─ temporal stability
      │
      ▼
Global Workspace
  ├─ memory listeners
  ├─ action listeners
  ├─ critic / learning
  └─ language readout (future)
      │
      ├─────────────┐
      ▼             ▼
Trace Store      Visualizer
```

## 2. Current v0.2.1 implementation

### `model.py`

Theory-level data contracts:

- `SparkKind`
- `EventKind`
- `BrainConfig`
- `EvidenceRecord`
- `Spark`
- `Connection`
- `Event`
- `Coalition`
- `WorkspaceItem`
- `Ignition`
- `EngineStats`
- `TraceFrame`

### `engine.py`

`SparkBrain` is the reference engine.

Responsibilities:

- graph construction
- deterministic priority queue
- lazy activation decay
- event integration and firing
- signed propagation
- evidence provenance
- active hypothesis tracking
- coalition scoring
- ignition and workspace management
- reward-modulated plasticity
- trace capture

### `worlds.py`

- canonical SwitchWorld scenario
- seeded random episodes
- hand-authored evidence routing
- standard brain topology factory

### `baselines/`

- dense evidence accumulator
- hard-WTA accumulator
- instant event classifier

`classic.py` retains the Phase-0 scalar baselines and `__init__.py` preserves the former
`sparkbrain.baselines` imports. `probabilistic.py` contains privileged Bayes and a causal
train-only Laplace HMM; `bounds.py` contains evaluator-only oracle and chance bounds.

`baselines/neural/` is optional-PyTorch code for GRU, LSTM, causal Transformer (context
64), top-two-of-four RIM-like recurrence, and explicit-state memory. All implement the
same reset/step/probability/trace/counter surface. C02 `Episode` construction stays outside
the models in `evaluation/baseline_data.py`; truth and test selection remain evaluator-only.
Training, analytical work accounting, profiling, paired statistics, and artifact output are
separate modules under `evaluation/`. This is a comparison harness, not an engine backend.

### `metrics.py`

- coverage
- all-step / decided-step accuracy
- truth and prediction changes
- unnecessary revisions
- revision precision / recall
- switch latency
- recovery rate
- noise-induced wrong switch

### `benchmark.py`

- repeated seeded episodes
- SFA ablations
- aggregate JSON / CSV / Markdown
- instrumentation metrics

### `tasks/` and `evaluation/` (C02)

`tasks/` defines versioned, deterministic `Observation`, evaluator-only `Target`, and
`Episode` contracts. Observations never contain truth labels. Six controlled generators
cover switching, source reliability, delayed evidence, contradiction, multiple objects,
and goal conflict.

`evaluation/` owns the shared ablation registry, engine adapter, episode metrics, paired
episode bootstrap intervals, Pareto dominance, immutable manifests, raw JSONL, and report
generation. World generators do not mutate an engine. The hard-WTA research condition uses
the explicit `erase_losing_hypotheses()` intervention after ignition; it is not normal
dynamics. Dense-update figures are labeled counterfactual accounting and are not executed
work or energy measurements.

### `learned/` (C04 optional backend)

`learned/` is imported only when the optional `learned` dependency extra is installed. Its
fixed-width hash encoder maps observation evidence/source/channel plus numeric strength and
delay into an event representation. A learned top-k router selects a bounded set of persistent
modules. The backend indexes only those states and their K-by-K edge block before recurrent
message passing; it does not compute a dense recurrent graph and mask it afterward.

The encoder/router remain dense and are counted separately. `LearnedBrainBackend` implements
the C01 `BrainBackend` schedule/run/snapshot/state contract. Belief and action heads are
separate. Coalition traces expose support, diversity, stability, contradiction, and score;
the calibrated confidence/margin gate preserves `None` as no-ignition. The additive
`learned/contracts.py` module is the C04/C05 exchange contract and does not change Episode
schema `0.2`.

### `structural/` (C08 optional backend)

`structural/` extends the C04 backend without resizing tensors at runtime. Boolean module and
edge masks define live capacity; top-k routing excludes inactive modules and message passing
enumerates only active selected edges. `StructuralController` applies seeded structural events
only at episode boundaries in priority/sequence order. Create, duplicate, split, merge, edge
grow/prune, and module prune are explicit, budgeted mechanisms with minimum-capacity safeguards.

Logical IDs, versions, lineage, tombstones, pending events, controller RNG, optimizer state,
statistics, and budgets are checkpointed together with the inherited C01 runtime queue and
trace state. Discovery uses unlabeled routing/coactivation/credit/confidence statistics. C08's
negative causal result is documented in `docs/C08_STRUCTURAL_PLASTICITY_RESULTS.md`.

### `visualizer.py`

- self-contained HTML + SVG
- no external network dependency
- event slider and autoplay
- node activation, firing, edges, coalition table, workspace, stats

## 3. Current event model

Python coroutineをSparkごとに生成しない。Spark数に比例するtask scheduler overheadを避けるため、単一のdeterministic priority queueを使う。

```text
heapq:
(t, priority, seq, event)
```

同一時刻では `priority` と `sequence` により順序を固定する。これによりtestとtraceを再現可能にする。

## 4. Lazy state update

Dormant Sparkを毎tick更新しない。

```python
activation_at_now = activation_at_last_touch * exp(-dt / tau)
```

次にeventが到来した時だけstateへ反映する。visualizerのsnapshotはstateを変更せず、投影値だけを計算する。

この不変条件は重要であり、trace取得が計算量や挙動を変えてはならない。

## 5. Data contracts for future backends

Rate-based、PyTorch、ローカルSNN backendを交換可能にするため、次の抽象interfaceを固定する。専用neuromorphic hardwareはコアinterfaceの利用先になり得るが、完成条件には含めない。

### Dynamics backend

```python
class DynamicsBackend(Protocol):
    def integrate(self, spark_ids, events, state, now): ...
    def detect_fires(self, spark_ids, state, now): ...
    def propagate(self, fired_ids, graph, now): ...
    def snapshot(self, state, now): ...
```

### Router

```python
class EventRouter(Protocol):
    def route(self, event_embedding, brain_state, top_k) -> list[Route]: ...
```

### Coalition scorer

```python
class CoalitionScorer(Protocol):
    def build(self, active_state, evidence_graph, now) -> list[Coalition]: ...
```

### Workspace

```python
class Workspace(Protocol):
    def consider(self, coalitions, now) -> Ignition | None: ...
    def broadcast(self, ignition) -> list[Event]: ...
```

## 6. Target implementation stack

### Stage A — Reference and science correctness

- Python 3.11+
- dataclasses / heapq / json / csv
- pytest
- ruff

Reason: fastest route to inspectability, determinism, and causal ablation.

### Stage B — Learnable rate-based model

- PyTorch
- optional PyTorch Geometric for sparse message passing
- NumPy / pandas only for analysis outputs

Use cases:

- learned event routing
- learnable edge weights and thresholds
- batched episodes
- differentiable coalition scoring
- GRU / Transformer / RIM baselines

PyTorch Geometric is appropriate when the active graph is represented by sparse `edge_index` / sparse tensors. However, first implementation should preserve a custom event scheduler because ordinary message passing may still evaluate all included edges in a batch.

### Stage C — Local interactive experiment UI

Recommended split:

```text
Local FastAPI backend (bind to 127.0.0.1 by default)
  ├─ REST: config, graph, experiment control
  ├─ WebSocket: live frames
  └─ artifact export

React + TypeScript frontend
  ├─ Canvas/WebGL or Cytoscape graph
  ├─ timeline
  ├─ coalition/workspace inspector
  ├─ parameter editor
  └─ experiment comparison
```

The existing static HTML visualizer remains the reference fallback and regression oracle. The release frontend must bundle its assets and must not require an external CDN, hosted font, analytics endpoint, or SaaS session.

### Stage D — Local spiking simulation backends

1. **Norse** for PyTorch-compatible LIF/recurrent cells and learning integration.
2. **snnTorch** as an alternative for surrogate-gradient experiments and simple neuron models.
3. **NengoSPA** for semantic/spiking cognitive modeling and associative memory comparison.
4. **Brian2** for equation-level neural dynamics, STDP, and detailed timing experiments.

Do not begin Stage D until the rate-based behavioral contract and tests are stable. A reduced CPU-runnable configuration is mandatory; local GPU acceleration is optional.

### Extension H — Dedicated hardware deployment (outside core)

- optional Lava or vendor-specific process mapping
- dedicated neuromorphic hardware, FPGA, or ASIC only after local algorithmic validation
- physical power/latency methodology fixed before measurement
- failure or absence of this extension does not block the core project

The core Stage D ends at local spiking simulation.

## 7. Storage and reproducibility

### Required persisted artifacts

```text
run_manifest.json
config.json
seed.json
trace.jsonl or trace.json
metrics.json
metrics.csv
report.md
software_versions.json
```

### Run manifest

```json
{
  "run_id": "...",
  "git_commit": "...",
  "theory_version": "0.2.1",
  "engine_version": "0.2.1",
  "schema_version": "0.2",
  "local_execution": true,
  "world": "switchworld",
  "seed": 123,
  "config_hash": "...",
  "started_at": "...",
  "completed": true
}
```

Never overwrite raw run artifacts. Aggregate reports may be regenerated from raw data.

## 8. Local runtime boundary

The mandatory architecture is single-machine and local-first:

```text
Local World / Dataset
        │
        ▼
Python Engine ── local files ── Trace / Checkpoint / Results
        │
        └── 127.0.0.1 or static HTML ── Local Browser
```

Core runtime rules:

- no mandatory remote inference or model API;
- no mandatory cloud database, queue, object storage, or authentication service;
- CPU reference behavior remains available;
- all runtime artifacts have user-visible local paths;
- after dependencies and datasets are installed, the primary workflow can run offline;
- an optional external-model adapter must sit outside the cognition core and be disabled by default.

## 9. Proposed local API

### REST

- `POST /brains` — create experiment brain
- `GET /brains/{id}/graph`
- `POST /brains/{id}/events`
- `POST /brains/{id}/run`
- `POST /brains/{id}/pause`
- `POST /brains/{id}/reset`
- `GET /brains/{id}/state`
- `GET /brains/{id}/trace`
- `POST /experiments`
- `GET /experiments/{id}/results`

### WebSocket messages

```json
{
  "type": "frame",
  "time": 3.02,
  "event": "bark",
  "sparks": [],
  "coalitions": [],
  "workspace": [],
  "metrics": {}
}
```

## 10. Visual semantics

The UI must distinguish:

- role/kind by hue or shape
- activation by size/intensity
- firing by temporary ring/pulse
- inhibitory edge by dashed/signed style
- active propagation by temporary edge highlight
- coalition membership by hull/group outline
- ignition by workspace transfer animation
- uncertainty/no-ignition by explicit empty workspace state
- contradiction by negative evidence markers

Visual encoding must not imply biological anatomy unless an anatomical mapping is explicitly supported.

## 11. Performance strategy

### Do

- batch events that share time and destination type
- maintain active node sets
- lazy decay
- prune expired evidence records
- compact adjacency lists
- instrument node/edge work separately from wall-clock
- profile CPU and GPU independently
- compare semantic work, not only kernel count

### Avoid initially

- one `asyncio.Task` per Spark
- `torch.compile` before dynamic shapes stabilize
- full graph tensor materialization every event
- recurrent cycles without event budget
- claiming sparse energy efficiency from GPU runtime alone

## 12. Security and operational boundaries

The current simulator executes no untrusted code and has no network API. When the localhost control plane is added:

- validate all configuration ranges
- cap event count and recurrent depth
- isolate user-defined plugins
- prevent arbitrary path writes
- bind to loopback by default and reject remote interfaces unless an explicit non-core development mode is enabled
- preserve immutable run records

## 13. Technical debt intentionally accepted

- hand-authored evidence routing
- scalar Spark activation
- heuristic coalition score
- single-process event loop
- no persistent database
- no learned embedding
- no calibrated probability interpretation
- no biological timing claim

These are explicit phase boundaries, not hidden omissions.

## 14. Reference integrity modules added in v0.2 and v0.2.1

- `protocols.py`: shared behavioral interface for future rate/learned/spiking backends.
- `validation.py`: finite-value, configuration, Spark, and graph invariant checks.
- `serialization.py`: canonical JSON checkpoint output and normalized state hash.
- `replay.py`: dynamics-free trace reading.
- `schemas/`: versioned JSON contracts for configuration, trace, and checkpoint state.

### `external_validation/` (C06)

Model-independent external evaluation contracts live outside the cognition core:

- `belief_r.py`: official pinned test-only cache acquisition, integrity verification,
  sequential pairing, and C02 Episode mapping;
- `symbolic.py`: seeded non-monotonic streams plus an independent symbolic oracle and
  template-group splits;
- `transforms.py`: target-blind adversarial evidence-order/source transforms;
- `metrics.py`: revision/error/attribution evaluation primitives;
- `interventions.py`: evidence removal/replacement and expected-effect assessment;
- `adapters.py`: strict dev-only C05 encoder state, artifact hashing, and real C04/C05
  checkpoint adapters;
- `evaluation.py`: network-blocked Track A/B/C execution, information-condition separation,
  metrics, sanitized predictions, and intervention deltas;
- `gate.py`: fail-closed C04/C05 prerequisite check.

Dataset acquisition is the only network-capable operation and must be explicitly requested.
Normal loading, transforms, evaluation primitives, and tests are local/offline. No external
dataset text or upstream executable code is packaged.

The C05 encoder state is a strict schema with ordered vocabulary, fitted split, input size,
and SHA-256. The frozen adapter manifest validates that input size against reconstructed model
architectures before loading weights. Fit, calibration, selection, and early-stopping helpers
reject test Episodes. C04 and C05 receive the same Observation API but do not share an
effective tokenizer: this is recorded as an unmatched feature condition, not hidden as a fair
semantic-encoder comparison.

Checkpoint state includes the pending event queue, sequence number, persistent hypotheses, stability, Workspace, eligibility, counters, trace buffer, frame-local audit buffers, and RNG state. The format is research-versioned and not yet promised as a permanent public storage API.


### v0.2.1 local integrity additions

- `scripts/local_readiness_check.py`: checks the local runtime contract, required files, package version, empty core runtime dependency list, and known remote-client imports.
- `tests/test_local_only.py`: guards the package version and local-only dependency/import boundary.
- `docs/LOCAL_EXECUTION_POLICY.md`: defines mandatory local execution and optional Extension H.
- persisted config/state/trace schema remains `0.2`; package version is `0.2.1`.

## 15. C01 reference replay and inspection contract

### Frame projection and recording

- `inspect_snapshot()` is a pure projection. It returns the current visible frame without appending to `trace`, clearing frame-local audit buffers, incrementing counters, or changing dynamics state.
- `snapshot()` remains the backward-compatible recording operation. It delegates projection to `inspect_snapshot()`, appends the returned frame to `trace`, and then consumes `fired_since_frame`, `active_edges_since_frame`, and `updated_since_frame` for the next recorded frame.
- Serialization is observational: `state_dict()` and normalized hashing do not increment counters or mutate runtime state.

### Counter semantics

- `events_processed`: number of events removed from the deterministic queue and processed, including reward and internal events.
- `spark_updates`: number of `_touch` state updates. Coalition evaluation may touch active hypotheses, so this is not the number of external inputs or unique Sparks.
- `edge_evaluations`: number of outgoing connections evaluated when a Spark fires.
- `fires`, `ignitions`, and `broadcasts`: actual occurrences of the corresponding engine operations.
- Inspection and serialization are excluded from all work counters.

### Deterministic persistence boundary

Schema `0.2` checkpoints require graph state, broadcast listeners, pending queue ordering, next sequence, RNG state, Coalition stability, Workspace, eligibility, counters, trace, and frame-local audit buffers. Unsupported, incomplete, nonfinite, dangling, duplicate-ID, and past-event payloads are rejected. Two fresh canonical runs must produce the same normalized trace and state hash; checkpoint continuation must reproduce future beliefs, ignitions, counters, and trace state.

## 16. C03 localhost Brain Lab

`sparkbrain.lab` はC01 reference engineの外側に置くoptional UI control planeである。`[project].dependencies` は空のまま保ち、FastAPI/Uvicornは `lab` extraへ分離する。

```text
Bundled HTML/CSS/JavaScript
        │ REST + finite SSE
        ▼
127.0.0.1 FastAPI app
        │ pure inspection / validated commands
        ▼
In-memory LabManager ── LabRun ── SparkBrain
        │                            │
        └── local export JSON        └── C01 checkpoint / trace
```

- launcherはloopback bindだけを許可する。
- UI assetはpackageへ同梱し、CDN、analytics、remote APIを使わない。
- pause、SSE、state取得はdynamicsを進めない。
- forkは親checkpointから子runを作り、親、base hash、patchを監査可能にする。
- comparisonはrun間を同じframe indexで同期する。
- blind modeはAPI、trace、exportの全階層でtruthを除外する。
- exportはartifact root配下へ限定し、importはsizeとschemaを検証する。
- 2,000 Sparks / 10,000 edgesではengine全体を変更せず、表示用relevant subsetだけを作る。
- 既存の静的Visualizerをserver不要のfallbackおよび回帰oracleとして残す。

画面、視覚legend、介入意味論、API、保存先、性能測定の詳細は `docs/BRAIN_LAB.md` を正本とする。

## 17. C07 reduced spiking backend boundary

`SnnTorchLIFHybridBackend` implements the C01 `BrainBackend` protocol. External currents
enter stateful snnTorch LIF sensory encoders; emitted spikes gate the unchanged signed
evidence graph. Hypothesis state, evidence identity, Coalition scoring, ignition,
broadcast, and Workspace remain the deterministic rate engine. State serialization adds
membrane, filtered-spike, spike/message counters, and raw spike events. Both traces retain
schema `0.2`; per-frame spiking counts are extra allowed statistics.

## 18. v0.3 modules and integrated runtime

`sparkbrain.v03_seed` contains the C11--C17 research primitives. `V03ReferenceLoop`
connects Sensory Field, an injectable interpreter, Evidence Ledger, Coalition Gate, and persistent
belief state. `sparkbrain.v03_integration` provides the additive schema-`0.3` trace, checkpoint,
replay, and fork contract. Neither namespace replaces the legacy `SparkBrain` engine.

The implemented engineering facade is `sparkbrain.v03`:

```text
SensorySample -> IntegratedV03Brain -> V03StepResult
                         |\
                         | \-> V03TraceSession / checkpoint / fork
                         \----> observer-only concept and organ monitors
```

`IntegratedV03Brain` and `V03BrainConfig` compose sensory, evidence, entity, Coalition, revision,
belief, Workspace, action/feedback, trace, checkpoint, restore, and replay state. I3 calls the
actual C15 `RevisionController`; explicit ablations alter only their registered paths. C16 concept
and C17 organ outputs remain observational and cannot alter decisions. The legacy engine is
retained, and live inspection uses a separate `/api/v03/*` boundary rather than changing
`/api/runs*`.

## 19. v0.3.2 corrective facade and release publication

`sparkbrain.v032.IntegratedV032Brain` wraps the accepted `IntegratedV03Brain` without changing its
state model or keyword arguments. It captures the single `SensoryObservation` through an
instance-local method override that is restored in `finally`; it never patches the sensory class
globally. The public result exposes immutable channel decisions and the original v0.3 result.

`DirectCheckpointManager` serializes the default integrated runtime's current object state into
strict canonical JSON. Loading uses a fixed class registry, exact node/envelope shapes, bounded
file/depth/node counts, an envelope digest, restored state-hash validation, and atomic no-clobber
file publication. This is a trusted-local persistence contract, not a hostile-input loader or an
authenticity signature. Unsupported learned-runtime object graphs fail closed.

`sparkbrain.release_atomic.atomic_publish_directory_noreplace` dispatches to native no-replace
rename primitives on Linux, macOS, and Windows. Candidate release groups are fully staged and
validated before that single publication operation. Post-publication validation failure raises
without deleting the published path, preventing path-based cleanup from removing a replacement.

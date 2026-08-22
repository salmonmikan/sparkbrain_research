# Software Architecture

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

## 2. Current v0.2 implementation

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

### `baselines.py`

- dense evidence accumulator
- hard-WTA accumulator
- instant event classifier

These are software sanity baselines, not sufficient neural baselines.

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

Rate-based、PyTorch、SNN、neuromorphic backendを交換可能にするため、次の抽象interfaceを固定する。

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

### Stage C — Interactive experiment UI

Recommended split:

```text
FastAPI backend
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

The existing static HTML visualizer remains the reference fallback and regression oracle.

### Stage D — Spiking backends

1. **Norse** for PyTorch-compatible LIF/recurrent cells and learning integration.
2. **snnTorch** as an alternative for surrogate-gradient experiments and simple neuron models.
3. **NengoSPA** for semantic/spiking cognitive modeling and associative memory comparison.
4. **Brian2** for equation-level neural dynamics, STDP, and detailed timing experiments.

Do not begin Stage D until the rate-based behavioral contract and tests are stable.

### Stage E — Neuromorphic deployment

- Lava Process abstraction
- CPU simulation first
- asynchronous/custom protocol second
- supported neuromorphic hardware only after algorithmic validation

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
  "theory_version": "0.2",
  "engine_version": "0.2.0",
  "world": "switchworld",
  "seed": 123,
  "config_hash": "...",
  "started_at": "...",
  "completed": true
}
```

Never overwrite raw run artifacts. Aggregate reports may be regenerated from raw data.

## 8. Proposed API

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

## 9. Visual semantics

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

## 10. Performance strategy

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

## 11. Security and operational boundaries

The current simulator executes no untrusted code and has no network API. When the web control plane is added:

- validate all configuration ranges
- cap event count and recurrent depth
- isolate user-defined plugins
- prevent arbitrary path writes
- authenticate remote experiment control
- preserve immutable run records

## 12. Technical debt intentionally accepted

- hand-authored evidence routing
- scalar Spark activation
- heuristic coalition score
- single-process event loop
- no persistent database
- no learned embedding
- no calibrated probability interpretation
- no biological timing claim

These are explicit phase boundaries, not hidden omissions.

## Reference integrity modules added in v0.2

- `protocols.py`: shared behavioral interface for future rate/learned/spiking backends.
- `validation.py`: finite-value, configuration, Spark, and graph invariant checks.
- `serialization.py`: canonical JSON checkpoint output and normalized state hash.
- `replay.py`: dynamics-free trace reading.
- `schemas/`: versioned JSON contracts for configuration, trace, and checkpoint state.

Checkpoint state includes the pending event queue, sequence number, persistent hypotheses, stability, Workspace, eligibility, counters, trace buffer, frame-local audit buffers, and RNG state. The format is research-versioned and not yet promised as a permanent public storage API.

# Software Architecture — Local-First v0.2.1

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

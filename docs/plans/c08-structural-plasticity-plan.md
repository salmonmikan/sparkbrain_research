# C08 Structural Plasticity Implementation Plan

## Scope and frozen inputs

- Base commit: `039577a`.
- C04 source checkpoint: `artifacts/phase2/learned-routing-v1/main/checkpoint.pt`, SHA-256
  `15be1b56f527cb3b46a0c0b089472c2f45e82177a90a96844c303bb7b49c770e`.
- C04 resolved config SHA-256:
  `8c659c8f93b6a90c7c8b957fef7e2b35d4299e8ade887a8ff537bd96d4ea7e60`.
- C02 dev manifest SHA-256:
  `968593ff7c5f4274aaeb416bd58200e8625218d1a0179a1dff8a31d1b82a85a8`.
- C02 test manifest SHA-256:
  `3815f3857c485fb6c596f496c00ce36c437ee3b17fd97105d0fb729ff16e9e20`.
- Input hashes are checked before and after every experiment. C08 never edits these inputs.
- Test labels, test-world function names, and test effects are never used to set event or Gate
  thresholds.

## Fixed-capacity representation

C08 allocates tensors once at a configured maximum module and edge capacity. Boolean active
module and edge masks define the live graph. Inactive slots are excluded before routing and
message evaluation, rather than computed densely and masked afterward. C04 parameters fill the
initial slots; remaining slots are deterministically initialized from the structural seed.

Every slot has a stable logical ID, version, status, creation event, parent lineage, and optional
tombstone. Slot reuse creates a new logical ID/version and retains the tombstone for the prior
identity. Structural history never mutates or deletes an earlier event.

## Structural event system

The seeded controller supports bounded create, duplicate, split, merge, edge-grow, edge-prune,
and module-prune events behind explicit flags. Candidate events are queued during an episode and
applied only at the next episode boundary in deterministic `(boundary, priority, sequence)`
order. Per-boundary, per-run, module-capacity, edge-capacity, minimum-live-module, and
minimum-degree budgets reject excess events without partial mutation.

Candidate discovery uses only routing load, state co-activation, edge credit, confidence change,
homeostatic deviation, and lineage state. It may not read truth, `world_id`, scenario tags,
function labels, or object labels. `object_id` is preserved in evaluation records only for
post-hoc held-out analysis.

## Credit, homeostasis, and optimizer state

- Edge credit is an exponential trace of co-activation and prediction-confidence change.
- Module credit combines routed use, confidence contribution, and load-balance pressure.
- Homeostasis penalizes dead and overloaded slots and prevents pruning below safety floors.
- Optional reward eligibility is separate from supervised C04 training.
- Checkpoints include active masks, tensors, logical identities, versions, lineage/tombstones,
  RNG state, optimizer state, pending events, event history, counters, and remaining budgets.

## Analysis and predeclared Gates

Candidate groups are lineage-connected or high-credit active subgraphs discovered without
functional labels. Post-hoc development analysis measures:

1. **Multiplicity:** the candidate appears in at least two independent structural seeds.
2. **Decisiveness:** paired targeted-ablation impairment exceeds both random and
   degree-matched control impairment by the predeclared margin.
3. **Fertility:** the effect remains beneficial or selectively causal on held-out C02 world
   families and seeds.
4. **Specificity:** targeted impairment exceeds degradation on unrelated held-out functions.

The main Gate requires all four. Thresholds are frozen in config before test execution.
Failure of any Gate produces a valid negative result, retains CL-008 at E0, and prohibits
“organs emerged.” Allowed wording is only “candidate functional specialization.”

## Controls and sensitivity

Each targeted ablation is paired by episode/seed with:

- a uniform random live-module ablation of equal size;
- a degree-matched live-module ablation of equal size;
- an unablated structural checkpoint;
- the frozen non-structural C04 source where applicable.

Budget sensitivity varies event budget and maximum added capacity without changing Gate
thresholds. The smoke profile has a ten-minute hard cap. The main profile has a 180-minute hard
cap; a measured smaller study is acceptable when its limit is recorded without extrapolation.

## Artifact layout

`artifacts/phase3/structural-plasticity-v1/{smoke,main}/` contains input hashes, resolved config,
source and structural checkpoints, structural-event JSONL, logical-ID/lineage/tombstone graph,
raw paired rows, targeted/random/degree-matched summaries, budget sensitivity, work counters,
Gate decisions, negative findings, runtime, and an acceptance matrix.

## Acceptance matrix

| Criterion | Evidence |
| --- | --- |
| Deterministic serialized structural events | replay and checkpoint-continuation tests |
| Bounded growth | capacity/event-budget invariant tests and rejected-event rows |
| All event mechanisms | focused create/duplicate/split/merge/grow/prune tests |
| C01 protocol | runtime protocol, queue/order, state and snapshot tests |
| Actual active-edge work | selected active-edge counter invariant and dense comparison |
| Label-free candidate discovery | restricted-input API and source/import guard tests |
| Random and degree controls | paired control artifact and matching tests |
| Multiplicity/decisiveness/fertility/specificity | machine-readable Gate matrix |
| Budget sensitivity | fixed-threshold multi-budget artifact |
| Positive specialization or valid negative | all-Gate claim decision and claims boundary |
| Offline CPU reproduction | smoke/main commands and recorded runtime |

## Verification

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe -m sparkbrain.structural.experiment --config configs\experiments\phase3\smoke.json
.venv\Scripts\python.exe -m sparkbrain.structural.experiment --config configs\experiments\phase3\main.json
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe scripts\local_readiness_check.py
.venv\Scripts\python.exe scripts\validate_bundle.py
```

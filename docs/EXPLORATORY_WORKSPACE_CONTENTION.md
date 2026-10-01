# Independent workspace-contention diagnostic

Status: executed; EXPLORATORY / NON_EVIDENTIARY. Review and repository-wide CI remain pending.

## Question and scope

In the **legacy `sparkbrain.engine.SparkBrain` only**, do simultaneous, independently compatible hypotheses compete at the global ignition gate even when they have distinct competition groups and no inhibitory edges? Does increasing retained Workspace capacity change admission?

This is a frozen, bounded implementation diagnostic, not a fresh formal scientific object or an M1 result. It does not execute or modify v03, v032, v05, SYSTEM_BUILD, active Forge/FLY-0 work, or scheduler state. It does not assert that the behavior is a defect: a globally competitive bottleneck may be intentional.

## Why this is a separate question

`_evaluate_coalitions` sorts all active hypotheses; `_maybe_ignite` compares the global first and second scores and considers only the first. `workspace_slots` truncates already admitted items. This source observation motivates measuring admission separately from retention. It does not by itself establish outcomes.

The earlier H6 workspace-accounting probe (branch `research/exploratory-sub-h6-workspace-accounting-20260917`) compares broadcast cost conventions in a separate analytical toy. This diagnostic instead executes the pinned legacy gate; it makes no communication-cost claim. Existing MultiObjectWorld concerns sequential object belief tasks; here all logical tasks remain independently compatible throughout, with no truth changes or learned routing.

## Frozen protocol

See `configs/experiments/exploratory/workspace_contention/protocol.json`. It freezes 216 cells: 3 seeds × 3 task counts × 2 capacities × 2 orders × 2 strength profiles × 3 variants. High Spark firing thresholds deliberately prevent firing/reset and isolate evidence accumulation plus Coalition admission. They are not the default SwitchWorld graph. All other gate defaults are inherited from the pinned config and recorded in raw rows.

Controls include one task, capacity-only change, zero-margin intervention, and separate engines receiving the identical per-task input subsequence. The separate-engine comparator has privileged explicit task separation already available as group metadata to shared engines, and unmatched engine count/total capacity. It is a diagnostic, not a resource-matched superiority baseline. Report admission and retention separately, every seed/cell, including failures.

## Planned files and verification

- `scripts/exploratory_workspace_contention.py`: offline standard-library runner and exact frozen-protocol validator
- `tests/test_exploratory_workspace_contention.py`: protocol mutation, controls, determinism and artifact checks
- `artifacts/exploratory/workspace_contention/`: bounded raw episodes, summary and source/protocol manifest

Before running the grid, source is checkpointed on GitHub. Two fresh processes with different hash seeds must produce byte-identical artifacts. Source hashes and full runtime configs remain attached to every aggregate. Applicable focused tests and lint run locally; repository-wide checks/CI are reported separately. No runtime or official artifact changes are authorized by this document.

## Collision check

Inspected main `59fc994b39d0ba02682e972161bb46801592d25b`, Analyst R176, MAIN R215 (M1-002/PR164), Theory R30 (local atomic WORLD effect journal), and current Forge branches. This diagnostic owns only the paths above on `independent/workspace-contention-20261001`; it does not take over their work.

## Observations from the frozen grid

All 216 cells completed. The table below uses **12 episodes per row/capacity**:
3 relabel/order seeds × 2 arrival schedules × 2 strength profiles. Each value is
an unweighted mean of the fraction of compatible logical tasks that ignited at
least once within an episode. It is not task accuracy, a population success
probability, an intelligence score, or independent repeated sampling.

| Variant | Tasks | Ever admitted, slots 1 | Ever admitted, slots 4 |
|---|---:|---:|---:|
| Shared legacy gate | 1 | 100% | 100% |
| Shared legacy gate | 2 | 54.1667% (13/24 task-episodes) | 54.1667% |
| Shared legacy gate | 4 | 29.1667% (14/48 task-episodes) | 29.1667% |
| Shared, zero margin | 2 | 54.1667% | 54.1667% |
| Shared, zero margin | 4 | 58.3333% (28/48 task-episodes) | 58.3333% |
| Isolated task engines | 1, 2, 4 | 100% | 100% |

Across all 108 capacity-paired cells, changing slots from 1 to 4 left the full
Ignition sequence unchanged. Retention differed: the shared four-task engine
retained a mean 25% of tasks with one slot and 29.1667% with four slots. Thus
storage capacity and admission are different mechanisms in this reference.

The adverse conditions matter. For four tasks and four slots, the ordinary
shared gate admitted 1/4 tasks in every balanced episode under both schedules;
dominant-first, task-blocked episodes admitted 2/4, 2/4 and 1/4 across the three
seeds. Zero margin admitted 3/4 in each balanced episode but only 1/4 in each
interleaved dominant episode. Removing the margin therefore does not generally
remove all contention. The source also has global top selection and stability;
this experiment does **not** isolate those remaining contributions separately.

The isolated reference admitted every task, but has multiple engines and a
larger total state/capacity budget. This is a construction/existence control,
not evidence that isolation is a superior matched architecture. Explicit task
identities and compatible facts are hand-authored; no entity discovery,
learning, semantic generalization, contradiction handling, or M1 behavior was
evaluated. A global competition gate may intentionally impose this bottleneck.

## Reproduction and verification

Runtime source: base 59fc994b39d0ba02682e972161bb46801592d25b; the runner verifies
exact Git blob hashes of engine.py, model.py and validation.py before execution.
Protocol SHA-256: 8f4be213aee46e83e9f992156d712301b9910de383290407186974cb3bce19b0.
Final source checkpoint: fc125e570677dd2ca215dd9e4da95b6db1cfcd3e.

Python 3.12.14, standard-library-only runtime, cloud CPU execution. All 11
focused tests and repository-configured Ruff rules passed. Two fresh processes
with PYTHONHASHSEED=1 and 37 produced byte-identical raw episodes, summary and
manifest. The raw file has 216 complete episode rows (1,036,443 bytes), retaining
all inputs, configs, Ignitions, final Coalition/Workspace state and counters.

- raw_episodes.jsonl SHA-256: 1f84a20fd63b2597b8471627e5fb30fa64849dfb3c87c19a07d94254eb077b83
- summary.json SHA-256: 18ba9e705a7ad8e5aaa25ca1a4163ab45cc41102e1802829855d8ac6b3d67d15
- manifest.json SHA-256: fcf29f6b9cbec94ac6032df0fd3b992b22f0479974a7e8a286b00de818b7980f

Commands from a normal repository checkout:

```bash
PYTHONPATH=src python -m pytest tests/test_exploratory_workspace_contention.py -q
python -m ruff check scripts/exploratory_workspace_contention.py tests/test_exploratory_workspace_contention.py
PYTHONHASHSEED=1 PYTHONPATH=src python scripts/exploratory_workspace_contention.py --output /tmp/workspace-check-1 --source-commit fc125e570677dd2ca215dd9e4da95b6db1cfcd3e
PYTHONHASHSEED=37 PYTHONPATH=src python scripts/exploratory_workspace_contention.py --output /tmp/workspace-check-37 --source-commit fc125e570677dd2ca215dd9e4da95b6db1cfcd3e
diff -qr /tmp/workspace-check-1 /tmp/workspace-check-37
```

The source checkpoint is an externally verified GitHub readback recorded by the
runner, not a claim of a full clean Git checkout. Execution used a minimal cloud
source materialization. Full repository tests, local readiness, demo, benchmark
and bundle validation were not run in that partial checkout. Required final-head
GitHub CI and Codex review must be checked separately before merge.

A line-wrap-only lint correction followed initial source 40bbc3296c39e41f6e164afcc8abe80a3ebdc621.
No protocol or experimental choice changed. Final-checkpoint raw and summary
bytes exactly match the initial execution; only source-bound manifest metadata
changed. The negative/bounded outcomes were retained without tuning.

## Interpretation and next question

The narrow finding is that enlarging retained Workspace capacity does not
increase admission in this fixed legacy gate. A future, separately scoped study
could compare global versus group-local stability/top-selection while matching
state budget. This diagnostic does not authorize that implementation, a runtime
fix, or formal promotion. No existing scientific claim grade changes.

### Retained raw transport

The repository retains all 216 rows as `artifacts/exploratory/workspace_contention/raw_episodes.jsonl.gz` (gzip with zero modification time). Compression is only a transport choice; the frozen runner still emits uncompressed JSONL, and the manifest binds the decompressed raw bytes. To inspect or compare:

```bash
gzip -dc artifacts/exploratory/workspace_contention/raw_episodes.jsonl.gz > /tmp/workspace-retained-raw.jsonl
sha256sum /tmp/workspace-retained-raw.jsonl
cmp /tmp/workspace-retained-raw.jsonl /tmp/workspace-check-1/raw_episodes.jsonl
```

The decompressed SHA-256 must be `1f84a20fd63b2597b8471627e5fb30fa64849dfb3c87c19a07d94254eb077b83`. This contains the exact original data, not a sample or a rerun.

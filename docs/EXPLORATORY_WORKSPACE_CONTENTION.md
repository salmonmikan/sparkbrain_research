# Independent workspace-contention diagnostic

Status: planned; EXPLORATORY / NON_EVIDENTIARY. No execution results yet.

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

# EXPLORATORY / NON_EVIDENTIARY — Structural order path dependence, cycle 1

- mode: `discovery`
- exploratory_target: `STRUCTURAL_ORDER_PATH_DEPENDENCE_DISCOVERY`
- candidate_pool_id: `null`
- exploration_cycle: `1/3`
- source semantics: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Why independent of MAIN

MAIN owns `CAND-TOPK-PA-01` and its router/persistent-state architecture study. This Discovery does not use that branch, candidate, result, harness, checkpoint, or outcome. It instead asks an architecture-level question about the existing structural-plasticity controller: whether identical unlabeled structural observations lead to different final graphs when only their order changes.

No consumed C08 run is retried, rescored, reinterpreted, or used as an input.

## Question

For the same multiset of synthetic unlabeled routing-load and edge-credit frames, is the final structural topology sensitive to observation order, and is any sensitivity explained only by the finite production total-event budget?

## Inputs used

The probe is standalone synthetic data only. It mirrors the stable semantics of:

- `src/sparkbrain/structural/controller.py`
- `src/sparkbrain/structural/config.py`
- `src/sparkbrain/structural/model.py`

The synthetic controller starts with 12 active source modules, 18 total slots, the same self/ring initial edge mask, production thresholds (`load_high=1.65`, `load_low=0.12`, `grow_credit=0.08`, `prune_credit=0.005`), event priorities, a two-event per-boundary cap, minimum live-module/in-degree constraints, and either total event budget 16 or 64.

It never reads a repository dataset, trained checkpoint, held-out TEST manifest, preserved formal raw, official scorer, frozen identity, or formal result. Synthetic routing-load and edge-credit frames are exogenous, so production homeostatic router-bias updates are intentionally outside this cycle and remain an open factor for any promoted study.

## Experiment

Five deterministic replicate seeds (`20260919` through `20260923`) each generate a fixed multiset of 12 unlabeled synthetic structural-statistic frames. For each seed, 120 permutations of exactly that same multiset are evaluated under three event families: `full` (duplicate + module prune + edge grow + edge prune), `module_only` (duplicate + module prune), and `edge_only` (edge grow + edge prune).

Each condition is evaluated at total event budget 16 and at a generous control budget 64. For each seed/condition/budget, 300 deterministic random pairs of final graphs are sampled and module-set and edge-set Jaccard distances are measured.

The high budget is a reduction control: if order dependence is merely exhaustion of the production-wide total event budget, the distances should collapse when budget is no longer binding.

## Observations

| Budget | Condition | Mean unique final graphs / 120 | Module Jaccard distance | Edge Jaccard distance | Median applied events | Mean remaining budget |
|---:|---|---:|---:|---:|---:|---:|
| 16 | full | 116.4 | 0.1877 | 0.3299 | 16 | 0.0 |
| 16 | module_only | 95.6 | 0.2066 | 0.2939 | 16 | 0.0 |
| 16 | edge_only | 1.0 | 0.0000 | 0.0000 | 16 | 0.0 |
| 64 | full | 108.2 | 0.2301 | 0.3003 | 24 | 40.18 |
| 64 | module_only | 70.8 | 0.2818 | 0.2818 | 23 | 41.38 |
| 64 | edge_only | 1.0 | 0.0000 | 0.0000 | 16 | 48.0 |

The exact per-seed rows are reproducible from the checked-in deterministic script; the checked-in aggregate JSON records the summary above.

The reduction result is sharp in this synthetic harness. Edge-only structural updates converge to the same final graph for every sampled order at both budgets. By contrast, full and module-only conditions retain substantial order dependence even when the total budget is no longer binding. Increasing the full budget from 16 to 64 leaves mean pairwise module/edge Jaccard distances at about `0.230/0.300`, with roughly 40 events of budget still unused.

This localizes the candidate source of noncommutativity to stateful module duplicate/prune decisions and the resulting active-slot history, rather than to edge update order or total budget exhaustion alone. This remains an architecture diagnostic, not evidence of functional benefit, harm, emergent specialization, novelty, or behavior on real DEV data.

## What would falsify or reduce it

A prospectively fixed DEV-only architecture study would reduce/reject this candidate if matched-multiset order permutations produce negligible topology/output divergence, or if divergence collapses under an identity-neutral/module-event comparator that preserves event counts/resources while removing stateful slot-selection history. A result that is topology-different but functionally indistinguishable should narrow this to an engineering reproducibility issue rather than a research object.

## Candidate next research layer

`ARCHITECTURE_STUDY`.

A fresh Analyst-owned prospective study could test matched-multiset regime-order permutations on a fresh DEV-only structural model and measure both graph divergence and functional/output divergence, with no C08 TEST or preserved material.

## Scientific choices still open

- fresh DEV-only task/regime construction and fixed train/probe split;
- exact matched-multiset permutation family;
- module-identity matching or identity-neutral graph distance;
- output/behavior divergence metric and horizon;
- event-count/resource-matched noncommutative comparator;
- whether to include homeostatic router-bias updates as a prospectively declared factor.

These choices must be fixed before any promoted architecture study. They are not tuned in this Discovery run.

## Recommendation

`PROMOTE_TO_ARCHITECTURE_STUDY`.

The promotion is for the system-level path-dependence question only. The synthetic numbers remain `NON_EVIDENTIARY` and must not be relabeled as formal support.

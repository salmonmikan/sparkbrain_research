# Project Status — SparkBrain v0.2

Status date: 2026-08-22

## 1. Current maturity

The repository is a **Phase-0 functional research prototype**. It demonstrates an inspectable event-driven state machine with persistent competing hypotheses, evidence provenance, Coalition scoring, ignition, Workspace broadcast, residual loser retention, and a minimal reward-modulated plasticity hook.

It is not yet a learned architecture, a spiking implementation, a validated biological model, or a matched comparison against modern neural baselines.

## 2. Completed and runnable

| Deliverable | State | Evidence |
|---|---|---|
| Project charter | complete v0.2 | `docs/PROJECT_CHARTER.md` |
| Theory specification | working v0.2 | `docs/THEORY_SPEC_v0.2.md` |
| Prior-art gap analysis | initial review complete | `docs/PRIOR_ART_GAP_ANALYSIS.md` |
| Deterministic reference engine | runnable | `src/sparkbrain/engine.py` |
| Spark/Event/Coalition/Workspace data model | runnable | `src/sparkbrain/model.py` |
| Canonical and randomized SwitchWorld | runnable | `src/sparkbrain/worlds.py` |
| Phase-0 scalar baselines and ablations | runnable | `src/sparkbrain/baselines.py`, `benchmark.py` |
| Metrics for stability/revision/recovery | runnable | `src/sparkbrain/metrics.py` |
| Static replay visualizer | runnable | `artifacts/demo/visualizer.html` |
| Unit tests | 26 passing | `python -m pytest -q` |
| Generated Phase-0 report | complete with limitations | `artifacts/benchmarks/benchmark_report.md` |
| Codex repository instructions | complete | `AGENTS.md`, `.agents/skills/sparkbrain-research/SKILL.md` |
| Versioned checkpoint and trace replay | implemented | `serialization.py`, `replay.py`, `schemas/` |
| Detailed Codex execution queue | complete | `docs/CODEX_EXECUTION_BRIEF.md`, `docs/codex/` |

## 3. Verified commands

```bash
python -m pytest -q
python scripts/run_demo.py
python scripts/run_benchmark.py --episodes 40 --steps 30
python scripts/validate_bundle.py
```

The verified baseline at this status date contains 26 passing tests. The benchmark is deterministic and hand-authored; it validates software behavior only.

## 4. Current Phase-0 observation

On the bundled 40×30 SwitchWorld run, the full SparkBrain configuration reached approximately:

- all-step accuracy: 0.640
- coverage: 0.937
- revision recall: 0.666
- revision precision: 0.614
- mean switch latency: 1.352 events
- recovery rate: 0.644

The accumulator baseline is close in this hand-authored setting. Therefore this result does **not** support a general performance advantage. The main valid observation is that residual removal materially harms the current scenario, while single-Spark ignition changes the revision/precision trade-off. These are hypothesis-generating results, not decisive evidence.

## 5. Major uncompleted work

| Priority | Missing capability | Codex task |
|---:|---|---|
| P0 | finish strict replay/schema edge cases, CI execution, compatibility policy | C01 |
| P0 | controlled worlds, full ablations, uncertainty estimates | C02 |
| P1 | live interactive Brain Lab and interventions | C03 |
| P1 | learned event encoding/routing and held-out generalization | C04 |
| P1 | matched GRU/Transformer/RIM/Bayesian baselines | C05 |
| P1 | external belief-revision and relational tasks | C06 |
| P2 | rate-to-spiking backend equivalence | C07 |
| P2 | structural plasticity and emergent-organ tests | C08 |
| continuous | systematic prior-art review and novelty audit | C09 |
| release | reproducibility/publication package | C10 |

## 6. Exit criteria for the requested final system

The project reaches its stated destination only when all are true:

1. Spark, interaction, Coalition, ignition, memory, learning, organ, and global state are formally versioned.
2. Every primary theoretical claim maps to code, tests, and an experiment.
3. The system can run continuously in at least three nontrivial worlds.
4. A user can observe and causally intervene on Spark and connection state through the visual interface.
5. Learned routing generalizes to held-out combinations.
6. Comparisons include matched modern neural and probabilistic baselines.
7. Belief maintenance, justified revision, no-ignition, and loser recovery are separately measured.
8. A spiking backend reproduces predefined behavioral invariants or documents where equivalence fails.
9. Raw results, seeds, configs, and code produce the reported figures independently.
10. Claims remain limited to evidence; biological and energy claims require separate validation.

## 7. Immediate execution order

```text
C01 ─┬─> C02 ─┬─> C04 ─┬─> C06 ─> C10
     │         └─> C05 ┘
     └─> C03

C04 ─> C07
C04 ─> C08
C09 runs continuously and must review C10 claims.
```

C01 is the only strict first task. C03 may begin once C01 freezes trace and control interfaces. C04 and C05 should share the same data harness and splits.

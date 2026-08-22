# Project Status — SparkBrain v0.2.1

Status date: 2026-08-23

## 1. Current maturity

The repository is a **Phase-0 local functional research prototype**. It demonstrates an inspectable event-driven state machine with persistent competing hypotheses, evidence provenance, Coalition scoring, ignition, Workspace broadcast, residual loser retention, and a minimal reward-modulated plasticity hook.

v0.2.1 fixes the core destination to one general-purpose local computer, adds a plain-language foundation guide and expanded glossary, and moves dedicated neuromorphic hardware to an independent extension track.

It is not yet a learned architecture, a completed spiking implementation, a validated biological model, or a matched comparison against modern neural baselines.

## 2. Local execution contract

The core system must:

- run its reference behavior on CPU;
- require no cloud service or remote model API at runtime;
- keep config, trace, checkpoint, results, and reports on local storage;
- provide a static or localhost-only UI;
- remain runnable offline after dependencies are installed.

Local GPU and local SNN simulation are optional. Dedicated hardware is not a core exit criterion.

See `docs/LOCAL_EXECUTION_POLICY.md`.

## 3. Completed and runnable

| Deliverable | State | Evidence |
|---|---|---|
| Project charter | complete v0.2.1 | `docs/PROJECT_CHARTER.md` |
| Theory specification | working v0.2.1 | `docs/THEORY_SPEC_v0.2.1.md` |
| Beginner foundation guide | complete | `docs/FOUNDATIONS_FOR_BEGINNERS.md` |
| Plain-language glossary | expanded | `docs/GLOSSARY.md` |
| Local execution policy | complete | `docs/LOCAL_EXECUTION_POLICY.md` |
| Prior-art gap analysis | initial review complete | `docs/PRIOR_ART_GAP_ANALYSIS.md` |
| Deterministic reference engine | runnable | `src/sparkbrain/engine.py` |
| Spark/Event/Coalition/Workspace model | runnable | `src/sparkbrain/model.py` |
| Canonical and randomized SwitchWorld | runnable | `src/sparkbrain/worlds.py` |
| Phase-0 scalar baselines and ablations | runnable | `src/sparkbrain/baselines.py`, `benchmark.py` |
| Metrics for stability/revision/recovery | runnable | `src/sparkbrain/metrics.py` |
| Static replay visualizer | runnable locally | `artifacts/demo/visualizer.html` |
| Unit tests | 55 passing | `python -m pytest -q` |
| Local readiness audit | runnable | `scripts/local_readiness_check.py` |
| Generated Phase-0 report | complete with limitations | `artifacts/benchmarks/benchmark_report.md` |
| Codex repository instructions | complete | `AGENTS.md`, `.agents/skills/sparkbrain-research/SKILL.md` |
| Versioned checkpoint and trace replay | C01 accepted | `serialization.py`, `replay.py`, `schemas/`, `tests/test_schemas.py`, CI run `32594805438` |
| Detailed Codex execution queue | complete | `docs/CODEX_EXECUTION_BRIEF.md`, `docs/codex/` |

## 4. Verified local commands

```bash
python scripts/local_readiness_check.py
python -m pytest -q
python scripts/run_demo.py
python scripts/checkpoint_demo.py
python scripts/replay_trace.py
python scripts/run_benchmark.py --episodes 40 --steps 30
python scripts/validate_bundle.py
```

The persisted config/state/trace schema remains `0.2`; package and documentation version is `0.2.1`.

## 5. Current Phase-0 observation

On the bundled 40×30 SwitchWorld run, the full SparkBrain configuration reached approximately:

- all-step accuracy: 0.640
- coverage: 0.937
- revision recall: 0.666
- revision precision: 0.614
- mean switch latency: 1.352 events
- recovery rate: 0.644

The accumulator baseline is close in this hand-authored setting. Therefore this result does **not** support a general performance advantage. The valid observation is narrower: residual removal materially harms the current scenario, while single-Spark ignition changes the revision/precision trade-off. These are hypothesis-generating results, not decisive evidence.

## 6. Major uncompleted work

| Priority | Missing capability | Codex task |
|---:|---|---|
| P0 | controlled worlds, full ablations, uncertainty estimates | C02 |
| P1 | local interactive Brain Lab and interventions | C03 |
| P1 | learned event encoding/routing and held-out generalization | C04 |
| P1 | matched GRU/Transformer/RIM/Bayesian baselines | C05 |
| P1 | external belief-revision and relational tasks with local cached datasets | C06 |
| P2 | local rate-to-spiking backend equivalence | C07 |
| P2 | structural plasticity and emergent-organ tests | C08 |
| continuous | systematic prior-art review and novelty audit | C09 |
| release | local reproducibility/publication package | C10 |

## 7. Exit criteria for the core final system

The project reaches its stated core destination only when all are true:

1. Spark, interaction, Coalition, ignition, memory, learning, organ, and global state are formally versioned.
2. Every primary theoretical claim maps to code, tests, and an experiment.
3. The system runs continuously in at least three nontrivial worlds on one local machine.
4. A user can observe and causally intervene on Spark and connection state through a local visual interface.
5. Learned routing generalizes to held-out combinations.
6. Comparisons include matched modern neural and probabilistic baselines.
7. Belief maintenance, justified revision, no-ignition, and loser recovery are separately measured.
8. A local spiking backend reproduces predefined behavioral invariants or documents where equivalence fails.
9. Raw results, seeds, configs, code, and local commands reproduce reported figures.
10. CPU reference execution remains available without a remote API or cloud service.
11. Core UI and storage remain local/offline-capable.
12. Claims remain limited to evidence; biological and hardware-energy claims require separate validation.

Dedicated hardware execution is not required by these criteria.

## 8. Immediate execution order

```text
C01 ─┬─> C02 ─┬─> C04 ─┬─> C06 ─> C10
     │         └─> C05 ┘
     └─> C03

C04 ─> C07
C04 ─> C08
C09 runs continuously and must review C10 claims.
```

C01 is accepted: schema `0.2`, deterministic fresh-run replay, checkpoint continuation, pure inspection, bounded event failure, and counter contracts are covered locally and by the Python 3.11/3.13 CI matrix. C02 and C03 are unblocked. C04 and C05 should share the same local data harness and splits.

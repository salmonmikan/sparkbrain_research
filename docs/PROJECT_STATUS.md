# Project Status — SparkBrain v0.2.1

Status date: 2026-08-23

## 1. Current maturity

The repository is a **Phase-0 local functional research prototype**. It demonstrates an inspectable event-driven state machine with persistent competing hypotheses, evidence provenance, Coalition scoring, ignition, Workspace broadcast, residual loser retention, and a minimal reward-modulated plasticity hook.

v0.2.1 fixes the core destination to one general-purpose local computer, adds a plain-language foundation guide and expanded glossary, and moves dedicated neuromorphic hardware to an independent extension track.

It now includes an optional controlled-synthetic learned-routing backend. It is not yet a
validated biological model or a matched comparison against modern neural baselines. C07 adds
only a reduced hybrid canonical comparison.

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
| Prior-art gap analysis | bounded adversarial second pass complete; monitoring remains continuous | `docs/PRIOR_ART_GAP_ANALYSIS.md`, `docs/research/` |
| Deterministic reference engine | runnable | `src/sparkbrain/engine.py` |
| Spark/Event/Coalition/Workspace model | runnable | `src/sparkbrain/model.py` |
| Canonical and randomized SwitchWorld | runnable | `src/sparkbrain/worlds.py` |
| Phase-0 scalar baselines and ablations | runnable | `src/sparkbrain/baselines.py`, `benchmark.py` |
| C02 controlled worlds and statistical suite | implemented with negative results | `src/sparkbrain/tasks/`, `evaluation/`, `artifacts/phase1/c02-main-1000/` |
| C04 learned sparse-rate backend | implemented with held-out synthetic result and collapse diagnostics | `src/sparkbrain/learned/`, `artifacts/phase2/`, `docs/C04_LEARNED_ROUTING_RESULTS.md` |
| Metrics for stability/revision/recovery | runnable | `src/sparkbrain/metrics.py` |
| Static replay visualizer | runnable locally | `artifacts/demo/visualizer.html` |
| Unit tests | 134 passing with PyTorch available; optional learned/spiking tests require their extras | `python -m pytest -q` |
| Local readiness audit | runnable | `scripts/local_readiness_check.py` |
| Generated Phase-0 report | complete with limitations | `artifacts/benchmarks/benchmark_report.md` |
| Codex repository instructions | complete | `AGENTS.md`, `.agents/skills/sparkbrain-research/SKILL.md` |
| Versioned checkpoint and trace replay | C01 accepted | `serialization.py`, `replay.py`, `schemas/`, `tests/test_schemas.py`, CI run `32594805438` |
| Interactive localhost Brain Lab | C03 accepted locally | `src/sparkbrain/lab/`, `docs/BRAIN_LAB.md`, `tests/test_brain_lab_*.py` |
| Reduced local spiking backend | hybrid canonical equivalence; fully spiking work remains | `src/sparkbrain/spiking.py`, `artifacts/spiking/` |
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
| P1 | matched GRU/Transformer/RIM/Bayesian baselines | C05 |
| P1 | external belief-revision and relational tasks with local cached datasets | C06 |
| P2 | fully spiking and multi-world equivalence beyond the reduced hybrid | C07 follow-on |
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

C01 is accepted: schema `0.2`, deterministic fresh-run replay, checkpoint continuation, pure inspection, bounded event failure, and counter contracts are covered locally and by the Python 3.11/3.13 CI matrix. C03 is locally accepted: loopback control, deterministic pause/step/reset, event injection, immutable-parent intervention forks, synchronized comparison, blind-safe export/import, bundled offline UI, API/E2E/accessibility contracts, and relevant-subset performance are covered.

C02 is locally implemented. The frozen main run completed 37 declared conditions with
1,000 episodes each and generated raw rows, bootstrap intervals, Pareto output, and three
deterministically selected failure visualizations. This is an E2 controlled synthetic result,
not external validation. MultiObjectWorld produced no full-system ignition under the frozen
configuration and is retained as a negative result; C04/C05 must not tune against its test
seeds. C04 and C05 must share this frozen data harness and its split manifests.

C04 is locally implemented on the immutable C02 manifests. Its 60-episode held-out CPU profile
beat chance and the training-majority baseline while retaining calibrated no-ignition and
non-hand-authored recovery cases. The router nevertheless exhibited dead/overloaded modules,
and the reduced smoke profile was below chance. These negative findings remain explicit.

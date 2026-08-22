# AGENTS.md — SparkBrain Research Repository v0.2.1

## Mission

Build and test an inspectable, falsifiable cognitive architecture in which persistent local activity units (Sparks) compete, form evidence-bearing Coalitions, ignite a capacity-limited Workspace, and revise beliefs over time.

The core artifact must run on one general-purpose local computer. Correct attribution, reproducibility, explicit limitations, negative results, and local/offline-capable execution are mandatory.

## Read before changing code

Read these files in order:

1. `docs/START_HERE.md`
2. `docs/PROJECT_CHARTER.md`
3. `docs/LOCAL_EXECUTION_POLICY.md`
4. `docs/THEORY_SPEC_v0.2.1.md`
5. `docs/PROJECT_STATUS.md`
6. `docs/SOFTWARE_ARCHITECTURE.md`
7. `docs/EXPERIMENT_PROTOCOL.md`
8. the assigned task in `docs/codex/`
9. `docs/DECISION_LOG.md`

For terminology or reader-facing explanations, also read:

- `docs/FOUNDATIONS_FOR_BEGINNERS.md`
- `docs/GLOSSARY.md`

For prior-art or claim changes, also read:

- `docs/PRIOR_ART_GAP_ANALYSIS.md`
- `docs/SOURCES.md`
- `docs/CLAIMS_REGISTER.md`

## Standard local commands

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
python scripts/local_readiness_check.py
python -m pytest -q
python -m ruff check .
python scripts/run_demo.py
python scripts/run_benchmark.py --episodes 40 --steps 30
python scripts/validate_bundle.py
```

Run the smallest relevant test during development and the full local validation sequence before completion.

## Non-negotiable local rules

1. Core runtime must not require a cloud service, remote LLM/model API, cloud database, remote queue, or remote object store.
2. Keep a CPU reference path for every required behavior. Local GPU acceleration may be optional but never the only path.
3. Runtime artifacts must have explicit local paths. Do not silently upload traces, configs, prompts, results, or telemetry.
4. Release UI must run as static files or on loopback/localhost and must not require external CDN assets, hosted fonts, analytics, or SaaS login.
5. External datasets may be downloaded during setup, but primary evaluation must run from a documented local cache afterward.
6. Dedicated neuromorphic hardware, FPGA, ASIC, or physical power measurement belongs to Extension H and must not block core tasks.
7. CI may supplement but never replace the equivalent local command sequence.

## Non-negotiable research rules

1. Do not call the system a human brain reproduction, conscious system, AGI, or biologically equivalent model.
2. Do not claim novelty because a search returned no exact match. Record search scope and uncertainty.
3. Do not claim energy efficiency from activity counts, FLOPs, masks, or CPU/GPU wall-clock alone.
4. Do not allow visualization code to invent, smooth, aggregate, or infer hidden state unless the UI labels the transformation explicitly.
5. Do not count repeated propagation of one evidence ID as independent evidence.
6. Do not count internal lateral inhibition as external contradiction evidence.
7. Keep deterministic reference behavior independent from learned and spiking backends.
8. Preserve no-ignition as a valid state. Never force a prediction solely to simplify a metric.
9. Retain raw per-episode outputs, seeds, configurations, and version metadata for every reported aggregate.
10. Record failed hypotheses and negative results in `docs/RESULTS_LEDGER.md`.

## Code conventions

- Python 3.11+; typed public APIs.
- Prefer small dataclasses and explicit state over implicit globals.
- Reference engine remains dependency-light, deterministic, CPU-runnable, and network-independent.
- Time-changing state must be serializable or represented in a trace.
- Inspection must not mutate dynamics or increment computation counters.
- Use seeded randomness and pass generators explicitly where practical.
- Public configuration requires validation and round-trip serialization tests.
- New backends implement a shared behavioral protocol rather than forking task logic.
- Avoid per-Spark `asyncio` tasks. Model as a discrete-event queue or batched active set.
- Use comments for invariant rationale, not line-by-line narration.

## Documentation consistency

Whenever a core term changes, update all affected layers:

1. formal definition in `THEORY_SPEC_v0.2.1.md` or its successor;
2. plain-language explanation in `FOUNDATIONS_FOR_BEGINNERS.md`;
3. concise term entry in `GLOSSARY.md`;
4. code/test contract;
5. Decision Log and version note.

Do not simplify a beginner explanation until it contradicts the formal specification. Clearly label analogies as analogies.

## Test expectations

Every dynamics change needs at least one focused test for the intended effect and one adversarial or boundary test. Relevant categories include:

- duplicate evidence
- contradictory evidence
- residual loser recovery
- cooldown and stability
- workspace capacity
- event ordering and delays
- refractory and homeostasis
- deterministic replay
- no-ignition behavior
- trace non-interference
- serialization compatibility
- sparse accounting
- local-only dependency boundary
- offline/static UI assets

## Documentation and claims

When behavior changes:

- update theory only when the intended theory changes;
- update software architecture when implementation contracts change;
- update experiment protocol when metrics/data/splits change;
- append a dated decision or result rather than silently rewriting history;
- regenerate generated artifacts and state the exact command.

Package patch version and persisted schema version are distinct. v0.2.1 intentionally keeps schema `0.2`.

Use evidence grades from `docs/CLAIMS_REGISTER.md`. Keep “implemented,” “observed in Phase-0,” “supported,” and “established” distinct.

## Definition of done for an assigned task

A task is done only when all of the following are true:

- every acceptance criterion in its `docs/codex/*.md` brief is met or explicitly marked blocked;
- local readiness passes;
- tests pass;
- generated artifacts are reproducible locally;
- docs and status are updated;
- no overclaim is introduced;
- no mandatory external-service dependency is introduced;
- the completion report includes changed files, local commands, results, acceptance status, limitations, and follow-up risks.

Do not merge unrelated cleanup into a research task. Keep changes reviewable and scoped.

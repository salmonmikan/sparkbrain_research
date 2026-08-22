# AGENTS.md — SparkBrain Research Repository

## Mission

Build and test an inspectable, falsifiable cognitive architecture in which persistent local activity units (Sparks) compete, form evidence-bearing Coalitions, ignite a capacity-limited Workspace, and revise beliefs over time.

This repository is a research system, not a product demo. Correct attribution, reproducibility, explicit limitations, and negative results are mandatory.

## Read before changing code

Read these files in order:

1. `docs/PROJECT_CHARTER.md`
2. `docs/THEORY_SPEC_v0.2.md`
3. `docs/PROJECT_STATUS.md`
4. `docs/SOFTWARE_ARCHITECTURE.md`
5. `docs/EXPERIMENT_PROTOCOL.md`
6. the assigned task in `docs/codex/`
7. `docs/DECISION_LOG.md`

For prior-art or claim changes, also read:

- `docs/PRIOR_ART_GAP_ANALYSIS.md`
- `docs/SOURCES.md`
- `docs/CLAIMS_REGISTER.md`

## Standard commands

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install -e ".[dev]"
python -m pytest -q
python -m ruff check .
python scripts/run_demo.py
python scripts/run_benchmark.py --episodes 40 --steps 30
python scripts/validate_bundle.py
```

Run the smallest relevant test during development and the full validation sequence before completion.

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
- Reference engine remains dependency-light and deterministic.
- Time-changing state must be serializable or represented in a trace.
- Inspection must not mutate dynamics or increment computation counters.
- Use seeded randomness and pass generators explicitly where practical.
- Public configuration requires validation and round-trip serialization tests.
- New backends implement a shared behavioral protocol rather than forking task logic.
- Avoid per-Spark `asyncio` tasks. Model as a discrete-event queue or batched active set.
- Use comments for invariant rationale, not line-by-line narration.

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

## Documentation and claims

When behavior changes:

- update theory only when the intended theory changes;
- update software architecture when implementation contracts change;
- update experiment protocol when metrics/data/splits change;
- append a dated decision or result rather than silently rewriting history;
- regenerate generated artifacts and state the exact command.

Use evidence grades from `docs/CLAIMS_REGISTER.md`. Keep “implemented,” “observed in Phase-0,” “supported,” and “established” distinct.

## Definition of done for an assigned task

A task is done only when all of the following are true:

- every acceptance criterion in its `docs/codex/*.md` brief is met or explicitly marked blocked;
- tests pass;
- generated artifacts are reproducible;
- docs and status are updated;
- no overclaim is introduced;
- the completion report includes changed files, commands, results, limitations, and follow-up risks.

Do not merge unrelated cleanup into a research task. Keep changes reviewable and scoped.

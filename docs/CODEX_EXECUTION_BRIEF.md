# Codex Execution Brief

## 1. Purpose

This document is the operator entrypoint for handing unfinished SparkBrain work to Codex. The repository already contains a runnable Phase-0 prototype. Codex should extend it through the detailed task briefs without conflating implementation completion with scientific validation.

## 2. First command to give Codex

```text
Use $sparkbrain-research. Read AGENTS.md, docs/PROJECT_STATUS.md, and docs/CODEX_EXECUTION_BRIEF.md. Execute C01 from docs/codex/C01_ENGINE_HARDENING.md completely. Work only within that task's scope. Run all acceptance tests and update the project status and results ledger before reporting completion.
```

After C01 is accepted, assign one task per Codex thread/worktree. Do not ask several agents to edit shared contracts simultaneously.

## 3. Task queue

| Task | Purpose | Depends on | Parallel notes |
|---|---|---|---|
| C01 | complete hardening around existing checkpoint/replay/config/CI scaffold | current v0.2 | first |
| C02 | controlled worlds, ablations, statistics | C01 | can run beside C03 |
| C03 | interactive Brain Lab | C01 interface freeze | avoid editing experiment core |
| C04 | learned encoder/router/active graph | C01, preferably C02 harness | coordinate data APIs with C05 |
| C05 | matched neural/probabilistic baselines | C01, C02 harness | parallel with C04 |
| C06 | external benchmark adapters | C04 and C05 minimum viable | after matched harness |
| C07 | spiking backend equivalence | C01 invariants; C04 optional | do not make energy claims |
| C08 | structural plasticity/emergent organs | C04 | high risk |
| C09 | systematic prior-art and novelty audit | none | continuous, separate docs branch |
| C10 | reproducibility and publication package | primary results from C02–C07 | last release task |

## 4. Recommended branch/worktree naming

```text
codex/c01-engine-hardening
codex/c02-controlled-worlds
codex/c03-brain-lab
codex/c04-learned-routing
codex/c05-matched-baselines
codex/c06-external-validation
codex/c07-spiking-backend
codex/c08-structural-plasticity
codex/c09-prior-art-audit
codex/c10-release-package
```

## 5. Shared integration contracts

Tasks must not independently invent incompatible representations. The following contracts are shared:

- `BrainBackend` behavior: reset, ingest event, advance/run, snapshot, serialize, restore, stats.
- `TraceFrame` versioned schema.
- `Episode` and `Observation` task schema.
- prediction may be `None` and metrics must preserve that state.
- raw output manifest: code version, config hash, dataset split, seeds, command, start/end time.
- Spark/edge IDs remain stable within a replay.
- UI consumes trace/control APIs and does not import engine internals directly.

C01 should formalize these before downstream implementation.

## 6. Integration gates

### Gate G1 — Reference integrity

C01 passes. Required before merging C02–C08.

### Gate G2 — Research harness

C02 provides datasets/splits/statistics and C05 provides baseline harness. Required before claiming comparative performance.

### Gate G3 — Learned architecture

C04 demonstrates held-out performance and real active routing. Required before calling SparkBrain a learned neural architecture.

### Gate G4 — External validity

C06 reports external benchmark results and failure analysis. Required before general claims about belief revision.

### Gate G5 — substrate comparison

C07 passes behavioral-equivalence tests. Required before claims about a spiking implementation.

### Gate G6 — release integrity

C09 reviews novelty wording and C10 reproduces all primary outputs from a clean environment.

## 7. Merge review checklist

- task acceptance criteria checked one by one;
- full tests and validation command pass;
- generated raw data included or reproducible;
- no undocumented parameter tuning on test data;
- no claim-grade increase without evidence record;
- no trace/UI mismatch;
- dependencies and licenses recorded;
- status, decision log, and results ledger updated;
- unrelated refactors excluded.

## 8. Completion report format for every Codex task

```text
Task:
Status: complete / partial / blocked
Summary:
Files changed:
Commands run:
Tests:
Generated artifacts:
Acceptance criteria:
Scientific result, if any:
Negative results:
Known limitations:
Claim-register changes:
Next recommended task:
```

## 9. Operator rule

A Codex task is not accepted merely because code compiles. Accept only against the task brief and generated evidence. A partial result should remain partial; do not ask Codex to hide or reword failures as completion.

---
name: sparkbrain-research
description: Implement, test, review, or document the local-first SparkBrain theory, event-driven dynamics, controlled worlds, visualizer, learned routing, neural baselines, belief-revision experiments, local spiking simulation, or reproducibility tasks in this repository.
---

# SparkBrain research workflow

1. Read root `AGENTS.md`, `docs/LOCAL_EXECUTION_POLICY.md`, and the assigned `docs/codex/*.md` brief.
2. Read `docs/PROJECT_STATUS.md` so completed and unvalidated work are not confused.
3. State the selected task ID, dependency status, and how it remains local/offline-capable.
4. Inspect the current implementation and tests before editing.
5. Implement the smallest complete vertical slice that satisfies the assigned acceptance criteria.
6. Add focused tests, including at least one failure or boundary case.
7. Run `python scripts/local_readiness_check.py` plus commands required by the task and root `AGENTS.md`.
8. Regenerate only artifacts affected by the change.
9. Update `docs/PROJECT_STATUS.md`, `docs/RESULTS_LEDGER.md`, and any changed contract document.
10. Return a completion report containing:
   - task ID;
   - files changed;
   - local commands run;
   - test and benchmark results;
   - acceptance criteria status;
   - local/offline compliance;
   - limitations and blocked items;
   - exact next task recommendation.

## Research safeguards

- Treat current equations and defaults as hypotheses, not biological constants.
- Never tune on test episodes and then report the same episodes as held-out evidence.
- Never compare against a deliberately weak baseline without also including the strongest feasible matched baseline.
- Preserve raw traces and configurations behind aggregate tables.
- Label hand-authored routing, learned routing, rate dynamics, and spiking dynamics distinctly.
- If a requested claim is unsupported, improve the experiment or narrow the claim; do not strengthen the wording.
- Keep cloud APIs and dedicated hardware outside core task acceptance criteria.
- Keep a CPU-runnable reduced configuration for learned and spiking experiments.

## Task invocation examples

```text
Use $sparkbrain-research. Audit the current v0.3.1 integration against docs/PROJECT_STATUS.md and docs/THEORY_SPEC_v0.3.md. Treat C01--C20 as recorded history, preserve scientific boundaries, and implement only the explicitly assigned follow-up.
```

```text
Use $sparkbrain-research. Audit C04 against its acceptance criteria without changing code; include CPU feasibility and offline data requirements in docs/audits/C04_AUDIT.md.
```

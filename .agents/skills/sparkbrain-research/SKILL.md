---
name: sparkbrain-research
description: Implement, test, review, or document SparkBrain theory, event-driven dynamics, controlled worlds, visualizer, learned routing, neural baselines, belief-revision experiments, spiking backends, or reproducibility tasks in this repository.
---

# SparkBrain research workflow

1. Read root `AGENTS.md` and the assigned `docs/codex/*.md` brief.
2. Read `docs/PROJECT_STATUS.md` so completed and unvalidated work are not confused.
3. State the selected task ID and its dependency status in the working plan.
4. Inspect the current implementation and tests before editing.
5. Implement the smallest complete vertical slice that satisfies the assigned acceptance criteria.
6. Add focused tests, including at least one failure or boundary case.
7. Run the commands required by the task and root `AGENTS.md`.
8. Regenerate only artifacts affected by the change.
9. Update `docs/PROJECT_STATUS.md`, `docs/RESULTS_LEDGER.md`, and any changed contract document.
10. Return a completion report containing:
   - task ID;
   - files changed;
   - commands run;
   - test and benchmark results;
   - acceptance criteria status;
   - limitations and blocked items;
   - exact next task recommendation.

## Research safeguards

- Treat current equations and defaults as hypotheses, not biological constants.
- Never tune on test episodes and then report the same episodes as held-out evidence.
- Never compare against a deliberately weak baseline without also including the strongest feasible matched baseline.
- Preserve raw traces and configurations behind aggregate tables.
- Label hand-authored routing, learned routing, rate dynamics, and spiking dynamics distinctly.
- If a requested claim is unsupported, improve the experiment or narrow the claim; do not strengthen the wording.

## Task invocation examples

```text
Use $sparkbrain-research. Execute C01 from docs/codex/C01_ENGINE_HARDENING.md completely. Do not start dependent tasks.
```

```text
Use $sparkbrain-research. Audit C04 against its acceptance criteria without changing code; write the findings to docs/audits/C04_AUDIT.md.
```

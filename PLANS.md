# Execution Plan Standard

For work expected to span multiple files or more than one implementation cycle, create `docs/plans/<task-id>-plan.md` before editing code.

The plan must contain:

1. **Objective** — the falsifiable outcome, not merely files to edit.
2. **Current behavior** — observed by tests or commands.
3. **Theory contract** — equations/invariants affected.
4. **Implementation slices** — independently testable increments.
5. **Data and evaluation** — train/dev/test split, seeds, metrics, raw outputs.
6. **Risk register** — scientific confounds, software risks, performance risks, and local/offline compliance risks.
7. **Acceptance criteria** — copied from the assigned task and made executable where possible.
8. **Validation commands** — exact local commands, including `python scripts/local_readiness_check.py`.
9. **Documentation updates** — files that will change.
10. **Local execution contract** — CPU path, local data paths, offline behavior, and optional acceleration.
11. **Rollback boundary** — how to revert without corrupting generated results.

Update the plan as facts change. Mark assumptions that were disproven rather than deleting them.

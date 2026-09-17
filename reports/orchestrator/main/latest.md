# MAIN Orchestrator — PRIMARY post-START reconciliation

Timestamp: `2026-09-18 02:18 JST`
Execution mode: `PRIMARY`
Evidence Analyst authority: `42836802e78abd26d19c5b8a789411f2b03d0ea1`

## MAIN frontier

C19-R1 remains the primary frontier, but the exact official identity `c19-r1-revision-authority-official-v1` is now terminal operationally as `POST_START_FAILURE`. It crossed STARTED on `control/c19-r1-revision-authority-started-20260918@62e4f03a2b276fa00627c6c198fa4cd3b8d8c2f2` and is consumed/no-retry.

## Fast path / reconciliation

PRIMARY began from the durable Relay checkpoint and acquired the MAIN lease because the previous lease was `BLOCKED` and its heartbeat was stale beyond the collision window. Fast-path assumptions then disagreed with the still-current Evidence Analyst handoff: that handoff describes R1 before STARTED and prospectively authorizes one execution, while authoritative remote state now contains STARTED plus a completed post-START failure. This triggered FULL RECONCILIATION.

Fresh remote facts:
- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` is unchanged.
- R1 execution package remains `research/c19-r1-revision-authority-reduction-20260917@7197ab0f9683616858859446ae9eed7b75707f25`.
- STARTED control remains `control/c19-r1-revision-authority-started-20260918@62e4f03a2b276fa00627c6c198fa4cd3b8d8c2f2`.
- one-way workflow `35248878958` is `completed/failure` on that STARTED commit.
- no `preserve/c19-r1*` ref exists and no `evidence/c19-r1*` tag exists.
- the sole authoritative evidence tag remains the immutable C19-v4 evidence tag; all 13 legacy `freeze/*` branches remain present.
- open PRs are `0`; the only open Issue observed is governance Issue `#139`.

## Workflow / failure state

The one-way run had already passed STARTED/authority/collision validation, exact package checkout, admission-only binding checks, Python/runtime setup, pre-START contract verification, and pinned Belief-R acquisition/verification. It then failed at `Execute target-blind R1 acquisition with network blocked` while importing the frozen runner dependency chain:

`ModuleNotFoundError: No module named 'torch'`

The failure occurred before target-blind R1 predictions were produced. Raw preservation, independent re-fetch, immutable-v4 comparator materialization, evaluator-target materialization/scoring, and terminal evidence were all skipped. Diagnostic artifact `10509360230` remains the only run artifact of interest, with digest `sha256:e277c15bc52336ca816012b54a9c308d28491c8f32d19160a385394f730f7300`.

## Scientific integrity / decision

No scientific measurement exists for R1. This is not `SURVIVES_REDUCTION`, `REDUCED`, or `INCONCLUSIVE`; it is operational `POST_START_FAILURE`.

The current Analyst authority itself prospectively requires STOP after any post-START failure. Therefore PRIMARY did **not** install `torch` into the consumed object, edit the R1 package, retry workflow `35248878958`, rerun the identity, materialize targets, score anything, or create R2. The missing dependency may inform future readiness only after a newer Analyst handoff defines any distinct successor prospectively.

SUB remains independent. Its current H3 correlation-reduction work is explicitly NON_EVIDENTIARY and did not touch R1; PRIMARY did not absorb it.

## Stop / lease

Final lease status: `BLOCKED`.

Stop reason: current Evidence Analyst authority `42836802...` predates and has not yet consumed STARTED commit `62e4f03...` plus post-START workflow failure `35248878958`. No further MAIN scientific mutation is prospectively authorized under this authority.

Expected next MAIN action: wait for a newer Evidence Analyst handoff that explicitly consumes the R1 post-START failure and decides prospectively whether the programme stops here or whether a distinct fresh object is scientifically justified. Same-ID repair/retry and automatic R2 remain forbidden.

Relay continuation is **not** expected under the current Analyst authority. Relay may continue only if a newer handoff appears that prospectively assigns a valid next MAIN action.

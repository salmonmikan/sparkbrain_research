# Utility STARTED — AUTOUTIL-20261001T1724+0900-M1-EXACTHEAD-PROVENANCE-7A3C91E5

schema_version: 2
status: STARTED
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: AUTOUTIL-20261001T1724+0900-M1-EXACTHEAD-PROVENANCE-7A3C91E5
max_runs: 1
evidentiary_status: NON_EVIDENTIARY
scientific_authority: NONE

## Objective

Perform one bounded read-only exact-head provenance/readiness audit for M1 PR #164 after conflict-only reconciliation. Verify the current PR head/base/mergeability, exact-head CI, current-main relation, changed-path scope, and whether Evidence Analyst R177 is still stale relative to the reconciled exact head. Produce Utility-owned operational support only; do not create scientific authority or a hidden MAIN dependency.

## Trigger / source

- Milestone 1 remains active.
- Control R150 holds merge pending fresh Analyst exact-head reconciliation.
- PRIMARY MAIN latest is R219; state/lease remain R215 caches.
- Evidence Analyst is R177 and predates the reconciled exact head.
- P0 remains OPEN with intermittent/nonuniform pre-GitHub mutation refusals.

## Ownership checks at task selection

- Utility assignment: schema-v2 clean IDLE.
- Control: R150.
- Evidence Analyst: R177.
- PRIMARY MAIN latest: R219.
- MAIN state/lease: R215.
- Relay: unallocated.
- M1 owner: PRIMARY_MAIN.
- Directive index: head 8ce979b9ec0bc7eede5225c0403698f8886d3e8d / blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d; no delta from prior Utility durable generation.

## Allowed actions

- Fresh read-only GitHub inspection of PR #164, exact refs, compare metadata, changed-file patches, and CI/workflow status.
- Utility-owned append-only terminal result and Utility state update if the task completes.

## Forbidden actions

- No mutation of PR #164, M1 branch, main, Analyst/Control/MAIN/Relay state, or scientific refs.
- No merge/rebase/cherry-pick.
- No workflow dispatch or scientific execution.
- No claim upgrade, readiness adjudication, or scientific credit.
- No scheduler mutation.
- No Work/Cloud Browser execution path.

## Stop condition

Stop after one bounded provenance/readiness audit, or fail closed immediately if assignment/ownership materially changes, exact refs become ambiguous, or persistence exhausts the five-attempt ceiling.

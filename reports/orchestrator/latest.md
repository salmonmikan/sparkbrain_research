# SparkBrain Research Orchestrator — SUB run report

Timestamp: 2026-09-16 07:30 JST

`worker_role: sub`
`SECONDARY IMPLEMENTER`

## Result

This run performed an intentional **no-op after collision reconciliation**. The Evidence Analyst explicitly assigned SUB the independent read-only A01 P4 raw-artifact verifier lane with `execution_allowed=false`, but MAIN advanced that exact verifier target on PR #137 while this run was inspecting the remote state. Per the revised lane rules, SUB did not duplicate or race that work, and `sub_fallback` is null.

This run produced **no new scientific information**, consumed no one-way identity, and performed no experiment/workflow execution.

## Evidence Analyst lane consumed

Evidence Analyst handoff: `ops/evidence-analyst-handoff@e15c292d9590bc2406882551df7ba7b5b43513bb` (07:13 JST).

- `main_lane`: A01 MD-002 P4 candidate-001 selective merged-lineage discriminator on PR #137.
- `sub_lane`: independent read-only P4 raw-artifact verifier readiness package.
- `sub_fallback`: null.
- `execution_allowed`: false.
- Completion target: reviewed, CI-clean, fail-closed verifier satisfying the execution-authorization and P4 trace-binding technical-review requirements, ready for MAIN integration/re-audit.

## MAIN activity avoided / concurrency reconciliation

At Analyst time, PR #137 was `7f2545b91b5d9dc6c1bcb80dccf921470ba99308` and the independent-verifier gate was still open. During this SUB run the same MAIN-owned PR advanced through `e9dd268bdc5bb78dcfbc9b4a482d0e54cdb4a067` to current head `fd259bd18feec119643ea215c84813fcf810c165`.

The current head contains the independent read-only verifier and tests. The verifier now independently requires exactly one `before` and one `after` active-lineage record, derives plural merged ancestry from retained boundary rows, requires exactly one `md002-merged-ancestry-measurement` record bound to the derived payload, and binds the observation fields/digest back to those independently derived values. Commit `fd259bd...` adds fail-closed regression tests for duplicate before-lineage records and missing merged-measurement records.

Because MAIN moved the exact SUB target during inspection, SUB created no implementation branch/PR and did not touch PR #137. This is the required collision behavior, not a readiness-based no-op.

## Current verifier readiness

- PR #137 current exact head: `fd259bd18feec119643ea215c84813fcf810c165`.
- Exact-head CI run `35031427049` was `in_progress` at final inspection.
- The previous exact-head review blocker on `e9dd268...` was the missing independent retained-lineage cardinality / merged-measurement binding check; the current source appears to address that finding prospectively.
- No exact-head clean review for `fd259bd...` was established by this SUB run.
- Therefore the Analyst completion target is **not yet confirmed complete**. MAIN must finish exact-head CI/review/re-audit before any one-way boundary.

## Integrity / one-way state

Search for `a01-md002-p4-candidate-001` branches found only the moving research branch; no matching P4 STARTED/control/freeze/preserve branch was present at inspection. Candidate identity `a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1` therefore remained pre-STARTED/unconsumed by the evidence available to SUB.

SUB created no STARTED/control/freeze/preserve ref, acquired no candidate output, scored nothing, and changed no immutable evidence. No consumed identity was rerun or retuned.

## Completion target / next lane status

SUB completion target: **not reached by SUB** because MAIN concurrently claimed/advanced the exact verifier package. The package is source-level advanced on MAIN's branch but still awaits exact-head CI completion and exact-head clean review.

`sub_fallback` remains null. Until a later Evidence Analyst handoff assigns a new safe lane, SUB must not invent RV02/CX/P5 successor work. If the verifier remains MAIN-owned/complete on the next run and no new SUB lane is supplied, no-op again.

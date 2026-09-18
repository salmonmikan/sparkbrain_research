# MAIN Orchestrator — PRIMARY PD0.1 pre-formal fading-memory package / corrected exact-head checks running

Timestamp: `2026-09-18 09:26 JST`
Execution mode: `PRIMARY`
Evidence Analyst authority: `b009f497e65cddf1dd93cd4edc50f874c159ccd7`

## MAIN frontier

The terminal C19-R2 line remains closed and immutable. MAIN is now on `PD01_REMOTE_HISTORY_LINEAGE_PERSISTENCE_SPECIFICATION`, where the current Analyst handoff authorizes specification/readiness only and requires a stop before any formal identity, STARTED, official acquisition, or one-way execution.

PRIMARY stayed on the FAST PATH. The prior R2 lease was non-running/stale, `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` and Analyst tip `b009f497...` were freshly re-fetched, and no pre-existing PD0.1 branch or fresh conflicting MAIN mutation existed before the new branch was created.

## Critical-path progress

The fresh pre-formal branch is now:

`research/pd01-fading-memory-preformal-20260918@1702bb1a2dd70e2f363be48ab4652183c461fbc0`

It contains one deterministic, non-trainable exponential fading-memory primitive with per-history reset and no cross-history state; target-free deterministic history ordering/inventory support; a `PREFORMAL_REVIEW_ONLY` contract that keeps all Analyst-controlled scientific fields explicitly `UNRESOLVED_BY_ANALYST`; synthetic/dev-only tests; a fail-closed contract checker; and a dedicated synthetic-only pre-formal workflow. The dev fixture values (`decay=0.5`, `order_field=seq`) are explicitly non-scientific and forbidden from promotion into a formal protocol.

The first dedicated run `35290714808` failed only at Ruff lint. Its job log showed import-order/modernization findings plus an explicit `zip(..., strict=...)` requirement; checker/tests never ran. MAIN classified this as the prospectively authorized `PRE_START_BLOCKER` mechanical branch and corrected only those lint mechanics. No candidate, task/world, history rule, lag grid, comparator science configuration, representation binding, metric, threshold/equivalence rule, contender count, resource budget, runtime/package pin, or official raw cardinality was selected or changed.

## Workflow/check state

On corrected exact head `1702bb1...`:

- ordinary CI `35291105188`: `in_progress`;
- dedicated PD0.1 pre-formal `35291105255`: `in_progress`.

No useful local critical-path action remains while these external jobs run, so MAIN exits under the external-wait rule rather than occupying the PRIMARY slot.

## Scientific/integrity state

Formal identity remains **UNRESERVED**. No STARTED/control ref, official data or targets, preserve/evidence object, scoring, or scientific execution was created or accessed. There is **no new scientific information**. Terminal C19-R2 evidence was not used to tune PD0.1.

Lease is `WAITING_EXTERNAL`. Relay/next MAIN should collect only runs `35291105188` and `35291105255` for exact head `1702bb1...`. If both are green, re-fetch Analyst authority and exact branch head, persist `PD01_PRE_START_READY_FOR_ANALYST_REVIEW`, and STOP; a newer Analyst handoff is required before any formal identity or STARTED. Further science-invariant mechanical failure remains MAIN-owned, while any repair requiring selection of an unresolved scientific contract value must STOP for fresh Analyst review.

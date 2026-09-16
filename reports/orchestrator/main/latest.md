# SparkBrain Research Orchestrator — MAIN run report

Timestamp: 2026-09-16 18:10 JST  
`worker_role: main`

## MAIN frontier

MAIN consumed and re-verified Evidence Analyst `78138099076b81f2a7adfa67c2b38be063e5ee0b`. The PRIMARY RESEARCH FRONTIER remains A01 Family-B `distributed-field-trace` Generation-1 readiness on PR #144 / `research/v061-a01-family-b-gen1-20260916`. One-way execution remains **STOP** because the current Analyst handoff has `execution_allowed=false`.

The run began by re-fetching remote refs, active research branches, open PRs/issues, CI/review state, A01 immutable/consumed authorities, both MAIN/SUB orchestrator streams, Control Brain doctrine, and current Analyst authority. The Analyst split remains valid: MAIN owns all Family-B PR #144 critical-path work; RV02 PR #142 remains reserved for SUB and independent of MAIN.

## Concurrent movement reconciled

Before MAIN's new fixes, PR #144 had moved from the prior reported head to `63c0a398fced0a685d130783fc668222dd3344c6`: a concurrent worker safely appended the previously missing dated Family-B Decision Log record. MAIN compared that movement rather than overwriting it.

Fresh review of that moved head exposed three new MAIN-owned findings:

1. the package labeled post-P4 `7af99d6c...` too much like a pre-P4 protocol source;
2. the readiness package did not bind an exact implementation head;
3. JSON-restored F-only carriers accepted booleans as numeric values because Python `bool` subclasses `int`.

MAIN fixed all three on the Family-B branch. The exact current head is now `7f9ac1a9c397562720071a167bcdcfa18ba688c5`.

Separately, SUB's reserved RV02 PR #142 advanced concurrently from `a835fc9...` to `8ce68b6ad939cfcf3211549385f4d91f1312eedc`, adding the canonical D1 ledger entry and a status-map update. MAIN only observed this for collision reconciliation and did not touch it.

## Critical-path fixes completed

MAIN added an explicit pre-P4 Family-B conceptual-family source `525ecd9e205b2657a4ed207ae2b6cef0bae4bffc`, while retaining `7af99d6c3bbbf946f90fc01d9bc7cc7661de2006` accurately as the post-P4 Generation-1 contract source. The contract and package binding now distinguish these roles instead of retroactively presenting the Generation-1 contract as pre-P4.

MAIN added implementation-head binding semantics (`421145d60645b2f3b0d4c46c69ef314a9fc4de74`) and verification, refreshed the exact source/blob/contract/input/provenance binding, and kept `execution_admitted=false`.

MAIN also made restored Field carriers fail closed on boolean eligibility, credit, and decay values and added adversarial tests. A transient test typo created during the edit was corrected in the same run before the final binding head.

All previously known substantive PR #144 review threads are resolved. The final PR diff remains scoped to Family-B readiness: 13 files, 1,521 additions, 15 deletions relative to A01 base `1b548043b8f0850294cc3cbfaaa84dbdad69342c`.

## CI / review / integration status

Exact-head CI is green at `7f9ac1a9c397562720071a167bcdcfa18ba688c5`:

- pull-request CI run `35076600929`: `success`
- push CI run `35076594688`: `success`
- Python 3.11 and 3.13 jobs completed successfully.

A fresh manual Codex review was requested for this exact head. At report time it is still **running**; the latest submitted review is still for the prior `63c0a398...` head. MAIN therefore did **not** merge PR #144. This is an exact-head review gate, not a scientific ambiguity and not a SUB dependency.

No STARTED/control ref, freeze/preserve authority, scoring, acquisition workflow, one-way output exposure, or identity consumption was created for Family-B. Branch inventory still shows only the research branch and a non-authoritative old scratch branch for Family-B.

## Scientific result / integrity

**New scientific information: none.** This run changed readiness/integrity code and metadata only.

Family-A P4 remains terminal-consumed `UNSUPPORTED_EN_BLOC_MERGED_CREDIT`; its source/STARTED/raw/scored authorities were not changed. No consumed A01, RV01, RV02, or CX01 identity was rerun, retuned, repaired, or rescored under changed rules. No experiment was dispatched.

The prospective Family-B identity `a01-family-b-distributed-field-trace-gen1-v1` remains fresh, unSTARTED, unconsumed, and not execution-admitted.

## MAIN/SUB role separation

No Analyst split was invalidated. No MAIN blocker was assigned to SUB.

MAIN did not touch SUB-reserved RV02 PR #142, even after observing its concurrent progress. SUB does not need to unblock PR #144, and MAIN does not need to wait for RV02.

## Next MAIN action

The only immediate MAIN gate is completion of the already-running exact-head PR #144 review. If it completes cleanly, MAIN must immediately re-fetch Analyst authority, PR head/diff/mergeability/checks/reviews and integrate only the unchanged reviewed exact head into `research/v061-a01-n3-adapter`. If the review finds a substantive defect, MAIN owns that fix and must re-establish binding, CI, and exact-head review before integration.

Even after readiness integration, **do not execute Family-B**. Return the exact integrated package to Evidence Analyst for a fresh admit/reject decision before STARTED/no-clobber, acquisition, raw preservation, or scoring.

## Persistence

This report is persisted only to the MAIN-owned latest/state and append-only MAIN history stream. SUB-owned and legacy shared report files are not modified.

# MAIN Orchestrator — PRIMARY C19-R2 pre-formal specification

Timestamp: `2026-09-18 04:31 JST`
Execution mode: `PRIMARY`
Evidence Analyst authority: `b09d90d0545a0448ea5a310f9373969e7471b15d`

## MAIN frontier

Evidence Analyst terminally closed the C19-R1 revision-authority line after successor-v2 post-START failure and assigned MAIN the scientifically distinct `C19_R2_FSA_STATE_TRACKER_PROSPECTIVE_SPECIFICATION` lane. R1-v1/v2 remain consumed/no-retry; no R1 transient raw was used, salvaged, scored, or used for R2 tuning.

PRIMARY recovered the stale prior WAITING_EXTERNAL lease only after reconciling the completed failed R1-v2 one-way workflow and the new Analyst handoff, then created a fresh R2 branch directly from immutable C19-v4 scientific package lineage:

- branch: `research/c19-r2-fsa-state-tracker-spec-20260918`
- exact current head: `5d5d171cf872baed7a636fd246ab36f3a91a6716`
- scientific parent: `research/c19-official-v4-preservation-qualified-20260917@74bfe6b4a39758656f291baaa3f16236e3e71964`
- formal identity: **none reserved**
- STARTED: **not created**
- official execution: **not authorized**

## Prospectively frozen R2 object

R2 is an explicit representation-matched seven-state tracker using the exact immutable C19-v4 I2 encoder and deterministic `c19-readout-v1` projection. Its state alphabet is `RESET`, plus weak/strong state for each of `a/b/c`. It resets every pair, has no cross-pair memory, no raw-history lookup, no external lookup, no fitting/tuning/selection, and zero trainable parameters.

The fixed observation uses deterministic top choice with lexical tie-break and a natural majority threshold of `0.5` to distinguish weak/strong. The transition table, final readout, exact pair/seed/runtime bindings, state/resource budget, raw-before-score preservation boundary, target-free atomic_idx source map, immutable v4 comparator binding, cluster-aware primary bootstrap, pair-IID secondary sensitivity, and terminal criteria were all frozen before any R2 outcome exists.

Only nine R2-owned paths differ from the exact v4 parent; no parent/v4 scientific path was modified. The pre-START checker fail-closes on exact parent ancestry, R2-only diff paths, pinned immutable source blobs, absence of formal identity/execution authority, and golden transition semantics.

## Same-run critical-path fixups

The first dedicated pre-START run `35264684899` failed at lint. MAIN classified it under the prospectively allowed `R2_PRE_START_BLOCKER` contingency and made science-invariant fixes only: remove the JSON contract from explicit Ruff inputs and wrap two overlong Python lines.

The next exact-head dedicated run `35264985183` passed lint and the network-blocked import smoke, then failed one golden fixture because the fixture used exact binary-float equality for the registered Type-7 quantile result. The scorer implementation itself was unchanged. MAIN changed only the fixture to `math.isclose(..., abs_tol=1e-12)`. No mechanism, threshold, state, input, runtime, resource contract, preservation rule, scorer algorithm, success criterion, or scientific binding changed.

## Exact-head workflow checkpoint

Final head is `5d5d171cf872baed7a636fd246ab36f3a91a6716`.

- dedicated R2 pre-START `35265194243` — **completed / success** on this exact head;
- ordinary CI `35265194183` — **in_progress** on this exact head at checkpoint.

The earlier failed runs are superseded by this exact head.

## Scientific / integrity state

No new scientific measurement or outcome exists. R2 remains pre-formal, unSTARTED, unconsumed, and without a formal identity. C19-v4 immutable evidence is referenced read-only; consumed C19/R1 identities and refs were not modified. SUB independent exploratory work was not touched.

## Stop / relay action

Lease is `WAITING_EXTERNAL`. No useful local critical-path action remains while ordinary CI `35265194183` runs, so PRIMARY is yielding rather than occupying the lane solely to wait.

Relay/next MAIN must collect that exact-head CI while retaining dedicated pre-START success `35265194243`:

- if CI fails for a science-invariant mechanical reason, fix only that blocker, obtain a new exact head, and require ordinary CI plus dedicated pre-START on that same SHA;
- if a failure exposes a semantic/scientific gap, STOP for Evidence Analyst without redesign;
- if CI is green, re-fetch Analyst authority and exact R2 head, persist `R2_PRE_START_READY_FOR_ANALYST_REVIEW`, and STOP. Under the current Analyst handoff, do **not** reserve a formal identity, create STARTED, or execute official data.

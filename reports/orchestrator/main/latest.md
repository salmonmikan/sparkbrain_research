# MAIN Orchestrator — PRIMARY C19-R2 pre-formal specification

Timestamp: `2026-09-18 04:28 JST`
Execution mode: `PRIMARY`
Evidence Analyst authority: `b09d90d0545a0448ea5a310f9373969e7471b15d`

## MAIN frontier

Evidence Analyst has terminally closed the C19-R1 revision-authority line after successor-v2 post-START failure and moved MAIN to the scientifically distinct `C19_R2_FSA_STATE_TRACKER_PROSPECTIVE_SPECIFICATION` lane. R1-v1/v2 remain consumed/no-retry; no R1 transient raw was used or salvaged.

PRIMARY recovered the stale prior WAITING_EXTERNAL lease only after reconciling the completed failed R1-v2 one-way workflow and the new Analyst handoff, then created a fresh R2 branch directly from immutable C19-v4 scientific package lineage:

- branch: `research/c19-r2-fsa-state-tracker-spec-20260918`
- exact current head: `3ddc73f548e3d82e240d76d081ee94f12b031912`
- scientific parent: `research/c19-official-v4-preservation-qualified-20260917@74bfe6b4a39758656f291baaa3f16236e3e71964`
- formal identity: **none reserved**
- STARTED: **not created**
- official execution: **not authorized**

## Prospectively frozen R2 object

R2 is an explicit representation-matched seven-state tracker using the exact immutable C19-v4 I2 encoder and deterministic `c19-readout-v1` projection. Its state alphabet is `RESET`, plus weak/strong state for each of `a/b/c`. It resets every pair, has no cross-pair memory, no raw-history lookup, no external lookup, no fitting/tuning/selection, and zero trainable parameters.

The fixed observation uses deterministic top choice with lexical tie-break and a natural majority threshold of `0.5` to distinguish weak/strong. The transition table, final readout, exact pair/seed/runtime bindings, state/resource budget, raw-before-score preservation boundary, target-free atomic_idx source map, v4 comparator binding, cluster-aware primary bootstrap, pair-IID secondary sensitivity, and terminal criteria are all frozen in the pre-formal config/protocol/preregistration.

Nine R2-owned paths were added relative to the exact v4 parent and no parent/v4 scientific path was modified. The pre-START checker fail-closes on exact parent ancestry, exact R2-only diff paths, pinned immutable source blobs, no formal identity, no execution authority, and golden transition semantics.

## Same-run mechanical fixups

The first exact-head dedicated R2 pre-START run `35264684899` failed before tests at lint only. The failure was mechanical and prospective contingency `R2_PRE_START_BLOCKER` permits science-invariant repair:

- the dedicated workflow incorrectly passed the JSON contract file explicitly to Ruff;
- `scripts/check_c19_r2_prestart.py` had one E501 path literal;
- `c19_r2_protocol.py` had one E501 tuple line.

PRIMARY removed the JSON path from Ruff input and wrapped only those two lines. No state definition, transition, threshold, input, resource, runtime, preservation, scorer, success criterion, or evidence binding changed.

## Exact-head workflow checkpoint

Final head is `3ddc73f548e3d82e240d76d081ee94f12b031912`.

Fresh final-head runs are now external:

- ordinary CI `35264985201` — queued at checkpoint;
- dedicated R2 pre-START `35264985183` — queued at checkpoint.

The earlier failed dedicated run `35264684899` is superseded by this new exact head.

## Scientific / integrity state

No new scientific measurement or outcome exists. R2 remains pre-formal, unSTARTED, unconsumed, and without a formal identity. C19-v4 immutable evidence is referenced read-only; consumed C19/R1 identities and refs were not modified. SUB's independent NON_EVIDENTIARY H2 exploratory work was not touched.

## Stop / relay action

Lease is `WAITING_EXTERNAL`. No useful local critical-path work remains until the two exact-head checks resolve.

Relay/next MAIN must collect **both** final-head runs above:

- if either fails for a science-invariant mechanical reason, fix only that blocker, obtain a new exact head, and require both ordinary CI and dedicated pre-START to pass on that same final SHA;
- if a failure exposes a semantic/scientific gap, STOP for Evidence Analyst without redesign;
- if both are green, re-fetch Analyst authority and exact R2 head, set the phase to `R2_PRE_START_READY_FOR_ANALYST_REVIEW`, persist the checkpoint, and STOP. Do **not** reserve a formal identity, create STARTED, or execute official data under the current Analyst handoff.

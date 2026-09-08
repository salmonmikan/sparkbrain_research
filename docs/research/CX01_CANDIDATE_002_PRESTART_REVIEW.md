# CX01 candidate-002 pre-start independent review

## Status boundary

This document is an outcome-blind review request. It is not an execution seal and it does not authorize formal execution.

| item | status |
|---|---|
| candidate | `cx01-candidate-002` |
| proposed seed band | `370110..370119` |
| formal capability | **NOT EXECUTED** |
| formal score | **NONE** |
| execution seal | **NOT ISSUED** |
| persistent `STARTED` marker | **ABSENT** |
| candidate consumed | **NO** |
| independent review | **PENDING** |

No comparator outcome may be generated or inspected before this review is completed and a separate execution seal is issued.

## Candidate-001 rejection record

`cx01-candidate-001` remains a pre-start rejection, not a formal result.

- rejected freeze: `freeze/cx01-001`
- source SHA: `f2c5ead5...`
- exposed seed band: `269810..269819`
- execution seal: none
- `STARTED`: absent
- formal capability: not executed
- formal score: none
- PR #22: closed without merge
- disposition: candidate namespace and seed band permanently excluded from reuse

The rejection reason was structural: fresh numerical seeds mainly relabelled anonymous tokens while topology, timing, exposure counts, branch ratios, contingency schedules, and loop structure remained substantially development-isomorphic.

Neither the rejected freeze nor its package is modified by candidate-002 work.

## New source revision

The candidate-002 generator retains each CX01 family identity while opening seed-conditioned structural degrees of freedom that are independent of comparator outcomes:

| family | seed-conditioned variation under review |
|---|---|
| HIGH_ORDER | context topology, anonymous assignment, lags, exposure schedule |
| TIMING | context length/topology, lags, exposure schedule |
| CYCLE | target-cycle structure, phase schedule, phase exposures |
| BRANCH | branch context/topology, lag pattern, branch/exposure ratios |
| SELECTIVITY | distinct main/control contexts, lag pattern, exposure schedule |
| LOOP | cue topology, loop context, lags, exposure schedule |

The revision does not alter comparator thresholds, scoring definitions, comparator implementations, privilege contracts, or rapid-cycle acceptance criteria. Generator construction does not read comparator outcomes.

## Structural-held-out audit contract

Anonymous tokens are canonicalized before structural comparison. Development and candidate worlds are compared on separate axes rather than only through one combined hash:

1. topology signature;
2. timing signature;
3. exposure/schedule signature;
4. contingency signature where applicable;
5. combined full-structure signature;
6. raw anonymous-token assignment as a separate, non-substitute axis.

A candidate world is not accepted merely because its token names differ. Every world must have a full-structure signature absent from development and at least two applicable non-token structural axes novel relative to development. Family-level seed diversity and zero full-structure overlap are also required.

The package must include the complete 60-world grid, all 420 unscored comparator declarations, all audit reports, an unsigned freeze manifest, package status, and byte-level checksums. Hash-only declarations are insufficient.

## Required independent review

A reviewer other than the source/package builder must verify all of the following before any seal can be issued:

- candidate-001 freeze and package remain unchanged;
- candidate-001 namespace and seed band are rejected by validation;
- candidate-002 seed band is fresh and disjoint;
- family identity remains intact;
- topology novelty is genuine after token canonicalization;
- timing values vary structurally and are not cosmetic relabels;
- exposure counts and schedules vary without outcome-directed redesign;
- branch ratios and contingency schedules vary where applicable;
- loop/cycle structural parameters vary without breaking task identifiability;
- every packaged world is reconstructable from the fixed source SHA;
- world-grid and declaration cardinalities are exact;
- declarations contain no score, capability result, or measurement;
- privilege, schedule, scoring, schema, and comparator inventory hashes are fixed;
- package checksums verify;
- no `execution_seal.json`, `STARTED`, result archive, or formal score exists;
- ordinary CI and development validation pass at the exact source SHA;
- no comparator-specific or success-directed tuning is present.

## Review disposition

The independent reviewer must record one of:

- `APPROVE_PRESTART`: source and package may proceed to a separately issued execution seal;
- `REJECT_PRESTART`: candidate-002 is exposed and must not be repaired or reused as the same candidate;
- `RETURN_SOURCE_ONLY`: review is incomplete because required evidence is missing; no formal start is permitted.

Current disposition: **PENDING**.

No result prediction or success-direction adjustment is authorized by this document.

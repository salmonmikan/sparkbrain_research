# RV01 R01-12 Status

## Current decision

```text
R01-11 physical resource/safety boundary: complete, negative limitation retained
R01-12A world contract:                   complete
R01-12B development runner:               complete
R01-12C intervention controls:            complete
R01-12D resource-matched reservoir:       complete, mixed development result fixed
R01-12E held-out review/freeze:            complete, source/candidate frozen before execution
R01-12F one-way held-out execution:        complete, consumed, no rerun
post-formal interpretation:                review in progress
same-candidate rerun:                      prohibited
main merge:                                blocked pending review/ledger closure
```

R01-12F is fixed historical evidence. This status document does not authorize a rerun, rescore, threshold change, comparator change, or post-outcome repair.

## Fixed world programme

The continual-interference programme remains unchanged:

```text
5 families × 3 development seeds = 15 development worlds
5 families × 10 held-out seeds   = 50 held-out worlds
```

Development seeds are `0, 1, 2`. Held-out seeds are `100` through `109`. The two sets are disjoint.

Families:

1. disjoint routes;
2. three shared-cue branches;
3. three shared-prefix branches;
4. opposing directed-edge reversal plus disjoint control;
5. dense route load exceeding the registered active-edge budget.

No world definition, threshold, exposure count, route order, probe order, active-edge budget, or seed was changed in response to development failures or held-out outcomes.

## R01-11 retained limitation

The physical safety suite remains a negative engineering boundary. Under its original queue budget, the disjoint-control probe reaches unit `5` and then halts when queue size reaches `13` against the fixed budget of `12`.

Therefore:

```text
local_path_failure_does_not_destroy_disjoint_path = false
engineering_candidate = false
intrinsic_runtime_safety_supported = false
external_execution_guard_required = true
```

See `RV01_R01_11_SAFETY_DIAGNOSTIC_ADDENDUM.md`.

## R01-12B and R01-12C

R01-12B executed only the 15 development worlds using the current external-only physical learner and ordinary Field runtime. R01-12C added the preregistered reset, weight/delay transplant, structural edge removal, matched disjoint edge removal, training-order reversal, probe-order permutation, deterministic replay, freeze-after-training, and endogenous-write controls.

Those stages remain development diagnostics. Their failures were retained rather than rescued by changing the world contract.

## R01-12D fixed development result

The resource-matched sparse reservoir comparison completed from source:

```text
b163117512daca23b613c8a109a544833af7d360
```

Canonical anchors:

```text
development world grid:
1d9aed2d3be9cd04460943023321fe519160afb1e3f2ef5622d74949b49e5c48

suite hash:
16e29a77ffa714adbe8bb93cda1bc0cbf67a4022da135069fe731ca65709e7c6

result payload hash:
4f07d2f645fc9319647b49775a6186eba95af4cf567f99b6b5f8f64fbe0ff79e
```

Aggregate development result:

| Measure | Physical Field | Resource-matched reservoir |
|---|---:|---:|
| route-weighted ordered retention | 1.000 | 0.900 |
| exact routes | 24 / 60 | 24 / 60 |
| contamination | 216 | 177 |

The reservoir matches or exceeds Field mean retention in 6 of 15 worlds. The Field has a repeatable ordered-retention advantage in shared-prefix, reversal, and dense-load worlds, but exact-route recovery is tied and reservoir contamination is lower.

This is a **mixed result**, not architectural superiority. The retained R01-12D repository evidence supports the aggregate values above; raw per-world/per-probe development rows are not retained locally and must not be represented as independently reproducible from this branch.

## R01-12E completed freeze boundary

Before held-out capability execution, R01-12E bound the held-out programme to an exact frozen source and capability-free preflight. The freeze separated development evidence from the 50 held-out worlds and retained the one-way/no-rerun policy.

The frozen held-out source used by R01-12F is:

```text
83d2c77d8ae3878727d2ed4e9e78bc169ce064b8
```

R01-12E is therefore historical freeze provenance, not an in-progress stage.

## R01-12F fixed one-way formal result

R01-12F executed the frozen held-out candidate once and is consumed. The retained raw formal result is bound by SHA-256:

```text
e3f0cef5428c1b9a550c986404c1435952bd23fd0bdc0cc24a73b8e0c9f70ff4
```

Fixed aggregate formal values used by the post-formal review are:

| Measure | Physical Field | Resource-matched reservoir |
|---|---:|---:|
| route-weighted ordered retention | 1.0000 | 0.9017 |
| exact-route rate | 0.4000 | 0.4000 |
| contamination / route | 3.6000 | 2.9450 |

The fixed result supports a narrower continuation/coverage difference, not cleaner or generally superior selective memory. Exact-route recovery remains tied while Field contamination is higher.

The same R01-12F candidate must never be rerun. No post-formal interpretation may alter raw evidence, scoring, worlds, thresholds, resource matching, or comparator behavior.

## Current post-formal boundary

The open review is documentation/verification only. It may:

- verify retained manifest/raw hashes;
- regenerate derived review summaries from retained evidence;
- narrow unsupported prose claims;
- synchronize this status record and the append-only results ledger.

It may **not**:

- rerun R01-12F;
- reconstruct missing development raw rows as if they had been retained;
- tune either architecture from the held-out outcome;
- convert broader continuation into a selective-memory superiority claim;
- use later development protocols retroactively to rescue R01-12F.

The post-formal review is not merge-ready until its independent review findings and results-ledger bookkeeping are closed.

# RV01 R01-12 Status

## Current decision

```text
R01-11 physical resource/safety boundary: complete, negative limitation retained
R01-12A world contract:                   complete
R01-12B development runner:               complete
R01-12C intervention controls:            complete
R01-12D resource-matched reservoir:       complete, mixed result fixed
R01-12E held-out review/freeze:            in progress
held-out interference capability:         not executed
main merge:                               blocked
```

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

No world definition, threshold, exposure count, route order, probe order, active-edge budget, or seed was changed in response to development failures.

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

R01-12B executes only the 15 development worlds using the current external-only physical learner and ordinary Field runtime. R01-12C adds the preregistered reset, weight/delay transplant, structural edge removal, matched disjoint edge removal, training-order reversal, probe-order permutation, deterministic replay, freeze-after-training, and endogenous-write controls.

These stages remain development diagnostics. Failures are recorded rather than rescued by changing the world contract.

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

This is a **mixed result**, not architectural superiority. See `RV01_R01_12D_DEVELOPMENT_RESULT.md` and the tracked development manifest.

## R01-12E boundary

R01-12E may regenerate, shape-validate, and hash the 50 held-out world specifications. It may not train the Field, execute held-out route probes, fit the reservoir on held-out routes, or inspect any held-out capability metric before the freeze is sealed.

The freeze review must bind at least:

- the full source Git SHA;
- all 50 deterministic held-out specification identities and their grid hash;
- development and held-out seed sets;
- physical plasticity configuration;
- Field/evaluator budgets and metric semantics;
- reservoir comparator configuration and resource contract;
- expected held-out result cardinalities;
- critical source-file hashes;
- the fixed R01-12D development-result hashes;
- one-way/no-rerun execution policy.

Only after a green source revision and a matching capability-free preflight may an execution seal be written. The seal itself must not execute held-out capability.

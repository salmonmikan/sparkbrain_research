# RV01 R01-12F Formal Held-Out Result — Fixed One-Way Execution

## Status

R01-12 formal held-out execution is complete.

```text
candidate:               rv01-r01-12-interference-heldout-v1
execution policy:        one-way-no-rerun
frozen source SHA:       83d2c77d8ae3878727d2ed4e9e78bc169ce064b8
seal commit:             003cc0c390d53ab3a09420b4ad61fc7bb5e9a059
seal payload hash:       aff4df1a8cbe61294645c8f43464c1d198b9a599153ced49f00d47be7571e9d5
workflow run:            33953949771
workflow conclusion:     success
held-out capability:     executed exactly once
held-out world count:    50
final route probes:      200
```

The execution sentinel was persisted before capability opening. The formal run then completed once and uploaded the raw result artifact. This seal/result pair must not be rerun, tuned, rescued, or overwritten.

## Result binding

```text
held-out world grid hash:
4b828e544741552b9ce4759507cfaea285b2a36fc6f2cd7da8ac8aa4b0788229

preflight payload hash:
9b6fd4541196cdad297f1f92e3316da92503db46c12bb17ff6abc4fd643963dd

Field suite hash:
bec4c50bd792afcb5fb902a128dcf161191e83057892713e82eec5bc9d076618

reservoir suite hash:
87e673c9964f5513976521af34527f484f28685fbe7efd546b405c220a8e175e

raw result file SHA-256:
e3f0cef5428c1b9a550c986404c1435952bd23fd0bdc0cc24a73b8e0c9f70ff4

canonical result payload hash:
c014c0513f113e48ddcf5322579106a318f220236d05f25d39c3bd47e88f0673

result artifact:
ID 9965780771
ZIP SHA-256 dd495ca0f0fbc57e7d730e6e39be2d1f05d72c9ac9d56dc894de7c71da30e8d2

execution sentinel artifact:
ID 9965749551
ZIP SHA-256 dc4fae3b5111e76a218d2ea65525b53c6e2564d7642456002928609e6460714d
```

All frozen evidence cardinalities matched:

| Record | Expected | Observed |
|---|---:|---:|
| held-out worlds | 50 | 50 |
| training phases | 200 | 200 |
| Field phase×route probes | 1000 | 1000 |
| reservoir final-route probes | 200 | 200 |

All 50 worlds passed the preregistered resource-match checks. All 50 reservoir worlds also reproduced both recurrent-state and probe hashes deterministically.

## Aggregate held-out result

| Measure | RV01 physical Field | Resource-matched reservoir |
|---|---:|---:|
| route-weighted ordered retention | **1.0000** | 0.9017 |
| exact routes recovered | 80 / 200 | 80 / 200 |
| contamination count | 720 | **589** |
| worlds with higher mean retention | 29 / 50 | — |
| worlds tied on mean retention | 21 / 50 | 21 / 50 |
| worlds where Field had lower mean retention | 0 / 50 | — |

The held-out route-weighted ordered-retention difference is:

```text
Field - reservoir = +0.098333...
```

The central development pattern therefore replicated almost exactly: the physical Field retains ordered continuation more broadly, but does not recover more exact routes and generates more off-route activity.

## Family-level result

| Family | Field retention | Reservoir retention | Exact routes | Contamination (Field / reservoir) |
|---|---:|---:|---:|---:|
| disjoint routes | 1.0000 | 1.0000 | 30 / 30 vs 30 / 30 | 0 / 0 |
| shared-cue branches | 1.0000 | 1.0000 | 0 / 30 vs 0 / 30 | 180 / 180 |
| shared-prefix branches | **1.0000** | 0.7778 | 0 / 30 vs 0 / 30 | 120 / **100** |
| opposing-edge reversal | **1.0000** | 0.9000 | 10 / 30 vs 10 / 30 | 60 / **39** |
| dense route load | **1.0000** | 0.8750 | 40 / 80 vs 40 / 80 | 360 / **270** |

### Disjoint routes

All 10 held-out worlds tied on every registered capability measure used in R01-12D:

```text
Field ordered retention:     1.000
reservoir ordered retention: 1.000
exact routes:                3 vs 3 per world
contamination:               0 vs 0
```

The physical Field has no advantage on the low-interference reference.

### Shared-cue branches

All 10 worlds again tied on ordered retention and exact-route recovery:

```text
Field ordered retention:     1.000
reservoir ordered retention: 1.000
exact routes:                0 vs 0 per world
contamination:               18 vs 18 per world
```

Both systems preserve branch elements while failing to select a clean exact branch. The held-out result reinforces the development conclusion that this task does not demonstrate useful branch selection.

### Shared-prefix branches

All 10 worlds reproduced the development pattern:

```text
Field ordered retention:     1.000
reservoir ordered retention: 0.777777...
exact routes:                0 vs 0 per world
contamination:               12 vs 10 per world
```

The Field preserves more ordered continuation, but the reservoir remains cleaner and neither system recovers an exact branch route.

### Opposing-edge reversal

Nine of 10 worlds reproduced the development retention gap; one world tied at 1.000 vs 1.000.

Aggregate:

```text
Field ordered retention:     1.000
reservoir ordered retention: 0.900
exact routes:                1 vs 1 per world
contamination:               60 vs 39 total
```

The Field never had lower mean retention, but the reservoir was consistently cleaner.

### Dense route load

All 10 worlds reproduced the development pattern:

```text
Field ordered retention:     1.000
reservoir ordered retention: 0.875
exact routes:                4 vs 4 per world
contamination:               36 vs 27 per world
Field first-hop coverage:    1.000
reservoir first-hop coverage:0.875
```

The Field retains broader continuation under dense load, while producing substantially more contamination.

## Development → held-out comparison

The held-out result is unusually close to the fixed R01-12D development result.

| Measure | Development | Held-out |
|---|---:|---:|
| Field ordered retention | 1.0000 | 1.0000 |
| reservoir ordered retention | 0.9000 | 0.9017 |
| Field exact-route rate | 24/60 = 0.400 | 80/200 = 0.400 |
| reservoir exact-route rate | 24/60 = 0.400 | 80/200 = 0.400 |
| Field contamination / final route | 216/60 = 3.600 | 720/200 = 3.600 |
| reservoir contamination / final route | 177/60 = 2.950 | 589/200 = 2.945 |
| reservoir matched/exceeded Field mean retention | 6/15 = 0.400 | 21/50 = 0.420 |

This materially strengthens confidence that the development pattern was not an accident of the 15 development seeds.

## Interpretation

R01-12F supports a narrow but real held-out statement:

> Under the frozen R01-12 interference contract and the preregistered resource-matched sparse reservoir comparator, the current G1/G2-free physical Field exhibits a reproducible sequence-retention / coverage profile that differs from the comparator.

The strongest positive evidence is not exact reconstruction. It is the repeatable retention/coverage advantage in shared-prefix, reversal, and dense-load worlds.

At the same time, the formal result also preserves the negative side of the development result:

- exact-route recovery is tied overall at `80 / 200`;
- shared-cue branch selection remains unresolved, with both systems at `0 / 30` exact routes in that family;
- the reservoir is cleaner overall (`589` contamination events versus `720`);
- disjoint routes show no Field advantage;
- a generic recurrent explanation remains viable for a substantial fraction of the observed capability.

Accordingly, this is stronger evidence for a **different continuation-retention trade-off**, not evidence that RV01 is already a superior or uniquely necessary architecture.

## Claim boundary

R01-12F does **not** establish:

- architectural uniqueness;
- semantic understanding;
- general superiority to recurrent models;
- clean branch selection;
- safe or graceful capacity scaling;
- production readiness;
- that the current mechanism is not expressible by another recurrent or learned dynamical substrate.

It does establish that the R01-12D development pattern survived a one-way preregistered held-out test without threshold tuning, world changes, comparator tuning, reruns, or rescue.

## Next research boundary

The next step should not be additional tuning of R01-12.

The useful next question is mechanistic discrimination: identify which part of the physical Field produces the replicated retention/coverage difference and test whether that effect survives controls that remove or transplant specific physical state loci.

That means moving to a new protocol/seed boundary for state-locus and mechanism-level experiments, while keeping this R01-12 seal and formal result immutable.

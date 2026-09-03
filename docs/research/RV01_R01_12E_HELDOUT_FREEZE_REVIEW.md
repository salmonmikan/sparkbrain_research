# RV01 R01-12E — Held-out Review and Freeze Boundary

## Purpose

R01-12E is the review/freeze stage immediately before any capability execution on the 50 held-out continual-interference worlds.

It is not a capability experiment. The only permitted held-out operations before the seal are:

- deterministic world-specification generation;
- schema/shape validation;
- seed-disjointness validation;
- specification hashing;
- world-grid hashing;
- expected-record cardinality calculation;
- source/configuration checksum generation.

The Field must not be trained on a held-out world, no held-out route probe may run, and the resource-matched reservoir must not be fitted to held-out routes before the seal.

## Prior evidence required

The freeze candidate must retain the completed development evidence without reinterpretation:

```text
R01-12B development runner: complete
R01-12C interventions:      complete
R01-12D comparator:         complete, mixed result
```

R01-12D fixed anchors:

```text
execution source:
b163117512daca23b613c8a109a544833af7d360

development world grid:
1d9aed2d3be9cd04460943023321fe519160afb1e3f2ef5622d74949b49e5c48

suite:
16e29a77ffa714adbe8bb93cda1bc0cbf67a4022da135069fe731ca65709e7c6

result payload:
4f07d2f645fc9319647b49775a6186eba95af4cf567f99b6b5f8f64fbe0ff79e
```

The mixed result must not be used to retune the held-out world programme or comparator.

## Frozen research interpretation entering held-out

The development result establishes neither architectural uniqueness nor general superiority.

Current interpretation:

- physical Field ordered retention exceeds the resource-matched reservoir in several overlapping/dense families;
- exact-route recovery is tied overall;
- reservoir contamination is lower overall;
- the reservoir matches or exceeds Field mean retention in 6/15 development worlds;
- R01-11 retains a queue-budget safety limitation and is not a positive engineering-safety result.

These observations may motivate the held-out question but may not change its worlds, budgets, thresholds, or metrics.

## Freeze checklist

A candidate is review-ready only if all of the following are true:

1. source CI is green on Python 3.11 and 3.13;
2. local readiness and bundle validation pass;
3. the current development world-grid hash exactly matches the fixed R01-12D grid hash;
4. there are exactly 50 held-out worlds from seeds 100–109;
5. development and held-out seeds remain disjoint;
6. all held-out specification hashes are unique and reproducible;
7. physical plasticity configuration is serialized into the preflight;
8. comparator configuration is serialized into the preflight;
9. evaluator budgets and metric semantics are serialized into the preflight;
10. expected held-out cardinalities are fixed;
11. critical implementation/protocol files are SHA-256 bound;
12. `held_out_capability_executed` remains false;
13. held-out Field and reservoir capability entry points remain fail-closed before the seal.

## Expected held-out cardinalities

From the unchanged five-family world contract:

```text
worlds:                         50
training phases:               200
Field phase×route probe rows: 1000
reservoir final-route probes:  200
```

These are inventory expectations, not success thresholds.

## Seal rule

After the last source/configuration/documentation change, one source revision must pass the full CI and produce a capability-free R01-12E preflight artifact.

Only then may a seal be written under `.github/confirmatory/`. The seal must bind the tested source SHA, held-out world-grid hash, preflight payload hash, R01-12D result anchors, expected record cardinalities, and one-way execution policy.

The seal commit is metadata only. It must not modify the tested source revision or execute held-out capability.

## Formal boundary after seal

Once sealed, the next step is a one-way held-out execution. If implementation correction is required after capability is opened, the current seal and result must remain immutable and a new protocol version, source seal, and fresh held-out seed set are required.

No held-out capability result exists at this review stage.

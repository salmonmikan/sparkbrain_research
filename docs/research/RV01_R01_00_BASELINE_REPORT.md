# RV01 R01-00 — Frozen v0.6 Baseline Reproduction Report

## Decision

```text
frozen v0.6 code SHA: f55f2ad9df1484a7ffb88850097ec5c5a7a41791
frozen v0.6 CI run:   33258287966
selected runtime blob fingerprints: PASS
canonical state probe:               PASS
canonical endogenous chain:          PASS
canonical boundary/world coupling:   PASS
canonical revision/reacquisition:    PASS
RV01 baseline reproducible:          YES
```

R01-00 is complete. RV01 may now compare replacement mechanisms against the frozen v0.6 behaviour
without silently rewriting that baseline.

## Why this gate exists

RV01 directly challenges the strongest limitation found in v0.6: demonstrated experience-dependent
behaviour is carried by explicit G1 local transition state and G2/consistency state. A replacement
cannot be credited merely by changing the old baseline until it becomes easier to beat.

The baseline therefore has two independent protections:

1. selected runtime and canonical-evaluator files are checked by Git blob SHA;
2. canonical behaviours are executed again and summarized deterministically.

## Fingerprinted runtime surface

The fingerprint set includes the frozen implementations for:

- provenance and endogenous-event contracts;
- G0 diagnostics;
- G1 local expectation;
- G2 local transition adaptation;
- normal-rule reinjection;
- autonomous endogenous chain execution;
- reality correction;
- anonymous boundary and world coupling;
- anonymous consistency and relation re-entry;
- taxonomy guards;
- canonical state, chain, boundary, and revision probes.

A missing or modified file fails closed. The fingerprint check does not accept a branch label as proof
that the code is still the frozen code.

## Reproduced canonical behaviour

### Same-input/different-history state probe

```text
reference learned history  -> endogenous unit:1
reconstructed replay       -> endogenous unit:1
alternate learned history  -> endogenous unit:2
no learned history         -> no endogenous event
```

### Sequential endogenous chain

```text
sham:                       1 -> 2 -> 3
targeted expansion block:   1
matched active control:     1 -> 2 -> 3
root reinjection blocked:   no chain
selective effect:           1.0
```

### Anonymous boundary and external stream

```text
sham main boundary events:          3
targeted main boundary events:      0
matched-control main events:        3
sham raw external main events:      3
internal-only positive links:       0
```

### Revision and reacquisition

```text
initial old relation reliability:   0.8
reversal old reliability:           0.5
reversal new reliability:           0.8
new relation first dominates:       reversal episode 2
old relation first dominates again: return episode 2
```

## Determinism

The canonical summary is hashed independently of Git metadata. Repeated execution produces the same
summary and summary hash.

## Validation

GitHub Actions run `33287859215` passed on Python 3.11 and Python 3.13:

```text
Install:          PASS
Ruff lint:        PASS
Local readiness: PASS
Full pytest:      PASS
Bundle validation: PASS
```

## Claim boundary

R01-00 does not support a new RV01 mechanism. It establishes only that the frozen v0.6 comparison
condition is intact and reproducible.

# SparkBrain v0.6 Confirmatory Preregistration Draft

## Status

This document defines the V06-15 qualification and confirmatory structure before result execution.
It is a **draft**, not a frozen preregistration, until:

- every required condition has an executable adapter;
- G3/G4/G5 remain isolated under `sparkbrain.baselines`;
- the code reference is replaced by a full frozen Git SHA;
- the manifest hash is recorded;
- the qualification runner and artifact schema pass review.

`src/sparkbrain/evaluation/v06_confirmatory.py` enforces these requirements fail-closed.

## Scientific purpose

The current Level-1, Level-2, and Level-3 results are canonical engineering candidates. V06-15 must
determine whether the same evidence survives structural variation rather than merely reproducing one
hand-authored world.

The confirmatory suite must also test whether comparator systems succeed where the Primary route
fails. Comparator-only success is a negative result for the Primary SparkBrain hypothesis.

## Frozen execution phases

### Qualification

```text
3 world families × 3 perturbation seeds
```

Qualification is used to debug the frozen adapters and artifact pipeline. It is not confirmatory
evidence and may not be merged into the final confirmatory statistics.

Qualification world families:

1. `identifier-permutation`
   - anonymous unit permutation;
   - anonymous port permutation.
2. `temporal-perturbation`
   - local lag jitter;
   - inter-episode spacing variation.
3. `field-gain-perturbation`
   - ordinary threshold offset;
   - input/reinjection magnitude scaling.

Qualification seeds:

```text
0, 1, 2
```

### Confirmatory

```text
5 held-out world families × 10 perturbation seeds
```

Confirmatory families are not used to tune the Primary or comparator implementations.

1. `heldout-sparse-permutation`
2. `heldout-lag-dispersion`
3. `heldout-threshold-band`
4. `heldout-branch-competition`
5. `heldout-contingency-cycles`

Confirmatory seeds:

```text
100 through 109
```

## Required conditions

Every world-family/seed/evidence cell must contain all conditions:

```text
Primary G0/G1/G2 route
no-endogenous generation
count/energy/time-matched random endogenous events
readout-only without Field reinjection
shuffled anonymous relation state
G3 generic recurrent predictor
G4 explicit Assembly-conditioned predictor
G5 typed functional-head comparator
```

An absent condition makes the result matrix incomplete. Incomplete matrices cannot be scored.

## Required evidence domains

The manifest requires all of:

1. endogenous origin;
2. same-input persistent-state dependence;
3. autonomous internal chain;
4. selective anonymous boundary effect;
5. external anonymous relation stabilization;
6. reversal and reacquisition;
7. relation re-entry into later Field Dynamics;
8. persistence-locus reset/transplant;
9. observer and taxonomy non-interference.

Missing-Middle remains a supporting validity assay. It cannot replace the required relation-reentry
or persistence-locus evidence domains.

## Frozen draft thresholds

The code contract currently defines:

```text
minimum overall success fraction:       0.80
minimum success in every world family:  0.70
maximum null false-positive fraction:   0.10
minimum targeted-minus-control effect:  0.50
required taxonomy hash match fraction:  1.00
maximum self-confirmation violations:   0
```

These are project decision thresholds, not universal scientific constants. Any change after manifest
freeze creates a new manifest hash and requires a new preregistration rather than silently altering
the existing run.

## Coverage rule

The expected matrix is:

```text
world family
× perturbation seed
× condition
× evidence domain
```

For qualification this is currently:

```text
3 × 3 × 8 × 9 = 648 records
```

For confirmatory execution:

```text
5 × 10 × 8 × 9 = 3,600 records
```

Duplicate, missing, or unexpected keys make the matrix unscorable.

## Interpretation rule

### Primary passes, comparators fail

Supports the Primary mechanism under the frozen conditions. It does not prove uniqueness outside the
tested comparators.

### Primary and one or more comparators pass

The Primary mechanism is supported, but architectural uniqueness is not established. Generalization,
resource, intervention-specificity, and stability comparisons must be reported.

### Primary fails, comparator passes

This is **comparator-only success and a negative result for the Primary hypothesis**.

### All fail

The tested capability is not supported under the frozen protocol.

## Current readiness result

The draft manifest already has the required world-family counts, seed counts, condition names,
evidence-domain names, thresholds, exclusions, and comparator isolation paths.

It is intentionally **not execution-ready** because:

- the code reference is `UNFROZEN`;
- the parameterized Primary world adapter is pending;
- the unified no-endogenous and readout-only adapters are pending;
- the random-matched endogenous adapter is pending;
- the shuffled-relation adapter is pending;
- G3 is not yet adapted to the frozen world/result interface;
- G4 is not yet adapted to the frozen world/result interface;
- G5 is not yet implemented under the isolated comparator interface.

The current engineering evidence is not copied into the confirmatory matrix. Fresh frozen executions
are required.

## Anti-rescue rule

The current persistence-locus result indicates that explicit G1 transition state and anonymous
consistency state dominate the demonstrated experience effects, while matched Field state alone did
not transfer them.

V06-15 must not add a new memory state merely to rescue a distributed-Field claim. The confirmatory
suite evaluates the architecture that exists at freeze time. Any architectural change after freeze
requires a new development cycle and a new manifest.

## Artifact requirements

Each run must persist:

- full manifest and manifest hash;
- code SHA;
- world-family and perturbation seed;
- condition and evidence domain;
- normalized raw runtime trace hash;
- observer artifact hash stored separately;
- event, energy, depth, and branch counts;
- external-observation and positive-commit counters;
- targeted, matched-random, and sham effects;
- pass/fail and raw metrics;
- exception or bounded-termination artifact;
- comparator isolation metadata.

## Release blocker

PR #10 remains Draft and `main` remains unchanged until:

- qualification matrix is complete;
- confirmatory manifest is frozen;
- the full held-out matrix is complete;
- G3/G4/G5 are interpreted;
- self-confirmation violations remain zero;
- taxonomy non-interference is complete;
- persistence limitations and strongest counterexamples are preserved in the final report.

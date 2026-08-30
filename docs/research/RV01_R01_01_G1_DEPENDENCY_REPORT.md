# RV01 R01-01 — Explicit G1 Dependency Report

## Decision

R01-01 disables learned G1 transition rows while retaining the same Field, G2 wrapper, reinjection,
reality-correction, provenance, and boundary mechanisms.

```text
same-input/different-history endogenous response requires G1: YES
sequential continuation requires G1:                       YES
branching candidate generation requires G1:                YES
forward missing-middle bridge requires G1:                 YES
terminal anonymous boundary event requires G1:             YES
initial Field state matched:                               YES
external input matched:                                    YES
internal-only positive commits:                              0
```

The complete currently demonstrated endogenous transition burden is carried by explicit G1 state.

## Experimental isolation

For every paired assay:

```text
G1 enabled
G1 disabled
```

share:

- identical `TemporalExcitableField` construction and initial state hash;
- identical receptor support and thresholds;
- identical G2 `SparseLocalTransitionAdaptation` implementation;
- identical `FieldReinjectionGate` configuration;
- identical external event identities, targets, times, magnitudes, and polarity;
- identical boundary coupling where applicable.

The only intended difference is whether `LocalTemporalExpectation` contains learned external
transition rows.

## Assay results

### 1. Same current input

```text
learned G1 + external unit:0 -> endogenous unit:1
empty G1   + external unit:0 -> no endogenous Spark
```

The Field does not reconstruct the learned next event independently of G1.

### 2. Sequential continuation

```text
learned G1: unit:0 cue -> 1 -> 2 -> 3
empty G1:   unit:0 cue -> no endogenous continuation
```

The normally thresholded later Sparks still execute in the Field, but their transition candidates are
supplied by explicit G1 rows.

### 3. Branching

G1 is trained with equal observations of:

```text
0 -> 1
0 -> 2
```

Result:

```text
learned G1 -> candidate Field Sparks at units 1 and 2
empty G1   -> no candidate branch
```

This shows that current branch representation originates in the explicit local transition table.
It does not yet show that RV01 can preserve ambiguity without such a table.

### 4. Forward bridge

Training sequence:

```text
0 -> 1 -> 2 -> 3
```

Test input:

```text
unit:0 at 100 ms
unit:1 at 105 ms
unit:3 at 120 ms
```

With learned G1, an endogenous unit:2 event occurs before the later external unit:3 event. With empty
G1, no unit:2 bridge appears.

### 5. Anonymous boundary effect

```text
learned G1 -> chain reaches unit:3 -> port:7 event
empty G1   -> chain never reaches unit:3 -> no boundary event
```

The boundary emitter itself remains unchanged. What disappears is the upstream learned transition
path needed to reach it.

## Self-confirmation boundary

For same-input response, chain, branching, and boundary assays:

```text
committed positive updates from endogenous-only activity: 0
```

Disabling G1 does not weaken the external-confirmation-only learning invariant.

## Interpretation

The strongest supported interpretation is:

> In the frozen v0.6 architecture, explicit G1 local source-target statistics are causally necessary
> for all currently demonstrated history-dependent endogenous transition capabilities. The Field
> executes, thresholds, suppresses, and propagates the proposed activity, but it does not currently
> recover those transitions from its own learned physical state when G1 is empty.

This does not prove that a generic Field substrate cannot acquire equivalent capability. It establishes
the exact burden that an RV01 replacement must carry.

## Validation

The first implementation run failed because the diagnostic incorrectly read the nested G1 transition
schema as a flat table. The capability assertions were not weakened; only the diagnostic traversal was
corrected.

GitHub Actions run `33287859215` then passed on Python 3.11 and Python 3.13:

```text
Install:          PASS
Ruff lint:        PASS
Local readiness: PASS
Full pytest:      PASS
Bundle validation: PASS
```

## Next gate

R01-02 keeps G1 intact and removes the adaptive contribution of G2. It separates:

- raw transition proposal generation;
- external stabilization;
- timing correction;
- reversal;
- reacquisition;
- long-run selectivity.
